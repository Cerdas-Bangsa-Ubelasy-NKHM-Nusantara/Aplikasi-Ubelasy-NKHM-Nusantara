# nkhm/dasbor.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from nkhm.scoring import calculate_nkhm_q, calculate_nkhm_total

def show_dasbor():
    st.markdown("## 👤 Dasbor Saya")
    st.markdown("Ringkasan perkembangan dan rekomendasi personal Anda.")
    
    # Sub-tab
    sub_tab1, sub_tab2 = st.tabs(["📊 Ringkasan & Progres", "📝 Catatan Pribadi"])
    
    # ========== SUB-TAB 1: RINGKASAN & PROGRES ==========
    with sub_tab1:
        scores = st.session_state.nkhm_scores
        history = st.session_state.nkhm_history
        total_questions = st.session_state.nkhm_total_questions
        user_name = st.session_state.nkhm_user
        
        nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
        nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👤 Nama Pengguna", user_name)
        with col2:
            st.metric("📖 Total Soal Dikerjakan", total_questions)
        with col3:
            st.metric("🏆 NKHM Total", f"{nkhm_total:.1f}")
        
        st.markdown("---")
        
        st.subheader("📈 Perkembangan Skor Kecerdasan")
        if history:
            df_history = pd.DataFrame(history)
            if "nkhm_total" in df_history.columns:
                df_recent = df_history.tail(15).copy()
                df_recent["urutan"] = range(1, len(df_recent) + 1)
                st.line_chart(df_recent.set_index("urutan")["nkhm_total"], height=300)
                st.caption("Perkembangan NKHM Total dari 15 kuis terakhir.")
            else:
                st.info("Belum cukup data untuk grafik perkembangan.")
        else:
            st.info("Belum ada riwayat kuis. Mulai kerjakan kuis!")
        
        st.markdown("---")
        
        st.subheader("📊 Analisis Kekuatan & Kelemahan")
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        col_weak, col_strong = st.columns(2)
        with col_strong:
            st.markdown("#### 💪 Kekuatan Teratas")
            for i, (kategori, skor) in enumerate(sorted_scores[:2]):
                st.progress(skor/100, text=f"{kategori}: {skor:.1f}")
        with col_weak:
            st.markdown("#### 📉 Area yang Perlu Ditingkatkan")
            for i, (kategori, skor) in enumerate(sorted_scores[-2:]):
                st.progress(skor/100, text=f"{kategori}: {skor:.1f}")
        
        st.markdown("---")
        
        st.subheader("💡 Rekomendasi untuk Anda")
        lowest_category = min(scores, key=scores.get)
        lowest_score = scores[lowest_category]
        if lowest_score < 50:
            st.warning(f"**🎯 Fokus pada {lowest_category}** – Skor Anda masih di bawah 50.")
        elif lowest_score < 75:
            st.info(f"**📚 Tingkatkan {lowest_category}** – Skor Anda sudah cukup baik, masih bisa ditingkatkan.")
        else:
            st.success(f"**🌟 Luar Biasa!** – Skor {lowest_category} Anda sudah sangat baik.")
        
        if nkhm_total < 40:
            st.info("💪 **NKHM Total masih di bawah 40.** Jangan menyerah!")
        elif nkhm_total < 60:
            st.info("📈 **NKHM Total Anda sudah di jalur yang baik.** Terus tingkatkan.")
        elif nkhm_total < 80:
            st.success("🎯 **NKHM Total Anda bagus!** Targetkan level Pahlawan Cerdas (80+).")
        else:
            st.balloons()
            st.success("🏆 **SELAMAT! Anda telah mencapai level Pahlawan Cerdas!**")
        
        st.markdown("---")
        
        st.subheader("📜 Riwayat Kuis Terbaru")
        if history:
            for item in history[-5:][::-1]:
                status = "✅" if item.get("correct", False) else "❌"
                st.write(f"{status} **{item.get('type', '?')}** – {item.get('question', '')[:60]}...")
            if len(history) > 5:
                st.caption(f"Menampilkan 5 dari {len(history)} riwayat.")
        else:
            st.info("Belum ada riwayat kuis.")
        
        st.markdown("---")
        
        st.subheader("🎯 Target Mingguan Anda")
        if history:
            now = datetime.now()
            week_ago = now - timedelta(days=7)
            questions_last_week = sum(1 for h in history if h.get("timestamp") and datetime.strptime(h["timestamp"], "%H:%M:%S") > week_ago)
            target = 20
            progress = min(questions_last_week / target, 1.0)
            st.progress(progress, text=f"Soal minggu ini: {questions_last_week} / {target}")
            if questions_last_week >= target:
                st.success("✅ Target mingguan tercapai!")
            else:
                st.info(f"Masih {target - questions_last_week} soal lagi.")
        else:
            st.info("Kerjakan soal untuk memulai target mingguan (20 soal/minggu).")
        
        st.markdown("---")
        
        with st.expander("⚠️ Pengaturan Lanjutan"):
            if st.button("Reset Semua Data Saya", use_container_width=True):
                st.warning("Apakah Anda yakin? Tindakan ini akan menghapus semua skor dan riwayat Anda.")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Ya, Reset Sekarang"):
                        st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
                        st.session_state.nkhm_history = []
                        st.session_state.nkhm_total_questions = 0
                        st.success("Data telah direset!")
                        st.rerun()
                with col_no:
                    if st.button("❌ Batal"):
                        st.rerun()
    
    # ========== SUB-TAB 2: CATATAN PRIBADI ==========
    with sub_tab2:
        try:
            from nkhm.catatan_pribadi.main import show_catatan_pribadi
            show_catatan_pribadi()
        except ImportError as e:
            st.error(f"Modul catatan pribadi tidak ditemukan: {e}")
            st.info("Pastikan folder `nkhm/catatan_pribadi/` sudah di-upload ke repository.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat catatan pribadi: {e}")