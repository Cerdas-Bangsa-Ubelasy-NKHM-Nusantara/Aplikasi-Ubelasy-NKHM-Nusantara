# nkhm/stomata.py
import streamlit as st
import pandas as pd
import random

# ========== BANK SOAL ==========
SOAL_KASIH = [
    ("Kasih itu sabar dan murah hati.", True),
    ("Kasih itu cemburu dan sombong.", False),
    ("Kasih tidak melakukan yang tidak sopan dan tidak mencari keuntungan diri sendiri.", True),
    ("Kasih itu pemarah dan suka menyimpan kesalahan orang lain.", False),
    ("Kasih bersukacita karena ketidakadilan.", False),
    ("Kasih menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu.", True),
    ("Sekalipun ada karunia bernubuat, tanpa kasih kita berguna.", False),
    ("Sekalipun memiliki iman yang sempurna, tanpa kasih kita tidak berguna.", True),
    ("Sekalipun membagi-bagikan harta, tanpa kasih ada faedahnya.", False),
    ("Kasih adalah yang terbesar di antara iman, pengharapan, dan kasih.", True),
]

SOAL_IMAN = [
    ("Iman adalah dasar dari segala sesuatu yang kita harapkan dan bukti dari segala sesuatu yang tidak kita lihat.", True),
    ("Iman sebesar biji sesawi dapat memindahkan gunung.", True),
    ("Iman tanpa perbuatan adalah hidup.", False),
    ("Iman timbul dari pendengaran akan firman Allah.", True),
    ("Iman adalah anugerah Allah, bukan hasil usaha manusia.", True),
    ("Allah memberikan iman kepada setiap orang dengan ukuran yang sama.", False),
    ("Dengan iman kita menerima janji-janji Allah.", True),
    ("Iman hanya diperlukan untuk keselamatan, bukan untuk kehidupan sehari-hari.", False),
    ("Iman dapat ditingkatkan dengan membenamkan diri dalam firman Allah.", True),
    ("Iman yang dihasilkan oleh kasih adalah yang terpenting.", True),
]

SOAL_PENGHARAPAN = [
    ("Pengharapan akan kebangkitan orang mati adalah bagian dari iman Kristen.", True),
    ("Pengharapan yang dilihat bukanlah pengharapan lagi.", True),
    ("Pengharapan mengecewakan karena sering tidak terwujud.", False),
    ("Kita diselamatkan dalam pengharapan.", True),
    ("Pengharapan adalah sauh yang kuat dan aman bagi jiwa kita.", True),
    ("Pengharapan hanya untuk hidup di dunia ini.", False),
    ("Kristus adalah pengharapan akan kemuliaan.", True),
    ("Pengharapan membuat kita bertekun dalam doa.", True),
    ("Orang yang tidak mempunyai pengharapan akan berdukacita seperti orang lain.", False),
    ("Pengharapan kita tertuju kepada Allah melalui kebangkitan Yesus.", True),
]

SEMUA_SOAL = (
    [("Kasih", text, jawaban) for text, jawaban in SOAL_KASIH] +
    [("Iman", text, jawaban) for text, jawaban in SOAL_IMAN] +
    [("Pengharapan", text, jawaban) for text, jawaban in SOAL_PENGHARAPAN]
)

# Nama 12 sisi sesuai usulan
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

def init_stomata_state():
    if "stomata_answers" not in st.session_state:
        st.session_state.stomata_answers = {}
    if "stomata_submitted" not in st.session_state:
        st.session_state.stomata_submitted = False
    if "stomata_results" not in st.session_state:
        st.session_state.stomata_results = None
    if "stomata_shuffled" not in st.session_state:
        shuffled = SEMUA_SOAL.copy()
        random.shuffle(shuffled)
        st.session_state.stomata_shuffled = shuffled

def reset_stomata():
    st.session_state.stomata_answers = {}
    st.session_state.stomata_submitted = False
    st.session_state.stomata_results = None
    # jangan hapus shuffled agar urutan tetap konsisten per sesi

def hitung_persentase(jawaban_benar, total_soal=10):
    return (jawaban_benar / total_soal) * 100

