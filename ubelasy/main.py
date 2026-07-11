# ubelasy/main.py - BAGIAN YANG DIUBAH

def main():
    # Inisialisasi session state
    if "simulasi_hasil" not in st.session_state:
        st.session_state.simulasi_hasil = None

    # ========== HEADER ==========
    script_dir = Path(__file__).parent.parent
    image_path = script_dir / "assets" / "ubelasy.jpg"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if image_path.exists():
            st.image(str(image_path), width='stretch')  # <-- TETAP PAKAI width DI SINI (st.image support)
        else:
            st.warning("Gambar ubelasy.jpg tidak ditemukan di folder assets/")
        st.markdown(
            "<h1 style='text-align: center;'>🌾 Ubelasy – Agregator Pinjaman Berkelanjutan</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center;'><strong>Skema PSH & Penurunan Suku Bunga 0,5% per Periode</strong></p>",
            unsafe_allow_html=True
        )
    st.markdown("---")
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        if "nkhm_scores" in st.session_state:
            nkhm_total = sum(st.session_state.nkhm_scores.values())
            st.metric("🧠 Skor NKHM", nkhm_total)
            st.caption("(Semakin tinggi skor, semakin baik peluang mendapat pinjaman)")
            st.markdown("---")
        else:
            st.info("Mainkan game NKHM untuk meningkatkan skor Anda!")
            st.markdown("---")
        
        # ========== TAB SELECTOR DI SIDEBAR ==========
        st.header("📑 Navigasi Ubelasy")
        tab_mode = st.radio(
            "Pilih Tab",
            ["📖 Sistem Ubelasy", "⚙️ Simulasi & Agregator"],
            index=1,
            label_visibility="collapsed"
        )
        st.markdown("---")
        
        if tab_mode == "⚙️ Simulasi & Agregator":
            st.header("⚙️ Simulasi Pinjaman")
            K = st.number_input("Pinjaman per Periode (Rp)", value=36_000_000, step=1_000_000, format="%d")
            r1 = st.number_input("Suku bunga awal (%)", value=11.0, step=0.5)
            delta = st.number_input("Penurunan per periode (%)", value=0.5, step=0.1)
            n = st.number_input("Jumlah periode", min_value=1, max_value=10, value=2, step=1)
            tp = st.number_input("Tenor per periode (tahun)", min_value=0.5, max_value=30.0, value=3.0, step=0.5)
            m = st.number_input("Tahun bayar di periode terakhir", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
            bank_type = st.selectbox("Tipe Bank", ["desa", "kota"], format_func=lambda x: "🏡 Pedesaan" if x=="desa" else "🏙️ Perkotaan")
            biaya_dana = st.number_input("Biaya Dana+Overhead (%)", value=9.0, step=0.5)
            hitung = st.button("🚀 Hitung Simulasi", type="primary")  # <-- HAPUS width
    
    # ========== INJECT CSS DOKUMEN ==========
    inject_ubelasy_document_css()
    
    # ========== TAMPILKAN KONTEN BERDASARKAN TAB ==========
    if tab_mode == "📖 Sistem Ubelasy":
        # Tampilkan dokumen lengkap
        st.markdown(get_ubelasy_document(), unsafe_allow_html=True)
        
        # Tombol aksi
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.caption("💡 Untuk menyimpan dokumen ini, gunakan fitur 'Print' di browser Anda (Ctrl+P) dan pilih 'Save as PDF'.")
            
            if st.button("📄 Download Dokumen (PDF)"):  # <-- HAPUS width
                st.info("Fitur download PDF akan segera tersedia. Saat ini silakan gunakan Print > Save as PDF.")
    
    else:
        # ... sisanya sama, untuk st.download_button dan st.dataframe tetap pakai width='stretch'