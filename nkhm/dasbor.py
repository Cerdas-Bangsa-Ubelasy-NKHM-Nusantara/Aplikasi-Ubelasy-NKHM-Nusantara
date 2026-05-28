# nkhm/dasbor.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from nkhm.scoring import calculate_nkhm_q, calculate_nkhm_total

def show_dasbor():
    st.markdown("## 👤 Dasbor Saya")
    st.markdown("Ringkasan perkembangan dan rekomendasi personal Anda.")
    
    # Ambil data dari session state
    scores = st.session_state.nkhm_scores
    history = st.session_state.nkhm_history
    total_questions = st.session_state.nkhm_total_questions
    user_name = st.session_state.nkhm_user
    
    # Hitung NKHM_Q dan NKHM_Total
    nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
    nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
    
    # ========== 1. KARTU PROFIL SINGKAT ==========
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 Nama Pengguna", user_name)
    with col2:
        st.metric("📖 Total Soal Dikerjakan", total_questions)
    with col3:
        st.metric("🏆 NKHM Total", f"{nkhm_total:.1f}")
    
    st.markdown("---")
    
    # ========== 2. GRAFIK PERKEMBANGAN SKOR ==========
    st.subheader("📈 Perkembangan Skor Kecerdasan")
    
    if history:
        df_history = pd.DataFrame(history)
        if "nkhm_total" in df_history.columns:
            df_recent = df_history.tail(15).copy()
            df_recent["urutan"] = range(1, len(df_recent) + 1)
            st.line_chart(df_recent.set_index("urutan")["nkhm_total"], height=300)
            st.caption("Grafik menunjukkan perkembangan NKHM Total dari 15 kuis terakhir.")
        else:
            st.info("Belum cukup data untuk menampilkan grafik perkembangan. Kerjakan lebih banyak kuis!")
    else:
        st.info("Belum ada riwayat kuis. Mulai kerjakan kuis untuk melihat perkembangan Anda!")
    
    st.markdown("---")
    
    # ========== 3. ANALISIS KEKUATAN & KELEMAHAN ==========
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
    
    # ========== 4. REKOMENDASI PERSONAL ==========
    st.subheader("💡 Rekomendasi untuk Anda")
    
    lowest_category = min(scores, key=scores.get)
    lowest_score = scores[lowest_category]
    
    if lowest_score < 50:
        st.warning(f"""
        **🎯 Fokus pada {lowest_category}**  
        Skor Anda masih di bawah 50. Coba lebih banyak mengerjakan soal dengan filter **Fokus = {lowest_category}**.
        """)
    elif lowest_score < 75:
        st.info(f"""
        **📚 Tingkatkan {lowest_category}**  
        Skor Anda sudah cukup baik, tetapi masih bisa ditingkatkan. Kerjakan 5-10 soal tambahan di kategori ini.
        """)
    else:
        st.success(f"""
        **🌟 Luar Biasa!**  
        Skor {lowest_category} Anda sudah sangat baik. Pertahankan dan bantu teman yang masih kesulitan.
        """)
    
    if nkhm_total < 40:
        st.info("💪 **NKHM Total masih di bawah 40.** Jangan menyerah! Konsistensi adalah kunci. Kerjakan minimal 5 soal setiap hari.")
    elif nkhm_total < 60:
        st.info("📈 **NKHM Total Anda sudah di jalur yang baik.** Terus tingkatkan dengan fokus pada area yang masih lemah.")
    elif nkhm_total < 80:
        st.success("🎯 **NKHM Total Anda bagus!** Pertahankan dan targetkan level Pahlawan Cerdas (80+).")
    else:
        st.balloons()
        st.success("🏆 **SELAMAT! Anda telah mencapai level Pahlawan Cerdas!** Terus asah kemampuan Anda.")
    
    st.markdown("---")
    
    # ========== 5. RIWAYAT KUIS TERBARU ==========
    st.subheader("📜 Riwayat Kuis Terbaru")
    
    if history:
        recent_history = history[-5:][::-1]
        for item in recent_history:
            status = "✅" if item.get("correct", False) else "❌"
            st.write(f"{status} **{item.get('type', '?')}** – {item.get('question', '')[:60]}...")
        if len(history) > 5:
            st.caption(f"Menampilkan 5 dari {len(history)} riwayat.")
    else:
        st.info("Belum ada riwayat kuis. Mulai kerjakan kuis sekarang!")
    
    st.markdown("---")
    
    # ========== 6. TARGET MINGGUAN ==========
    st.subheader("🎯 Target Mingguan Anda")
    
    if history:
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        questions_last_week = sum(1 for h in history if h.get("timestamp") and datetime.strptime(h["timestamp"], "%H:%M:%S") > week_ago)
        target = 20
        progress = min(questions_last_week / target, 1.0)
        st.progress(progress, text=f"Soal minggu ini: {questions_last_week} / {target}")
        if questions_last_week >= target:
            st.success("✅ Target mingguan tercapai! Pertahankan konsistensi Anda.")
        else:
            st.info(f"Masih {target - questions_last_week} soal lagi untuk mencapai target mingguan. Semangat!")
    else:
        st.info("Kerjakan soal untuk memulai target mingguan Anda (20 soal/minggu).")
    
    st.markdown("---")
    
    # ========== 7. TOMBOL RESET ==========
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