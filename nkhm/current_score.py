# nkhm/current_score.py
import streamlit as st
from nkhm.scoring import (
    get_normalized_score,
    calculate_nkhm_q,
    calculate_nkhm_total,
    MAX_POIN_IQ, MAX_POIN_EQ, MAX_POIN_SQ, MAX_POIN_AQ, MAX_POIN_NASIONALISME
)

def get_current_nkhm():
    """Menghitung NKHM_Q, NKHM_Total, dan nilai persentase semua kecerdasan"""
    raw = st.session_state.nkhm_scores
    
    # Hitung total raw points untuk EQ dan AQ (PG + skala)
    eq_raw_total = raw["EQ"] + st.session_state.eq_scale_total
    aq_raw_total = raw["AQ"] + st.session_state.aq_scale_total
    
    # Konversi ke persentase (0-100)
    iq_pct = get_normalized_score(raw["IQ"], MAX_POIN_IQ)
    eq_pct = get_normalized_score(eq_raw_total, MAX_POIN_EQ)
    sq_pct = get_normalized_score(raw["SQ"], MAX_POIN_SQ)
    aq_pct = get_normalized_score(aq_raw_total, MAX_POIN_AQ)
    nas_pct = get_normalized_score(raw["Nasionalisme"], MAX_POIN_NASIONALISME)
    
    nkhm_q = calculate_nkhm_q(iq_pct, eq_pct, sq_pct, aq_pct)
    nkhm_total = calculate_nkhm_total(nkhm_q, nas_pct)
    return nkhm_q, nkhm_total, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct
