# nkhm/tutorial.py
"""
Modul Tutorial untuk NKHM Nusantara.
Berisi panduan lengkap semua fitur aplikasi.
"""

import streamlit as st
import logging

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== STYLING ==========
def inject_tutorial_css():
    """Menambahkan CSS kustom untuk tampilan tutorial."""
    st.markdown("""
    <style>
    .tutorial-step {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        padding: 12px 0;
        border-bottom: 1px solid #e9ecef;
    }
    .tutorial-step:last-child {
        border-bottom: none;
    }
    .tutorial-number {
        background-color: #2e7daf;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
        font-size: 14px;
    }
    .tutorial-icon {
        font-size: 24px;
        margin-right: 8px;
    }
    .tutorial-tip {
        background-color: #e8f0fe;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 12px 0;
        border-left: 4px solid #2e7daf;
    }
    .tutorial-warning {
        background-color: #fff3cd;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 12px 0;
        border-left: 4px solid #ffc107;
    }
    .tutorial-success {
        background-color: #d4edda;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 12px 0;
        border-left: 4px solid #28a745;
    }
    .dark-mode .tutorial-step {
        border-bottom-color: #333;
    }
    .dark-mode .tutorial-tip {
        background-color: #1a1a3a;
        border-left-color: #4a8abf;
    }
    .dark-mode .tutorial-warning {
        background-color: #2a2a0a;
        border-left-color: #ffc107;
    }
    .dark-mode .tutorial-success {
        background-color: #0a2a1a;
        border-left-color: #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

def create_step(number, title, description):
    """Membuat elemen step tutorial menggunakan columns."""
    col1, col2 = st.columns([1, 11])
    with col1:
        st.markdown(f'<div class="tutorial-number">{number}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f"**{title}**")
        st.markdown(description)

def show_tutorial_umum():
    """Tutorial umum tentang aplikasi NKHM."""
    st.markdown("## 🌿 Selamat Datang di NKHM Nusantara")
    st.markdown("Aplikasi pembelajaran berbasis kecerdasan untuk mengembangkan **IQ, EQ, SQ, AQ** dan **Nasionalisme**.")
    
    with st.expander("🎯 Apa itu NKHM?", expanded=True):
        st.markdown("""
        **NKHM** adalah singkatan dari **Nusantara Kecerdasan Hati dan Minda**.
        Aplikasi ini dirancang untuk mengembangkan 4 kecerdasan utama:
        
        - **🧠 IQ (Intelligence Quotient)** – Kecerdasan intelektual, logika, dan analisis
        - **❤️ EQ (Emotional Quotient)** – Kecerdasan emosional, empati, dan sosial
        - **🙏 SQ (Spiritual Quotient)** – Kecerdasan spiritual, nilai, dan makna hidup
        - **💪 AQ (Adversity Quotient)** – Kecerdasan menghadapi tantangan dan kesulitan
        - **🇮🇩 Nasionalisme** – Cinta tanah air dan kebangsaan
        """)
    
    with st.expander("📊 Rumus NKHM", expanded=True):
        st.markdown("""
        ```
        NKHM_Q = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
        NKHM_Total = (NKHM_Q + Nasionalisme) / 2
        ```
        💡 Semakin tinggi NKHM Total, semakin baik perkembangan kecerdasan Anda!
        """)
    
    st.info("💡 **Tips Awal:** Mulailah dengan mengerjakan kuis untuk mendapatkan skor awal Anda.")

def show_tutorial_kuis():
    """Tutorial fitur Kuis."""
    st.markdown("## 🎮 Fitur Kuis")
    
    with st.expander("📝 Cara Menggunakan Kuis", expanded=True):
        create_step(1, "Pilih Filter Soal", "Gunakan filter **Kategori** (Semua, Nasionalisme, Umum) dan **Fokus** (Semua, IQ, EQ, SQ, AQ, Nasionalisme) untuk memilih jenis soal.")
        create_step(2, "Baca Soal dengan Seksama", "Setiap soal memiliki teks dan pilihan jawaban. Pilih jawaban yang menurut Anda benar.")
        create_step(3, "Klik 'JAWAB'", "Setelah memilih jawaban, klik tombol **JAWAB** untuk mengirimkan jawaban.")
        create_step(4, "Lihat Feedback", "Setelah menjawab, Anda akan melihat feedback **✅ BENAR** atau **❌ SALAH**. Jawaban benar akan menambah poin sesuai kategori.")
        create_step(5, "Navigasi ke Soal Berikutnya", "Gunakan tombol **⏩ SOAL BERIKUTNYA** untuk melanjutkan ke soal berikutnya, atau **🔄 KUIS BARU** untuk memulai ulang dari awal.")
    
    st.success("💡 **Tips:** Kerjakan soal sebanyak-banyaknya untuk meningkatkan skor NKHM Anda! Setiap jawaban benar akan menambah poin pada kategori yang bersangkutan.")
    st.warning("⚠️ **Perhatikan:** Soal dengan filter berbeda akan menghasilkan soal yang berbeda pula. Ganti filter untuk variasi soal yang lebih banyak.")

def show_tutorial_dasbor():
    """Tutorial fitur Dasbor."""
    st.markdown("## 📊 Fitur Dasbor")
    
    with st.expander("👤 Dasbor Saya", expanded=True):
        st.markdown("Dasbor menampilkan ringkasan perkembangan dan rekomendasi personal Anda.")
        
        st.markdown("#### 📋 Ringkasan & Progres")
        st.markdown("""
        - **👤 Nama Pengguna** – Nama yang Anda gunakan saat login
        - **📖 Total Soal Dikerjakan** – Jumlah soal yang sudah Anda jawab
        - **🏆 NKHM Total** – Skor NKHM keseluruhan Anda
        - **📈 Perkembangan NKHM** – Grafik perkembangan skor Anda
        - **🧠 Analisis Kecerdasan** – Skor per kategori (IQ, EQ, SQ, AQ, Nasionalisme)
        - **💡 Rekomendasi Personal** – Saran untuk meningkatkan setiap kategori
        - **📋 Riwayat Terbaru** – 5 soal terakhir yang Anda kerjakan
        - **🎯 Target Berikutnya** – Target skor berikutnya untuk dicapai
        """)
        
        st.markdown("#### 📝 Catatan")
        st.markdown("""
        - **✏️ Catatan Cepat** – Tulis catatan harian atau ide belajar
        - **📱 Catatan Pribadi (React)** – Aplikasi catatan interaktif dengan fitur lengkap
        """)
    
    with st.expander("📊 Dasbor NKHM", expanded=True):
        st.markdown("""
        - **🧠 NKHM_Q** – Skor kombinasi IQ, EQ, SQ, dan AQ
        - **🏆 NKHM Total** – Gabungan NKHM_Q dan Nasionalisme
        - **📊 Grafik Skor** – Visualisasi skor per kategori
        - **📖 Tentang Rumus** – Penjelasan rumus perhitungan NKHM
        """)
    
    st.info("💡 **Tips:** Gunakan fitur **Catatan** untuk mencatat hal-hal penting yang Anda pelajari. Catatan disimpan di server dan bisa diakses kembali kapan saja.")

def show_tutorial_prestasi():
    """Tutorial fitur Prestasi."""
    st.markdown("## 🏆 Fitur Prestasi")
    
    with st.expander("🏅 Pencapaian", expanded=True):
        st.markdown("Fitur ini menampilkan badge yang Anda peroleh berdasarkan pencapaian:")
        st.markdown("""
        - **🧠 Cendekia** – IQ ≥ 50
        - **❤️ Empati** – EQ ≥ 50
        - **🙏 Bhinneka** – SQ ≥ 50
        - **💪 Tangguh** – AQ ≥ 50
        - **🇮🇩 Patriot** – Nasionalisme ≥ 50
        - **🌟 Pahlawan Cerdas Nusantara** – Semua kategori ≥ 50
        """)
        st.success("Jika semua kategori ≥ 50, Anda akan mendapatkan gelar **PAHLAWAN CERDAS NUSANTARA**! 🎉")
    
    with st.expander("📊 Statistik", expanded=True):
        st.markdown("""
        - **📖 Total Soal** – Jumlah soal yang sudah dikerjakan
        - **✅ Benar** – Jumlah jawaban benar
        - **📊 Akurasi** – Persentase jawaban benar
        """)
    
    with st.expander("🏆 Leaderboard", expanded=True):
        st.markdown("""
        - **🏅 Peringkat** – 10 pemain teratas berdasarkan skor NKHM
        - **🎖️ Peraih Medali** – 3 pemain teratas mendapat medali emas, perak, perunggu
        - **📊 Statistik Kompetitif** – Total peserta, rata-rata skor, skor tertinggi
        - **🎯 Level & Progress** – Level Anda dan progress menuju level berikutnya
        - **📈 Tren Skor** – Distribusi skor semua peserta
        """)
    
    st.info("💡 **Tips:** Semakin tinggi skor Anda, semakin tinggi posisi Anda di leaderboard. Kejar posisi teratas dan raih medali emas! 🥇")

def show_tutorial_tanding():
    """Tutorial fitur Tanding."""
    st.markdown("## ⚔️ Fitur Tanding")
    
    with st.expander("⚔️ Mode 1v1 (Hot Seat)", expanded=True):
        st.markdown("Dua pemain bergantian menjawab soal menggunakan **perangkat yang sama**.")
        st.markdown("#### 📋 Cara Bermain:")
        create_step(1, "Atur Pertandingan", "Masukkan nama kedua pemain, pilih jumlah soal (3, 5, 7, atau 10), dan tentukan waktu per giliran (15, 30, 45, atau 60 detik).")
        create_step(2, "Bergantian Menjawab", "Pemain bergiliran menjawab soal. Pemain yang gilirannya sedang aktif harus menjawab sebelum waktu habis.")
        create_step(3, "Lihat Hasil", "Setelah semua soal selesai, aplikasi akan menampilkan pemenang berdasarkan poin tertinggi.")
    
    with st.expander("🏆 Mode Turnamen Kelas", expanded=True):
        st.markdown("Sistem gugur untuk kompetisi antar peserta.")
        st.markdown("""
        - **Peserta** – Masukkan nama peserta (pisahkan dengan koma)
        - **Bracket** – Sistem pertandingan gugur
        - **Pemenang** – Peserta yang memenangkan semua pertandingan
        """)
    
    st.info("💡 **Tips:** Mode Tanding sangat cocok untuk kompetisi di kelas atau antar teman. Semakin banyak soal, semakin seru pertandingannya!")

def show_tutorial_karunia():
    """Tutorial fitur Karunia."""
    st.markdown("## 🎁 Fitur Karunia Motivasi")
    
    with st.expander("📜 Karunia Umum", expanded=True):
        st.markdown("Tes untuk mengetahui 7 karunia motivasi Anda:")
        st.markdown("""
        1. **Bernubuat (Perceiver)** – Melihat kebenaran, membedakan baik dan jahat
        2. **Melayani (Doer)** – Menolong dan memenuhi kebutuhan praktis
        3. **Mengajar (Teacher)** – Menyampaikan kebenaran secara logis
        4. **Menasihati (Encourager)** – Mendorong dan memotivasi orang lain
        5. **Memberi (Giver)** – Memberi dengan sukacita
        6. **Memimpin (Leader)** – Memimpin dan mengarahkan orang lain
        7. **Berbelas Kasihan (Compassion)** – Mengasihi dan menolong yang menderita
        """)
        st.markdown("**Cara:** Jawab 70 pernyataan dengan nilai 0-5. Hasil akan menunjukkan 3 karunia tertinggi Anda.")
    
    with st.expander("✨ Karunia 140 Karakter", expanded=True):
        st.markdown("""
        Versi lebih detail dengan 140 pernyataan untuk mengidentifikasi karunia motivasi.
        - 140 pernyataan dengan skala 0-5
        - Hasil menunjukkan 3 karunia tertinggi
        - Cocok untuk analisis yang lebih mendalam
        """)
    
    with st.expander("📋 Karakter & Masalah", expanded=True):
        st.markdown("""
        Menggabungkan 140 pernyataan karakteristik dengan 35 pernyataan masalah.
        - Total 175 pernyataan
        - Membantu mengidentifikasi potensi dan area pengembangan
        """)
    
    with st.expander("💖 Sto-mata Hati", expanded=True):
        st.markdown("Alat uji tingkat Iman, Kasih, dan Pengharapan (IKP) dengan 3 mode:")
        st.markdown("""
        - **📝 Tanggapan (Skala Likert)** – 33 pernyataan dengan skala 0-4
        - **✅ Pilihan Benar/Salah** – 33 pernyataan benar/salah
        - **🔢 Pilihan Ganda** – 33 soal pilihan ganda (a, b, c, d)
        """)
        st.markdown("Hasil menunjukkan posisi Stomata Hati berdasarkan 12 sisi.")
    
    with st.expander("📚 Pengembangan Diri", expanded=True):
        st.markdown("Materi edukasi dalam format markdown untuk pengembangan diri dan literasi keuangan.")
        st.markdown("""
        - **📚 Pengembangan Diri** – Materi spiritual, mental, dan karakter
        - **💰 Literasi Keuangan** – Panduan mengelola keuangan dan investasi
        """)
    
    st.info("💡 **Tips:** Tes karunia membantu Anda memahami potensi diri dan area pengembangan dalam pelayanan.")

def show_tutorial_hadiah():
    """Tutorial fitur Hadiah."""
    st.markdown("## 🎁 Fitur Hadiah & Permainan")
    
    with st.expander("🦅 Tebak Pahlawan", expanded=True):
        st.markdown("Tebak pahlawan nasional dari 12 pahlawan yang tersedia.")
        st.markdown("""
        - **Aturan:** 5 kesempatan untuk mengumpulkan skor
        - **Benar:** +10 poin
        - **Target:** Pahlawan berganti setelah setiap tebakan
        """)
    
    with st.expander("🔢 Angka Rahasia", expanded=True):
        st.markdown("Permainan angka untuk melatih logika dan perhitungan.")
        st.markdown("""
        - Tuliskan deretan angka di Baris 1
        - Aplikasi menyiapkan jawaban rahasia
        - Lengkapi Baris 2-5 sesuai petunjuk
        - Cocokkan hasil penjumlahan dengan jawaban rahasia
        """)
    
    with st.expander("🚣 Pahlawan Menyeberang Sungai", expanded=True):
        st.markdown("Permainan strategi menyeberangkan 4 entitas dengan aturan tertentu.")
        st.markdown("""
        - **Entitas:** Pahlawan, Tawanan, Perbekalan, Anak Buah
        - **Aturan 1:** Tawanan + Perbekalan tanpa pahlawan = GAGAL
        - **Aturan 2:** Tawanan + Anak Buah tanpa pahlawan = TIDAK GAGAL, tapi tidak dapat poin
        - **Poin:** 10 poin jika berhasil tanpa melanggar aturan
        """)
    
    with st.expander("🇮🇩 Tiang Bendera", expanded=True):
        st.markdown("Permainan menara Hanoi versi Indonesia dengan bendera.")
        st.markdown("""
        - **Susunan Awal:** 🚩 Merah Putih → 🟢 Hijau → 🟡 Kuning → 🔵 Biru
        - **Target:** Pindahkan semua ke Tiang C
        - **Aturan:** Cakram besar tidak boleh di atas cakram kecil
        """)
    
    st.info("💡 **Tips:** Permainan hadiah melatih berbagai keterampilan: pengetahuan sejarah, logika, strategi, dan pemecahan masalah.")

def show_tutorial_gamifikasi():
    """Tutorial fitur Gamifikasi."""
    st.markdown("## 🎮 Fitur Gamifikasi")
    
    with st.expander("🎯 Misi & Tantangan", expanded=True):
        st.markdown("Selesaikan misi untuk mendapatkan poin reward dan naik level!")
        
        st.markdown("#### 📅 Tantangan Harian")
        st.markdown("Setiap hari Anda mendapatkan tantangan berbeda:")
        st.markdown("""
        - **Senin:** 📝 Senin Cerdas – 10 soal
        - **Selasa:** 🧠 Selasa Analisis – 10 soal IQ
        - **Rabu:** ❤️ Rabu Empati – 10 soal EQ
        - **Kamis:** 🙏 Kamis Spiritual – 10 soal SQ
        - **Jumat:** 💪 Jumat Tangguh – 10 soal AQ
        - **Sabtu:** 🇮🇩 Sabtu Patriot – 10 soal Nasionalisme
        - **Minggu:** 🏆 Minggu Juara – 15 soal
        """)
        st.success("✅ Selesaikan tantangan harian untuk mendapatkan **5-8 poin reward**!")
        
        st.markdown("#### 📋 Daftar Misi (12 Misi)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🌱 Level Pemula:**")
            st.markdown("""
            - 🌱 Perintis Jalan – 10 soal → 5 poin
            - 📖 Penjelajah Ilmu – 50 soal → 10 poin
            """)
        with col2:
            st.markdown("**📚 Level Menengah:**")
            st.markdown("""
            - 📚 Cendekia Muda – 100 soal → 15 poin
            - 🎯 Akurasi 80% – 80% akurasi → 10 poin
            - 🧠 Master IQ – IQ ≥ 80 → 15 poin
            - ❤️ Master EQ – EQ ≥ 80 → 15 poin
            - 🙏 Master SQ – SQ ≥ 80 → 15 poin
            - 💪 Master AQ – AQ ≥ 80 → 15 poin
            """)
        with col3:
            st.markdown("**🌟 Level Lanjutan:**")
            st.markdown("""
            - 🌟 Pahlawan Cerdas – 200 soal → 25 poin
            - 🏆 Akurasi 90% – 90% akurasi → 20 poin
            - 🇮🇩 Patriot Sejati – Nasionalisme ≥ 80 → 20 poin
            - 💎 NKHM 100 – NKHM Total 100 → 30 poin
            """)
    
    with st.expander("🏆 Leaderboard", expanded=True):
        st.markdown("Kompetisi sehat untuk meraih posisi teratas!")
        
        st.markdown("#### 📊 Sistem Level")
        st.markdown("""
        - **🌿 Novice** – Skor 0-19 (Merah)
        - **📖 Beginner** – Skor 20-39 (Abu-abu)
        - **🌱 Learner** – Skor 40-59 (Oranye)
        - **📚 Expert** – Skor 60-74 (Hijau)
        - **🏆 Master** – Skor 75-89 (Biru)
        - **🌟 Grand Master** – Skor 90-100 (Emas)
        """)
        
        st.markdown("#### 🎖️ Medali")
        st.markdown("""
        - 🥇 Emas – Peringkat 1
        - 🥈 Perak – Peringkat 2
        - 🥉 Perunggu – Peringkat 3
        """)
    
    st.info("💡 **Tips Gamifikasi:** Kerjakan tantangan harian setiap hari untuk mengumpulkan poin. Fokus selesaikan misi level pemula terlebih dahulu. Kejar posisi teratas di leaderboard. Semakin tinggi level, semakin besar reward yang didapat.")
    
    st.success("🎉 **Target Akhir:** Capai **🌟 Grand Master** dan raih posisi **🥇 Juara 1** di leaderboard!")

def show_tutorial_tips():
    """Tips dan trik menggunakan aplikasi."""
    st.markdown("## 💡 Tips & Trik")
    
    with st.expander("🎯 Tips Umum", expanded=True):
        st.markdown("""
        - **Konsistensi:** Kerjakan soal setiap hari untuk meningkatkan skor
        - **Variasi:** Gunakan filter berbeda untuk variasi soal
        - **Catatan:** Gunakan fitur catatan untuk mencatat hal penting
        - **Kompetisi:** Tantang teman di mode Tanding
        """)
    
    with st.expander("🚀 Tips Meningkatkan Skor", expanded=True):
        st.markdown("""
        - **IQ:** Banyak membaca dan latihan logika
        - **EQ:** Latih empati dan kesadaran diri
        - **SQ:** Refleksi dan meditasi nilai-nilai kehidupan
        - **AQ:** Hadapi tantangan dengan sikap positif
        - **Nasionalisme:** Pelajari sejarah dan budaya Indonesia
        """)
    
    with st.expander("🎮 Tips Gamifikasi", expanded=True):
        st.markdown("""
        - **Tantangan Harian:** Jangan lewatkan reward harian
        - **Misi:** Selesaikan misi level pemula terlebih dahulu
        - **Leaderboard:** Pantau posisi Anda dan kejar ranking
        - **Level:** Semakin tinggi level, semakin besar prestise
        """)
    
    st.warning("⚠️ **Ingat!** Aplikasi ini adalah alat bantu belajar. Kunci utama adalah **konsistensi** dan **niat belajar** yang tulus.")
    
    st.success("🌟 **Selamat belajar!** Semoga Anda menjadi **Pahlawan Cerdas Nusantara**! 🇮🇩")

# ========== FUNGSI UTAMA ==========
def show_tutorial():
    """Menampilkan halaman Tutorial lengkap."""
    try:
        inject_tutorial_css()
        
        st.markdown("## 📘 Tutorial NKHM Nusantara")
        st.markdown("Panduan lengkap untuk menggunakan semua fitur di aplikasi NKHM.")
        st.markdown("---")
        
        # ===== TAB SELECTOR =====
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "🏠 Umum",
            "🎮 Kuis",
            "📊 Dasbor",
            "🏆 Prestasi",
            "⚔️ Tanding",
            "🎁 Karunia",
            "🎁 Hadiah",
            "🎮 Gamifikasi",
            "💡 Tips"
        ])
        
        with tab1:
            show_tutorial_umum()
        
        with tab2:
            show_tutorial_kuis()
        
        with tab3:
            show_tutorial_dasbor()
        
        with tab4:
            show_tutorial_prestasi()
        
        with tab5:
            show_tutorial_tanding()
        
        with tab6:
            show_tutorial_karunia()
        
        with tab7:
            show_tutorial_hadiah()
        
        with tab8:
            show_tutorial_gamifikasi()
        
        with tab9:
            show_tutorial_tips()
        
        # ===== FOOTER =====
        st.markdown("---")
        st.caption("🌿 NKHM Nusantara – Aplikasi Gaming 4 Kecerdasan + Nasionalisme")
        st.caption("Berbasis Perkembangan Data Personal | © 2026")
        
    except Exception as e:
        logging.error(f"Error di show_tutorial: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Tutorial: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_tutorial()