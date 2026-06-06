# nkhm/stomata.py
import streamlit as st
import random
import json
from pathlib import Path

# ========== MEMBACA SOAL DARI FILE JSON ==========
def load_soal_from_json(folder_name):
    """Membaca soal dari file JSON berdasarkan folder"""
    base_path = Path(__file__).parent / "soal_stomata_hati" / folder_name
    json_path = base_path / f"soal_{folder_name}.json"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.warning(f"⚠️ File soal {folder_name} tidak ditemukan di {json_path}")
        return []
    except json.JSONDecodeError:
        st.warning(f"⚠️ File {json_path} format JSON tidak valid")
        return []

def load_sampled_soal_stomata(jumlah_per_kategori=11):
    """
    Memuat soal dari ketiga kategori dan mengambil sample acak
    sebanyak jumlah_per_kategori dari setiap kategori
    """
    # Muat semua soal
    soal_kasih = load_soal_from_json("kasih")
    soal_iman = load_soal_from_json("iman")
    soal_pengharapan = load_soal_from_json("pengharapan")
    
    # Ambil sample acak dari setiap kategori
    sample_kasih = random.sample(soal_kasih, min(jumlah_per_kategori, len(soal_kasih))) if soal_kasih else []
    sample_iman = random.sample(soal_iman, min(jumlah_per_kategori, len(soal_iman))) if soal_iman else []
    sample_pengharapan = random.sample(soal_pengharapan, min(jumlah_per_kategori, len(soal_pengharapan))) if soal_pengharapan else []
    
    # Konversi ke format yang seragam
    all_soal = []
    for soal in sample_kasih:
        all_soal.append({
            "kategori": "Kasih",
            "id": soal.get("id", 0),
            "teks": soal.get("teks", ""),
            "pilihan": soal.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    for soal in sample_iman:
        all_soal.append({
            "kategori": "Iman",
            "id": soal.get("id", 0),
            "teks": soal.get("teks", ""),
            "pilihan": soal.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    for soal in sample_pengharapan:
        all_soal.append({
            "kategori": "Pengharapan",
            "id": soal.get("id", 0),
            "teks": soal.get("teks", ""),
            "pilihan": soal.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    
    # Acak urutan semua soal
    random.shuffle(all_soal)
    
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
        st.session_state.stomata_all_soal = load_sampled_soal_stomata(11)
    if "stomata_current_sample_size" not in st.session_state:
        st.session_state.stomata_current_sample_size = 11

def reset_stomata():
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    # Muat ulang dengan sample baru yang berbeda
    st.session_state.stomata_all_soal = load_sampled_soal_stomata(st.session_state.stomata_current_sample_size)

def refresh_questions():
    """Mengganti soal dengan sample baru (tanpa reset jawaban)"""
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    st.session_state.stomata_all_soal = load_sampled_soal_stomata(st.session_state.stomata_current_sample_size)

def hitung_persentase(skor, max_skor=44):
    """
    Menghitung persentase dari skor Likert.
    Maksimal skor per kategori: 11 soal × 4 = 44 poin
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
    
    Anda akan menjawab **33 pernyataan** (11 Iman + 11 Kasih + 11 Pengharapan) yang dipilih secara acak dari total 99 soal.  
    
    **Skala Jawaban (0-4):**  
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

    # Informasi jumlah soal per kategori
    jumlah_kasih = sum(1 for s in soal_list if s['kategori'] == "Kasih")
    jumlah_iman = sum(1 for s in soal_list if s['kategori'] == "Iman")
    jumlah_pengharapan = sum(1 for s in soal_list if s['kategori'] == "Pengharapan")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.info(f"💖 **Kasih:** {jumlah_kasih} soal")
    with col_info2:
        st.info(f"🙏 **Iman:** {jumlah_iman} soal")
    with col_info3:
        st.info(f"✨ **Pengharapan:** {jumlah_pengharapan} soal")
    
    # Tombol untuk refresh soal (mendapatkan sample baru)
    col_refresh1, col_refresh2 = st.columns([3, 1])
    with col_refresh2:
        if st.button("🔄 Ganti Soal", use_container_width=True, help="Ambil sample soal baru yang berbeda"):
            refresh_questions()
            st.rerun()
    
    st.markdown("---")

    with st.form(key="stomata_form"):
        st.markdown(f"### 📝 Total Soal: {total_soal}")
        
        # Gunakan container dengan scrolling
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
                    label_visibility="collapsed",
                    horizontal=True
                )
                if selected:
                    st.session_state.stomata_answers[idx] = selected
                st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            submitted = st.form_submit_button("📊 Hitung Hasil Sto-mata", use_container_width=True, type="primary")
        with col2:
            reset_clicked = st.form_submit_button("🔄 Reset Semua Jawaban", use_container_width=True)
        with col3:
            if st.form_submit_button("🎲 Soal Baru", use_container_width=True):
                refresh_questions()
                st.rerun()
    
    if reset_clicked:
        reset_stomata()
        st.rerun()
    
    if submitted:
        soal_terjawab = len(st.session_state.stomata_answers)
        if soal_terjawab < total_soal:
            st.error(f"⚠️ Anda baru menjawab {soal_terjawab} dari {total_soal} soal. Selesaikan semua soal terlebih dahulu!")
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
            
            # Maksimal skor per kategori: 11 soal × 4 = 44
            max_per_kategori = 11 * 4
            persen_kasih = hitung_persentase(skor_kasih, max_per_kategori)
            persen_iman = hitung_persentase(skor_iman, max_per_kategori)
            persen_pengharapan = hitung_persentase(skor_pengharapan, max_per_kategori)
            
            sisi_list = tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan)
            
            st.session_state.stomata_results = {
                "kasih": persen_kasih,
                "iman": persen_iman,
                "pengharapan": persen_pengharapan,
                "sisi_list": sisi_list,
                "skor_kasih": skor_kasih,
                "skor_iman": skor_iman,
                "skor_pengharapan": skor_pengharapan,
                "max_per_kategori": max_per_kategori,
                "jumlah_soal_kasih": jumlah_kasih,
                "jumlah_soal_iman": jumlah_iman,
                "jumlah_soal_pengharapan": jumlah_pengharapan,
            }
            st.session_state.stomata_submitted = True
            st.rerun()

    if st.session_state.stomata_submitted and st.session_state.stomata_results:
        res = st.session_state.stomata_results
        st.markdown("---")
        st.subheader("📊 Hasil Uji IKP")
        
        # Tampilkan hasil dalam bentuk meter
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("💖 Kasih", f"{res['kasih']:.1f}%")
            st.progress(res['kasih']/100)
        with col_b:
            st.metric("🙏 Iman", f"{res['iman']:.1f}%")
            st.progress(res['iman']/100)
        with col_c:
            st.metric("✨ Pengharapan", f"{res['pengharapan']:.1f}%")
            st.progress(res['pengharapan']/100)
        
        # Tampilkan skor mentah
        with st.expander("📈 Detail Skor Mentah"):
            st.metric("Skor Kasih", f"{res['skor_kasih']} / {res['max_per_kategori']} ({res['jumlah_soal_kasih']} soal × 4)")
            st.metric("Skor Iman", f"{res['skor_iman']} / {res['max_per_kategori']} ({res['jumlah_soal_iman']} soal × 4)")
            st.metric("Skor Pengharapan", f"{res['skor_pengharapan']} / {res['max_per_kategori']} ({res['jumlah_soal_pengharapan']} soal × 4)")
        
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
        
        # Tombol aksi setelah hasil
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🔄 Tes Lagi (Soal Baru)", use_container_width=True):
                refresh_questions()
                st.rerun()
        with col_btn2:
            if st.button("📝 Reset & Ulangi", use_container_width=True):
                reset_stomata()
                st.rerun()
        with col_btn3:
            if st.button("👍 Selesai", use_container_width=True):
                st.session_state.stomata_submitted = False
                st.rerun()

if __name__ == "__main__":
    show_stomata()