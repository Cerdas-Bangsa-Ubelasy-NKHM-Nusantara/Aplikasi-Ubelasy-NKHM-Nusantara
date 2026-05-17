‎# app.py (bagian splash screen)
‎import streamlit as st
‎import os
‎from pathlib import Path
‎
‎# Dapatkan path absolut ke direktori root
‎script_dir = Path(__file__).parent
‎logo_path = script_dir / "assets" / "pmd_logo.jpg"
‎
‎st.set_page_config(page_title="Sistem Keuangan Nusantara", layout="wide")
‎
‎# Splash screen (dengan session state baru)
‎if "splash_two_in_one_done" not in st.session_state:
‎    st.session_state.splash_two_in_one_done = False
‎
‎if not st.session_state.splash_two_in_one_done:
‎    st.empty()
‎    col1, col2, col3 = st.columns([1,2,1])
‎    with col2:
‎        st.image("https://raw.githubusercontent.com/SRPakpahanSST/Ubelasy-NKHM-Nusantara/main/assets/pmd_logo.jpg", width=200)
‎        st.markdown("<h1 style='text-align: center;'>Ubelasy + NKHM Nusantara</h1>", unsafe_allow_html=True)
‎        st.markdown(
‎            "<p style='text-align: center;'>Aplikasi Sistem Keuangan (Pinjaman) Ubelasy Berbasis Pembebasan Sisa Hutang (PSH),<br>"
‎            "dan gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme Berbasis Data Personal</p>",
‎            unsafe_allow_html=True
‎        )
‎        if st.button("🚀 Mulai", use_container_width=True):
‎            st.session_state.splash_two_in_one_done = True
‎            st.rerun()
‎    st.stop()
‎
‎# ========== SIDEBAR UTAMA ==========
‎st.sidebar.title("🚀 Pilih Aplikasi")
‎app_mode = st.sidebar.radio(
‎    "Pilih Aplikasi",  # ← beri label yang bermakna
‎    ["🌾 Ubelasy (Loan Aggregator)", "🌿 NKHM Nusantara (Gamifikasi)"],
‎    index=0,
‎    label_visibility="collapsed"  # opsional: sembunyikan label tapi tetap ada nilainya
‎)
‎st.sidebar.markdown("---")   # Pemisah agar radio tetap terlihat
‎
‎# Import modul
‎try:
‎    from ubelasy.main import main as ubelasy_main
‎    from nkhm.main import main as nkhm_main
‎except Exception as e:
‎    st.error(f"Gagal memuat modul: {e}")
‎    st.stop()
‎
‎if app_mode == "🌾 Ubelasy (Loan Aggregator)":
‎    ubelasy_main()
‎else:
‎    nkhm_main()
‎
