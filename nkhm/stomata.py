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

def get_random_soals():
    """
    Mengambil 11 soal acak dari setiap kategori
    Fungsi ini dipanggil ULANG setiap kali diperlukan
    """
    # Muat semua soal dari file JSON
    soal_kasih = load_soal_from_json("kasih")
    soal_iman = load_soal_from_json("iman")
    soal_pengharapan = load_soal_from_json("pengharapan")
    
    # Validasi jumlah soal
    if len(soal_kasih) < 11:
        st.warning(f"⚠️ Soal Kasih hanya {len(soal_kasih)} tersedia")
        sample_kasih = soal_kasih
    else:
        sample_kasih = random.sample(soal_kasih, 11)
    
    if len(soal_iman) < 11:
        st.warning(f"⚠️ Soal Iman hanya {len(soal_iman)} tersedia")
        sample_iman = soal_iman
    else:
        sample_iman = random.sample(soal_iman, 11)
    
    if len(soal_pengharapan) < 11:
        st.warning(f"⚠️ Soal Pengharapan hanya {len(soal_pengharapan)} tersedia")
        sample_pengharapan = soal_pengharapan
    else:
        sample_pengharapan = random.sample(soal_pengharapan, 11)
    
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

# ========== SKOR LIKERT (0-4) dan KONVERSI KE SKOR 0-1 ==========
LIKERT_SCORE = {
    "Sangat Tidak Setuju": 0,
    "Tidak Setuju": 1,
    "Netral": 2,
    "Setuju": 3,
    "Sangat Setuju": 4
}

def konversi_ke_skor_0_1(nilai_likert):
    """
    Mengkonversi nilai Likert 0-4 menjadi skor 0-1
    Nilai 3 atau 4 dianggap positif (skor 1)
    Nilai 0,1,2 dianggap negatif/netral (skor 0)
    """
    return 1 if nilai_likert >= 3 else 0

def init_stomata_state():
    """Inisialisasi state"""
    if "stomata_answers" not in st.session_state:
        st.session_state.stomata_answers = {}
    if "stomata_submitted" not in st.session_state:
        st.session_state.stomata_submitted = False
    if "stomata_results" not in st.session_state:
        st.session_state.stomata_results = None
    if "stomata_soal_version" not in st.session_state:
        st.session_state.stomata_soal_version = 0
    if "stomata_all_soal" not in st.session_state:
        st.session_state.stomata_all_soal = get_random_soals()

def force_refresh_questions():
    """Memaksa refresh soal dengan version increment"""
    new_soals = get_random_soals()
    st.session_state.stomata_all_soal = new_soals
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    st.session_state.stomata_soal_version += 1

def hide_results():
    """Reset jawaban dan sembunyikan hasil (tanpa menghapus jawaban yang sudah diisi)"""
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None

def hitung_persentase(skor, max_skor=11):
    """Menghitung persentase dari skor (maksimal 11 per kategori)"""
    return (skor / max_skor) * 100 if max_skor > 0 else 0

def tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan):
    total = persen_kasih + persen_iman + persen_pengharapan
    if total == 0:
        return [10]
    
    rk = (persen_kasih / total) * 100
    ri = (persen_iman / total) * 100
    rp = (persen_pengharapan / total) * 100

    if max(rk, ri, rp) - min(rk, ri, rp) < 5:
        return [1, 8, 9]

    max_val = max(rk, ri, rp)
    if max_val >= 60:
        if rk == max_val:
            return [1]
        elif ri == max_val:
            return [2]
        else:
            return [3]
    elif (rk >= 40 and ri >= 40) or (ri >= 40 and rp >= 40) or (rp >= 40 and rk >= 40):
        if rk >= 40 and ri >= 40:
            return [5]
        elif ri >= 40 and rp >= 40:
            return [4]
        elif rp >= 40 and rk >= 40:
            return [6]
        else:
            return [10]
    else:
        if rk == max_val:
            return [9]
        elif ri == max_val:
            return [7]
        else:
            return [8]

