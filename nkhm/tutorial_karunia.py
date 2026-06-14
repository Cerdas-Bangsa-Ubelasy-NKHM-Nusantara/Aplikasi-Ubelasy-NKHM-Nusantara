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
        Soal dibagi ke dalam 7 kolom karunia dengan pola berulang setiap 7 soal:
        
        | Kolom | Karunia | Nomor Soal |
        |-------|---------|-------------|
        | 1 | Bernubuat | 1, 8, 15, 22, 29, 36, 43, 50, 57, 64 |
        | 2 | Melayani | 2, 9, 16, 23, 30, 37, 44, 51, 58, 65 |
        | 3 | Mengajar | 3, 10, 17, 24, 31, 38, 45, 52, 59, 66 |
        | 4 | Menasihati | 4, 11, 18, 25, 32, 39, 46, 53, 60, 67 |
        | 5 | Memberi | 5, 12, 19, 26, 33, 40, 47, 54, 61, 68 |
        | 6 | Memimpin | 6, 13, 20, 27, 34, 41, 48, 55, 62, 69 |
        | 7 | Kemurahan Hati | 7, 14, 21, 28, 35, 42, 49, 56, 63, 70 |
        
        **Hasil:**  
        Anda akan mendapatkan skor untuk masing-masing karunia. Tiga karunia dengan skor tertinggi menunjukkan kecenderungan motivasi utama Anda.
        """)
        
    with tab2:
        st.markdown("""
        ### 📌 Kuesioner 140 Soal (Karunia 140 Karakter)
        Kuesioner ini merupakan versi lebih lengkap dengan **140 pernyataan**. Setiap pernyataan juga dinilai 0–5 dengan skala yang sama.
        
        **Penilaian:**  
        Sama seperti kuesioner 70 soal, pembagian karunia mengikuti pola 7 kolom berulang. Tapi dengab urutan yang berbeda berikut ini:
        
        - Soal nomor **1, 8, 15, ... , 134** → Karunia Bernubuat
        - Soal nomor **2, 9, 16, ... , 135** → Karunia Memimpin 
        - Soal nomor **3, 10, 17, ... , 136** → Karunia Melayani 
        - Soal nomor **4, 11, 18, ... , 137** → Karunia Menasihati
        - Soal nomor **5, 12, 19, ... , 138** → Karunia Memberi
        - Soal nomor **6, 13, 20, ... , 139** → Karunia Mengajar
        - Soal nomor **7, 14, 21, ... , 140** → Karunia Kemurahan Hati (Berbelas Kasihan)
        
        Setiap kolom berisi 20 soal (karena 140/7 = 20).
        
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
