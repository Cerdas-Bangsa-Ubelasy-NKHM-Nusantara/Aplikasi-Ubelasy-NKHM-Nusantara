# nkhm/tutorial.py
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def show_tutorial():
    st.markdown("## 📘 Tutorial NKHM Nusantara")
    st.markdown("Selamat datang di NKHM Nusantara! Tutorial ini akan memandu Anda.")

    # Gunakan tabs untuk mengorganisir konten
    tab_intro, tab_kuis, tab_skor, tab_tips = st.tabs([
        "🌟 Pengantar", "🎮 Panduan Kuis", "📊 Memahami Skor", "💡 Tips & Trik"
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

def show_tutorial_simple():
    """Fungsi fallback jika konten interaktif tidak diperlukan."""
    st.markdown("## 📘 Tutorial NKHM Nusantara")
    st.info("Tutorial akan segera hadir dalam versi yang lebih interaktif!")
