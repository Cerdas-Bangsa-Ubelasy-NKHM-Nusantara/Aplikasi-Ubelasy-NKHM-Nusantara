# nkhm/tutorial.py
import streamlit as st

def show_tutorial():
    st.markdown("## 📘 Tutorial NKHM Nusantara")
    
    with st.expander("📖 Panduan Penggunaan"):
        st.markdown("""
        ### 1. Login
        Masukkan nama Anda pada halaman awal, lalu klik **🚀 MULAI BELAJAR**.
        
        ### 2. Memilih Kuis
        - **Kategori**: Pilih ✨ Semua, 🇮🇩 Nasionalisme, atau 📚 Umum.  
        - **Fokus**: Pilih Semua, IQ, EQ, SQ, AQ, atau Nasionalisme.  
        
        ### 3. Menjawab Soal
        - **Pilihan ganda** (IQ, SQ, Nasionalisme, sebagian EQ/AQ):  
          Pilih satu jawaban, klik **✅ JAWAB**. Jawaban benar akan menambah skor kecerdasan terkait.  
        - **Skor tanggapan** (EQ_scale, AQ_scale):  
          Pilih angka 0–3 sesuai tingkat persetujuan (3=Setuju sekali, 0=Tidak setuju sekali).  
          Setelah menyelesaikan semua soal dalam satu **bagian** (misal "Ketrampilan Emosi"), klik **✅ Selesai Bagian Ini** untuk menambahkan skor.
        
        ### 4. Melihat Hasil
        - Tab **📊 DASHBOARD**: Grafik skor per kecerdasan dan riwayat kuis.  
        - Tab **🏆 PRESTASI**: Badge pencapaian (skor ≥50 per kecerdasan) dan leaderboard nasional.  
        
        ### 5. Reset Skor
        Klik **🔄 Reset Skor** di sidebar untuk memulai dari awal (skor diatur ulang ke 0).  
        
        ### 6. Keluar / Ganti Pengguna
        Klik **🚪 Keluar / Ganti Pengguna** di sidebar untuk kembali ke halaman login.
        """)
    
    with st.expander("📄 Dokumentasi Penilaian NKHM"):
        st.markdown("""
        ### Rumus NKHM
        - **NKHM_Q** = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))  
        - **NKHM_Total** = (NKHM_Q + Nasionalisme) / 2  
        Semua skor dalam rentang **0–100**.
        
        ### Standar Soal & Penilaian
        | Kategori | Jenis Soal | Standar Soal | Skor Mentah Maks | Konversi ke 100% |
        |----------|------------|--------------|------------------|------------------|
        | IQ | Pilihan ganda | 32 soal | 320 | (raw / 320) × 100 |
        | EQ | Pilihan ganda | 38 soal | 380 | (raw / 380) × 100 |
        | EQ | Skor tanggapan | (tidak tetap) | 380 | (akumulasi per bagian) dibatasi 380 |
        | **EQ Total** | - | - | - | **(PG + SkorTanggapan) / 2** |
        | SQ | Pilihan ganda (strategis) | 14 soal (2×) | 140 | (raw / 140) × 100 |
        | AQ | Pilihan ganda (strategis) | 14 soal (2×) | 140 | (raw / 140) × 100 |
        | AQ | Skor tanggapan | (tidak tetap) | 140 | (akumulasi per bagian) dibatasi 140 |
        | **AQ Total** | - | - | - | **(PG + SkorTanggapan) / 2** |
        | Nasionalisme | Pilihan ganda (strategis) | 20 soal (2×) | 200 | (raw / 200) × 100 |
        
        > **Strategis** berarti nilai 100% dicapai setelah menjawab **2× standar** soal (misal 28 soal SQ untuk mendapat 100).  
        
        ### Skor Tanggapan (EQ_scale / AQ_scale)
        Setiap soal bernilai 0–3 (pilihan 3,2,1,0 atau 0,1,2,3).  
        Untuk setiap **bagian** (contoh: Ketrampilan Emosi), jawaban dikelompokkan per kolom (posisi pilihan), lalu dijumlahkan per kolom.  
        **Nilai bagian** = jumlah semua kolom.  
        Nilai tersebut langsung ditambahkan ke total skor tanggapan (dibatasi maks 380 untuk EQ, 140 untuk AQ).  
        
        **Contoh perhitungan bagian dengan 4 soal:**  
        - Soal1 jawab 3 → kolom1 +1  
        - Soal2 jawab 2 → kolom3 +1  
        - Soal3 jawab 1 → kolom2 +1  
        - Soal4 jawab 0 → (tidak menambah)  
        Kolom1=1, kolom2=1, kolom3=1, kolom4=0 → nilai bagian = 3.
        
        ### Level NKHM
        | Nilai NKHM_Total | Level |
        |------------------|-------|
        | ≥ 80 | 🌟 Pahlawan Cerdas |
        | 60 – 79 | 📚 Cendekia Muda |
        | 40 – 59 | 🌱 Penjelajah Ilmu |
        | < 40 | 🌿 Perintis Jalan |
        
        ### Badge Pencapaian
        Setiap kecerdasan (IQ, EQ, SQ, AQ, Nasionalisme) memiliki badge yang didapat jika skor ≥ 50.  
        Gelar **PAHLAWAN CERDAS NUSANTARA** diberikan jika semua skor ≥ 50.
        """)
