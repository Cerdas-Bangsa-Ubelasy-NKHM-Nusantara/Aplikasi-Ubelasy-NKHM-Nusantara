import streamlit as st
from pathlib import Path

# ========== SPLASH SCREEN ==========𝐪𝐩𝐚𝐦𝐲𝐦 𝐥

if not st.session_state.get("splash_selesai", False):
    st.set_page_config(page_title="Ubelasy + NKHM Nusantara", page_icon="🇮🇩", layout="wide")

    # Kosongkan area utama
    splash_holder = st.empty()

    with splash_holder.container():
        # ----- Layout 3 kolom untuk center -----
        col_kiri, col_tengah, col_kanan = st.columns([1, 2, 1])
        with col_tengah:
            # 1. Gambar logo (pakai raw URL dari GitHub)
            logo_url = "https://raw.githubusercontent.com/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara/Aplikasi-Ubelasy-NKHM-Nusantara/refs/heads/main/assets/ubelasy+nkhm.jpg"
            st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="300"></div>',
    unsafe_allow_html=True
)
            # 2. Judul "Ubelasy + NKHM Nusantara"
            st.markdown(
                "<h1 style='text-align: center;'>Ubelasy + NKHM Nusantara</h1>",
                unsafe_allow_html=True,
            )

            # 3. Deskripsi tambahan (baris kedua)
            st.markdown(
                "<p style='text-align: center; font-size: 18px;'>Aplikasi Sistem Pinjaman Model Ubelasy Berbasis PSH\n +\n Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>Berbasis Perkembangan Data Personal</p>",
                unsafe_allow_html=True,
            )

            # 4. CSS untuk tombol hijau & besar
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
                unsafe_allow_html=True,
            )

            # 5. Tombol "Mulai"
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_selesai = True
                st.rerun()

    # Hentikan eksekusi aplikasi utama sampai tombol ditekan
    st.stop()
    
    # Tempat untuk splash
    splash_holder = st.empty()
    with splash_holder.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Tampilkan logo PMD Pakpahan Ministry (jika file ada)
            logo_path = "assets/pmd_logo.jpg"  # Ganti dengan nama file gambar Anda
            if os.path.exists(logo_path):
                st.image(logo_path, width=200)
            else:
                # Fallback teks jika gambar belum diupload
                st.markdown("<h1 style='text-align: center;'>PMD</h1>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center;'>Pakpahan Ministry</h3>", unsafe_allow_html=True)
            
            st.markdown("<h1 style='text-align: center;'>🇮🇩 NKHM Nusantara</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Asah 4 Kecerdasan + Nasionalisme</h3>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center;'>
                <p>🧠 <b>IQ</b> – Kecerdasan Intelektual<br>
                ❤️ <b>EQ</b> – Kecerdasan Emosi<br>
                🙏 <b>SQ</b> – Kecerdasan Spiritual<br>
                💪 <b>AQ</b> – Kecerdasan Daya Juang</p>
                <p>Berbasis nilai kebangsaan dan sejarah Indonesia.</p>
                <p><b>Rumus NKHM:</b> ((IQ+EQ)×(SQ+AQ)) / ((IQ+EQ)+(SQ+AQ))</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
            if st.button("🚀 Mulai Sekarang", use_container_width=True):
                st.session_state.splash_selesai = True
                st.rerun()
    st.stop()
    
    
# Mode gelap toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_mode_toggle = st.sidebar.toggle("🌙 Mode Gelap", value=st.session_state.dark_mode)
if dark_mode_toggle != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_mode_toggle
    st.rerun()

if st.session_state.dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #1e1e2f;
    }
    </style>
    """, unsafe_allow_html=True)

# ========== SIDEBAR UTAMA ==========
st.sidebar.title("🚀 Pilih Aplikasi")
app_mode = st.sidebar.radio(
    "Pilih Aplikasi",
    ["🌾 Ubelasy (Loan Aggregator)", "🌿 NKHM Nusantara (Gamifikasi)"],
    index=0,
    label_visibility="collapsed"
)
st.sidebar.markdown("---")

# Import modul
try:
    from ubelasy.main import main as ubelasy_main
    from nkhm.main import main as nkhm_main
except Exception as e:
    st.error(f"Gagal memuat modul: {e}")
    st.stop()

if app_mode == "🌾 Ubelasy (Loan Aggregator)":
    ubelasy_main()
else:
    nkhm_main()
    
