import streamlit as st

st.set_page_config(page_title="Sistem Keuangan Nusantara", layout="wide")

# Inisialisasi session state untuk splash
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Halaman Splash
if not st.session_state.splash_done:
    # Bersihkan semua konten sebelumnya
    st.empty()
    
    # Layout tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo dari URL raw GitHub (jaminan muncul)
        st.image(
            "https://raw.githubusercontent.com/SRPakpahanSST/Ubelasy-NKHM-Nusantara/main/assets/pmd_logo.jpg",
            width=200
        )
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
    st.stop()

# ========== SETELAH SPLASH ==========
# Hanya tampilkan pilihan aplikasi, bukan langsung NKHM
st.sidebar.title("🚀 Pilih Aplikasi")
app_mode = st.sidebar.radio(
    "",
    ["🌾 Ubelasy (Loan Aggregator)", "🌿 NKHM Nusantara (Gamifikasi)"]
)

if app_mode == "🌾 Ubelasy (Loan Aggregator)":
    from ubelasy.main import main as ubelasy_main
    ubelasy_main()
else:
    from nkhm.main import main as nkhm_main
    nkhm_main()
