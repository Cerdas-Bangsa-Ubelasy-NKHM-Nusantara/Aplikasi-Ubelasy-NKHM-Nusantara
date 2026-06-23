# nkhm/tabs_others.py
import streamlit as st
import pandas as pd
from pathlib import Path
from nkhm.leaderboard import show_leaderboard
from nkhm.dasbor import show_dasbor
from nkhm.battle import show_battle
from nkhm.stomata import show_stomata
from nkhm.tebak_pahlawan import show_tebak_pahlawan
from nkhm.angka_rahasia import show_angka_rahasia
from nkhm.seberang_sungai import show_river_game
from nkhm.tutorial import show_tutorial
from nkhm.tiang_bendera import show_tiang_bendera
from nkhm.karunia import show_karunia  # Langsung import tanpa try-except
from nkhm.current_score import get_current_nkhm  # <-- PERUBAHAN DI SINI

# Import opsional
try:
    from nkhm.tournament import show_tournament
    TOURNAMENT_AVAILABLE = True
except ImportError:
    TOURNAMENT_AVAILABLE = False
    show_tournament = None

try:
    from nkhm.karunia_140_karakter import show_karunia_140_karakter
    KARUNIA_140_AVAILABLE = True
except ImportError:
    KARUNIA_140_AVAILABLE = False

try:
    from nkhm.karunia_karakter_masalah import show_karunia_karakter_masalah
    KARUNIA_KARAKTER_AVAILABLE = True
except ImportError:
    KARUNIA_KARAKTER_AVAILABLE = False

try:
    from nkhm.pengembangan_diri import show_pengembangan_diri
    PENGEMBANGAN_DIRI_AVAILABLE = True
except ImportError:
    PENGEMBANGAN_DIRI_AVAILABLE = False

# ========== TAB 2: DASHBOARD ==========
def show_tab2():
    st.markdown("### Dashboard")
    # Hapus import dari nkhm.main, gunakan dari current_score
    _, _, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct = get_current_nkhm()
    df_chart = pd.DataFrame({
        "Kecerdasan": ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"],
        "Skor": [iq_pct, eq_pct, sq_pct, aq_pct, nas_pct]
    })
    st.bar_chart(df_chart.set_index("Kecerdasan"), height=400)
    with st.expander("📖 Tentang Rumus NKHM"):
        st.markdown("""
        **NKHM_Q** = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
        **NKHM_Total** = (NKHM_Q + Nasionalisme) / 2
        Dimana: IQ, EQ, SQ, AQ, Nasionalisme dalam skala 0-100
        """)
    if st.session_state.nkhm_history:
        st.markdown("### Riwayat Kuis")
        history_df = pd.DataFrame(st.session_state.nkhm_history[-10:])
        history_df = history_df[["timestamp", "type", "question",