def tentukan_sisi(persen_kasih, persen_iman, persen_pengharapan):
    """
    Menentukan sisi stomata berdasarkan persentase relatif.
    Logika di bawah ini contoh; Anda dapat mengubah sesuai preferensi.
    """
    # Normalisasi ke total 100% untuk perbandingan
    total = persen_kasih + persen_iman + persen_pengharapan
    if total == 0:
        return 10  # default
    rel_k = (persen_kasih / total) * 100
    rel_i = (persen_iman / total) * 100
    rel_p = (persen_pengharapan / total) * 100
    
    # Tentukan dominasi
    max_val = max(rel_k, rel_i, rel_p)
    if max_val >= 60:
        # Dominasi tunggal
        if rel_k == max_val:
            return 1  # Kasih
        elif rel_i == max_val:
            return 2  # Iman
        else:
            return 3  # Pengharapan
    elif max_val >= 40 and (rel_k + rel_i >= 70 or rel_i + rel_p >= 70 or rel_p + rel_k >= 70):
        # Kombinasi dua dominan
        if rel_k >= 40 and rel_i >= 40:
            return 5  # Kasih-Iman
        elif rel_i >= 40 and rel_p >= 40:
            return 4  # Iman-Pengharapan
        elif rel_p >= 40 and rel_k >= 40:
            return 6  # Pengharapan-Kasih
        else:
            return 10  # Kasih-Iman-Pengharapan (keseimbangan)
    else:
        # Nilai rendah atau seimbang – masuk ke tindakan
        # Berdasarkan nilai tertinggi untuk menentukan tindakan yang dominan
        if rel_k == max_val:
            return 9  # Berbuat kasih
        elif rel_i == max_val:
            return 7  # Berbuat iman
        else:
            return 8  # Berbuat pengharapan
    # Fallback
    return 10

def show_stomata():
    init_stomata_state()
    
    st.markdown("## 💖 Stomata Hati")
    st.markdown("""
    **Alat Uji Tingkat Iman, Kasih, dan Pengharapan (IKP)**  
    Berdasarkan 1 Korintus 13:13.
    
    Jawablah 30 pernyataan berikut dengan **Benar** atau **Salah**.  
    Setiap jawaban benar bernilai 1 poin. Setelah selesai, sistem akan menghitung persentase masing‑masing kriteria dan menentukan posisi Anda pada 12 sisi Stomata Hati.
    """)
    
    soal_list = st.session_state.stomata_shuffled
    
    with st.container(height=500):
        for idx, (kategori, text, _) in enumerate(soal_list):
            st.markdown(f"**{idx+1}. [{kategori}]** {text}")
            key = f"stomata_{idx}"
            current = st.session_state.stomata_answers.get(idx, None)
            selected = st.radio(
                "Jawaban:",
                ("Benar", "Salah"),
                index=0 if current == True else (1 if current == False else None),
                key=key,
                label_visibility="collapsed"
            )
            st.session_state.stomata_answers[idx] = (selected == "Benar")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Hitung Hasil Stomata", use_container_width=True):
            # Hitung skor per kategori
            skor_kasih = skor_iman = skor_pengharapan = 0
            for idx, (kategori, _, jawaban_benar) in enumerate(soal_list):
                if st.session_state.stomata_answers.get(idx, False) == jawaban_benar:
                    if kategori == "Kasih":
                        skor_kasih += 1
                    elif kategori == "Iman":
                        skor_iman += 1
                    else:
                        skor_pengharapan += 1
            # Pastikan semua soal telah dijawab
            if len(st.session_state.stomata_answers) < len(soal_list):
                st.error(f"Anda baru menjawab {len(st.session_state.stomata_answers)} dari {len(soal_list)} soal. Selesaikan semua!")
                return
            persen_kasih = hitung_persentase(skor_kasih, 10)
            persen_iman = hitung_persentase(skor_iman, 10)
            persen_pengharapan = hitung_persentase(skor_pengharapan, 10)
            sisi = tentukan_sisi(persen_kasih, persen_iman, persen_pengharapan)
            
            st.session_state.stomata_results = {
                "kasih": persen_kasih,
                "iman": persen_iman,
                "pengharapan": persen_pengharapan,
                "sisi": sisi,
                "nama_sisi": SISI_NAMES.get(sisi, "Tidak terdefinisi")
            }
            st.session_state.stomata_submitted = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_stomata()
            st.rerun()
    
    if st.session_state.stomata_submitted and st.session_state.stomata_results:
        res = st.session_state.stomata_results
        st.markdown("---")
        st.subheader("📊 Hasil Uji IKP")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Kasih", f"{res['kasih']:.1f}%")
        col_b.metric("Iman", f"{res['iman']:.1f}%")
        col_c.metric("Pengharapan", f"{res['pengharapan']:.1f}%")
        
        st.markdown(f"### 🌿 Posisi Stomata Hati Anda: **Sisi {res['sisi']} – {res['nama_sisi']}**")
        
        # Diagram sederhana (simbolik segitiga)
        st.markdown("""
        ```
              Kasih
               /\\
              /  \\
             /    \\
        Iman /______\\ Pengharapan
        ```
        """)
        
        with st.expander("📖 Penjelasan 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"**{no}. {nama}**")
        
        st.info("Hasil ini membantu Anda memahami keseimbangan Iman, Kasih, dan Pengharapan dalam hidup serta panggilan untuk berbuat.")

if __name__ == "__main__":
    # Untuk testing
    show_stomata()
