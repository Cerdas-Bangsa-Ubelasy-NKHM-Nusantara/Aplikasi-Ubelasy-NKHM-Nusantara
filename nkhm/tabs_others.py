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
from nkhm.current_score import get_current_nkhm  # <-- PERUBAHAN: import dari current_score

# Import opsional
try:
    from nkhm.tournament import show_tournament
    TOURNAMENT_AVAILABLE = True
except ImportError:
    TOURNAMENT_AVAILABLE = False
    show_tournament = None

try:
    from nkhm.karunia import show_karunia
    KARUNIA_AVAILABLE = True
except ImportError:
    KARUNIA_AVAILABLE = False
    show_karunia = None

# ========== TAB 2: DASHBOARD ==========
def show_tab2():
    st.markdown("### Dashboard")
    # HAPUS: from nkhm.main import get_current_nkhm
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
        history_df = history_df[["timestamp", "type", "question", "correct", "nkhm_total"]]
        history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
        history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil", "NKHM Total"]
        st.dataframe(history_df, use_container_width=True, hide_index=True)

# ========== TAB 3: PRESTASI ==========
def show_tab3():
    st.markdown("### Pencapaian")
    # HAPUS: from nkhm.main import get_current_nkhm
    cols = st.columns(5)
    badges = {"IQ": "🧠 Cendekia", "EQ": "❤️ Empati", "SQ": "🙏 Bhinneka", "AQ": "💪 Tangguh", "Nasionalisme": "🇮🇩 Patriot"}
    _, _, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct = get_current_nkhm()
    scores_pct = {
        "IQ": iq_pct,
        "EQ": eq_pct,
        "SQ": sq_pct,
        "AQ": aq_pct,
        "Nasionalisme": nas_pct
    }
    for i, (t, label) in enumerate(badges.items()):
        if scores_pct[t] >= 50:
            cols[i].success(f"✅ **{label}**")
        else:
            cols[i].info(f"🔒 {label} (50+)")
    if all(scores_pct[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]):
        st.balloons()
        st.success("🎉 **GELAR: PAHLAWAN CERDAS NUSANTARA!** 🎉")
    answered = len(st.session_state.nkhm_history)
    correct = sum(1 for h in st.session_state.nkhm_history if isinstance(h.get("correct"), bool) and h["correct"])
    accuracy = (correct / answered * 100) if answered > 0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("📖 Total Soal", answered)
    col2.metric("✅ Benar", correct)
    col3.metric("📊 Akurasi", f"{accuracy:.1f}%")
    show_leaderboard()

# ========== TAB 4: DASBOR SAYA ==========
def show_tab4():
    show_dasbor()

# ... (sisanya tetap sama)
