# nkhm/karunia.py
import streamlit as st
import pandas as pd

# Daftar 70 pernyataan (sesuai urutan)
QUESTIONS = [
    "Dapat cepat dan tepat mengenali sesuatu itu baik atau jahat dan membenci kejahatan.",
    "Cepat mengetahui kebutuhan orang lain dan tanggap memenuhi kebutuhan tersebut.",
    "Menyampaikan kebenaran dengan cara yang logis dan sistematis.",
    "Senang mendorong orang lain untuk hidup berkemenangan.",
    "Rela memberi uang, barang-barang, waktu, dan kasih.",
    "Senang mengatur segala sesuatu yang menjadi tanggung-jawabnya.",
    "Memiliki kemampuan yang besar untuk menyatakan kasih.",
    "Menyatakan segala sesuatu itu benar atau salah dengan tegas.",
    "Menjaga agar segala sesuatu rapi dan teratur serta tidak tahan berada di tempat yang kurang tepat.",
    "Selalu suka menguji dengan fakta-fakta yang ada dan memiliki keyakinan yang kuat berdasarkan hal itu.",
    "Lebih suka menerapkan kebenaran daripada menyelidikinya.",
    "Suka memberi dengan diam-diam, tanpa diketahui oleh orang lain.",
    "Dapat mewujudkan ide/pemikiran dan menyampaikannya kepada orang lain dengan jelas.",
    "Selalu mencari hal-hal yang baik pada diri seseorang.",
    "Dapat dengan mudah mengetahui karakter seseorang.",
    "Menyelesaikan apa yang sudah dimulainya dengan tuntas.",
    "Senang belajar dan menyelidiki kitab suci (Alkitab).",
    "Lebih suka belajar segala sesuatu yang dapat digunakan secara praktis.",
    "Senang bila pemberiannya merupakan suatu jawaban doa bagi seseorang.",
    "Senang di bawah otoritas supaya memiliki otoritas.",
    "Menaruh perhatian pada orang yang terluka dan dalam keadaan susah.",
    "Mendorong orang lain untuk bertobat, sehingga dapat menghasilkan buah yang baik.",
    "Lebih tertarik dalam memenuhi kebutuhan orang lain daripada kebutuhan sendiri.",
    "Menginginkan kebenaran ditegakkan dalam setiap situasi, dan kecewa jika Firman Tuhan yang digunakan di luar konteksnya.",
    "Senang membimbing orang lain tentang langkah-langkah yang praktis dilakukan supaya bertumbuh dan mengembangkan pelayanan mereka.",
    "Ingin memberi yang terbaik yang dapat ia berikan.",
    "Tidak akan berusaha mengambil suatu tanggung-jawab kepemimpinan, kecuali didelegasikan oleh orang-orang yang berotoritas.",
    "Mengambil tindakan untuk menyembuhkan luka dan melepaskan beban yang ada pada orang lain.",
    "Berani hidup berdasarkan prinsip-prinsip rohani (tanpa berkompromi).",
    "Menyatakan kasih pada orang lain lebih banyak dalam perbuatan dan tindakan daripada dalam perkataan.",
    "Mudah mengembangkan dan memakai perbendaharaan kata yang luas.",
    "Sering menemukan kebenaran dalam pengalaman, kemudian dihubungkan dengan kitab suci (Alkitab).",
    "Memberi untuk mendukung dan memberkati orang lain atau membantu suatu pelayanan.",
    "Seorang pribadi yang memiliki Visi dengan sudut pandangan yang luas.",
    "Terdorong untuk menolong orang lain supaya memiliki hubungan yang baik dengan sesama.",
    "Senang mendorong pertumbuhan rohani orang lain.",
    "Cenderung untuk melakukan lebih dari apa yang diminta.",
    "Menyelidiki dari mana sumber-sumber pengetahuan yang diajarkan oleh orang lain.",
    "Senang menolong orang lain dengan konseling.",
    "Memiliki kemampuan untuk mengatur uang dengan bijaksana dan baik.",
    "Senang mendelegasikan tugas dan mengawasi orang lain dan tahu menempatkan orang yang tepat untuk menyelesaikan suatu pekerjaan.",
    "Senang melakukan segala sesuatu yang menyenangkan orang lain.",
    "Dipanggil untuk berdoa syafaat bagi orang lain.",
    "Menemukan suka cita terbesar dalam menolong orang.",
    "Merasakan bahwa penyelidikan kitab suci (Alkitab) adalah dasar dari pengoperasian semua karunia.",
    "Menginginkan kebenaran ditegakkan dalam setiap situasi.",
    "Cepat membantu dimana kebutuhan terlihat.",
    "Seorang pemimpin yang alami dan sangat cakap.",
    "Menghindari konflik dan perselisihan dengan orang lain.",
    "Memiliki pendapat dan keyakinan yang kuat dan standar pribadi yang ketat.",
    "Sulit berkata 'tidak' terhadap permintaan tolong.",
    "Memecahkan masalah dengan mempergunakan prinsip yang ditentukan kitab suci (Alkitab).",
    "Percaya pencobaan dan masalah dapat menolong orang untuk bertumbuh.",
    "Berdoa tentang jumlah yang akan diberikan, dan memberi hanya dengan pimpinan Roh Kudus Allah.",
    "Tahu kapan waktunya untuk tetap melakukan metode yang lama, dan kapan untuk memperkenalkan yang baru.",
    "Orang bertipe riang dan penuh suka cita.",
    "Ingin sekali melihat kelemahannya sendiri, dan menolong orang lain untuk melihat kelemahan mereka juga.",
    "Lebih suka melakukan sendiri suatu pekerjaan daripada menyuruh orang lain untuk melakukannya.",
    "IQ atau tingkat kecerdasan intelektualnya tinggi.",
    "Menerima orang lain sebagaimana adanya tanpa menghakimi mereka.",
    "Percaya bahwa Allah akan memenuhi segala kebutuhannya.",
    "Senang bekerja-sama dan berada diantara orang-orang.",
    "Lebih dikendalikan oleh perasaan daripada pikiran.",
    "Berkeinginan kuat untuk taat kepada Allah dan berani membayar harganya.",
    "Berpandangan bahwa melayani adalah hal yang terpenting dalam kehidupan.",
    "Dapat mendisiplinkan diri dan mengendalikan diri secara emosional.",
    "Ingin cepat menjernihkan masalah dengan orang lain.",
    "Bekerja keras untuk mengumpulkan uang supaya lebih banyak yang dapat ia berikan.",
    "Dapat menahan kritikan sampai tugas tersebut terlaksana.",
    "Bersuka-cita melihat orang lain diberkati, dan berduka-cita melihat orang lain terluka."
]

