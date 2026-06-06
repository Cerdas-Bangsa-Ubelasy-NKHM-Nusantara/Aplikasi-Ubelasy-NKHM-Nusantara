# app.py
import streamlit as st
import os
from pathlib import Path

# ========== INISIALISASI SESSION STATE ==========
if "splash_selesai" not in st.session_state:
    st.session_state.splash_selesai = False
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ========== SPLASH SCREEN ==========
if not st.session_state.splash_selesai:
    st.set_page_config(page_title="Ubelasy + NKHM Nusantara", page_icon="🇮🇩", layout="wide")
    
    # Kosongkan area utama
    splash_holder = st.empty()
    
    with splash_holder.container():
        col_kiri, col_tengah, col_kanan = st.columns([1, 2, 1])
        with col_tengah:
            # Logo dari raw GitHub
            logo_url = "https://raw.githubusercontent.com/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara/Aplikasi-Ubelasy-NKHM-Nusantara/refs/heads/main/assets/ubelasy+nkhm.jpg"
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="300"></div>',
                unsafe_allow_html=True
            )
            # Judul
            st.markdown(
                "<h1 style='text-align: center;'>Ubelasy + NKHM Nusantara</h1>",
                unsafe_allow_html=True
            )
            # Deskripsi
            st.markdown(
                "<p style='text-align: center; font-size: 18px;'>Aplikasi Sistem Pinjaman Model Ubelasy Berbasis PSH<br>"
                "+ Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>"
                "Berbasis Perkembangan Data Personal</p>",
                unsafe_allow_html=True
            )
            # CSS tombol
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
            # Tombol Mulai
            if st.button("🚀 Mulai", use_container_width=True):
                st.session_state.splash_selesai = True
                st.rerun()
    
    st.stop()

# ========== SETELAH SPLASH (HALAMAN UTAMA) ==========
st.set_page_config(page_title="Ubelasy + NKHM Nusantara", page_icon="🇮🇩", layout="wide")

# ========== DARK MODE TOGGLE DI SIDEBAR ==========
dark_mode_toggle = st.sidebar.toggle("🌙 Mode Gelap", value=st.session_state.dark_mode)
if dark_mode_toggle != st.session_state.dark_mode:
    st.session_state.dark_mode = dark_mode_toggle
    st.rerun()

if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stSidebar {
            background-color: #1e1e2f;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ========== SIDEBAR UTAMA ==========
st.sidebar.title("🚀 Pilih Aplikasi")
app_mode = st.sidebar.radio(
    "Pilih Aplikasi",
    ["🌾 Ubelasy (Loan Aggregator)", "🌿 NKHM Nusantara (Gamifikasi)"],
    index=0,
    label_visibility="collapsed"
)

# Label tips
st.sidebar.caption("💡 Tips: Aplikasi ada dalam 2 sidebar: kanan dan kiri. Klik tanda << atau >>, lalu sentuh layar di sisi kanan")

st.sidebar.markdown("---")

# ========== TOMBOL CATATAN PRIBADI (HANYA UNTUK NKHM) ==========
if app_mode == "🌿 NKHM Nusantara (Gamifikasi)":
    vercel_url = "https://my-personal-notes-app-187q.vercel.app"
    nkhm_url = "https://tim-cerdas-bangsa-ubelasy-nkhm-nusantara.streamlit.app"
    target_url = f"{nkhm_url}?tab=dasbor&subtab=catatan"
  
    # Tombol Catatan Pribadi (membuka di tab baru)
    st.sidebar.link_button("📝 Catatan Pribadi", vercel_url, use_container_width=True)
    
    st.sidebar.markdown("---")   # separator setelah tombol
    
# ========== IMPORT MODUL ==========
try:
    from ubelasy.main import main as ubelasy_main
    from nkhm.main import main as nkhm_main
except Exception as e:
    st.error(f"Gagal memuat modul: {e}")
    st.stop()

# ========== JALANKAN MODUL YANG DIPILIH ==========
if app_mode == "🌾 Ubelasy (Loan Aggregator)":
    ubelasy_main()
else:
    nkhm_main()
