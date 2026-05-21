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
        st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
    if "nkhm_history" not in st.session_state:
        st.session_state.nkhm_history = []
    if "nkhm_total_questions" not in st.session_state:
        st.session_state.nkhm_total_questions = 0
    if "nkhm_ai_conversation" not in st.session_state:
        st.session_state.nkhm_ai_conversation = []
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
    if "last_score_type" not in st.session_state:
        st.session_state.last_score_type = ""

def get_current_nkhm():
    scores = st.session_state.nkhm_scores
    nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
    nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
    return nkhm_q, nkhm_total

def main():
    init_session_state()
    
    # Splash screen / login
    if not st.session_state.nkhm_user:
        st.empty()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            logo_url = "https://raw.githubusercontent.com/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara/Aplikasi-Ubelasy-NKHM-Nusantara/8785f300fb10ede15e1ade31af699a964938e9ff/assets/nasionalisme1.jpg"
            st.markdown(f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="300"></div>', unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center;'>🌿 NKHM Nusantara</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 18px;'>Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>Berbasis Perkembangan Data Personal</p>", unsafe_allow_html=True)
            st.markdown("""
            <style>
            div.stButton > button { background-color: #4CAF50; color: white; font-size: 22px; font-weight: bold; border-radius: 12px; padding: 12px 24px; width: 100%; }
            div.stButton > button:hover { background-color: #45a049; }
            div[data-testid="stTextInput"] > div > div > input { text-align: center; }
            </style>
            """, unsafe_allow_html=True)
            name = st.text_input("Masukkan namamu", placeholder="contoh: Budi Santoso", label_visibility="collapsed")
            if st.button("🚀 MULAI BELAJAR", use_container_width=True):
                if name and name.strip():
                    st.session_state.nkhm_user = name.strip()
                    st.rerun()
                else:
                    st.error("Masukkan nama dulu!")
        return
    
    QUESTION_BANK = load_all_questions()
    if not QUESTION_BANK:
        st.error("Bank soal kosong. Pastikan folder 'soal' berisi JSON.")
        return
    
    # DEBUG (bisa dihapus nanti)
    st.write("=== DEBUG INFO ===")
    st.write(f"Total soal: {len(QUESTION_BANK)}")
    type_counts = {}
    for q in QUESTION_BANK:
        t = q.get("type", "TIDAK ADA TYPE")
        type_counts[t] = type_counts.get(t, 0) + 1
    st.write(f"Distribusi type: {type_counts}")
    st.write("================")
    
    nkhm_q, nkhm_total = get_current_nkhm()
    nkhm_level, _ = get_nkhm_level(nkhm_total)
    
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
    
    tab1, tab2, tab3 = st.tabs(["🎮 KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
    
    with tab1:
        st.markdown("### Pilih Kuis")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            kategori = st.radio("Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], horizontal=True, key="kategori_filter_kuis")
        with col_f2:
            kecerdasan = st.selectbox("Fokus", ["Semua", "IQ", "EQ", "SQ", "AQ", "Nasionalisme"], key="kecerdasan_filter_kuis")
        
        # ========== FILTER SOAL ==========
        filtered_questions = []
        for q in QUESTION_BANK:
            if kategori == "✨ Semua":
                kategori_ok = True
            elif kategori == "🇮🇩 Nasionalisme":
                kategori_ok = q.get("national", False)
            else:
                kategori_ok = not q.get("national", False)
            if not kategori_ok:
                continue
            if kecerdasan == "Semua":
                fokus_ok = True
            elif kecerdasan == "Nasionalisme":
                fokus_ok = q.get("type") == "Nasionalisme"
            else:
                fokus_ok = q.get("type") == kecerdasan
            if fokus_ok:
                filtered_questions.append(q)
        
        # ========== DETEKSI PERUBAHAN FILTER ==========
        filter_berubah = (st.session_state.nkhm_current_kategori != kategori or 
                          st.session_state.nkhm_current_kecerdasan != kecerdasan)
        
        if filter_berubah:
            st.session_state.nkhm_current_kategori = kategori
            st.session_state.nkhm_current_kecerdasan = kecerdasan
            st.session_state.nkhm_current_filtered = filtered_questions
            st.session_state.nkhm_answered = False
            st.session_state.nkhm_feedback = None
            if filtered_questions:
                st.session_state.nkhm_current_q = random.choice(filtered_questions)
            else:
                st.session_state.nkhm_current_q = None
        else:
            if filtered_questions and (st.session_state.nkhm_current_q is None or 
                                        st.session_state.nkhm_current_q not in filtered_questions):
                st.session_state.nkhm_current_q = random.choice(filtered_questions)
                st.session_state.nkhm_answered = False
                st.session_state.nkhm_feedback = None
            elif not filtered_questions:
                st.session_state.nkhm_current_q = None
        
        # ========== TAMPILKAN SOAL ATAU PERINGATAN ==========
        if not filtered_questions:
            st.warning("Tidak ada soal dengan filter ini. Coba pilih filter lain!")
        else:
            if st.session_state.nkhm_current_q is None:
                st.session_state.nkhm_current_q = random.choice(filtered_questions)
            q = st.session_state.nkhm_current_q
            
            st.markdown(f"### 📝 {q['text']}")
            col_tag1, col_tag2 = st.columns(2)
            display_type = "🇮🇩 Nasionalisme" if q.get('type') == "Nasionalisme" else f"🧠 {q['type']}"
            col_tag1.info(display_type)
            if q.get('national'):
                col_tag2.success("🇮🇩 Nasional")
            else:
                col_tag2.info("📚 Umum")
            
            # Tampilkan bagian dan skala untuk soal EQ_scale
            if q.get("type") == "EQ_scale":
                if q.get("section") and q.get("scale"):
                    st.caption(f"📂 **{q['section']}** — *{q['scale']}*")
                st.info(
                    "📌 **Petunjuk Skor Tanggapan:**\n\n"
                    "Berikan skor tanggapan dalam pilihan Anda (angka 0, 1, 2 atau 3) yang menggambarkan pikiran atau perasaan Anda terhadap hal yang diuraikan:\n"
                    "- **3** = Setuju sekali\n"
                    "- **2** = Setuju\n"
                    "- **1** = Kurang setuju\n"
                    "- **0** = Tidak setuju sekali"
                )
            
            # Tentukan label radio
            radio_label = "Pilih jawabanmu:" if q.get("type") != "EQ_scale" else "Pilih skor tanggapan:"
            
            selected = st.radio(radio_label, q['options'], key=f"radio_{q['text']}", index=None, disabled=st.session_state.nkhm_answered)
            
            # Tombol JAWAB
            if st.button("✅ JAWAB", disabled=st.session_state.nkhm_answered or selected is None, use_container_width=True):
                st.session_state.nkhm_answered = True
                st.session_state.nkhm_total_questions += 1
                
                if q.get("type") == "EQ_scale":
                    # Soal skor tanggapan: nilai langsung dari pilihan (0-3)
                    skor_tambahan = int(selected)
                    skor_baru = st.session_state.nkhm_scores["EQ"] + skor_tambahan
                    st.session_state.nkhm_scores["EQ"] = min(100, skor_baru)
                    st.session_state.nkhm_feedback = "scale_answered"
                    st.session_state.last_score_type = "EQ (skala)"
                    st.session_state.nkhm_history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50],
                        "type": "EQ_scale",
                        "correct": f"Skor {skor_tambahan}",
                        "nkhm_total": get_current_nkhm()[1]
                    })
                else:
                    # Soal pilihan ganda (IQ, EQ biasa, SQ, AQ, Nasionalisme)
                    if q['type'] == "Nasionalisme":
                        score_type = "Nasionalisme"
                    elif q['type'] == "EQ":
                        score_type = "EQ"
                    else:
                        score_type = q['type']
                    
                    st.session_state.last_score_type = score_type
                    
                    if selected == q['correct']:
                        new_score = min(100, st.session_state.nkhm_scores[score_type] + 10)
                        st.session_state.nkhm_scores[score_type] = new_score
                        st.session_state.nkhm_feedback = "benar"
                        _, nkhm_total_baru = get_current_nkhm()
                        save_score(st.session_state.nkhm_user, nkhm_total_baru)
                    else:
                        st.session_state.nkhm_feedback = "salah"
                    
                    nkhm_q_now, nkhm_total_now = get_current_nkhm()
                    st.session_state.nkhm_history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50],
                        "type": score_type,
                        "correct": selected == q['correct'],
                        "nkhm_q": nkhm_q_now,
                        "nkhm_total": nkhm_total_now
                    })
                
                st.rerun()
            
            # Tampilkan feedback (setelah dijawab)
            if st.session_state.nkhm_feedback == "benar":
                fb_type = st.session_state.get("last_score_type", "kecerdasan")
                st.success(f"✅ BENAR! +10 poin untuk {fb_type}")
            elif st.session_state.nkhm_feedback == "salah":
                if q.get('correct'):
                    st.error(f"❌ SALAH! Jawaban benar: **{q['correct']}**")
                else:
                    st.error("❌ Jawaban salah.")
            elif st.session_state.nkhm_feedback == "scale_answered":
                st.success(f"✅ Skor {selected} ditambahkan ke EQ (skala)")
            
            # Tombol navigasi setelah menjawab
            if st.session_state.nkhm_answered:
                col_nav1, col_nav2 = st.columns(2)
                with col_nav1:
                    if st.button("⏩ SOAL SELANJUTNYA", use_container_width=True):
                        if st.session_state.nkhm_current_filtered:
                            st.session_state.nkhm_current_q = random.choice(st.session_state.nkhm_current_filtered)
                        else:
                            st.session_state.nkhm_current_q = None
                        st.session_state.nkhm_answered = False
                        st.session_state.nkhm_feedback = None
                        st.rerun()
                with col_nav2:
                    if st.button("🎮 KUIS BARU", use_container_width=True):
                        if filtered_questions:
                            st.session_state.nkhm_current_q = random.choice(filtered_questions)
                        else:
                            st.session_state.nkhm_current_q = None
                        st.session_state.nkhm_answered = False
                        st.session_state.nkhm_feedback = None
                        st.rerun()
    
    with tab2:
        st.markdown("### Dashboard")
        df_chart = pd.DataFrame({
            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"],
            "Skor": [st.session_state.nkhm_scores["IQ"], st.session_state.nkhm_scores["EQ"],
                     st.session_state.nkhm_scores["SQ"], st.session_state.nkhm_scores["AQ"],
                     st.session_state.nkhm_scores["Nasionalisme"]]
        })
        st.bar_chart(df_chart.set_index("Kecerdasan"), height=400)
        with st.expander("📖 Tentang Rumus NKHM"):
            st.markdown("""
            **NKHM_Q** = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
            **NKHM_Total** = (NKHM_Q + Nasionalisme) / 2
            Dimana: IQ, EQ, SQ, AQ, Nasionalisme 0-100
            """)
        if st.session_state.nkhm_history:
            st.markdown("### Riwayat Kuis")
            history_df = pd.DataFrame(st.session_state.nkhm_history[-10:])
            history_df = history_df[["timestamp", "type", "question", "correct", "nkhm_total"]]
            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
            history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil", "NKHM Total"]
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Pencapaian")
        cols = st.columns(5)
        badges = {"IQ": "🧠 Cendekia", "EQ": "❤️ Empati", "SQ": "🙏 Bhinneka", "AQ": "💪 Tangguh", "Nasionalisme": "🇮🇩 Patriot"}
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
