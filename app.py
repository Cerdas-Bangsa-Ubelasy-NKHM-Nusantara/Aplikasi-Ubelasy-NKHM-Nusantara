import streamlit as st

st.set_page_config(page_title="Sistem Keuangan Nusantara", layout="wide")

# Reset session jika ada parameter ?reset=1 di URL
query_params = st.query_params
if query_params.get("reset") == "1":
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.query_params.clear()
    st.rerun()

# Inisialisasi session state untuk splash
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Fungsi splash screen
def show_splash():
    st.empty()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo dari raw GitHub (jamin muncul)
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

# Tampilkan splash jika belum dilewati
if not st.session_state.splash_done:
    show_splash()
    st.stop()   # ← Hentikan eksekusi di sini, tidak akan lanjut ke bawah

# ========== SETELAH SPLASH ==========
# Di sini session_state.splash_done sudah True

# Impor modul dengan penanganan error
try:
    from ubelasy.main import main as ubelasy_main
    from nkhm.main import main as nkhm_main
except Exception as e:
    st.error(f"Gagal mengimpor modul: {e}")
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
