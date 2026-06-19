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
    from nkhm.main import get_current_nkhm  # import lokal agar tidak circular
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
    from nkhm.main import get_current_nkhm
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
            if KARUNIA_AVAILABLE and show_karunia is not None:
                show_karunia()
            else:
                st.info("🎁 Fitur Karunia Motivasi akan segera hadir!")
        with subsub_tab2:
            try:
                from nkhm.karunia_140_karakter import show_karunia_140_karakter
                show_karunia_140_karakter()
            except ImportError:
                st.error("❌ Modul 'karunia_140_karakter' tidak ditemukan. Pastikan file sudah ada di folder nkhm.")
            except Exception as e:
                st.error(f"Terjadi error: {e}")
        with subsub_tab3:
            try:
                from nkhm.karunia_karakter_masalah import show_karunia_karakter_masalah
                show_karunia_karakter_masalah()
            except ImportError:
                st.error("❌ Modul 'karunia_karakter_masalah' tidak ditemukan.")
            except Exception as e:
                st.error(f"Terjadi error: {e}")
        with subsub_tab4:
            try:
                from nkhm.pengembangan_diri import show_pengembangan_diri
                show_pengembangan_diri()
            except ImportError:
                st.error("❌ Modul 'pengembangan_diri' tidak ditemukan.")
            except Exception as e:
                st.error(f"Terjadi error: {e}")
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
    sub_tab1, sub_tab2, sub_tab3, sub_tab4  sub_tab5 = st.tabs([
        "🦅 Tebak Pahlawan", "🔢 Angka Rahasia", "🚣 Pahlawan Menyeberang Sungai", "🏗️ Tiang & Bendera", "🎲 Lainnya (Coming Soon)"
    ])
    with sub_tab1:
        show_tebak_pahlawan()
    with sub_tab2:
        show_angka_rahasia()
    with sub_tab3:
        show_river_game()
    with sub_tab4:
        from nkhm.tiang_bendera import show_tiang_bendera
        show_tiang_bendera()
    with sub_tab5:
        st.info("🎁 Fitur hadiah lainnya akan segera hadir. Dapatkan koin atau reward dengan menjawab kuis!")

# ========== TAB 8: TUTORIAL ==========
def show_tab8():
    show_tutorial()
