# nkhm/gamifikasi.py
"""
Fitur Gamifikasi NKHM Nusantara.
Menggabungkan Misi & Tantangan dengan Leaderboard.
"""

import streamlit as st
import logging
from nkhm.misi import show_misi_dan_tantangan
from nkhm.leaderboard import show_leaderboard

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def show_gamifikasi():
    """
    Menampilkan halaman Gamifikasi dengan 2 tab:
    1. 🎯 Misi & Tantangan
    2. 🏆 Leaderboard
    """
    try:
        st.markdown("## 🎮 Gamifikasi NKHM")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">🎮</div>
                <div>
                    <div style="font-size: 20px; font-weight: bold;">Selamat datang di Gamifikasi!</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Selesaikan misi, kumpulkan poin, dan raih posisi teratas di leaderboard!
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== TAB SELECTOR =====
        tab1, tab2 = st.tabs(["🎯 Misi & Tantangan", "🏆 Leaderboard"])
        
        with tab1:
            show_misi_dan_tantangan()
        
        with tab2:
            show_leaderboard()
            
    except Exception as e:
        logging.error(f"Error di show_gamifikasi: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Gamifikasi: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_gamifikasi()