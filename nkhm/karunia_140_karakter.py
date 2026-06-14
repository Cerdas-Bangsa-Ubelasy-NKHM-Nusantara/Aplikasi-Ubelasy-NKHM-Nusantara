# nkhm/karunia_140_karakter.py
import streamlit as st
import pandas as pd

# 70 pernyataan asli (sama seperti di karunia.py)
ORIGINAL_70 = [
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

# 140 pertanyaan = 70 asli + 70 asli (duplikasi)
QUESTIONS_140 = ORIGINAL_70 + ORIGINAL_70

KARUNIA_NAMES_140 = [
    "A. Karunia Bernubuat (Perceiver)",
    "B. Karunia Melayani (Doer)",
    "C. Karunia Mengajar (Teacher)",
    "D. Karunia Menasihati (Encourager)",
    "E. Karunia Memberi (Giver)",
    "F. Karunia Memimpin (Leader)",
    "G. Karunia Kemurahan hati (Compassion)"
]

def init_karunia_140_state():
    if "karunia_140_answers" not in st.session_state:
        st.session_state.karunia_140_answers = [0] * 140
    if "karunia_140_submitted" not in st.session_state:
        st.session_state.karunia_140_submitted = False
    if "karunia_140_totals" not in st.session_state:
        st.session_state.karunia_140_totals = [0] * 7

def reset_karunia_140():
    st.session_state.karunia_140_answers = [0] * 140
    st.session_state.karunia_140_submitted = False
    st.session_state.karunia_140_totals = [0] * 7

def show_karunia_140_karakter():
    init_karunia_140_state()
    
    st.markdown("## ✨ Karunia 140 Karakter")
    st.markdown("""
    **Petunjuk:**: Bacalah setiap pernyataan dengan seksama. Berikan nilai 0–5 sesuai dengan seberapa sering pernyataan tersebut menggambarkan diri Anda:

0 = Tidak pernah
1 = Jarang
2 = Kadang-kadang
3 = Biasanya
4 = Kebanyakan
5 = Selalu
Jawablah dengan jujur dan tidak perlu takut terhadap penilaian orang lain.**. Setelah selesai, klik **Hitung Skor**.
    """)
    
    st.markdown("### 📋 Kuesioner (140 pernyataan)")
    
    # Tampilkan pernyataan dengan selectbox (setiap selectbox punya key unik)
    for i, question in enumerate(QUESTIONS_140):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"**{i+1}. {question}**")
        with col2:
            current_val = st.session_state.karunia_140_answers[i]
            selected = st.selectbox(
                "Nilai",
                options=[0, 1, 2, 3, 4, 5],
                index=current_val,
                key=f"karunia_140_select_{i}",
                label_visibility="collapsed"
            )
            st.session_state.karunia_140_answers[i] = selected
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Hitung Skor Karunia 140", key="hitung_karunia_140_button", use_container_width=True):
            totals = [0] * 7
            for i, val in enumerate(st.session_state.karunia_140_answers):
                col_idx = i // 20
                if col_idx < 7:
                    totals[col_idx] += val
            st.session_state.karunia_140_totals = totals
            st.session_state.karunia_140_submitted = True
            st.rerun()
    with col2:
        if st.button("🔄 Reset", key="reset_karunia_140_button", use_container_width=True):
            reset_karunia_140()
            st.rerun()
    
    if st.session_state.get("karunia_140_submitted", False):
        totals = st.session_state.karunia_140_totals
        st.markdown("---")
        st.subheader("📊 Hasil Karunia 140 Karakter")
        df = pd.DataFrame({
            "Karunia": KARUNIA_NAMES_140,
            "Total Skor": totals
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        sorted_idx = sorted(range(7), key=lambda i: totals[i], reverse=True)
        top3 = [(KARUNIA_NAMES_140[i], totals[i]) for i in sorted_idx[:3]]
        
        st.markdown("### 🏆 Tiga Karunia Tertinggi Anda:")
        for rank, (name, score) in enumerate(top3, 1):
            st.success(f"{rank}. **{name}** – Skor: {score}")
        
        with st.expander("📖 Penjelasan Karunia"):
            st.markdown("""
            **A. Karunia Bernubuat (Perceiver)** – Kemampuan melihat kebenaran, membedakan yang baik dan jahat.
            **B. Karunia Melayani (Doer)** – Kemampuan menolong dan memenuhi kebutuhan praktis.
            **C. Karunia Mengajar (Teacher)** – Kemampuan menyampaikan kebenaran secara logis dan sistematis.
            **D. Karunia Menasihati (Encourager)** – Kemampuan mendorong dan memotivasi orang lain.
            **E. Karunia Memberi (Giver)** – Kemampuan memberi dengan sukacita dan mengelola sumber daya.
            **F. Karunia Memimpin (Leader)** – Kemampuan memimpin, mengatur, dan mengarahkan.
            **G. Karunia Kemurahan hati (Compassion)** – Kemampuan mengasihi dan berbelas kasihan.
            """)
        st.info("Hasil tes ini dapat membantu Anda memahami potensi diri.")

if __name__ == "__main__":
    show_karunia_140_karakter()
