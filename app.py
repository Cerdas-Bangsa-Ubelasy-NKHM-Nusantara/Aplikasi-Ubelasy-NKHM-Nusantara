import streamlit as st

st.set_page_config(page_title="Sistem Keuangan Nusantara", layout="wide")

# ========== SPLASH SCREEN ==========
# Gunakan kunci session state baru agar tidak terpengaruh session lama
if not st.session_state.get("splash_two_in_one_done", False):
    splash_holder = st.empty()
    with splash_holder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Logo dari raw GitHub (dengan fallback)
            logo_url = "https://raw.githubusercontent.com/SRPakpahanSST/Ubelasy-NKHM-Nusantara/main/assets/pmd_logo.jpg"
            try:
                st.image(logo_url, width=180)
            except:
                st.markdown("<h2 style='text-align: center;'>🌾</h2>", unsafe_allow_html=True)
            
            st.markdown("<h1 style='text-align: center;'>Ubelasy + NKHM Nusantara</h1>", unsafe_allow_html=True)
            st.markdown(
                "<p style='text-align: center; font-size: 18px;'>"
                "Aplikasi Sistem Keuangan (Pinjaman) Ubelasy Berbasis Pembebasan Sisa Hutang (PSH),<br>"
                "dan gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme Berbasis Data Personal"
                "</p>",
                unsafe_allow_html=True
            )
            # CSS tombol hijau
            st.markdown(
                """
                <style>
                div.stButton > button {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 22px;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 12px 24px;
                    width: 100%;
                }
                div.stButton > button:hover {
                    background-color: #45a049;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_two_in_one_done = True
                st.rerun()
    st.stop()

# ========== APLIKASI UTAMA (SETELAH SPLASH) ==========
# Impor modul dengan penanganan error
try:
    from ubelasy.main import main as ubelasy_main
    from nkhm.main import main as nkhm_main
except Exception as e:
    st.error(f"Gagal memuat modul: {e}")
    st.stop()

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
