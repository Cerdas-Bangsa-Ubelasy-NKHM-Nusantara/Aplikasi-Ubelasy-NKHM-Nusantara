# nkhm/main.py
import streamlit as st
import pandas as pd
import random
import os
from pathlib import Path
from datetime import datetime
from nkhm.questions import load_all_questions
from nkhm.scoring import (
    MAX_SCORE, get_increment, get_column_index, calculate_section_value,
    calculate_nkhm_q, calculate_nkhm_total, get_nkhm_level,
    get_normalized_score,
    MAX_POIN_IQ, MAX_POIN_EQ, MAX_POIN_SQ, MAX_POIN_AQ, MAX_POIN_NASIONALISME
)
from nkhm.ai_assistant import get_ai_response
from nkhm.leaderboard import show_leaderboard, save_score
from nkhm.tutorial import show_tutorial
from nkhm.battle import show_battle
from nkhm.stomata import show_stomata
from nkhm.dasbor import show_dasbor
from nkhm.tebak_pahlawan import show_tebak_pahlawan
from nkhm.angka_rahasia import show_angka_rahasia
from nkhm.seberang_sungai import show_river_game
from nkhm.tiang_bendera import show_tiang_bendera


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

# ========== INISIALISASI SESSION STATE ==========
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
    # State untuk skor tanggapan (EQ dan AQ) dalam poin mentah
    if "eq_scale_total" not in st.session_state:
        st.session_state.eq_scale_total = 0
    if "aq_scale_total" not in st.session_state:
        st.session_state.aq_scale_total = 0
    if "eq_section_answers" not in st.session_state:
        st.session_state.eq_section_answers = {}
    if "aq_section_answers" not in st.session_state:
        st.session_state.aq_section_answers = {}
    if "current_section" not in st.session_state:
        st.session_state.current_section = None
    if "current_scale_type" not in st.session_state:
        st.session_state.current_scale_type = None
    # State untuk multi-jawaban
    if "nkhm_multi_answers" not in st.session_state:
        st.session_state.nkhm_multi_answers = {}
    # State untuk melacak soal yang sudah ditampilkan
    if "nkhm_seen_questions" not in st.session_state:
        st.session_state.nkhm_seen_questions = set()
    # State untuk menyimpan feedback yang akan ditampilkan
    if "nkhm_feedback_display" not in st.session_state:
        st.session_state.nkhm_feedback_display = None
    if "nkhm_feedback_correct" not in st.session_state:
        st.session_state.nkhm_feedback_correct = None
    if "nkhm_feedback_is_multi" not in st.session_state:
        st.session_state.nkhm_feedback_is_multi = False
    # State untuk deteksi perubahan soal
    if "nkhm_last_q_id" not in st.session_state:
        st.session_state.nkhm_last_q_id = ""
    # State untuk menampilkan tombol navigasi
    if "nkhm_show_navigation" not in st.session_state:
        st.session_state.nkhm_show_navigation = False

# ========== FUNGSI UNTUK MENDAPATKAN NILAI PERSENTASE FINAL ==========
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

# ========== FUNGSI BANTU UNTUK MEMILIH SOAL BELUM TERLIHAT ==========
def get_next_question(filtered_questions):
    """Pilih soal secara acak dari filtered_questions yang belum pernah ditampilkan."""
    seen = st.session_state.nkhm_seen_questions
    available = [q for q in filtered_questions if q['text'] not in seen]
    if not available:
        return None
    return random.choice(available)

# ========== RESET STATE KUIS ==========
def reset_quiz_state(keep_feedback=False):
    """Reset semua state kuis untuk soal baru."""
    st.session_state.nkhm_answered = False
    st.session_state.nkhm_multi_answers = {}
    if not keep_feedback:
        st.session_state.nkhm_feedback = None
        st.session_state.nkhm_feedback_display = None
        st.session_state.nkhm_feedback_correct = None
        st.session_state.nkhm_feedback_is_multi = False
        st.session_state.nkhm_show_navigation = False

