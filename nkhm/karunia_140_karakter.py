# nkhm/karunia_140_karakter.py
import streamlit as st
import pandas as pd

# 140 pertanyaan berdasarkan PDF (urutan 1-140)
QUESTIONS_140 = [
    "Dengan cepat dan tepat sekali dapat mengetahui sesuatu yang baik atau jahat serta membenci kejahatan",
    "Cepat mengetahui kebutuhan orang lain dan tanggap memenuhi kebutuhan tersebut",
    "Menyampaikan kebenaran dengan cara yang logis dan sistematis",
    "Senang mendorong orang lain untuk hidup berkemenangan",
    "Dengan rela memberi uang, barang-barang, waktu dan perhatian",
    "Senang mengatur segala sesuatu yang menjadi tanggung jawabnya",
    "Memiliki kemampuan yang besar untuk menyatakan kasih",
    "Menyatakan segala sesuatu benar atau salah dengan tegas",
    "Senang melakukan pekerjaan dengan ketrampilan tangan",
    "Suka menguji sesuatu dengan fakta-fakta",
    "Menyukai respon yang kelihatan ketika mengajar atau berbicara",
    "Suka memberi dengan diam-diam",
    "Dapat mewujudkan ide dan mampu mendelegasikan kepada orang lain dengan jelas",
    "Selalu mencari hal yang baik pada diri seseorang",
    "Dapat dengan mudah mengetahui karakter seseorang",
    "Menjaga segala sesuatu tetap rapi dan teratur",
    "Senang mempelajari dan menyelidiki Alkitab",
    "Lebih suka menerapkan kebenaran daripada menyelidikinya",
    "Merasa sebagai bagian dari pelayanan yang ia sumbang",
    "Senang berada dibawah otoritas supaya memiliki otoritas",
    "Peka terhadap keadaan rohani dan emosi orang lain",
    "Senang mendorong orang lain untuk bertobat sehingga dapat menghasilkan buah yang baik",
    "Mudah mengingat hal-hal yang kecil",
    "Senang mempelajari arti kata (dari bahasa aslinya)",
    "Lebih suka belajar segala sesuatu yang dapat digunakan secara praktis",
    "Banyak berdoa bagi keselamatan orang lain",
    "Tidak mengambil suatu tanggung jawab kepemimpinan kecuali didelegasikan oleh pihak yang berwewenang.",
    "Tertarik pada orang yang terluka dan berada dalam keadaan susah",
    "Percaya bahwa karakter terbentuk melalui masalah dan kesulitan",
    "Senang mengundang orang ke rumahnya",
    "Lebih suka menggunakan ilustrasi Alkitab daripada ilustrasi sehari-hari",
    "Senang membimbing orang lain dengan langkah-langkah yang praktis",
    "Senang bila pemberiannya merupakan jawaban bagi doa seseorang",
    "Mengambil alih kepemimpinan jika tidak ada pemimpin",
    "Mengambil langkah pertolongan untuk menyembuhkan luka dan melepaskan beban orang lain",
    "Hanya mempunyai sedikit teman atau hampir tidak samasekali",
    "Menyelesaikan dengan tuntas apa yang sudah dimulainya",
    "Kecewa jika firman Tuhan yang digunakan diluar konteksnya",
    "Senang bekerja dengan orang (bukan alat)",
    "Ingin memberi yang terbaik yang dapat ia berikan",
    "Menyenangi pekerjaan yang mempunyai sasaran dan proyek jangka panjang",
    "Lebih memperhatikan luka batin dan emosi daripada luka fisik",
    "Memandang Alkitab sebagai dasar dari kebenaran, kepercayaan, tindakan dan otoritas.",
    "Sulit berkata 'tidak' terhadap permohonan orang lain",
    "Menginginkan kebenaran ditegakkan dalam setiap situasi",
    "Mendorong orang lain untuk mengembangkan pelayanan mereka",
    "Memberi dengan pimpinan Roh Kudus",
    "Seseorang pribadi yang memiliki visi dengan sudut pandang yang luas",
    "Terdorong menolong orang lain untuk memiliki hubungan yang baik dengan sesama",
    "Berani hidup berdasarkan prinsip-prinsip rohani (tanpa kompromi)",
    "Lebih tertarik untuk memenuhi kebutuhan orang lain daripada kebutuhan sendiri",
    "Mampu menganalisa secara obyektif (tanpa perasaan pribadi)",
    "Senang menemukan kebenaran dalam pengalaman dan mulai dihubungkan dengan Alkitab",
    "Memberi untuk mendukung dan memberkati orang lain / suatu pelayanan",
    "Mampu menempatkan orang yang tepat untuk menyelesaikan suatu pekerjaan",
    "Senang memberikan tempat / kesempatan yang lebih baik kepada orang lain",
    "Berkata jujur, terus terang dan tidak bersiasat",
    "Senang bekerja pada proyek yang selesai dalam waktu singkat (proyek jangka pendek)",
    "Mudah mengembangkan dan menggunakan perbendaharaan yang luas",
    "Senang menolong orang lain dengan konseling",
    "Senang mengundang orang ke rumahnya",
    "Senang mendelegasikan tugas dan mengawasi orang lain",
    "Berhati-hati dengan perkataan dan tindakan supaya tidak melukai orang lain",
    "Cara berbicara sangat meyakinkan",
    "Lebih sering menyatakan kasih lewat perbuatan dan tindakan daripada perkataan",
    "Mengutamakan fakta dan ketepatan dalam memakai kata-kata",
    "Berhenti konseling apabila orang tersebut tidak mau berubah",
    "Mampu mengatur keuangan dengan bijaksana",
    "Dapat menahan kritikan sampai tugas tersebut terlaksana",
    "Mudah mengetahui ketidaktulusan / motivasi lain dari seseorang",
    "Berdukacita karena dosa yang dilakukan orang lain",
    "Ingin perbuatannya dihargai",
    "Suka menyelidiki apa yang diajarkan orang lain",
    "Tidak menemui hambatan dalam berkomunikasi dengan orang lain",
    "Cepat bereaksi untuk membantu saat dibutuhkan",
    "Memiliki minat dan semangat yang besar dalam mengerjakan sesuatu",
    "Tertarik pada orang lain yang juga memiliki karunia belas kasihan",
    "Menyadari kelemahan sendiri dan membantu orang lain menyadari kelemahannya masing-masing",
    "Cenderung melakukan lebih dari yang diminta",
    "Lebih suka mengajar orang-orang percaya supaya dapat menginjili",
    "Percaya pencobaan dan masalah dapat menolong orang untuk bertumbuh",
    "Berdoa untuk jumlah uang yang akan diberikan",
    "Menemukan sukacita ketika bekerja menuju suatu sasaran",
    "Senang melakukan hal-hal yang menyenangkan orang lain",
    "Keinginan yang paling utama adalah melihat kehendak Allah tergenapi dalam segala aspek kehidupan",
    "Mendapat sukacita yang besar manakala mampu menolong orang lain",
    "Merasa bahwa dengan menyelidiki isi Alkitab, semua karunia dapat bekerja",
    "Menerima orang sebagaimana adanya tanpa menghakimi",
    "Memberi perpuluhan dan persembahan lainnya",
    "Membiarkan orang lain mendapat penghargaan agar suatu pekerjaan terlaksana",
    "Mempercayai dan dipercayai",
    "Senang mendorong pertumbuhan rohani orang lain",
    "Tidak ingin memimpin orang",
    "Memecahkan masalah dengan mempergunakan prinsip yang ditentukan Alkitab",
    "Sangat dikasihi karena sikapnya yang positif",
    "Senang menginjili",
    "Sesudah suatu sasaran dicapai, memilih tantangan yang baru",
    "Menghindari konflik dan perselisihan dengan orang lain",
    "Berdoa syafaat bagi orang lain",
    "Memiliki daya tahan tubuh yang tinggi",
    "Memiliki IQ / tingkat kecerdasan yang tinggi",
    "Lebih suka bersaksi melalui cara hidup daripada dengan kata-kata",
    "Percaya bahwa Allah akan memenuhi segala keperluan",
    "Menulis catatan untuk dirinya sendiri secara terus menerus",
    "Tidak suka tergesa-gesa dalam melakukan sesuatu",
    "Merasa perlu menunjukkan atau mendramatisir apa yang ia lihat",
    "Tidak tahan berada di tempat yang kurang rapi",
    "Dapat mendisiplinkan diri",
    "Membuat keputusan dengan mudah",
    "Bekerja keras untuk mengumpulka uang supaya lebih banyak yang dapat ia berikan",
    "Seorang pemimpin yang alami dan sangat cakap",
    "Orang bertipe riang dan penuh sukacita",
    "Cenderung untuk introspeksi diri",
    "Cenderung ingin segala sesuatu sempurna",
    "Mengendalikan diri secara emosional",
    "Selalu menyelesaikan apa yang telah dimulai",
    "Memiliki talenta / kemampuan berbisnis",
    "Tahu kapan menggunakan metode lama dan kapan memperkenalkan metode baru",
    "Lebih dikendalikan oleh perasaan daripada pikiran",
    "Memiliki pendapat dan keyakinan yang kuat",
    "Berpandangan bahwa melayani adalah hal terpenting dalam kehidupan",
    "Hanya memiliki sedikit sahabat",
    "Ingin cepat-cepat menjernahkan masalah dengan orang lain",
    "Berhati-hati untuk tidak menghamburkan uang bagi diri sendiri",
    "Senang bekerja sama dan berada di antara orang - orang",
    "Bersukacita melihat orang lain diberkati dan berdukacita melihat orang lain terluka",
    "Memiliki standar pribadi yang ketat",
    "Lebih suka melakukan sendiri suatu pekerjaan daripada menyuruh orang lain",
    "Memiliki keyakinan dan pendapat yang kuat berdasarkan penyelidikan fakta-fakta",
    "Berharap banyak dari diri sendiri",
    "Tidak mudah dibodohi",
    "Ingin melihat segala sesuatu selesai secepat mungkin",
    "Mau berjuang bagi perkara yang baik",
    "Berkeinginan kuat untuk taat kepada Allah dan berani membayar harganya",
    "Suka menolong pemimpin untuk menyelesaikan pekerjaannya",
    "Percaya kebenaran berkuasa untuk menghasilkan perubahan dalam diri seseorang",
    "Butuh seseorang teman dekat untuk membagikan ide dan pemikirannya",
    "Memiliki baik hikmat yang alami maupun yang dari Allah",
    "Tidak suka melakukan suatu yang rutin",
    "Berdoa syafaat bagi orang-orang yang terluka"
]