def tampilkan_hasil():
    """Fungsi untuk menghitung dan menampilkan hasil"""
    soal_list = st.session_state.stomata_all_soal
    total_soal = len(soal_list)
    
    if len(st.session_state.stomata_answers) < total_soal:
        st.error(f"⚠️ Anda baru menjawab {len(st.session_state.stomata_answers)} dari {total_soal} soal. Selesaikan semua soal terlebih dahulu!")
        return False
    
    # Hitung skor (konversi ke 0-1 per soal)
    skor_kasih = 0
    skor_iman = 0
    skor_pengharapan = 0
    
    # Hitung juga skor mentah Likert untuk informasi tambahan
    skor_mentah_kasih = 0
    skor_mentah_iman = 0
    skor_mentah_pengharapan = 0
    
    for idx, soal in enumerate(soal_list):
        jawaban = st.session_state.stomata_answers.get(idx)
        nilai_likert = LIKERT_SCORE.get(jawaban, 0)
        nilai_0_1 = konversi_ke_skor_0_1(nilai_likert)
        
        if soal['kategori'] == "Kasih":
            skor_mentah_kasih += nilai_likert
            skor_kasih += nilai_0_1
        elif soal['kategori'] == "Iman":
            skor_mentah_iman += nilai_likert
            skor_iman += nilai_0_1
        else:  # Pengharapan
            skor_mentah_pengharapan += nilai_likert
            skor_pengharapan += nilai_0_1
    
    max_per_kategori = 11  # Maksimal 11 soal × 1 poin
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
        "skor_mentah_kasih": skor_mentah_kasih,
        "skor_mentah_iman": skor_mentah_iman,
        "skor_mentah_pengharapan": skor_mentah_pengharapan,
        "max_per_kategori": max_per_kategori,
        "max_mentah_per_kategori": 44,  # 11 soal × 4
    }
    st.session_state.stomata_submitted = True
    return True

