# nkhm/tutorial.py
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from pathlib import Path

def show_tutorial():
    st.markdown("## 📘 Tutorial NKHM Nusantara")
    st.markdown("Selamat datang di NKHM Nusantara! Tutorial ini akan memandu Anda.")

    # Gunakan tabs untuk mengorganisir konten
    tab_intro, tab_kuis, tab_skor, tab_tips, tab_stomata = st.tabs([
        "🌟 Pengantar", "🎮 Panduan Kuis", "📊 Memahami Skor", "💡 Tips & Trik", "💖 Stomata Hati"
    ])

    with tab_intro:
        st.markdown("""
        **Apa itu NKHM Nusantara?**
        NKHM Nusantara adalah aplikasi gamifikasi yang dirancang untuk mengasah 4 kecerdasan Anda (IQ, EQ, SQ, AQ) sekaligus menumbuhkan rasa nasionalisme.
        """)
        try:
            response = requests.get("https://raw.githubusercontent.com/SRPakpahanSST/nusantara-nkhm/main/assets/human.jpg")
            img = Image.open(BytesIO(response.content))
            st.image(img, caption="Logo NKHM Nusantara", width=200)
        except:
            st.info("Logo NKHM Nusantara")

    with tab_kuis:
        st.markdown("### 🎮 Panduan Menjawab Kuis")
        with st.expander("📝 Soal Pilihan Ganda"):
            st.markdown("""
            1. Bacalah pertanyaan dengan saksama.
            2. Pilih satu jawaban yang menurut Anda paling benar.
            3. Klik tombol **✅ JAWAB**.
            """)
        with st.expander("📊 Soal Skor Tanggapan (EQ/AQ)"):
            st.markdown("""
            1. Soal ini mengukur tingkat persetujuan Anda.
            2. Berikan skor 0-3 sesuai perasaan Anda:
                - **3** = Setuju sekali
                - **2** = Setuju
                - **1** = Kurang setuju
                - **0** = Tidak setuju sekali
            3. Klik **✅ JAWAB**.
            4. **Selesaikan seluruh soal dalam satu bagian, lalu klik tombol ✅ Selesai Bagian Ini.**
            """)
        with st.expander("🏆 Mode Tanding"):
            st.markdown("""
            1. Pada tab **⚔️ TANDING**, masukkan nama kedua pemain.
            2. Tentukan jumlah soal dan batas waktu.
            3. Pemain akan bergiliran menjawab soal.
            4. Pemain dengan poin tertinggi di akhir pertandingan adalah pemenang!
            """)
        with st.expander("🎯 Filter Soal"):
            st.markdown("""
            - **Kategori**: Pilih '✨ Semua', '🇮🇩 Nasionalisme', atau '📚 Umum'.
            - **Fokus**: Pilih jenis kecerdasan yang ingin diasah (IQ, EQ, SQ, AQ, Nasionalisme).
            """)
        with st.expander("🤖 Asisten AI Ki Hajar"):
            st.markdown("""
            Ki Hajar siap membantu menjawab pertanyaan Anda! Cukup tanyakan di *chat input* yang tersedia di *sidebar*.
            """)

    with tab_skor:
        st.markdown("### 📊 Memahami Skor dan NKHM")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("NKHM_Q", "0-100", help="Nilai Kemampuan Hidup Manusia (4 Kecerdasan)")
            st.caption("Rumus: **((IQ+EQ) × (SQ+AQ)) / ((IQ+EQ)+(SQ+AQ))**")
        with col2:
            st.metric("NKHM_Total", "0-100", help="Nilai Akhir setelah digabung dengan Nasionalisme")
            st.caption("Rumus: **(NKHM_Q + Nasionalisme) / 2**")
        st.markdown("---")
        st.markdown("#### Level NKHM Total:")
        st.progress(0, text="🌿 Perintis Jalan (0 - 39)")
        st.progress(0.4, text="🌱 Penjelajah Ilmu (40 - 59)")
        st.progress(0.6, text="📚 Cendekia Muda (60 - 79)")
        st.progress(0.8, text="🌟 Pahlawan Cerdas (80 - 100)")

    with tab_tips:
        st.markdown("### 💡 Tips & Trik")
        st.info("""
        **✨ Tips Menjawab Soal:**
        - Bacalah setiap pertanyaan dengan saksama sebelum menjawab.
        - Jangan terburu-buru, manfaatkan waktu yang tersedia.
        - Untuk soal skor tanggapan, jawablah dengan **jujur** sesuai perasaan Anda.
        - Ikuti terus *progress* Anda di tab **📊 DASHBOARD**.

        **✨ Meningkatkan Skor NKHM:**
        - Kerjakan lebih banyak soal.
        - Perhatikan area kecerdasan mana yang masih rendah, lalu fokuslah pada kategori itu.
        - Capai semua *badge* untuk mendapatkan gelar **PAHLAWAN CERDAS NUSANTARA**.

        **✨ Fitur Lainnya:**
        - Gunakan filter untuk fokus pada soal tertentu.
        - Ajak teman bertanding di tab **⚔️ TANDING** untuk menguji kemampuan Anda!
        """)

    # ========== TAB STOMATA HATI ==========
    with tab_stomata:
        st.markdown("### 💖 Stomata Hati – Alat Uji Iman, Kasih, Pengharapan")
        st.markdown("""
        **Apa Itu Stomata Hati?**  
        Stomata Hati adalah alat uji berbentuk seperti celah‑celah stomata daun yang berfungsi mengukur tingkat kesatuan **Iman**, **Kasih**, dan **Pengharapan** (IKP) seseorang berdasarkan 1 Korintus 13:13.

        > *"Demikianlah tinggal ketiga hal ini, yaitu iman, pengharapan dan kasih, dan yang paling besar di antaranya ialah kasih."*

        Terdapat **12 sisi (celah)** stomata hati, masing‑masing mewakili kombinasi sikap dan tindakan.
        """)

        with st.expander("📌 12 Sisi Stomata Hati"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                | No | Nama Sisi |
                |----|-----------|
                | 1  | Kasih |
                | 2  | Iman |
                | 3  | Pengharapan |
                | 4  | Iman‑Pengharapan |
                | 5  | Kasih‑Iman |
                | 6  | Pengharapan‑Kasih |
                """)
            with col2:
                st.markdown("""
                | No | Nama Sisi |
                |----|-----------|
                | 7  | Berbuat iman |
                | 8  | Berbuat pengharapan |
                | 9  | Berbuat kasih |
                | 10 | Kasih‑Iman‑Pengharapan (keseimbangan) |
                | 11 | Berbuat kasih‑beriman |
                | 12 | Berbuat kasih‑berpengharapan |
                """)

        with st.expander("📐 Cara Menentukan Tingkat Persentase IKP"):
            st.markdown("""
            1. **Jawab 30 soal** (masing‑masing 10 soal tentang Kasih, Iman, Pengharapan).  
               Setiap jawaban benar = 1 poin, salah = 0. Maksimal nilai per kriteria = 10.

            2. **Hitung persentase setiap kriteria**  
               `Persen Kasih = (skor Kasih / 10) × 100%` (begitu pula untuk Iman dan Pengharapan).

            3. **Hitung total persentase**  
               `Total = Persen Kasih + Persen Iman + Persen Pengharapan`.

            4. **Hitung IKP relatif (normalisasi ke 100)**  
               `IKP Kasih = (Persen Kasih / Total) × 100` (lakukan juga untuk Iman dan Pengharapan).

            5. **Terapkan pada segitiga IKP** – tarik tiga garis lurus:
               - **Garis Iman**: dari titik nilai Iman → sejajar sisi Kasih → menuju sisi Pengharapan.
               - **Garis Kasih**: dari titik nilai Kasih → sejajar sisi Pengharapan → menuju sisi Iman.
               - **Garis Pengharapan**: dari titik nilai Pengharapan → sejajar sisi Iman → menuju sisi Kasih.

            6. **Titik potong** ketiga garis pada sisi‑sisi segitiga menentukan **satu, dua, atau tiga posisi** dari 12 sisi Stomata Hati.
            """)

        with st.expander("📊 Contoh Perhitungan"):
            st.markdown("""
            Misalkan hasil tes:
            - Kasih = 12%  
            - Iman = 61%  
            - Pengharapan = 27%  

            Total = 100% (sudah dalam skala relatif).  
            Maka:
            - Iman = 61 → tarik garis sejajar Kasih → potong di sisi **Berbuat kasih (sisi 9)**.  
            - Kasih = 12 → garis sejajar Pengharapan → potong di sisi yang sama (sisi 9).  
            - Pengharapan = 27 → garis sejajar Iman → juga menuju sisi 9.  

            **Hasil:** Posisi Stomata Hati berada di **sisi 9 – Berbuat kasih**.
            """)
        
        # Perbaikan path gambar
        img_path = Path(__file__).parent.parent / "assets" / "stomata_hati_contoh.jpg"
        if img_path.exists():
            st.image(str(img_path), caption="Contoh Ilustrasi Stomata Hati", use_container_width=True)
        else:
            st.warning("Gambar contoh Stomata Hati belum tersedia.")
                      
        with st.expander("💡 Bagaimana Aplikasi Membantu Anda?"):
            st.markdown("""
            - Aplikasi secara otomatis menghitung persentase IKP setelah Anda menjawab 30 soal.
            - Menentukan posisi Anda pada 12 sisi Stomata Hati.
            - Menampilkan hasil beserta gambar segitiga IKP.

            > Gunakan hasil ini untuk merenungkan keseimbangan iman, kasih, dan pengharapan dalam hidup Anda, serta panggilan untuk **berbuat** sesuai dengan sisi yang Anda peroleh.
            """)

def show_tutorial_simple():
    """Fungsi fallback jika konten interaktif tidak diperlukan."""
    st.markdown("## 📘 Tutorial NKHM Nusantara")
    st.info("Tutorial akan segera hadir dalam versi yang lebih interaktif!")
