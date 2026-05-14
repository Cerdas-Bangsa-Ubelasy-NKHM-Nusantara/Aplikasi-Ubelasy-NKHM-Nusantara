import streamlit as st
import time

st.set_page_config(page_title="Sistem Keuangan Nusantara", layout="wide")

# Inisialisasi session state
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Fungsi splash
def splash():
    st.empty()  # bersihkan
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # Logo (gunakan raw GitHub)
        st.image("https://raw.githubusercontent.com/SRPakpahanSST/Ubelasy-NKHM-Nusantara/main/assets/pmd_logo.jpg", width=200)
        st.markdown("<h2 style='text-align: center;'>Ubelasy + NKHM Nusantara</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center;'>Aplikasi Sistem Keuangan (Pinjaman) Ubelasy Berbasis Pembebasan Sisa Hutang (PSH),<br>"
            "dan gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme Berbasis Data Personal</p>",
            unsafe_allow_html=True
        )
        if st.button("🚀 Mulai", use_container_width=True):
            st.session_state.splash_done = True
            st.rerun()

# Tampilkan splash jika belum selesai
if not st.session_state.splash_done:
    splash()
    st.stop()

# Setelah splash, baru import dan tampilkan pilihan
from ubelasy.main import main as ubelasy_main
from nkhm.main import main as nkhm_main

st.sidebar.title("🚀 Pilih Aplikasi")
app_mode = st.sidebar.radio("", ["🌾 Ubelasy (Loan Aggregator)", "🌿 NKHM Nusantara (Gamifikasi)"])

if app_mode == "🌾 Ubelasy (Loan Aggregator)":
    ubelasy_main()
else:
    nkhm_main()