# Nama karunia per kolom (A-G)
KARUNIA_NAMES = [
    "A. Karunia Bernubuat (Perceiver)",
    "B. Karunia Melayani (Doer)",
    "C. Karunia Mengajar (Teacher)",
    "D. Karunia Menasihati (Encourager)",
    "E. Karunia Memberi (Giver)",
    "F. Karunia Memimpin (Leader)",
    "G. Karunia Kemurahan hati (Compassion)"
]

def init_karunia_state():
    """Inisialisasi session state untuk jawaban karunia"""
    if "karunia_answers" not in st.session_state:
        st.session_state.karunia_answers = [0] * 70
    if "karunia_submitted" not in st.session_state:
        st.session_state.karunia_submitted = False

def reset_karunia():
    st.session_state.karunia_answers = [0] * 70
    st.session_state.karunia_submitted = False

def show_karunia():
    
    init_karunia_state()
    
    st.markdown("## 🎁 Tes Karunia Motivasi")
    st.markdown("""
    **Petunjuk:** Bacalah setiap pernyataan dengan seksama. Berikan nilai 0–5 sesuai dengan seberapa sering pernyataan tersebut menggambarkan diri Anda:
    
    - **0** = Tidak pernah
    - **1** = Jarang
    - **2** = Kadang-kadang
    - **3** = Biasanya
    - **4** = Kebanyakan
    - **5** = Selalu
    
    Jawablah dengan **jujur** dan tidak perlu takut terhadap penilaian orang lain.
    """)
    
    st.markdown("### 📋 Kuesioner (70 pernyataan)")
    
    # Tampilkan pernyataan dalam bentuk list vertikal dengan teks lengkap
    # Setiap baris menampilkan 1 pernyataan
    for i, question in enumerate(QUESTIONS):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"**{i+1}. {question}**")
        with col2:
            current_val = st.session_state.karunia_answers[i]
            selected = st.selectbox(
                "Nilai",
                options=[0, 1, 2, 3, 4, 5],
                index=current_val,
                key=f"karunia_{i}",
                label_visibility="collapsed"
            )
            st.session_state.karunia_answers[i] = selected
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Hitung Skor Karunia", use_container_width=True):
            # Hitung total per kolom (setiap 7 soal membentuk 1 kolom karunia)
            totals = [0] * 7
            for i, val in enumerate(st.session_state.karunia_answers):
                col_idx = i % 7
                totals[col_idx] += val
            st.session_state.karunia_totals = totals
            st.session_state.karunia_submitted = True
            st.rerun()
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_karunia()
            st.rerun()
    
    if st.session_state.get("karunia_submitted", False):
        totals = st.session_state.karunia_totals
        st.markdown("---")
        st.subheader("📊 Hasil Tes Karunia Motivasi")
        
        # Tampilkan tabel per kolom
        df = pd.DataFrame({
            "Karunia": KARUNIA_NAMES,
            "Total Skor": totals
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Urutkan untuk cari 3 tertinggi
        sorted_idx = sorted(range(7), key=lambda i: totals[i], reverse=True)
        top3 = [(KARUNIA_NAMES[i], totals[i]) for i in sorted_idx[:3]]
        
        st.markdown("### 🏆 Tiga Karunia Motivasi Tertinggi Anda:")
        for rank, (name, score) in enumerate(top3, 1):
            st.success(f"{rank}. **{name}** – Skor: {score}")
        
        # Penjelasan singkat (opsional)
        with st.expander("📖 Penjelasan Karunia"):
            st.markdown("""
            **A. Karunia Bernubuat (Perceiver)** – Kemampuan melihat kebenaran, membedakan yang baik dan jahat, serta menyatakan kebenaran dengan tegas.
            
            **B. Karunia Melayani (Doer)** – Kemampuan menolong, memenuhi kebutuhan praktis orang lain, dan bekerja dengan rajin.
            
            **C. Karunia Mengajar (Teacher)** – Kemampuan menyampaikan kebenaran secara logis, sistematis, dan mengajar orang lain.
            
            **D. Karunia Menasihati (Encourager)** – Kemampuan mendorong, memotivasi, dan menasihati orang lain untuk bertumbuh.
            
            **E. Karunia Memberi (Giver)** – Kemampuan memberi dengan sukacita, mengelola sumber daya untuk memberkati.
            
            **F. Karunia Memimpin (Leader)** – Kemampuan memimpin, mengatur, dan mengarahkan orang lain.
            
            **G. Karunia Kemurahan hati (Compassion)** – Kemampuan mengasihi, berbelas kasihan, dan menolong yang menderita.
            """)
        
        st.info("Hasil tes ini dapat membantu Anda memahami talenta/potensi diri dan area pengembangan.")