# Nama karunia per kolom (A-G) sesuai urutan 7 karunia
KARUNIA_NAMES_140 = [
    "1. Karunia Bernubuat (Perceiver)",
    "2. Karunia Memimpin (Leader)",
    "3. Karunia Melayani (Doer)",
    "4. Karunia Menasihati (Encourager)",
    "5. Karunia Memberi (Giver)",
    "6. Karunia Mengajar (Teacher)",
    "7. Karunia Berbelas Kasihan (Compassion)"
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
    **Petunjuk:** Berikan nilai 0–5 untuk setiap pernyataan sesuai dengan frekuensi yang Anda alami:
    - **0** = Tidak pernah
    - **1** = Jarang
    - **2** = Kadang-kadang
    - **3** = Biasa
    - **4** = Kebanyakan
    - **5** = Selalu
    
    Terdapat **140 pernyataan, **Jawablah dengan **jujur** dan tidak perlu takut terhadap penilaian orang lain. Setelah selesai, klik **Hitung Skor**.
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
            # Hitung total per karunia (setiap 20 soal membentuk 1 karunia, karena 140/7=20)
            totals = [0] * 7
            for i, val in enumerate(st.session_state.karunia_140_answers):
                col_idx = i // 20  # 20 soal per karunia
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
        
        # Urutkan untuk mencari 3 karunia tertinggi
        sorted_idx = sorted(range(7), key=lambda i: totals[i], reverse=True)
        top3 = [(KARUNIA_NAMES_140[i], totals[i]) for i in sorted_idx[:3]]
        
        st.markdown("### 🏆 Tiga Karunia Tertinggi Anda:")
        for rank, (name, score) in enumerate(top3, 1):
            st.success(f"{rank}. **{name}** – Skor: {score}")
        
        # Skor maksimal per karunia = 20 * 5 = 100
        with st.expander("📖 Penjelasan Karunia (Roma 12:6-8)"):
            st.markdown("""
            **1. Karunia Bernubuat (Perceiver)** – Kemampuan melihat kebenaran, membedakan yang baik dan jahat, menyatakan kebenaran dengan tegas.
            
            **2. Karunia Memimpin (Leader)** – Kemampuan memimpin, mengatur, mengarahkan, dan mendelegasikan tugas.
            
            **3. Karunia Melayani (Doer)** – Kemampuan menolong, memenuhi kebutuhan praktis, bekerja dengan rajin dan tanggap.
            
            **4. Karunia Menasihati (Encourager)** – Kemampuan mendorong, memotivasi, dan menasihati untuk pertumbuhan rohani.
            
            **5. Karunia Memberi (Giver)** – Kemampuan memberi dengan sukacita, mengelola sumber daya untuk memberkati.
            
            **6. Karunia Mengajar (Teacher)** – Kemampuan menyampaikan kebenaran secara logis, sistematis, dan mengajar.
            
            **7. Karunia Berbelas Kasihan (Compassion)** – Kemampuan mengasihi, berbelas kasihan, dan menolong yang menderita.
            """)
        
        st.info("Hasil tes ini dapat membantu Anda memahami talenta/potensi diri dan area pengembangan dalam pelayanan.")

if __name__ == "__main__":
    show_karunia_140_karakter()
