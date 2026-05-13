# nkhm.py
import streamlit as st
import pandas as pd
import json
import os
import random
from datetime import datetime

# Load semua soal dari folder soal_mentah/
def load_questions():
    questions = []
    
    # Mapping folder ke file JSON
    folder_mapping = {
        "IQ": "iq_1.json",
        "EQ": "eq_1.json",
        "SQ": "sq_1.json",
        "AQ": "aq_1.json",
        "Nasionalisme": "nasionalisme_1.json"
    }
    
    base_path = "soal_mentah"
    
    for folder, filename in folder_mapping.items():
        filepath = os.path.join(base_path, folder, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for soal in data:
                    # Pastikan format sesuai
                    if all(k in soal for k in ["text", "options", "correct", "type", "national"]):
                        questions.append(soal)
    
    return questions

# Hitung NKHM
def calculate_nkhm(iq, eq, sq, aq):
    pembilang = (iq + eq) * (sq + aq)
    penyebut = (iq + eq) + (sq + aq)
    if penyebut == 0:
        return 0
    return round(pembilang / penyebut, 2)

def get_nkhm_level(nkhm):
    if nkhm >= 80:
        return "🌟 Pahlawan Cerdas", "green"
    elif nkhm >= 60:
        return "📚 Cendekia Muda", "blue"
    elif nkhm >= 40:
        return "🌱 Penjelajah Ilmu", "orange"
    else:
        return "🌿 Perintis Jalan", "gray"

def main():
    """Halaman utama NKHM Nusantara"""
    
    st.title("🌿 NKHM Nusantara")
    st.markdown("**Asah 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme**")
    st.markdown("Berbasis Perkembangan Data Personal | AI Asisten Ki Hajar")
    st.markdown("---")
    
    # Inisialisasi session state
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "scores" not in st.session_state:
        st.session_state.scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
    if "history" not in st.session_state:
        st.session_state.history = []
    if "total_questions" not in st.session_state:
        st.session_state.total_questions = 0
    if "ai_conversation" not in st.session_state:
        st.session_state.ai_conversation = []
    
    # Load soal
    QUESTION_BANK = load_questions()
    
    # ========== LOGIN ==========
    if not st.session_state.user:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Coba tampilkan logo jika ada
            logo_path = "assets/pmd_logo.jpg"
            if os.path.exists(logo_path):
                st.image(logo_path, width=150)
            else:
                st.markdown("<h1 style='text-align: center;'>🇮🇩</h1>", unsafe_allow_html=True)
            
            st.title("🇮🇩 NKHM NUSANTARA")
            st.markdown("### Asah 4 Kecerdasan + Nasionalisme")
            st.markdown("---")
            name = st.text_input("🖊️ Masukkan namamu", placeholder="contoh: Budi Santoso")
            col_a, col_b = st.columns(2)
            with col_a:
                st.caption("🧠 IQ = Intelektual")
                st.caption("❤️ EQ = Emosi")
            with col_b:
                st.caption("🙏 SQ = Spiritual")
                st.caption("💪 AQ = Daya Juang")
            if st.button("🚀 MULAI BELAJAR", use_container_width=True):
                if name and name.strip():
                    st.session_state.user = name.strip()
                    st.rerun()
                else:
                    st.error("Masukkan nama dulu ya!")
        return
    
    # ========== SIDEBAR ==========
    nkhm = calculate_nkhm(
        st.session_state.scores["IQ"],
        st.session_state.scores["EQ"],
        st.session_state.scores["SQ"],
        st.session_state.scores["AQ"]
    )
    nkhm_level, _ = get_nkhm_level(nkhm)
    
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.user}")
        st.markdown("---")
        st.markdown(f"### 🎯 NKHM: **{nkhm}**")
        st.markdown(f"*Level: {nkhm_level}*")
        st.progress(min(nkhm/100, 1.0), text="Progress")
        st.markdown("---")
        st.markdown("### 📊 Skor Kecerdasan")
        for t in ["IQ", "EQ", "SQ", "AQ"]:
            st.progress(st.session_state.scores[t]/100, text=f"{t}: {st.session_state.scores[t]}")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📖 Total Soal", st.session_state.total_questions)
        with col2:
            best = max([h.get("nkhm", 0) for h in st.session_state.history] + [nkhm])
            st.metric("🏆 Best NKHM", best)
        if st.button("🔄 Reset Semua Skor", use_container_width=True):
            st.session_state.scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0}
            st.session_state.history = []
            st.session_state.total_questions = 0
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 🤖 Asisten Ki Hajar")
        # Tampilkan chat sederhana (tanpa OpenAI karena API key di secrets)
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.ai_conversation[-10:]:
                if msg["role"] == "user":
                    st.write(f"🧑 {msg['content']}")
                else:
                    st.write(f"🤖 {msg['content']}")
        
        user_msg = st.chat_input("Tanya Ki Hajar...")
        if user_msg:
            st.session_state.ai_conversation.append({"role": "user", "content": user_msg})
            # Respons sederhana (bisa ganti dengan OpenAI jika ada API key)
            response = f"Halo {st.session_state.user}! Teruslah belajar untuk meningkatkan 4 kecerdasanmu. NKHM-mu saat ini {nkhm} ({nkhm_level})."
            st.session_state.ai_conversation.append({"role": "assistant", "content": response})
            st.rerun()
    
    # ========== MAIN TAB ==========
    tab1, tab2, tab3 = st.tabs(["🎮 MAIN KUIS", "📊 DASHBOARD", "🏆 PRESTASI"])
    
    # TAB 1: Kuis
    with tab1:
        st.markdown("### 🎮 Pilih Kuis")
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            kategori = st.radio("🏷️ Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], horizontal=True)
        with filter_col2:
            kecerdasan = st.selectbox("🧠 Fokus Kecerdasan", ["Semua", "IQ", "EQ", "SQ", "AQ"])
        
        filtered = QUESTION_BANK.copy()
        if kategori == "🇮🇩 Nasionalisme":
            filtered = [q for q in filtered if q.get("national", False)]
        elif kategori == "📚 Umum":
            filtered = [q for q in filtered if not q.get("national", False)]
        if kecerdasan != "Semua":
            filtered = [q for q in filtered if q.get("type") == kecerdasan]
        
        if not filtered:
            st.warning("Tidak ada soal dengan filter ini. Coba filter lain!")
        else:
            if "current_q" not in st.session_state:
                st.session_state.current_q = random.choice(filtered)
                st.session_state.answered = False
            
            q = st.session_state.current_q
            with st.container():
                st.markdown("---")
                st.markdown(f"### 📝 {q['text']}")
                col_tag1, col_tag2 = st.columns(2)
                with col_tag1:
                    st.info(f"🧠 {q['type']}")
                with col_tag2:
                    if q.get('national', False):
                        st.success("🇮🇩 Nasional")
                    else:
                        st.info("📚 Umum")
                
                selected = st.radio("Pilih jawabanmu:", q['options'], key=f"q_{q['text']}", disabled=st.session_state.answered)
                
                if st.button("✅ JAWAB", use_container_width=True, disabled=st.session_state.answered):
                    st.session_state.answered = True
                    st.session_state.total_questions += 1
                    if selected == q['correct']:
                        st.session_state.scores[q['type']] = min(100, st.session_state.scores[q['type']] + 10)
                        st.success(f"✅ **BENAR!** +10 poin untuk {q['type']}")
                    else:
                        st.error(f"❌ **SALAH!** Jawaban benar: **{q['correct']}**")
                    
                    st.session_state.history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50] + "...",
                        "type": q['type'],
                        "correct": selected == q['correct'],
                        "nkhm": nkhm
                    })
                    
                    if st.button("⏩ SOAL SELANJUTNYA", use_container_width=True):
                        st.session_state.current_q = random.choice(filtered)
                        st.session_state.answered = False
                        st.rerun()
                
                if st.session_state.answered:
                    if st.button("🎮 Kuis Baru", use_container_width=True):
                        st.session_state.current_q = random.choice(filtered)
                        st.session_state.answered = False
                        st.rerun()
    
    # TAB 2: Dashboard
    with tab2:
        st.markdown("### 📊 Dashboard Perkembangan")
        df_chart = pd.DataFrame({
            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ"],
            "Skor": [st.session_state.scores["IQ"], st.session_state.scores["EQ"], st.session_state.scores["SQ"], st.session_state.scores["AQ"]]
        })
        st.bar_chart(df_chart.set_index("Kecerdasan"), height=300)
        
        st.markdown("### 📝 Rekomendasi Peningkatan")
        lowest = min(st.session_state.scores, key=st.session_state.scores.get)
        if st.session_state.scores[lowest] < 50:
            st.info(f"💡 **Tingkatkan {lowest}:** Latihan lebih giat di bagian {lowest}!")
        else:
            st.success("🌟 Semua kecerdasan sudah terasah dengan baik!")
        
        if st.session_state.history:
            st.markdown("### 📜 Riwayat Kuis (10 Terakhir)")
            history_df = pd.DataFrame(st.session_state.history[-10:])
            history_df = history_df[["timestamp", "type", "question", "correct"]]
            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
            history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil"]
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    # TAB 3: Prestasi
    with tab3:
        st.markdown("### 🏆 Pencapaianmu")
        cols = st.columns(4)
        badges = {"IQ": "🧠 Cendekia", "EQ": "❤️ Empati", "SQ": "🙏 Bhinneka", "AQ": "💪 Tangguh"}
        for i, (t, label) in enumerate(badges.items()):
            if st.session_state.scores[t] >= 50:
                cols[i].success(f"✅ **{label}**")
            else:
                cols[i].info(f"🔒 {label} (butuh 50)")
        
        if all(st.session_state.scores[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ"]):
            st.balloons()
            st.success("🎉 **GELAR: PAHLAWAN CERDAS NUSANTARA!** 🎉")
        
        st.markdown("---")
        answered = len(st.session_state.history)
        correct = sum(1 for h in st.session_state.history if h["correct"])
        accuracy = (correct / answered * 100) if answered > 0 else 0
        col1, col2, col3 = st.columns(3)
        col1.metric("📖 Total Soal", answered)
        col2.metric("✅ Benar", correct)
        col3.metric("📊 Akurasi", f"{accuracy:.1f}%")

if __name__ == "__main__":
    main()
