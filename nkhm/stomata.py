# nkhm/stomata.py
import streamlit as st
import logging
from nkhm.stomata_tanggapan import show_tanggapan
from nkhm.stomata_pilihan_benar_salah import show_pilihan_benar_salah
from nkhm.stomata_pilihan_ganda import show_pilihan_ganda

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_rerun():
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di stomata: {e}")

def show_stomata():
    try:
        st.markdown("## 💖 Sto-mata Hati")
        tab1, tab2, tab3 = st.tabs(["📝 Tanggapan (Skala Likert)", "✅ Pilihan Benar/Salah", "🔢 Pilihan Ganda (a,b,c,d)"])
        
        with tab1:
            show_tanggapan()
        with tab2:
            show_pilihan_benar_salah()
        with tab3:
            show_pilihan_ganda()
    except Exception as e:
        logging.error(f"Error di show_stomata: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Sto-mata Hati: {e}")
        st.exception(e)