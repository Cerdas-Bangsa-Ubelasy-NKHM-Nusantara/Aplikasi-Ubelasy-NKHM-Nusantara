# nkhm/main.py
‎import streamlit as st
‎import pandas as pd
‎import random
import os
‎from pathlib import Path
‎from datetime import datetime
‎from nkhm.questions import
load_all_questions
from nkhm.utils import calculate_nkhm, get_nkhm_level
‎from nkhm.ai_assistant import get_ai_response
‎from nkhm.leaderboard import show_leaderboard, save_score

‎def init_session_state():
‎    if "nkhm_user" not in st.session_state:
‎        st.session_state.nkhm_user = ""
‎    if "nkhm_scores" not in st.session_state:
‎        st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
‎    if "nkhm_history" not in st.session_state:
‎        st.session_state.nkhm_history = []
‎    if "nkhm_total_questions" not in st.session_state:
‎        st.session_state.nkhm_total_questions = 0
‎    if "nkhm_ai_conversation" not in st.session_state:
‎        st.session_state.nkhm_ai_conversation = []
‎
‎def main():
‎    init_session_state()
‎    
‎    if not st.session_state.nkhm_user:
‎        # ========== LOGIN PAGE DENGAN KONTEN DI TENGAH ==========
‎        st.empty()
‎        col_outer1, col_outer2, col_outer3 = st.columns([1, 2, 1])
‎        with col_outer2:
‎            # Gunakan kolom untuk memusatkan gambar
‎            col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
‎            with col_img2:
‎                script_dir = Path(__file__).parent.parent  # naik ke root
‎                image_path = script_dir / "assets" / "human.jpg"
‎                if image_path.exists():
‎                    st.image(str(image_path), width=150)
‎                else:
‎                    st.warning("Gambar human.jpg tidak ditemukan di folder assets/")
‎            
‎            # Judul di tengah
‎            st.markdown(
‎                "<h1 style='text-align: center;'>🇮🇩 NKHM Nusantara</h1>",
‎                unsafe_allow_html=True
‎            )
‎            
‎            # Input nama (rata tengah dengan CSS)
‎            st.markdown(
‎                """
‎                <style>
‎                div[data-testid="stTextInput"] > div > div > input {
‎                    text-align: center;
‎                }
‎                </style>
‎                """,
‎                unsafe_allow_html=True
‎            )
‎            
‎            name = st.text_input("Masukkan namamu", placeholder="contoh: Budi Santoso", label_visibility="collapsed")
‎            
‎            # Tombol MULAI BELAJAR
‎            if st.button("🚀 MULAI BELAJAR", use_container_width=True):
‎                if name and name.strip():
‎                    st.session_state.nkhm_user = name.strip()
‎                    st.rerun()
‎                else:
‎                    st.error("Masukkan nama dulu!")
‎        return
‎    
‎    QUESTION_BANK = load_all_questions()
‎    if not QUESTION_BANK:
‎        st.error("Bank soal kosong. Pastikan folder 'soal' berisi JSON.")
‎        return
‎    
‎    nkhm = calculate_nkhm(
‎        st.session_state.nkhm_scores["IQ"],
‎        st.session_state.nkhm_scores["EQ"],
‎        st.session_state.nkhm_scores["SQ"],
‎        st.session_state.nkhm_scores["AQ"]
‎    )
‎    nkhm_level, _ = get_nkhm_level(nkhm)
‎    
‎    with st.sidebar:
‎        st.markdown(f"## 👤 {st.session_state.nkhm_user}")
‎        st.markdown(f"### 🎯 NKHM: **{nkhm}**")
‎        st.markdown(f"*Level: {nkhm_level}*")
‎        st.progress(min(nkhm/100, 1.0))
‎        st.markdown("### 📊 Skor")
‎        for t in ["IQ", "EQ", "SQ", "AQ"]:
‎            st.progress(st.session_state.nkhm_scores[t]/100, text=f"{t}: {st.session_state.nkhm_scores[t]}")
‎        col1, col2 = st.columns(2)
‎        col1.metric("📖 Total Soal", st.session_state.nkhm_total_questions)
‎        best = max([h.get("nkhm", 0) for h in st.session_state.nkhm_history] + [nkhm])
‎        col2.metric("🏆 Best NKHM", best)
‎        if st.button("🔄 Reset Skor", use_container_width=True):
‎            st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
‎            st.session_state.nkhm_history = []
‎            st.session_state.nkhm_total_questions = 0
‎            st.rerun()
‎        st.markdown("---")
‎        st.markdown("## 🤖 Ki Hajar")
‎        for msg in st.session_state.nkhm_ai_conversation[-10:]:
‎            if msg["role"] == "user":
‎                st.write(f"🧑 {msg['content']}")
‎            else:
‎                st.write(f"🤖 {msg['content']}")
‎        user_msg = st.chat_input("Tanya Ki Hajar...")
‎        if user_msg:
‎            st.session_state.nkhm_ai_conversation.append({"role": "user", "content": user_msg})
‎            resp = get_ai_response(user_msg, st.session_state.nkhm_ai_conversation, st.session_state.nkhm_user, nkhm, nkhm_level)
‎            st.session_state.nkhm_ai_conversation.append({"role": "assistant", "content": resp})
‎            st.rerun()
‎    
‎    tab1, tab2, tab3 = st.tabs(["🎮 KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
‎    
‎    with tab1:
‎        st.markdown("### Pilih Kuis")
‎        kategori = st.radio("Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], horizontal=True)
‎        kecerdasan = st.selectbox("Fokus", ["Semua", "IQ", "EQ", "SQ", "AQ"])
‎        
‎        filtered = [q for q in QUESTION_BANK 
‎                    if (kategori == "✨ Semua" or 
‎                        (kategori == "🇮🇩 Nasionalisme" and q.get("national", False)) or
‎                        (kategori == "📚 Umum" and not q.get("national", False))) and
‎                    (kecerdasan == "Semua" or q.get("type") == kecerdasan)]
‎        if not filtered:
‎            st.warning("Tidak ada soal.")
‎        else:
‎            if "nkhm_current_q" not in st.session_state:
‎                st.session_state.nkhm_current_q = random.choice(filtered)
‎                st.session_state.nkhm_answered = False
‎            q = st.session_state.nkhm_current_q
‎            st.markdown(f"### 📝 {q['text']}")
‎            col_tag1, col_tag2 = st.columns(2)
‎            col_tag1.info(f"🧠 {q['type']}")
‎            col_tag2.success("🇮🇩 Nasional") if q.get('national') else col_tag2.info("📚 Umum")
‎            selected = st.radio("Pilih jawaban:", q['options'], key=f"q_{q['text']}", disabled=st.session_state.nkhm_answered)
‎            if st.button("✅ JAWAB", disabled=st.session_state.nkhm_answered):
‎                st.session_state.nkhm_answered = True
‎                st.session_state.nkhm_total_questions += 1
‎                if selected == q['correct']:
‎                    st.session_state.nkhm_scores[q['type']] = min(100, st.session_state.nkhm_scores[q['type']] + 10)
‎                    st.success(f"✅ BENAR! +10 poin untuk {q['type']}")
‎                    
‎                    # Hitung ulang NKHM setelah skor berubah
‎                    nkhm_baru = calculate_nkhm(
‎                        st.session_state.nkhm_scores["IQ"],
‎                        st.session_state.nkhm_scores["EQ"],
‎                        st.session_state.nkhm_scores["SQ"],
‎                        st.session_state.nkhm_scores["AQ"]
‎                    )
‎                    # Simpan ke leaderboard
‎                    save_score(st.session_state.nkhm_user, nkhm_baru)
‎                else:
‎                    st.error(f"❌ SALAH! Jawaban: {q['correct']}")
‎                st.session_state.nkhm_history.append({
‎                    "timestamp": datetime.now().strftime("%H:%M:%S"),
‎                    "question": q['text'][:50],
‎                    "type": q['type'],
‎                    "correct": selected == q['correct'],
‎                    "nkhm": calculate_nkhm(
‎                        st.session_state.nkhm_scores["IQ"],
‎                        st.session_state.nkhm_scores["EQ"],
‎                        st.session_state.nkhm_scores["SQ"],
‎                        st.session_state.nkhm_scores["AQ"]
‎                    )
‎                })
‎                if st.button("⏩ SOAL SELANJUTNYA"):
‎                    st.session_state.nkhm_current_q = random.choice(filtered)
‎                    st.session_state.nkhm_answered = False
‎                    st.rerun()
‎            if st.session_state.nkhm_answered:
‎                if st.button("🎮 Kuis Baru"):
‎                    st.session_state.nkhm_current_q = random.choice(filtered)
‎                    st.session_state.nkhm_answered = False
‎                    st.rerun()
‎    
‎    with tab2:
‎        st.markdown("### Dashboard")
‎        df_chart = pd.DataFrame({
‎            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ"],
‎            "Skor": [st.session_state.nkhm_scores["IQ"], st.session_state.nkhm_scores["EQ"],
‎                     st.session_state.nkhm_scores["SQ"], st.session_state.nkhm_scores["AQ"]]
‎        })
‎        st.bar_chart(df_chart.set_index("Kecerdasan"), height=300)
‎        if st.session_state.nkhm_history:
‎            st.markdown("### Riwayat Kuis")
‎            history_df = pd.DataFrame(st.session_state.nkhm_history[-10:])
‎            history_df = history_df[["timestamp", "type", "question", "correct"]]
‎            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
‎            st.dataframe(history_df, use_container_width=True, hide_index=True)
‎    
‎    with tab3:
‎        st.markdown("### Pencapaian")
‎        cols = st.columns(4)
‎        badges = {"IQ": "🧠 Cendekia", "EQ": "❤️ Empati", "SQ": "🙏 Bhinneka", "AQ": "💪 Tangguh"}
‎        for i, (t, label) in enumerate(badges.items()):
‎            if st.session_state.nkhm_scores[t] >= 50:
‎                cols[i].success(f"✅ **{label}**")
‎            else:
‎                cols[i].info(f"🔒 {label} (50+)")
‎        if all(st.session_state.nkhm_scores[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ"]):
‎            st.balloons()
‎            st.success("🎉 **GELAR: PAHLAWAN CERDAS NUSANTARA!** 🎉")
‎        answered = len(st.session_state.nkhm_history)
‎        correct = sum(1 for h in st.session_state.nkhm_history if h["correct"])
‎        accuracy = (correct / answered * 100) if answered > 0 else 0
‎        col1, col2, col3 = st.columns(3)
‎        col1.metric("📖 Total Soal", answered)
‎        col2.metric("✅ Benar", correct)
‎        col3.metric("📊 Akurasi", f"{accuracy:.1f}%")
‎        show_leaderboard()
‎
‎if __name__ == "__main__":
‎    main()
‎
