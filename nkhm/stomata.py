# nkhm/stomata.py
import streamlit as st
import logging
from nkhm.stomata_tanggapan import show_tanggapan
from nkhm.stomata_pilihan_benar_salah import show_pilihan_benar_salah
from nkhm.stomata_pilihan_ganda import show_pilihan_ganda

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def show_stomata():
    try:
        st.markdown("## 💖 Sto-mata Hati")
        tab1, tab2, tab3 = st.tabs(["📝 Tanggapan (Skala Likert)", "✅ Pilihan Benar/Salah", "🔢 Pilihan Ganda (a,b,c,d)"])
        
        with tab1:
            try:
                show_tanggapan()
            except Exception as e:
                logging.error(f"Error di tab Tanggapan: {e}", exc_info=True)
                st.error(f"❌ Error di mode Tanggapan: {e}")
        
        with tab2:
            try:
                show_pilihan_benar_salah()
            except Exception as e:
                logging.error(f"Error di tab Pilihan Benar/Salah: {e}", exc_info=True)
                st.error(f"❌ Error di mode Pilihan Benar/Salah: {e}")
        
        with tab3:
            try:
                show_pilihan_ganda()
            except Exception as e:
                logging.error(f"Error di tab Pilihan Ganda: {e}", exc_info=True)
                st.error(f"❌ Error di mode Pilihan Ganda: {e}")
                
    except Exception as e:
        logging.error(f"Error di show_stomata: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Sto-mata Hati: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_stomata()