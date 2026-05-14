import streamlit as st

# Konfigurasi halaman utama (hanya sekali)
st.set_page_config(
    page_title="Sistem Keuangan Nusantara - Ubelasy & NKHM",
    page_icon="🌾",
    layout="wide"
)

# ========== SPLASH SCREEN ==========
if not st.session_state.get("splash_selesai", False):
    # Bersihkan area utama
    splash_holder = st.empty()

    with splash_holder.container():
        # Layout 3 kolom untuk center
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Logo dari raw GitHub (pastikan URL benar)
            logo_url = "https://raw.githubusercontent.com/SRPakpahanSST/Ubelasy-NKHM-Nusantara/main/assets/pmd_logo.jpg"
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="180"></div>',
                unsafe_allow_html=True
            )

            # Judul utama (2 baris: baris1 = Ubelasy + NKHM Nusantara)
            st.markdown(
                "<h1 style='text-align: center;'>Ubelasy + NKHM Nusantara</h1>",
                unsafe_allow_html=True
            )

            # Deskripsi (baris2: penjelasan singkat)
            st.markdown(
                "<p style='text-align: center; font-size: 18px;'>"
                "Aplikasi Sistem Keuangan (Pinjaman) Ubelasy Berbasis Pembebasan Sisa Hutang (PSH),<br>"
                "dan gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme Berbasis Data Personal"
                "</p>",
                unsafe_allow_html=True
            )

            # CSS untuk tombol hijau besar
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

            # Tombol "Mulai"
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_selesai = True
                st.rerun()

    # Hentikan eksekusi sampai tombol ditekan
    st.stop()

# ========== APLIKASI UTAMA (SETELAH SPLASH) ==========
# Impor modul (dengan penanganan error)
try:
    from ubelasy.main import main as ubelasy_main
    from nkhm.main import main as nkhm_main
except Exception as e:
    st.error(f"Gagal memuat modul: {e}")
    st.stop()

# Sidebar untuk memilih aplikasi
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