# ========== MAIN ==========
def main():
    init_session_state()
    
    # Splash screen / login
    if not st.session_state.nkhm_user:
        st.empty()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            logo_url = "https://raw.githubusercontent.com/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara/Aplikasi-Ubelasy-NKHM-Nusantara/refs/heads/main/assets/garuda_2.jpg"
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
            if st.button("🚀 MULAI BELAJAR", width='stretch'):  # <-- PERUBAHAN
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
    with st.expander("🔧 Debug Info (klik untuk lihat)"):
        st.write(f"Total soal: {len(QUESTION_BANK)}")
        type_counts = {}
        for q in QUESTION_BANK:
            t = q.get("type", "TIDAK ADA TYPE")
            type_counts[t] = type_counts.get(t, 0) + 1
        st.write(f"Distribusi type: {type_counts}")
    
    nkhm_q, nkhm_total, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct = get_current_nkhm()
    nkhm_level, _ = get_nkhm_level(nkhm_total)
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.nkhm_user}")
        st.markdown(f"### 🎯 NKHM Total: **{nkhm_total:.2f}**")
        st.markdown(f"### 📊 NKHM_Q: {nkhm_q:.2f}")
        st.markdown(f"*Level: {nkhm_level}*")
        st.progress(min(nkhm_total/100, 1.0))
        st.markdown("### 📊 Skor (0-100)")
        st.progress(iq_pct/100, text=f"IQ: {iq_pct:.1f}")
        st.progress(eq_pct/100, text=f"EQ: {eq_pct:.1f}")
        st.progress(sq_pct/100, text=f"SQ: {sq_pct:.1f}")
        st.progress(aq_pct/100, text=f"AQ: {aq_pct:.1f}")
        st.progress(nas_pct/100, text=f"Nasionalisme: {nas_pct:.1f}")
        
        col1, col2 = st.columns(2)
        col1.metric("📖 Total Soal", st.session_state.nkhm_total_questions)
        best = max([h.get("nkhm_total", 0) for h in st.session_state.nkhm_history] + [nkhm_total])
        col2.metric("🏆 Best NKHM", f"{best:.1f}")
        if st.button("🔄 Reset Skor", width='stretch'):  # <-- PERUBAHAN
            st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
            st.session_state.nkhm_history = []
            st.session_state.nkhm_total_questions = 0
            st.session_state.eq_scale_total = 0
            st.session_state.aq_scale_total = 0
            st.session_state.eq_section_answers = {}
            st.session_state.aq_section_answers = {}
            st.session_state.current_section = None
            st.session_state.current_scale_type = None
            st.session_state.nkhm_seen_questions = set()
            st.session_state.nkhm_last_q_id = ""
            reset_quiz_state()
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
        if st.button("🚪 Keluar / Ganti Pengguna", width='stretch'):  # <-- PERUBAHAN
            for key in list(st.session_state.keys()):
                if key.startswith("nkhm_"):
                    del st.session_state[key]
            st.rerun()
    
    # ========== TAB UTAMA ==========
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🎮 KUIS", "📊 DASHBOARD", "🏆 PRESTASI", "👤 DASBOR SAYA", "⚔️ TANDING", "🎁 KARUNIA", "🎁 HADIAH", "📘 TUTORIAL"
])
        
    # ========== TAB 1: KUIS ==========
    with tab1:
        # ========== GANTI DENGAN VIDEO ==========
        video_path = Path(__file__).parent.parent / "assets" / "kuis.mp4"
        if video_path.exists():
            # Baca file video sebagai bytes
            with open(video_path, "rb") as f:
                video_bytes = f.read()
            st.video(video_bytes, loop=True, autoplay=False)
        
        st.markdown("---")
        
        st.markdown("### Pilih Kuis")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            kategori = st.radio("Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], horizontal=True, key="kategori_filter_kuis")
        with col_f2:
            kecerdasan = st.selectbox("Fokus", ["Semua", "IQ", "EQ", "SQ", "AQ", "Nasionalisme"], key="kecerdasan_filter_kuis")
        
        # Filter soal
        filtered_questions = []
        for q in QUESTION_BANK:
            if kecerdasan == "Nasionalisme":
                if q.get("national", False):
                    filtered_questions.append(q)
                continue
            
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
                fokus_ok = q.get("national", False)
            elif kecerdasan == "EQ":
                fokus_ok = q.get("type") in ["EQ", "EQ_scale"]
            elif kecerdasan == "AQ":
                fokus_ok = q.get("type") in ["AQ", "AQ_scale"]
            else:
                fokus_ok = q.get("type") == kecerdasan
            
            if fokus_ok:
                filtered_questions.append(q)
        
        # Deteksi perubahan filter
        filter_berubah = (st.session_state.nkhm_current_kategori != kategori or 
                          st.session_state.nkhm_current_kecerdasan != kecerdasan)
        if filter_berubah:
            st.session_state.nkhm_current_kategori = kategori
            st.session_state.nkhm_current_kecerdasan = kecerdasan
            st.session_state.nkhm_current_filtered = filtered_questions
            st.session_state.nkhm_answered = False
            st.session_state.nkhm_feedback = None
            st.session_state.current_section = None
            st.session_state.current_scale_type = None
            st.session_state.nkhm_multi_answers = {}
            st.session_state.nkhm_seen_questions = set()
            st.session_state.nkhm_last_q_id = ""
            reset_quiz_state()
            if filtered_questions:
                st.session_state.nkhm_current_q = get_next_question(filtered_questions)
            else:
                st.session_state.nkhm_current_q = None
        else:
            if filtered_questions:
                if st.session_state.nkhm_current_q is None:
                    st.session_state.nkhm_current_q = get_next_question(filtered_questions)
                elif st.session_state.nkhm_current_q['text'] in st.session_state.nkhm_seen_questions:
                    st.session_state.nkhm_current_q = get_next_question(filtered_questions)
            else:
                st.session_state.nkhm_current_q = None
        
        if not filtered_questions:
            st.warning("Tidak ada soal dengan filter ini. Coba pilih filter lain!")
        else:
            if st.session_state.nkhm_current_q is None:
                st.session_state.nkhm_current_q = get_next_question(filtered_questions)
            if st.session_state.nkhm_current_q is None:
                st.info("🎉 Semua soal sudah dijawab! Silakan ganti filter atau reset.")
                st.session_state.nkhm_answered = True
            else:
                q = st.session_state.nkhm_current_q
                
                # ============================================================
                # DETEKSI PERUBAHAN SOAL - HANYA RESET JIKA SOAL BERBEDA
                # ============================================================
                current_q_id = q.get('text', '')
                is_new_question = st.session_state.nkhm_last_q_id != current_q_id
                
                if is_new_question:
                    # Jika soal baru dan kita sudah menjawab sebelumnya, reset answered saja
                    # Tapi JANGAN reset feedback_display karena kita ingin menampilkannya
                    st.session_state.nkhm_answered = False
                    st.session_state.nkhm_multi_answers = {}
                    st.session_state.nkhm_last_q_id = current_q_id
                # ============================================================
                
                # Buat key unik untuk soal ini
                question_key = f"q_{hash(q['text'])}"
                
                # ============================================================
                # TAMPILKAN FEEDBACK DI ATAS SOAL (jika ada)
                # ============================================================
                if st.session_state.nkhm_feedback_display == "benar":
                    st.success(f"✅ BENAR! + poin untuk {st.session_state.last_score_type}")
                    st.balloons()
                elif st.session_state.nkhm_feedback_display == "salah":
                    if st.session_state.nkhm_feedback_is_multi:
                        correct_list = st.session_state.nkhm_feedback_correct
                        st.error(f"❌ SALAH! Jawaban benar: **{', '.join(correct_list)}**")
                    else:
                        correct_answer = st.session_state.nkhm_feedback_correct
                        if correct_answer:
                            st.error(f"❌ SALAH! Jawaban benar: **{correct_answer}**")
                        else:
                            st.error("❌ Jawaban salah.")
                elif st.session_state.nkhm_feedback_display == "scale_answered":
                    st.success(f"✅ Jawaban tercatat für {st.session_state.last_score_type}")
                # ============================================================
                
                # ============================================================
                # TAMPILKAN SOAL
                # ============================================================
                st.markdown(f"### 📝 {q['text']}")
                col_tag1, col_tag2 = st.columns(2)
                display_type = "🇮🇩 Nasionalisme" if q.get('type') == "Nasionalisme" else f"🧠 {q['type']}"
                col_tag1.info(display_type)
                if q.get('national'):
                    col_tag2.success("🇮🇩 Nasional")
                else:
                    col_tag2.info("📚 Umum")
                
                # Tampilkan progress
                seen_count = len(st.session_state.nkhm_seen_questions)
                total_available = len(filtered_questions)
                st.caption(f"📊 Soal dilihat: {seen_count} / {total_available}")
                
                if q.get("type") in ["EQ_scale", "AQ_scale"]:
                    if q.get("section") and q.get("scale"):
                        st.caption(f"📂 **{q['section']}** — *{q['scale']}*")
                    st.info(
                        "📌 **Petunjuk Skor Tanggapan:**\n\n"
                        "Berikan skor tanggapan dalam pilihan Anda (angka 0, 1, 2 atau 3):\n"
                        "- **3** = Setuju sekali\n"
                        "- **2** = Setuju\n"
                        "- **1** = Kurang setuju\n"
                        "- **0** = Tidak setuju sekali"
                    )
                    if st.session_state.current_section:
                        st.info(f"📌 Sedang mengerjakan bagian: **{st.session_state.current_section}**")
                # ============================================================
                
                # ========== DETEKSI MULTI-JAWABAN ==========
                is_multi = False
                correct_list = q.get('correct')
                if isinstance(correct_list, list):
                    is_multi = True
                elif isinstance(correct_list, str) and ',' in correct_list:
                    correct_list = [c.strip() for c in correct_list.split(',')]
                    is_multi = True
                
                # ============================================================
                # RADIO BUTTON / CHECKBOX - Aktif jika belum menjawab
                # ============================================================
                if not st.session_state.nkhm_answered:
                    if is_multi:
                        st.markdown("**Pilih semua jawaban yang benar:**")
                        selected_options = []
                        saved = st.session_state.nkhm_multi_answers.get(q['text'], [])
                        for opt in q['options']:
                            checked = st.checkbox(
                                opt,
                                value=(opt in saved),
                                key=f"multi_{question_key}_{opt}",
                                disabled=False
                            )
                            if checked:
                                selected_options.append(opt)
                        st.session_state.nkhm_multi_answers[q['text']] = selected_options
                        selected = selected_options
                    else:
                        radio_label = "Pilih jawabanmu:" if q.get("type") not in ["EQ_scale", "AQ_scale"] else "Pilih skor tanggapan:"
                        selected = st.radio(
                            radio_label, 
                            q['options'], 
                            key=f"radio_{question_key}", 
                            index=None, 
                            disabled=False
                        )
                else:
                    # Jika sudah menjawab, tampilkan pilihan tetapi disabled
                    if is_multi:
                        st.markdown("**Pilih semua jawaban yang benar:**")
                        saved = st.session_state.nkhm_multi_answers.get(q['text'], [])
                        for opt in q['options']:
                            st.checkbox(
                                opt,
                                value=(opt in saved),
                                key=f"multi_{question_key}_{opt}_disabled",
                                disabled=True
                            )
                        selected = saved
                    else:
                        radio_label = "Pilih jawabanmu:" if q.get("type") not in ["EQ_scale", "AQ_scale"] else "Pilih skor tanggapan:"
                        previous_selection = st.session_state.get(f"radio_{question_key}", None)
                        selected = st.radio(
                            radio_label, 
                            q['options'], 
                            key=f"radio_{question_key}", 
                            index=q['options'].index(previous_selection) if previous_selection in q['options'] else None,
                            disabled=True
                        )
                # ============================================================
                
                # ========== TOMBOL JAWAB ==========
                # Tombol JAWAB hanya muncul jika belum menjawab
                if not st.session_state.nkhm_answered:
                    if is_multi:
                        disable_btn = not selected
                    else:
                        disable_btn = selected is None
                    
                    if seen_count >= total_available:
                        st.info("🎉 Semua soal sudah dijawab! Silakan ganti filter atau reset.")
                        disable_btn = True
                    
                    if st.button("✅ JAWAB", disabled=disable_btn, width='stretch', key=f"jawab_{question_key}"):  # <-- PERUBAHAN
                        # Tandai soal ini sudah dilihat
                        st.session_state.nkhm_seen_questions.add(q['text'])
                        st.session_state.nkhm_answered = True
                        st.session_state.nkhm_total_questions += 1
                        st.session_state.nkhm_show_navigation = True
                        
                        if q.get("type") in ["EQ_scale", "AQ_scale"]:
                            section = q.get("section", "Unknown")
                            q_type = q.get("type")
                            selected_value = int(selected) if not is_multi else 0
                            column_index = get_column_index(selected_value, q['options'])
                            
                            if st.session_state.current_section != section:
                                st.session_state.current_section = section
                                st.session_state.current_scale_type = q_type
                            
                            if q_type == "EQ_scale":
                                if section not in st.session_state.eq_section_answers:
                                    st.session_state.eq_section_answers[section] = [0, 0, 0, 0]
                                st.session_state.eq_section_answers[section][column_index] += 1
                            else:
                                if section not in st.session_state.aq_section_answers:
                                    st.session_state.aq_section_answers[section] = [0, 0, 0, 0]
                                st.session_state.aq_section_answers[section][column_index] += 1
                            
                            # Set feedback untuk ditampilkan
                            st.session_state.nkhm_feedback_display = "scale_answered"
                            st.session_state.nkhm_feedback = "scale_answered"
                            st.session_state.last_score_type = f"{q_type} (skala)"
                            st.session_state.nkhm_history.append({
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "question": q['text'][:50],
                                "type": q_type,
                                "correct": f"Pilihan {selected} (kolom {column_index+1})",
                                "nkhm_total": get_current_nkhm()[1]
                            })
                        else:
                            if q['type'] == "Nasionalisme":
                                score_type = "Nasionalisme"
                            elif q['type'] in ["EQ", "IQ", "SQ", "AQ"]:
                                score_type = q['type']
                            else:
                                score_type = q['type']
                            
                            st.session_state.last_score_type = score_type
                            
                            if is_multi:
                                user_answers = selected
                                total_correct = len(correct_list)
                                user_correct = sum(1 for ans in user_answers if ans in correct_list)
                                raw_increment = 10 * (user_correct / total_correct)
                                increment = round(raw_increment)
                                max_raw_map = {
                                    "IQ": MAX_POIN_IQ,
                                    "EQ": MAX_POIN_EQ,
                                    "SQ": MAX_POIN_SQ,
                                    "AQ": MAX_POIN_AQ,
                                    "Nasionalisme": MAX_POIN_NASIONALISME
                                }
                                max_raw = max_raw_map.get(score_type, 100)
                                new_raw = min(max_raw, st.session_state.nkhm_scores[score_type] + increment)
                                st.session_state.nkhm_scores[score_type] = new_raw
                                
                                # Set feedback untuk ditampilkan
                                if user_correct > 0:
                                    st.session_state.nkhm_feedback_display = "benar"
                                    st.session_state.nkhm_feedback = "benar"
                                else:
                                    st.session_state.nkhm_feedback_display = "salah"
                                    st.session_state.nkhm_feedback = "salah"
                                    st.session_state.nkhm_feedback_correct = correct_list
                                    st.session_state.nkhm_feedback_is_multi = True
                                
                                _, nkhm_total_now, _, _, _, _, _ = get_current_nkhm()
                                st.session_state.nkhm_history.append({
                                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                                    "question": q['text'][:50],
                                    "type": score_type,
                                    "correct": f"{user_correct}/{total_correct} benar",
                                    "nkhm_total": nkhm_total_now
                                })
                            else:
                                if selected == q['correct']:
                                    raw_increment = get_increment(score_type)
                                    max_raw_map = {
                                        "IQ": MAX_POIN_IQ,
                                        "EQ": MAX_POIN_EQ,
                                        "SQ": MAX_POIN_SQ,
                                        "AQ": MAX_POIN_AQ,
                                        "Nasionalisme": MAX_POIN_NASIONALISME
                                    }
                                    max_raw = max_raw_map.get(score_type, 100)
                                    new_raw = min(max_raw, st.session_state.nkhm_scores[score_type] + raw_increment)
                                    st.session_state.nkhm_scores[score_type] = new_raw
                                    
                                    # Set feedback untuk ditampilkan
                                    st.session_state.nkhm_feedback_display = "benar"
                                    st.session_state.nkhm_feedback = "benar"
                                    
                                    _, nkhm_total_baru, _, _, _, _, _ = get_current_nkhm()
                                    save_score(st.session_state.nkhm_user, nkhm_total_baru)
                                else:
                                    # Set feedback untuk ditampilkan
                                    st.session_state.nkhm_feedback_display = "salah"
                                    st.session_state.nkhm_feedback = "salah"
                                    st.session_state.nkhm_feedback_correct = q['correct']
                                    st.session_state.nkhm_feedback_is_multi = False
                                
                                _, nkhm_total_now, _, _, _, _, _ = get_current_nkhm()
                                st.session_state.nkhm_history.append({
                                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                                    "question": q['text'][:50],
                                    "type": score_type,
                                    "correct": selected == q['correct'],
                                    "nkhm_total": nkhm_total_now
                                })
                        
                        # Set last_q_id ke soal ini
                        st.session_state.nkhm_last_q_id = current_q_id
                        st.rerun()
                # ============================================================
                
                # ========== TOMBOL SELESAI BAGIAN (skala) ==========
                if q.get("type") in ["EQ_scale", "AQ_scale"] and st.session_state.current_section and st.session_state.nkhm_answered:
                    if st.button("✅ Selesai Bagian Ini", width='stretch', key=f"selesai_{question_key}"):  # <-- PERUBAHAN
                        section = st.session_state.current_section
                        q_type = st.session_state.current_scale_type
                        
                        if q_type == "EQ_scale":
                            section_answers = st.session_state.eq_section_answers.get(section, [0,0,0,0])
                            section_value = calculate_section_value(section_answers)
                            new_total = min(MAX_POIN_EQ, st.session_state.eq_scale_total + section_value)
                            st.session_state.eq_scale_total = new_total
                            del st.session_state.eq_section_answers[section]
                            st.success(f"✅ Bagian '{section}' selesai! +{section_value} poin. Total EQ Skor Tanggapan: {st.session_state.eq_scale_total}")
                        else:
                            section_answers = st.session_state.aq_section_answers.get(section, [0,0,0,0])
                            section_value = calculate_section_value(section_answers)
                            new_total = min(MAX_POIN_AQ, st.session_state.aq_scale_total + section_value)
                            st.session_state.aq_scale_total = new_total
                            del st.session_state.aq_section_answers[section]
                            st.success(f"✅ Bagian '{section}' selesai! +{section_value} poin. Total AQ Skor Tanggapan: {st.session_state.aq_scale_total}")
                        
                        st.session_state.current_section = None
                        st.session_state.current_scale_type = None
                        reset_quiz_state()
                        if filtered_questions:
                            st.session_state.nkhm_current_q = get_next_question(filtered_questions)
                            st.session_state.nkhm_last_q_id = st.session_state.nkhm_current_q.get('text', '') if st.session_state.nkhm_current_q else ""
                            st.rerun()
                
                # ========== TOMBOL NAVIGASI ==========
                # Tampilkan tombol navigasi jika sudah menjawab
                if st.session_state.nkhm_answered and q.get("type") not in ["EQ_scale", "AQ_scale"]:
                    st.markdown("---")
                    st.markdown("### 📌 Navigasi")
                    col_nav1, col_nav2 = st.columns(2)
                    with col_nav1:
                        if st.button("⏩ SOAL BERIKUTNYA", width='stretch', key=f"next_{question_key}"):  # <-- PERUBAHAN
                            if filtered_questions:
                                next_q = get_next_question(filtered_questions)
                                if next_q is None:
                                    st.info("🎉 Semua soal sudah dijawab! Silakan ganti filter.")
                                    st.session_state.nkhm_answered = True
                                else:
                                    # Reset state dan pindah ke soal berikutnya
                                    # TAPI tetap pertahankan feedback yang sudah ada
                                    st.session_state.nkhm_current_q = next_q
                                    st.session_state.nkhm_answered = False
                                    st.session_state.nkhm_last_q_id = next_q.get('text', '')
                                    # Jangan reset feedback_display agar tetap tampil
                                    st.rerun()
                    with col_nav2:
                        if st.button("🔄 KUIS BARU", width='stretch', key=f"reset_{question_key}"):  # <-- PERUBAHAN
                            if filtered_questions:
                                # Reset semua, mulai dari awal
                                st.session_state.nkhm_seen_questions = set()
                                next_q = get_next_question(filtered_questions)
                                if next_q is None:
                                    st.info("🎉 Semua soal sudah dijawab! Silakan ganti filter.")
                                    st.session_state.nkhm_answered = True
                                else:
                                    reset_quiz_state()  # Reset semua termasuk feedback
                                    st.session_state.nkhm_current_q = next_q
                                    st.session_state.nkhm_last_q_id = next_q.get('text', '')
                                    st.rerun()
    
    # ========== TAB 2: DASHBOARD ==========
    with tab2:
        st.markdown("### Dashboard NKHM")
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
            st.dataframe(history_df, width='stretch', hide_index=True)  # <-- PERUBAHAN
    
    # ========== TAB 3: PRESTASI ==========
    with tab3:
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
    with tab4:
        show_dasbor()
    
    # ========== TAB 5: TANDING ==========
    with tab5:
        img_path = Path(__file__).parent.parent / "assets" / "garuda.jpg"
        if img_path.exists():
            st.image(str(img_path), caption="Bertanding Untuk Menang 🇮🇩", width='stretch')  # <-- PERUBAHAN
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

    # ========== TAB 6: KARUNIA & STOMATA =========
    with tab6:
        sub_tab1, sub_tab2 = st.tabs(["🎁 Karunia Motivasi", "💖 Sto-mata Hati"])
        with sub_tab1:
            img_path = Path(__file__).parent.parent / "assets" / "karunia.jpg"
            if img_path.exists():
                st.image(str(img_path), caption="Grow in Grace 🇮🇩", width='stretch')  # <-- PERUBAHAN
            else:
                st.info("💡 Gambar 'karunia.jpg' belum tersedia.")
            st.markdown("---")
            subsub_tab1, subsub_tab2, subsub_tab3, subsub_tab4 = st.tabs(["📜 Karunia Umum", "✨ Karunia 140 Karakter", "📋 Karakter & Masalah", "📚 Pengembangan Diri"])
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
    with tab7:
        img_path = Path(__file__).parent.parent / "assets" / "hadiah.gif"
        if img_path.exists():
            st.image(str(img_path), caption="A Giveaway 🇮🇩", width='stretch')  # <-- PERUBAHAN
        else:
            st.info("💡 Gambar 'hadiah.gif' belum tersedia.")
        st.markdown("---")
        sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs(["🦅 Tebak Pahlawan", "🔢 Angka Rahasia", "🚣 Pahlawan Menyeberang Sungai", "🇮🇩 Tiang Bendera", "🎲 Lainnya (Coming Soon)"])
        with sub_tab1:
            from nkhm.tebak_pahlawan import show_tebak_pahlawan
            show_tebak_pahlawan()
        with sub_tab2:
            show_angka_rahasia()
        with sub_tab3:
            from nkhm.seberang_sungai import show_river_game
            show_river_game()
        with sub_tab4:
            from nkhm.tiang_bendera import show_tiang_bendera
            show_tiang_bendera()
        with sub_tab5:
            st.info("🎁 Fitur hadiah lainnya akan segera hadir. Dapatkan koin atau reward dengan menjawab kuis!")
    
    # ========== TAB 8: TUTORIAL ==========
    with tab8:
        show_tutorial()

if __name__ == "__main__":
    main()