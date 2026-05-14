import streamlit as st

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="Sistem Keuangan Nusantara - Ubelasy & NKHM",
    page_icon="🌾",
    layout="wide"
)

# ========== SPLASH SCREEN ==========
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    # Bersihkan area utama
    splash_placeholder = st.empty()
    
    with splash_placeholder.container():
        # Layout 3 kolom untuk center
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Logo: coba dari file, jika gagal tampilkan teks
            try:
                st.image("assets/pmd_logo.jpg", width=200)
            except:
                st.markdown("<h1 style='text-align: center;'>🌾</h1>", unsafe_allow_html=True)
            
            # Baris 1
            st.markdown(
                "<h2 style='text-align: center;'>Ubelasy + NKHM Nusantara</h2>",
                unsafe_allow_html=True
            )
            # Baris 2
            st.markdown(
                "<p style='text-align: center;'>Aplikasi Sistem Keuangan (Pinjaman) Ubelasy Berbasis Pembebasan Sisa Hutang (PSH),<br>"
                "dan gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme Berbasis Data Personal</p>",
                unsafe_allow_html=True
            )
            # Tombol Mulai
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_done = True
                st.rerun()
    
    # Hentikan eksekusi sampai tombol ditekan
    st.stop()

# ========== APLIKASI UTAMA (setelah splash) ==========
# Import modul hanya setelah splash selesai
from ubelasy.main import main as ubelasy_main
from nkhm.main import main as nkhm_main

st.sidebar.title("🚀 Pilih Aplikasi")
app_mode = st.sidebar.radio(
    "",
    ["🌾 Ubelasy (Loan Aggregator)", "🌿 NKHM Nusantara (Gamifikasi)"],
    index=0
)

if app_mode == "🌾 Ubelasy (Loan Aggregator)":
    ubelasy_main()
else:
    nkhm_main()
