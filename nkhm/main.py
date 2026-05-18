# nkhm/main.py
import streamlit as st
import pandas as pd
import random
import os
from pathlib import Path
from datetime import datetime
from nkhm.questions import load_all_questions
from nkhm.utils import calculate_nkhm_q, calculate_nkhm_total, get_nkhm_level
from nkhm.ai_assistant import get_ai_response
from nkhm.leaderboard import show_leaderboard, save_score

def init_session_state():
    if "nkhm_user" not in st.session_state:
        st.session_state.nkhm_user = ""
    if "nkhm_scores" not in st.session_state:
        # Skor untuk 4 kecerdasan (IQ, EQ, SQ, AQ) dan Nasionalisme
        st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
    if "nkhm_history" not in st.session_state:
        st.session_state.nkhm_history = []
    if "nkhm_total_questions" not in st.session_state:
        st.session_state.nkhm_total_questions = 0
    if "nkhm_ai_conversation" not in st.session_state:
        st.session_state.nkhm_ai_conversation = []
    # State untuk kuis
    if "nkhm_current_q" not in st.session_state:
        st.session_state.nkhm_current_q = None
    if "nkhm_answered" not in st.session_state:
        st.session_state.nkhm_answered = False
    if "nkhm_current_filtered" not in st.session_state:
        st.session_state.nkhm_current_filtered = []
    if "nkhm_current_kategori" not in st.session_state:
        st.session_state.nkhm_current_kategori = "✨ Semua"
    if "nkhm_current_kecerdasan" not in st.session_state:
        st.session_state.nkhm_current_kecerdasan = "Semua"
    if "nkhm_feedback" not in st.session_state:
        st.session_state.nkhm_feedback = None

def get_current_nkhm():
    """Menghitung NKHM_Q dan NKHM_Total berdasarkan skor saat ini"""
    scores = st.session_state.nkhm_scores
    nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
    nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
    return nkhm_q, nkhm_total

