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
    if len(soal_kasih) >= jumlah_per_kategori:
        sample_kasih = random.sample(soal_kasih, jumlah_per_kategori)
    else:
        sample_kasih = soal_kasih
        st.warning(f"⚠️ Soal Kasih hanya {len(soal_kasih)} tersedia, kurang dari {jumlah_per_kategori}")
    
    if len(soal_iman) >= jumlah_per_kategori:
        sample_iman = random.sample(soal_iman, jumlah_per_kategori)
    else:
        sample_iman = soal_iman
        st.warning(f"⚠️ Soal Iman hanya {len(soal_iman)} tersedia, kurang dari {jumlah_per_kategori}")
    
    if len(soal_pengharapan) >= jumlah_per_kategori:
        sample_pengharapan = random.sample(soal_pengharapan, jumlah_per_kategori)
    else:
        sample_pengharapan = soal_pengharapan
        st.warning(f"⚠️ Soal Pengharapan hanya {len(soal_pengharapan)} tersedia, kurang dari {jumlah_per_kategori}")
    
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

# ========== SKOR LIKERT ==========
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
    if "stomata_refresh_counter" not in st.session_state:
        st.session_state.stomata_refresh_counter = 0

def reset_stomata():
    """Reset semua jawaban dan hasil"""
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    # Jangan load ulang soal, biarkan soal yang sama

def refresh_questions():
    """Mengganti soal dengan sample baru yang benar-benar berbeda"""
    # Load soal baru dengan sample acak
    st.session_state.stomata_all_soal = load_sampled_soal_stomata(11)
    # Reset jawaban dan hasil
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    # Increment counter untuk memaksa rerun
    st.session_state.stomata_refresh_counter += 1

def hitung_persentase(skor, max_skor=44):
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

def show_stomata():
    init_stomata_state()

    st.markdown("## 💖 Sto-mata Hati")
    st.markdown("""
    **Alat Uji Tingkat Iman, Kasih, dan Pengharapan (IKP)**  
    
    Anda akan menjawab **33 pernyataan** (11 Iman + 11 Kasih + 11 Pengharapan) yang dipilih secara acak dari total soal.  
    
    **Skala Jawaban (0-4):**  
    - Sangat Tidak Setuju = 0 | Tidak Setuju = 1 | Netral = 2 | Setuju = 3 | Sangat Setuju = 4
    """)

    soal_list = st.session_state.stomata_all_soal
    total_soal = len(soal_list)

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
    
    # Tombol untuk refresh soal
    col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
    with col_btn1:
        if st.button("🔄 Ganti Soal Baru (Acak)", use_container_width=True, type="primary"):
            refresh_questions()
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Reset Jawaban Saja", use_container_width=True):
            reset_stomata()
            st.rerun()
    
    st.markdown("---")

    # Form untuk soal
    with st.form(key="stomata_form"):
        st.markdown(f"### 📝 Soal {total_soal} (Silakan dijawab semua)")
        
        with st.container(height=500):
            for idx, soal in enumerate(soal_list):
                st.markdown(f"**{idx+1}. [{soal['kategori']}]** {soal['teks']}")
                key = f"stomata_radio_{idx}_{soal['id']}_{st.session_state.stomata_refresh_counter}"
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
        
        col_submit1, col_submit2 = st.columns(2)
        with col_submit1:
            submitted = st.form_submit_button("📊 Hitung Hasil Sto-mata", use_container_width=True, type="primary")
        with col_submit2:
            if st.form_submit_button("🎲 Ambil Soal Baru", use_container_width=True):
                refresh_questions()
                st.rerun()
    
    if submitted:
        soal_terjawab = len(st.session_state.stomata_answers)
        if soal_terjawab < total_soal:
            st.error(f"⚠️ Anda baru menjawab {soal_terjawab} dari {total_soal} soal. Selesaikan semua soal terlebih dahulu!")
        else:
            # Hitung skor
            skor_kasih = skor_iman = skor_pengharapan = 0
            
            for idx, soal in enumerate(soal_list):
                jawaban = st.session_state.stomata_answers.get(idx)
                nilai = LIKERT_SCORE.get(jawaban, 0)
                
                if soal['kategori'] == "Kasih":
                    skor_kasih += nilai
                elif soal['kategori'] == "Iman":
                    skor_iman += nilai
                else:
                    skor_pengharapan += nilai
            
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
            }
            st.session_state.stomata_submitted = True
            st.rerun()

    # Tampilkan hasil jika sudah submit
    if st.session_state.stomata_submitted and st.session_state.stomata_results:
        res = st.session_state.stomata_results
        st.markdown("---")
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
        
        with st.expander("📈 Detail Skor Mentah"):
            st.metric("Skor Kasih", f"{res['skor_kasih']} / {res['max_per_kategori']}")
            st.metric("Skor Iman", f"{res['skor_iman']} / {res['max_per_kategori']}")
            st.metric("Skor Pengharapan", f"{res['skor_pengharapan']} / {res['max_per_kategori']}")
        
        sisi_list = res['sisi_list']
        nama_list = [SISI_NAMES[s] for s in sisi_list]
        if len(sisi_list) == 1:
            st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **{nama_list[0]}** (Sisi {sisi_list[0]})")
        else:
            st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **{', '.join(nama_list)}** (Sisi {', '.join(map(str, sisi_list))})")
        
        with st.expander("📖 Penjelasan 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"**{no}. {nama}**")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎲 Tes Lagi dengan Soal Baru", use_container_width=True):
                refresh_questions()
                st.rerun()
        with col_btn2:
            if st.button("📝 Reset & Mulai Lagi", use_container_width=True):
                reset_stomata()
                st.rerun()

if __name__ == "__main__":
    show_stomata()