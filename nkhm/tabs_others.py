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
from nkhm.current_score import get_current_nkhm

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
        history_df = history_df[["timestamp", "type", "question", "correct", "nkhm_total"]]
        history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
        history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil", "NKHM Total"]
        st.dataframe(history_df, use_container_width=True, hide_index=True)

# ========== TAB 3: PRESTASI ==========
def show_tab3():
    st.markdown("### Pencapaian")
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

# ========== TAB 5: TANDING ==========
def show_tab5():
    img_path = Path(__file__).parent.parent / "assets" / "garuda.jpg"
    if img_path.exists():
        st.image(str(img_path), caption="Bertanding Untuk Menang 🇮🇩", use_container_width=True)
    else:
        st.info("💡 Gambar 'garuda.jpg' belum tersedia.")
    st.markdown("---")
    if TOURNAMENT_AVAILABLE and show_tournament is not None:
        tanding_mode = st.radio(
            "Pilih Mode Tanding:",
            ["⚔️ Mode 1v1 (Hot Seat)", "🏆 Mode Turnamen Kelas"],
            horizontal=True,
            key="tanding_mode"
        )
        if tanding_mode == "⚔️ Mode 1v1 (Hot Seat)":
            show_battle()
        else:
            show_tournament()
    else:
        show_battle()
        st.info("🏆 Mode Turnamen Kelas akan segera hadir!")

# ========== TAB 6: KARUNIA & STOMATA ==========
def show_tab6():
    sub_tab1, sub_tab2 = st.tabs(["🎁 Karunia Motivasi", "💖 Sto-mata Hati"])
    with sub_tab1:
        img_path = Path(__file__).parent.parent / "assets" / "karunia.jpg"
        if img_path.exists():
            st.image(str(img_path), caption="Grow in Grace 🇮🇩", use_container_width=True)
        else:
            st.info("💡 Gambar 'karunia.jpg' belum tersedia.")
        st.markdown("---")
        subsub_tab1, subsub_tab2, subsub_tab3, subsub_tab4 = st.tabs([
            "📜 Karunia Umum", "✨ Karunia 140 Karakter", "📋 Karakter & Masalah", "📚 Pengembangan Diri"
        ])
        with subsub_tab1:
            show_karunia()
        with subsub_tab2:
            if KARUNIA_140_AVAILABLE:
                show_karunia_140_karakter()
            else:
                st.error("❌ Modul 'karunia_140_karakter' tidak ditemukan.")
        with subsub_tab3:
            if KARUNIA_KARAKTER_AVAILABLE:
                show_karunia_karakter_masalah()
            else:
                st.error("❌ Modul 'karunia_karakter_masalah' tidak ditemukan.")
        with subsub_tab4:
            if PENGEMBANGAN_DIRI_AVAILABLE:
                show_pengembangan_diri()
            else:
                st.error("❌ Modul 'pengembangan_diri' tidak ditemukan.")
    with sub_tab2:
        show_stomata()

# ========== TAB 7: HADIAH ==========
def show_tab7():
    img_path = Path(__file__).parent.parent / "assets" / "hadiah.gif"
    if img_path.exists():
        st.image(str(img_path), caption="A Giveaway 🇮🇩", use_container_width=True)
    else:
        st.info("💡 Gambar 'hadiah.gif' belum tersedia.")
    st.markdown("---")
    sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs([
        "🦅 Tebak Pahlawan", "🔢 Angka Rahasia", "🚣 Pahlawan Menyeberang Sungai", "🏗️ Tiang & Bendera", "🎲 Lainnya (Coming Soon)"
    ])
    with sub_tab1:
        show_tebak_pahlawan()
    with sub_tab2:
        show_angka_rahasia()
    with sub_tab3:
        show_river_game()
    with sub_tab4:
        show_tiang_bendera()
    with sub_tab5:
        st.info("🎁 Fitur hadiah lainnya akan segera hadir. Dapatkan koin atau reward dengan menjawab kuis!")

# ========== TAB 8: TUTORIAL ==========
def show_tab8():
    show_tutorial()