def main():
    init_session_state()
    
    # ========== SPLASH SCREEN / LOGIN ==========
    if not st.session_state.nkhm_user:
        st.empty()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            logo_url = "https://raw.githubusercontent.com/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara/Aplikasi-Ubelasy-NKHM-Nusantara/fe55392b6f600c353b40436a6d02a4e98e3769c6/assets/human.jpg"
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="180"></div>',
                unsafe_allow_html=True
            )
            
            st.markdown(
                "<h1 style='text-align: center;'>NKHM Nusantara</h1>",
                unsafe_allow_html=True
            )
            
            st.markdown(
                "<p style='text-align: center; font-size: 18px;'>Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>Berbasis Perkembangan Data Personal</p>",
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <style>
                div.stButton > button {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 22px;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 12px 24px;
                    width: 100%;
                }
                div.stButton > button:hover {
                    background-color: #45a049;
                }
                div[data-testid="stTextInput"] > div > div > input {
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            name = st.text_input("Masukkan namamu", placeholder="contoh: Budi Santoso", label_visibility="collapsed")
            
            if st.button("🚀 MULAI BELAJAR", use_container_width=True):
                if name and name.strip():
                    st.session_state.nkhm_user = name.strip()
                    st.rerun()
                else:
                    st.error("Masukkan nama dulu!")
        return
    
    # ========== SETELAH LOGIN ==========
    QUESTION_BANK = load_all_questions()
    if not QUESTION_BANK:
        st.error("Bank soal kosong. Pastikan folder 'soal' berisi JSON.")
        return
    
    # Hitung NKHM saat ini
    nkhm_q, nkhm_total = get_current_nkhm()
    nkhm_level, _ = get_nkhm_level(nkhm_total)
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.nkhm_user}")
        st.markdown(f"### 🎯 NKHM Total: **{nkhm_total}**")
        st.markdown(f"### 📊 NKHM_Q: {nkhm_q}")
        st.markdown(f"*Level: {nkhm_level}*")
        st.progress(min(nkhm_total/100, 1.0))
        st.markdown("### 📊 Skor")
        for t in ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]:
            st.progress(st.session_state.nkhm_scores[t]/100, text=f"{t}: {st.session_state.nkhm_scores[t]}")
        
        col1, col2 = st.columns(2)
        col1.metric("📖 Total Soal", st.session_state.nkhm_total_questions)
        best = max([h.get("nkhm_total", 0) for h in st.session_state.nkhm_history] + [nkhm_total])
        col2.metric("🏆 Best NKHM", best)
        
        if st.button("🔄 Reset Skor", use_container_width=True):
            st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
            st.session_state.nkhm_history = []
            st.session_state.nkhm_total_questions = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 🤖 Ki Hajar")
        
        for msg in st.session_state.nkhm_ai_conversation[-10:]:
            if msg["role"] == "user":
                st.write(f"🧑 {msg['content']}")
            else:
                st.write(f"🤖 {msg['content']}")
        
        user_msg = st.chat_input("Tanya Ki Hajar...")
        if user_msg:
            st.session_state.nkhm_ai_conversation.append({"role": "user", "content": user_msg})
            resp = get_ai_response(user_msg, st.session_state.nkhm_ai_conversation, st.session_state.nkhm_user, nkhm_total, nkhm_level)
            st.session_state.nkhm_ai_conversation.append({"role": "assistant", "content": resp})
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Keluar / Ganti Pengguna", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith("nkhm_"):
                    del st.session_state[key]
            st.rerun()
    
    # ========== TAB UTAMA ==========
    tab1, tab2, tab3 = st.tabs(["🎮 KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
    
    # ========== TAB 1: KUIS ==========
    with tab1:
        st.markdown("### Pilih Kuis")
        
        # Filter kategori dan kecerdasan
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            kategori = st.radio(
                "Kategori", 
                ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], 
                horizontal=True,
                key="kategori_filter_kuis"
            )
        with col_f2:
            kecerdasan = st.selectbox(
                "Fokus", 
                ["Semua", "IQ", "EQ", "SQ", "AQ", "Nasionalisme"],
                key="kecerdasan_filter_kuis"
            )
        
        # Filter soal berdasarkan pilihan
        filtered = []
        for q in QUESTION_BANK:
            # Filter berdasarkan Kategori
            if kategori == "✨ Semua":
                kategori_ok = True
            elif kategori == "🇮🇩 Nasionalisme":
                kategori_ok = q.get("national", False)
            else:  # "📚 Umum"
                kategori_ok = not q.get("national", False)
            
            if not kategori_ok:
                continue
            
            # Filter berdasarkan Fokus
            if kecerdasan == "Semua":
                fokus_ok = True
            elif kecerdasan == "Nasionalisme":
                fokus_ok = q.get("type") == "Nasionalisme"
            else:
                fokus_ok = q.get("type") == kecerdasan
            
            if fokus_ok:
                filtered.append(q)
        
        if not filtered:
            st.warning("Tidak ada soal dengan filter ini. Coba pilih filter lain!")
        else:
            # Reset jika filter berubah
            if (st.session_state.nkhm_current_kategori != kategori or 
                st.session_state.nkhm_current_kecerdasan != kecerdasan):
                st.session_state.nkhm_current_kategori = kategori
                st.session_state.nkhm_current_kecerdasan = kecerdasan
                st.session_state.nkhm_current_filtered = filtered
                st.session_state.nkhm_current_q = random.choice(filtered)
                st.session_state.nkhm_answered = False
                st.session_state.nkhm_feedback = None
            
            # Inisialisasi soal pertama jika belum ada
            if st.session_state.nkhm_current_q is None:
                st.session_state.nkhm_current_q = random.choice(filtered)
                st.session_state.nkhm_current_filtered = filtered
            
            # Ambil soal saat ini
            q = st.session_state.nkhm_current_q
            
            # Tampilkan soal
            st.markdown(f"### 📝 {q['text']}")
            col_tag1, col_tag2 = st.columns(2)
            
            # Tentukan tipe soal untuk ditampilkan
            if q.get('type') == "Nasionalisme":
                display_type = "🇮🇩 Nasionalisme"
            else:
                display_type = f"🧠 {q['type']}"
            col_tag1.info(display_type)
            
            if q.get('national'):
                col_tag2.success("🇮🇩 Nasional")
            else:
                col_tag2.info("📚 Umum")
            
            # Tampilkan pilihan jawaban (tanpa default)
            selected = st.radio(
                "Pilih jawabanmu:", 
                q['options'], 
                key=f"radio_{q['text']}",
                index=None,
                disabled=st.session_state.nkhm_answered
            )
            
            # Tombol JAWAB
            if st.button("✅ JAWAB", disabled=st.session_state.nkhm_answered or selected is None, use_container_width=True):
                st.session_state.nkhm_answered = True
                st.session_state.nkhm_total_questions += 1
                
                # Tentukan tipe skor yang akan ditambah
                score_type = q['type'] if q['type'] == "Nasionalisme" else q['type']
                
                if selected == q['correct']:
                    st.session_state.nkhm_scores[score_type] = min(100, st.session_state.nkhm_scores[score_type] + 10)
                    st.session_state.nkhm_feedback = "benar"
                    
                    # Hitung ulang NKHM_Total untuk leaderboard
                    _, nkhm_total_baru = get_current_nkhm()
                    save_score(st.session_state.nkhm_user, nkhm_total_baru)
                else:
                    st.session_state.nkhm_feedback = "salah"
                
                # Simpan riwayat
                st.session_state.nkhm_history.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "question": q['text'][:50],
                    "type": score_type,
                    "correct": selected == q['correct'],
                    "nkhm_q": get_current_nkhm()[0],
                    "nkhm_total": get_current_nkhm()[1]
                })
                st.rerun()
            
            # Tampilkan feedback (setelah dijawab)
            if st.session_state.nkhm_feedback == "benar":
                st.success(f"✅ BENAR! +10 poin untuk {score_type}")
            elif st.session_state.nkhm_feedback == "salah":
                st.error(f"❌ SALAH! Jawaban benar: **{q['correct']}**")
            
            # Tombol navigasi setelah menjawab
            if st.session_state.nkhm_answered:
                col_nav1, col_nav2 = st.columns(2)
                with col_nav1:
                    if st.button("⏩ SOAL SELANJUTNYA", use_container_width=True):
                        st.session_state.nkhm_current_q = random.choice(st.session_state.nkhm_current_filtered)
                        st.session_state.nkhm_answered = False
                        st.session_state.nkhm_feedback = None
                        st.rerun()
                with col_nav2:
                    if st.button("🎮 KUIS BARU", use_container_width=True):
                        st.session_state.nkhm_current_q = random.choice(filtered)
                        st.session_state.nkhm_answered = False
                        st.session_state.nkhm_feedback = None
                        st.rerun()
    
    # ========== TAB 2: DASHBOARD ==========
    with tab2:
        st.markdown("### Dashboard")
        df_chart = pd.DataFrame({
            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"],
            "Skor": [st.session_state.nkhm_scores["IQ"], st.session_state.nkhm_scores["EQ"],
                     st.session_state.nkhm_scores["SQ"], st.session_state.nkhm_scores["AQ"],
                     st.session_state.nkhm_scores["Nasionalisme"]]
        })
        st.bar_chart(df_chart.set_index("Kecerdasan"), height=400)
        
        # Tampilkan rumus NKHM
        with st.expander("📖 Tentang Rumus NKHM"):
            st.markdown("""
            **NKHM_Q** = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
            
            **NKHM_Total** = (NKHM_Q + Nasionalisme) / 2
            
            Dimana:
            - IQ, EQ, SQ, AQ, Nasionalisme memiliki rentang skor 0-100
            - NKHM_Q dan NKHM_Total juga memiliki rentang 0-100
            """)
        
        if st.session_state.nkhm_history:
            st.markdown("### Riwayat Kuis")
            history_df = pd.DataFrame(st.session_state.nkhm_history[-10:])
            history_df = history_df[["timestamp", "type", "question", "correct", "nkhm_total"]]
            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
            history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil", "NKHM Total"]
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    # ========== TAB 3: PRESTASI ==========
    with tab3:
        st.markdown("### Pencapaian")
        cols = st.columns(5)
        badges = {
            "IQ": "🧠 Cendekia", 
            "EQ": "❤️ Empati", 
            "SQ": "🙏 Bhinneka", 
            "AQ": "💪 Tangguh",
            "Nasionalisme": "🇮🇩 Patriot"
        }
        for i, (t, label) in enumerate(badges.items()):
            if st.session_state.nkhm_scores[t] >= 50:
                cols[i].success(f"✅ **{label}**")
            else:
                cols[i].info(f"🔒 {label} (50+)")
        
        if all(st.session_state.nkhm_scores[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]):
            st.balloons()
            st.success("🎉 **GELAR: PAHLAWAN CERDAS NUSANTARA!** 🎉")
        
        answered = len(st.session_state.nkhm_history)
        correct = sum(1 for h in st.session_state.nkhm_history if h["correct"])
        accuracy = (correct / answered * 100) if answered > 0 else 0
        col1, col2, col3 = st.columns(3)
        col1.metric("📖 Total Soal", answered)
        col2.metric("✅ Benar", correct)
        col3.metric("📊 Akurasi", f"{accuracy:.1f}%")
        show_leaderboard()

if __name__ == "__main__":
    main()
