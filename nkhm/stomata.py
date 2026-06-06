# nkhm/stomata.py
import streamlit as st
import random
import json
from pathlib import Path

# ========== MEMBACA SOAL DARI FILE JSON ==========
def load_soal_from_json(kategori, folder_name):
    """Membaca soal dari file JSON berdasarkan kategori"""
    base_path = Path(__file__).parent / "soal_stomata_hati" / folder_name
    json_path = base_path / f"soal_{folder_name}.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Mengembalikan list of tuples (kategori, teks, pilihan) 
        # Untuk stomata, kita perlu format (kategori, teks, jawaban_benar?)
        # Karena soal stomata adalah pernyataan yang dinilai setuju/tidak setuju dengan skala Likert
        # Tapi kode lama menggunakan format True/False (benar/salah)
        # Kita konversi ke format baru dengan skala Likert 5 poin
        return data
    except FileNotFoundError:
        st.warning(f"⚠️ File soal {folder_name} tidak ditemukan di {json_path}")
        return []
    except json.JSONDecodeError:
        st.warning(f"⚠️ File {json_path} format JSON tidak valid")
        return []

def load_all_soal_stomata():
    """Memuat semua soal dari ketiga kategori"""
    soal_kasih = load_soal_from_json("kasih", "kasih")
    soal_iman = load_soal_from_json("iman", "iman")
    soal_pengharapan = load_soal_from_json("pengharapan", "pengharapan")
    
    # Konversi ke format (kategori, teks, pilihan_skala)
    all_soal = []
    for soal in soal_kasih:
        all_soal.append({
            "kategori": "Kasih",
            "id": soal.get("id", 0),
            "teks": soal.get("teks", ""),
            "pilihan": soal.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    for soal in soal_iman:
        all_soal.append({
            "kategori": "Iman",
            "id": soal.get("id", 0),
            "teks": soal.get("teks", ""),
            "pilihan": soal.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    for soal in soal_pengharapan:
        all_soal.append({
            "kategori": "Pengharapan",
            "id": soal.get("id", 0),
            "teks": soal.get("teks", ""),
            "pilihan": soal.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    
    return all_soal

# ========== SISI NAMES ==========
SISI_NAMES = {
    1: "Kasih",
    2: "Iman",
    3: "Pengharapan",
    4: "Iman-Pengharapan",
    5: "Kasih-Iman",
    6: "Pengharapan-Kasih",
    7: "Berbuat iman",
    8: "Berbuat pengharapan",
    9: "Berbuat kasih",
    10: "Kasih-Iman-Pengharapan",
    11: "Berbuat kasih-beriman",
    12: "Berbuat kasih-berpengharapan",
}

# ========== SKOR LIKERT (untuk 5 pilihan) ==========
# Konversi pilihan ke nilai: 
# Sangat Tidak Setuju = 0, Tidak Setuju = 1, Netral = 2, Setuju = 3, Sangat Setuju = 4
LIKERT_SCORE = {
    "Sangat Tidak Setuju": 0,
    "Tidak Setuju": 1,
    "Netral": 2,
    "Setuju": 3,
    "Sangat Setuju": 4
}

def init_stomata_state():
    if "stomata_answers" not in st.session_state:
        st.session_state.stomata_answers = {}
    if "stomata_submitted" not in st.session_state:
        st.session_state.stomata_submitted = False
    if "stomata_results" not in st.session_state:
        st.session_state.stomata_results = None
    if "stomata_all_soal" not in st.session_state:
        all_soal = load_all_soal_stomata()
        random.shuffle(all_soal)
        st.session_state.stomata_all_soal = all_soal

def reset_stomata():
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    # Reshuffle soal saat reset
    all_soal = load_all_soal_stomata()
    random.shuffle(all_soal)
    st.session_state.stomata_all_soal = all_soal

def hitung_persentase(skor, max_skor=132):
    """
    Menghitung persentase dari skor Likert.
    Maksimal skor per kategori: 33 soal × 4 = 132 poin
    """
    return (skor / max_skor) * 100 if max_skor > 0 else 0

def tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan):
    """
    Mengembalikan daftar nomor sisi (1-12) berdasarkan persentase.
    """
    total = persen_kasih + persen_iman + persen_pengharapan
    if total == 0:
        return [10]
    
    # Normalisasi ke 100
    rk = (persen_kasih / total) * 100
    ri = (persen_iman / total) * 100
    rp = (persen_pengharapan / total) * 100

    # Jika ketiga nilai relatif seimbang (selisih maks < 5%)
    if max(rk, ri, rp) - min(rk, ri, rp) < 5:
        return [1, 8, 9]

    max_val = max(rk, ri, rp)
    if max_val >= 60:
        # Dominasi tunggal -> satu sisi sudut
        if rk == max_val:
            return [1]
        elif ri == max_val:
            return [2]
        else:
            return [3]
    elif (rk >= 40 and ri >= 40) or (ri >= 40 and rp >= 40) or (rp >= 40 and rk >= 40):
        # Kombinasi dua -> satu sisi kombinasi
        if rk >= 40 and ri >= 40:
            return [5]
        elif ri >= 40 and rp >= 40:
            return [4]
        elif rp >= 40 and rk >= 40:
            return [6]
        else:
            return [10]
    else:
        # Nilai sedang -> satu sisi tindakan berdasarkan tertinggi
        if rk == max_val:
            return [9]   # Berbuat kasih
        elif ri == max_val:
            return [7]   # Berbuat iman
        else:
            return [8]   # Berbuat pengharapan

def show_stomata():
    init_stomata_state()

    st.markdown("## 💖 Sto-mata Hati")
    st.markdown("""
    **Alat Uji Tingkat Iman, Kasih, dan Pengharapan (IKP)**  
    Berdasarkan 1 Korintus 13:13.
    
    Jawablah 99 pernyataan berikut dengan memilih tingkat persetujuan Anda (skala 0-4).  
    - **Sangat Tidak Setuju** = 0  
    - **Tidak Setuju** = 1  
    - **Netral** = 2  
    - **Setuju** = 3  
    - **Sangat Setuju** = 4  
    
    Setelah selesai, sistem akan menghitung persentase masing‑masing kriteria dan menentukan posisi Anda pada 12 sisi Stomata Hati.
    """)

    soal_list = st.session_state.stomata_all_soal
    total_soal = len(soal_list)

    if total_soal == 0:
        st.error("❌ Tidak ada soal yang ditemukan. Pastikan folder 'soal_stomata_hati' berisi file JSON yang valid!")
        st.info("📁 Struktur folder yang diharapkan:\n"
                "- nkhm/soal_stomata_hati/iman/soal_iman.json\n"
                "- nkhm/soal_stomata_hati/kasih/soal_kasih.json\n"
                "- nkhm/soal_stomata_hati/pengharapan/soal_pengharapan.json")
        return

    with st.form(key="stomata_form"):
        st.markdown(f"### 📝 Total Soal: {total_soal}")
        
        # Gunakan expander untuk menghemat ruang
        with st.container(height=500):
            for idx, soal in enumerate(soal_list):
                st.markdown(f"**{idx+1}. [{soal['kategori']}]** {soal['teks']}")
                key = f"stomata_radio_{idx}_{soal['id']}"
                current = st.session_state.stomata_answers.get(idx, None)
                selected = st.radio(
                    "Pilih jawaban:",
                    soal['pilihan'],
                    index=soal['pilihan'].index(current) if current in soal['pilihan'] else None,
                    key=key,
                    label_visibility="collapsed"
                )
                if selected:
                    st.session_state.stomata_answers[idx] = selected
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("📊 Hitung Hasil Sto-mata", use_container_width=True)
        with col2:
            reset_clicked = st.form_submit_button("🔄 Reset", use_container_width=True)
    
    if reset_clicked:
        reset_stomata()
        st.rerun()
    
    if submitted:
        if len(st.session_state.stomata_answers) < total_soal:
            st.error(f"⚠️ Anda baru menjawab {len(st.session_state.stomata_answers)} dari {total_soal} soal. Selesaikan semua soal terlebih dahulu!")
        else:
            # Hitung skor untuk setiap kategori
            skor_kasih = 0
            skor_iman = 0
            skor_pengharapan = 0
            
            for idx, soal in enumerate(soal_list):
                jawaban = st.session_state.stomata_answers.get(idx)
                nilai = LIKERT_SCORE.get(jawaban, 0)
                
                if soal['kategori'] == "Kasih":
                    skor_kasih += nilai
                elif soal['kategori'] == "Iman":
                    skor_iman += nilai
                else:  # Pengharapan
                    skor_pengharapan += nilai
            
            # Maksimal skor per kategori: 33 soal × 4 = 132
            persen_kasih = hitung_persentase(skor_kasih, 132)
            persen_iman = hitung_persentase(skor_iman, 132)
            persen_pengharapan = hitung_persentase(skor_pengharapan, 132)
            
            sisi_list = tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan)
            
            st.session_state.stomata_results = {
                "kasih": persen_kasih,
                "iman": persen_iman,
                "pengharapan": persen_pengharapan,
                "sisi_list": sisi_list,
                "skor_kasih": skor_kasih,
                "skor_iman": skor_iman,
                "skor_pengharapan": skor_pengharapan,
            }
            st.session_state.stomata_submitted = True
            st.rerun()

    if st.session_state.stomata_submitted and st.session_state.stomata_results:
        res = st.session_state.stomata_results
        st.markdown("---")
        st.subheader("📊 Hasil Uji IKP")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("💖 Kasih", f"{res['kasih']:.1f}%")
        col_b.metric("🙏 Iman", f"{res['iman']:.1f}%")
        col_c.metric("✨ Pengharapan", f"{res['pengharapan']:.1f}%")
        
        # Tampilkan skor mentah
        with st.expander("📈 Detail Skor Mentah"):
            st.metric("Skor Kasih", f"{res['skor_kasih']} / 132")
            st.metric("Skor Iman", f"{res['skor_iman']} / 132")
            st.metric("Skor Pengharapan", f"{res['skor_pengharapan']} / 132")
            st.progress(res['kasih']/100, text=f"Kasih: {res['kasih']:.1f}%")
            st.progress(res['iman']/100, text=f"Iman: {res['iman']:.1f}%")
            st.progress(res['pengharapan']/100, text=f"Pengharapan: {res['pengharapan']:.1f}%")
        
        # Tampilkan gambar stomata hati
        img_path = Path(__file__).parent.parent / "assets" / "stomata_hati.jpg"
        if img_path.exists():
            st.image(str(img_path), caption="Stomata Hati - Segitiga IKP", use_container_width=True)
        else:
            st.warning("⚠️ Gambar Stomata Hati belum tersedia. Harap upload file 'stomata_hati.jpg' ke folder 'assets'.")
        
        sisi_list = res['sisi_list']
        nama_list = [SISI_NAMES[s] for s in sisi_list]
        if len(sisi_list) == 1:
            st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **{nama_list[0]}** (Sisi {sisi_list[0]})")
        else:
            st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **{', '.join(nama_list)}** (Sisi {', '.join(map(str, sisi_list))})")
        
        with st.expander("📖 Penjelasan 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"**{no}. {nama}**")
        
        st.info("💡 Hasil ini membantu Anda memahami keseimbangan Iman, Kasih, dan Pengharapan dalam hidup serta panggilan untuk berbuat.")
        
        # Tombol untuk reset setelah melihat hasil
        if st.button("🔄 Mulai Tes Ulang", use_container_width=True):
            reset_stomata()
            st.rerun()

if __name__ == "__main__":
    show_stomata()