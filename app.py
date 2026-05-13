import streamlit as st

# Konfigurasi halaman utama (hanya satu kali)
st.set_page_config(
    page_title="Sistem Keuangan Berkelanjutan Nusantara",
    page_icon="🌾",
    layout="wide"
)

# Sidebar untuk memilih aplikasi
st.sidebar.title("🚀 Pilih Sistem")
app_mode = st.sidebar.radio(
    "Aplikasi Keuangan Berkelanjutan",
    ["🌾 Sistem Ubelasy (Pinjaman Berbasis PSH)", "🌿 NKHM Nusantara (4 Kecerdasan + Nasionalisme + AI)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Tim Cerdas Bangsa")

# Panggil modul sesuai pilihan
if app_mode == "🌾 Sistem Ubelasy (Pinjaman Berbasis PSH)":
    import ubelasy as active_app
else:
    import nkhm as active_app

# Jalankan halaman utama modul
active_app.main()