def show_stomata():
    init_stomata_state()

    st.markdown("## 💖 Sto-mata Hati")
    st.markdown("""
    **Alat Uji Tingkat Iman, Kasih, dan Pengharapan (IKP)**  
    
    Anda akan menjawab **33 pernyataan** (11 Iman + 11 Kasih + 11 Pengharapan) yang dipilih secara acak dari total soal.  
    
    **Skala Jawaban (0-4):**  
    - Sangat Tidak Setuju = 0 | Tidak Setuju = 1 | Netral = 2 | Setuju = 3 | Sangat Setuju = 4
    
    **Penilaian:** Jawaban dengan skala **Setuju (3)** atau **Sangat Setuju (4)** dihitung sebagai **1 poin**.  
    Maksimal skor per kategori adalah **11 poin** (dari 11 soal).
    
    **Jawaban akan otomatis tersimpan** setiap kali Anda memilih opsi.
    """)

    soal_list = st.session_state.stomata_all_soal
    total_soal = len(soal_list)
    current_version = st.session_state.stomata_soal_version

    if total_soal == 0:
        st.error("❌ Tidak ada soal yang ditemukan. Pastikan folder 'soal_stomata_hati' berisi file JSON!")
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
    
    st.markdown("---")
    
    # Tombol kontrol di atas
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔄 Ganti Semua Soal (Baru)", use_container_width=True, type="primary"):
            force_refresh_questions()
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Reset Jawaban Saya (Sembunyikan Hasil)", use_container_width=True, help="Sembunyikan hasil yang sudah ditampilkan (jawaban tetap tersimpan)"):
            hide_results()
            st.rerun()
    
    st.markdown("---")
    
    # Tampilkan soal-soal
    st.markdown(f"### 📝 Soal - Versi {current_version + 1}")
    
    # Gunakan container dengan scrolling untuk soal
    with st.container(height=500):
        for idx, soal in enumerate(soal_list):
            with st.container():
                st.markdown(f"**{idx+1}. [{soal['kategori']}]** {soal['teks']}")
                key = f"stomata_radio_{idx}_{soal['id']}_v{current_version}"
                current = st.session_state.stomata_answers.get(idx, None)
                
                # Cari index dari current value
                current_index = None
                if current in soal['pilihan']:
                    current_index = soal['pilihan'].index(current)
                
                selected = st.radio(
                    "Pilih jawaban:",
                    soal['pilihan'],
                    index=current_index,
                    key=key,
                    label_visibility="collapsed",
                    horizontal=True
                )
                
                # Simpan jawaban secara otomatis saat berubah
                if selected != current:
                    st.session_state.stomata_answers[idx] = selected
                    # Jika jawaban berubah, sembunyikan hasil yang lama karena sudah tidak valid
                    if st.session_state.stomata_submitted:
                        hide_results()
                    st.rerun()
                
                st.markdown("---")
    
    # Progress bar diletakkan di bawah setelah semua soal (sebelum tombol Lihat Hasil)
    st.markdown("---")
    jawaban_terjawab = len(st.session_state.stomata_answers)
    st.progress(jawaban_terjawab / total_soal, text=f"📊 Progress: {jawaban_terjawab} dari {total_soal} soal terjawab")
    
    # Tombol Lihat Hasil di bawah progress bar
    st.markdown("---")
    col_result1, col_result2, col_result3 = st.columns([1, 2, 1])
    with col_result2:
        if st.button("📊 Lihat Hasil", use_container_width=True, type="primary"):
            if tampilkan_hasil():
                st.rerun()

    # Tampilkan hasil jika sudah submit
    if st.session_state.stomata_submitted and st.session_state.stomata_results:
        st.markdown("---")
        
        res = st.session_state.stomata_results
        
        # Tampilkan 3 metrik persentase
        st.subheader("📊 Hasil Uji IKP")
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
        
        # Detail Skor Mentah (dalam expander)
        with st.expander("📈 Detail Skor Mentah"):
            st.markdown("**Skor berdasarkan jawaban Setuju/Sangat Setuju (1 poin per soal):**")
            st.metric("Skor Kasih", f"{res['skor_kasih']} / {res['max_per_kategori']} poin")
            st.metric("Skor Iman", f"{res['skor_iman']} / {res['max_per_kategori']} poin")
            st.metric("Skor Pengharapan", f"{res['skor_pengharapan']} / {res['max_per_kategori']} poin")
            
            st.markdown("---")
            st.markdown("**Skor Likert mentah (0-4 per soal):**")
            st.metric("Skor Mentah Kasih", f"{res['skor_mentah_kasih']} / {res['max_mentah_per_kategori']}")
            st.metric("Skor Mentah Iman", f"{res['skor_mentah_iman']} / {res['max_mentah_per_kategori']}")
            st.metric("Skor Mentah Pengharapan", f"{res['skor_mentah_pengharapan']} / {res['max_mentah_per_kategori']}")
        
        # Gambar stomata hati
        img_path = Path(__file__).parent.parent / "assets" / "stomata_hati.jpg"
        if img_path.exists():
            st.image(str(img_path), caption="Stomata Hati - Segitiga Iman, Kasih, Pengharapan", use_container_width=True)
        else:
            st.warning("⚠️ Gambar Stomata Hati belum tersedia. Harap upload file 'stomata_hati.jpg' ke folder 'assets'.")
        
        # Posisi Stomata Hati
        sisi_list = res['sisi_list']
        nama_list = [SISI_NAMES[s] for s in sisi_list]
        if len(sisi_list) == 1:
            st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **{nama_list[0]}** (Sisi {sisi_list[0]})")
        else:
            st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **{', '.join(nama_list)}** (Sisi {', '.join(map(str, sisi_list))})")
        
        # Penjelasan 12 sisi
        with st.expander("📖 Penjelasan 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"**{no}. {nama}**")
        
        # Tombol aksi setelah hasil
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎲 Tes Lagi dengan Soal Baru", use_container_width=True):
                force_refresh_questions()
                st.rerun()
        with col_btn2:
            if st.button("📝 Mulai Lagi (Soal Sama)", use_container_width=True):
                hide_results()
                st.rerun()

if __name__ == "__main__":
    show_stomata()