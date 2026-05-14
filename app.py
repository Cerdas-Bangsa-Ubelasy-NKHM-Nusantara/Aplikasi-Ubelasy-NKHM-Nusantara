import streamlit as st

st.set_page_config(
    page_title="Sistem Keuangan Nusantara - Ubelasy & NKHM",
    page_icon="🌾",
    layout="wide"
)

# Inisialisasi session state untuk splash
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Fungsi untuk menampilkan splash screen
def show_splash():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Coba tampilkan logo dari assets (gunakan URL raw GitHub jika perlu)
            try:
                st.image("assets/pmd_logo.jpg", width=200)
            except:
                # fallback: tampilkan teks
                st.markdown("<h1 style='text-align: center;'>🌾</h1>", unsafe_allow_html=True)
            
            st.markdown(
                "<h2 style='text-align: center;'>Ubelasy + NKHM Nusantara</h2>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='text-align: center;'>Aplikasi Sistem Keuangan (Pinjaman) Ubelasy Berbasis Pembebasan Sisa Hutang (PSH),<br>"
                "dan gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme Berbasis Data Personal</p>",
                unsafe_allow_html=True
            )
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_done = True
                st.rerun()

# Jika splash belum dilewati, tampilkan splash
if not st.session_state.splash_done:
    show_splash()
    st.stop()

# ========== SETELAH SPLASH ==========
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
