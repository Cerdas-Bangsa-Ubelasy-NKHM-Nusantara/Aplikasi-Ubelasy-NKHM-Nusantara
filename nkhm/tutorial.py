# nkhm/tutorial.py
import streamlit as st
from pathlib import Path

def show_tutorial():
    """Menampilkan halaman tutorial NKHM Nusantara"""
    st.markdown("## 📘 Tutorial NKHM Nusantara")
    st.markdown("""
    Selamat datang di NKHM Nusantara! Aplikasi ini dirancang untuk mengasah 
    4 kecerdasan (IQ, EQ, SQ, AQ) dan Nasionalisme melalui permainan interaktif.
    
    ### 🎮 Cara Bermain Kuis
    1. Pilih kategori kuis (IQ, EQ, SQ, AQ, atau Nasionalisme)
    2. Jawab pertanyaan dengan memilih pilihan yang tersedia
    3. Dapatkan poin untuk setiap jawaban benar
    4. Pantau perkembangan skor Anda di Dashboard
    
    ### 🏆 Fitur Lainnya
    - **Dashboard**: Lihat ringkasan skor dan riwayat kuis
    - **Prestasi**: Raih gelar berdasarkan pencapaian skor
    - **Tanding**: Ajak teman berkompetisi
    - **Karunia**: Materi motivasi dan pengembangan diri
    - **Hadiah**: Mini games seru
    - **Gamifikasi**: Kumpulkan koin dan bersaing di leaderboard
    
    ### 💡 Tips
    - Semakin banyak kuis yang dikerjakan, semakin tinggi skor Anda
    - Skor NKHM yang tinggi meningkatkan peluang pinjaman di Ubelasy
    - Jangan lupa klaim hadiah dari misi yang telah selesai!
    """)
    
    # ========== TAMPILKAN GAMBAR ILUSTRASI (AMAN) ==========
    st.markdown("---")
    st.markdown("### 🖼️ Ilustrasi Stomata Hati")
    
    img_path = Path(__file__).parent.parent / "assets" / "stomata_ilustrasi.jpg"
    
    if img_path.exists():
        # Gunakan columns untuk mengatur lebar gambar dan menghindari parameter use_container_width
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(img_path), caption="Contoh Ilustrasi Stomata Hati")
    else:
        st.info("💡 Gambar ilustrasi belum tersedia. Silakan tambahkan 'stomata_ilustrasi.jpg' ke folder assets/.")
    
    st.markdown("---")
    st.markdown("""
    ### 📚 Sumber Belajar
    - [Pola Hidup dan Pola Pikir yang Arif Bijaksana](https://...)
    - [Literasi Keuangan untuk Pemula](https://...)
    
    Selamat belajar dan berkembang! 🌿
    """)