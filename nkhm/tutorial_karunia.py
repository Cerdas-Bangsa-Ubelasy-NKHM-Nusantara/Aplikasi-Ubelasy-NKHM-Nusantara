# nkhm/tutorial_karunia.py
import streamlit as st

def show_tutorial_karunia():
    st.markdown("## 🎁 Tutorial Karunia Motivasi")
    st.markdown("""
    **Karunia Motivasi** adalah kecenderungan alamiah yang diberikan Tuhan kepada setiap orang untuk mendorong, memotivasi, dan memberdayakan diri sendiri serta orang lain. Karunia ini disebut juga **"Charisma"** dalam Roma 12:6-8.
    
    Karunia Motivasi bersifat:
    - **Vertikal** → untuk memuliakan Tuhan
    - **Horizontal** → untuk melayani sesama
    - **Internal** → untuk kebahagiaan dan produktivitas pribadi
    """)
    
    # Tabs untuk dua versi tes
    tab1, tab2 = st.tabs(["📋 Kuesioner 70 Soal", "📋 Kuesioner 140 Soal"])
    
    with tab1:
        st.markdown("""
        ### 📌 Kuesioner 70 Soal (Karunia Umum)
        Kuesioner ini terdiri dari **70 pernyataan**. Setiap pernyataan dinilai dengan skala 0–5:
        
        - **0** = Tidak pernah
        - **1** = Jarang
        - **2** = Kadang-kadang
        - **3** = Biasa
        - **4** = Kebanyakan
        - **5** = Selalu
        
        **Cara mengisi:**
        1. Baca setiap pernyataan dengan seksama.
        2. Pilih nilai yang paling sesuai dengan diri Anda saat ini.
        3. Setelah semua terisi, klik **"Hitung Skor Karunia"**.
        
        **Penilaian:**  
        Secara berurutan, setiap **10 pernyataan** mewakili satu jenis karunia (karena 70/7 = 10). Urutan karunia:
        
        | Karunia | Nomor Soal | Nama Karunia |
        |---------|------------|---------------|
        | A | 1–10 | Bernubuat (Perceiver) |
        | B | 11–20 | Melayani (Doer) |
        | C | 21–30 | Mengajar (Teacher) |
        | D | 31–40 | Menasihati (Encourager) |
        | E | 41–50 | Memberi (Giver) |
        | F | 51–60 | Memimpin (Leader) |
        | G | 61–70 | Kemurahan Hati (Compassion) |
        
        **Hasil:**  
        Anda akan mendapatkan skor untuk masing-masing karunia. Tiga karunia dengan skor tertinggi menunjukkan kecenderungan motivasi utama Anda.
        """)
        
    with tab2:
        st.markdown("""
        ### 📌 Kuesioner 140 Soal (Karunia 140 Karakter)
        Kuesioner ini merupakan versi lebih lengkap dengan **140 pernyataan**. Setiap pernyataan juga dinilai 0–5 dengan skala yang sama.
        
        **Penilaian:**  
        Setiap **20 pernyataan** mewakili satu jenis karunia (karena 140/7 = 20). Urutan karunia tetap sama seperti di atas.
        
        - Soal 1–20 → Karunia Bernubuat
        - Soal 21–40 → Karunia Melayani
        - Soal 41–60 → Karunia Mengajar
        - Soal 61–80 → Karunia Menasihati
        - Soal 81–100 → Karunia Memberi
        - Soal 101–120 → Karunia Memimpin
        - Soal 121–140 → Karunia Kemurahan Hati
        
        **Interpretasi Skor Maksimal:**  
        Skor maksimal per karunia = 20 × 5 = 100. Semakin tinggi skor, semakin kuat karunia tersebut dalam diri Anda.
        """)
    
    # Bagian penjelasan ketujuh karunia
    st.markdown("---")
    st.markdown("## 🔍 Ketujuh Karunia Motivasi")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **1. Karunia Bernubuat (Perceiver)**  
        *Melihat kebenaran, membedakan yang baik dan jahat.*  
        Ciri: tegas, berani, jujur, membenci kejahatan, menginginkan kebenaran ditegakkan.
        
        **2. Karunia Melayani (Doer)**  
        *Memenuhi kebutuhan praktis dengan tanggap.*  
        Ciri: membantu, bekerja dengan tangan, suka melakukan, praktis.
        
        **3. Karunia Mengajar (Teacher)**  
        *Menyampaikan kebenaran secara logis dan sistematis.*  
        Ciri: suka menyelidiki Alkitab, menjelaskan dengan jelas, menggunakan ilustrasi.
        """)
    with col2:
        st.markdown("""
        **4. Karunia Menasihati (Encourager)**  
        *Mendorong, memotivasi, dan membantu orang bertumbuh.*  
        Ciri: suka mendorong, konseling, sabar, positif.
        
        **5. Karunia Memberi (Giver)**  
        *Memberi dengan sukacita, mengelola sumber daya.*  
        Ciri: dermawan, bijak dalam keuangan, memberi dengan diam-diam.
        
        **6. Karunia Memimpin (Leader)**  
        *Memimpin, mengatur, mengarahkan.*  
        Ciri: visioner, delegator, bertanggung jawab, tegas.
        
        **7. Karunia Kemurahan Hati (Compassion)**  
        *Mengasihi, berbelas kasihan, menolong yang menderita.*  
        Ciri: peduli, sabar, suka menolong, empati.
        """)
    
    # Tips dan masalah yang dihadapi
    with st.expander("💡 Tips Mengenali Karunia Anda"):
        st.markdown("""
        - Jujurlah dalam menjawab – tidak perlu berusaha menjadi “rohani” atau sesuai ekspektasi orang lain.
        - Amati **tiga karunia tertinggi** Anda – itulah motivator utama Anda.
        - Karunia yang rendah tidak berarti buruk; itu bisa menjadi area yang perlu dikembangkan.
        - Gunakan hasil ini untuk melayani di bidang yang sesuai.
        """)
    
    with st.expander("⚠️ Masalah yang Sering Dihadapi (Kekurangan Karunia)"):
        st.markdown("""
        Setiap karunia juga memiliki sisi negatif jika tidak diimbangi dengan kasih dan kebijaksanaan:
        
        - **Bernubuat:** Cenderung menghakimi, ceplas-ceplos.
        - **Melayani:** Lupa menolong keluarga karena terlalu sibuk melayani orang lain.
        - **Mengajar:** Cenderung merasa lebih cerdas, menggunakan firman di luar konteks.
        - **Menasihati:** Memotong pembicaraan, memberi nasihat yang sama berulang kali.
        - **Memberi:** Berusaha mengontrol uang yang diberikan, mengabaikan tanggung jawab lain.
        - **Memimpin:** Terganggu jika orang tidak bekerja baik, kadang memakai orang untuk sasaran sendiri.
        - **Kemurahan hati:** Mudah terluka, terlalu memiliki empati hingga mengabaikan diri sendiri.
        
        Kenali kelemahan Anda agar dapat bertumbuh.
        """)
    
    st.info("📌 Setelah mengisi kuesioner, Anda akan mendapatkan tiga karunia tertinggi. Gunakan informasi ini untuk melayani dengan lebih efektif dan melengkapi satu sama lain dalam komunitas.")

if __name__ == "__main__":
    show_tutorial_karunia()
