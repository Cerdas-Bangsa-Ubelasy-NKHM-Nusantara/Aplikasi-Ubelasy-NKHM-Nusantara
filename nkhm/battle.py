# nkhm/battle.py, untuk Hot Seat (tanpa undangan antar perangkat)
import streamlit as st
import random
import time
from nkhm.questions import load_all_questions

def init_battle_state():
    if "battle_active" not in st.session_state:
        st.session_state.battle_active = False
    if "battle_players" not in st.session_state:
        st.session_state.battle_players = ["", ""]
    if "battle_current_player" not in st.session_state:
        st.session_state.battle_current_player = 0
    if "battle_questions" not in st.session_state:
        st.session_state.battle_questions = []
    if "battle_current_q_index" not in st.session_state:
        st.session_state.battle_current_q_index = 0
    if "battle_scores" not in st.session_state:
        st.session_state.battle_scores = [0, 0]
    if "battle_time_left" not in st.session_state:
        st.session_state.battle_time_left = 30
    if "battle_timer_running" not in st.session_state:
        st.session_state.battle_timer_running = False
    if "battle_last_update" not in st.session_state:
        st.session_state.battle_last_update = time.time()
    if "battle_total_time" not in st.session_state:
        st.session_state.battle_total_time = 30
    if "battle_finished" not in st.session_state:
        st.session_state.battle_finished = False
    if "battle_answers" not in st.session_state:
        st.session_state.battle_answers = []

def reset_battle():
    st.session_state.battle_active = False
    st.session_state.battle_players = ["", ""]
    st.session_state.battle_current_player = 0
    st.session_state.battle_questions = []
    st.session_state.battle_current_q_index = 0
    st.session_state.battle_scores = [0, 0]
    st.session_state.battle_time_left = 30
    st.session_state.battle_timer_running = False
    st.session_state.battle_total_time = 30
    st.session_state.battle_finished = False
    st.session_state.battle_answers = []

def update_timer():
    if st.session_state.battle_timer_running and not st.session_state.battle_finished:
        current_time = time.time()
        elapsed = current_time - st.session_state.battle_last_update
        if elapsed >= 1:
            st.session_state.battle_time_left -= int(elapsed)
            st.session_state.battle_last_update = current_time
            if st.session_state.battle_time_left <= 0:
                st.session_state.battle_time_left = 0
                st.session_state.battle_timer_running = False
                st.session_state.battle_finished = True
                st.rerun()

def show_battle():
    init_battle_state()
    
    st.markdown("## ⚔️ Mode Tanding (Hot Seat)")
    st.markdown("Dua pemain bergantian menjawab soal menggunakan **perangkat yang sama**.")
    st.markdown("---")
    
    # ========== BELUM MULAI ==========
    if not st.session_state.battle_active and not st.session_state.battle_finished:
        st.subheader("🏁 Atur Pertandingan")
        
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.text_input("👤 Nama Pemain 1", value=st.session_state.battle_players[0], placeholder="Contoh: Budi")
        with col2:
            player2 = st.text_input("👤 Nama Pemain 2", value=st.session_state.battle_players[1], placeholder="Contoh: Ani")
        
        col3, col4 = st.columns(2)
        with col3:
            num_questions = st.selectbox("📊 Jumlah Soal", [3, 5, 7, 10], index=1)
        with col4:
            time_limit = st.selectbox("⏱️ Waktu per Giliran", [15, 30, 45, 60], index=1)
        
        st.markdown("---")
        st.markdown("### 🎯 Filter Soal (opsional)")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            kategori_filter = st.selectbox("Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"])
        with col_f2:
            fokus_filter = st.selectbox("Fokus", ["Semua", "IQ", "EQ", "SQ", "AQ", "Nasionalisme"])
        
        if st.button("🚀 MULAI PERTANDINGAN", use_container_width=True):
            if not player1 or not player2:
                st.error("Masukkan nama kedua pemain!")
                return
            
            # Load bank soal
            QUESTION_BANK = load_all_questions()
            if not QUESTION_BANK:
                st.error("Bank soal kosong.")
                return
            
            # Filter soal
            filtered = []
            for q in QUESTION_BANK:
                if fokus_filter == "Nasionalisme":
                    if q.get("national", False):
                        filtered.append(q)
                    continue
                
                if kategori_filter == "✨ Semua":
                    kategori_ok = True
                elif kategori_filter == "🇮🇩 Nasionalisme":
                    kategori_ok = q.get("national", False)
                else:
                    kategori_ok = not q.get("national", False)
                if not kategori_ok:
                    continue
                
                if fokus_filter == "Semua":
                    fokus_ok = True
                elif fokus_filter == "Nasionalisme":
                    fokus_ok = q.get("national", False)
                elif fokus_filter == "EQ":
                    fokus_ok = q.get("type") in ["EQ", "EQ_scale"]
                elif fokus_filter == "AQ":
                    fokus_ok = q.get("type") in ["AQ", "AQ_scale"]
                else:
                    fokus_ok = q.get("type") == fokus_filter
                
                if fokus_ok:
                    filtered.append(q)
            
            if len(filtered) < num_questions:
                st.error(f"Soal hanya {len(filtered)}. Kurangi jumlah soal atau ubah filter.")
                return
            
            # Pilih soal acak
            selected_questions = random.sample(filtered, num_questions)
            
            # Inisialisasi battle
            st.session_state.battle_players = [player1, player2]
            st.session_state.battle_questions = selected_questions
            st.session_state.battle_scores = [0, 0]
            st.session_state.battle_current_player = 0
            st.session_state.battle_current_q_index = 0
            st.session_state.battle_time_left = time_limit
            st.session_state.battle_total_time = time_limit
            st.session_state.battle_timer_running = True
            st.session_state.battle_last_update = time.time()
            st.session_state.battle_active = True
            st.session_state.battle_finished = False
            st.session_state.battle_answers = []
            st.rerun()
    
    # ========== PERTANDINGAN BERLANGSUNG ==========
    elif st.session_state.battle_active and not st.session_state.battle_finished:
        update_timer()
        
        # Tampilkan status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"👤 {st.session_state.battle_players[0]}", f"{st.session_state.battle_scores[0]} poin")
        with col2:
            current_player = st.session_state.battle_players[st.session_state.battle_current_player]
            st.metric("🎯 Giliran", current_player)
        with col3:
            progress = f"{st.session_state.battle_current_q_index + 1} / {len(st.session_state.battle_questions)}"
            st.metric("📊 Soal", progress)
        
        # Timer
        timer_progress = st.session_state.battle_time_left / st.session_state.battle_total_time
        st.progress(timer_progress, text=f"⏱️ Sisa waktu: {st.session_state.battle_time_left} detik")
        
        if st.session_state.battle_time_left <= 0:
            st.error(f"⏰ Waktu habis! {current_player} kehilangan giliran.")
            # Pindah giliran ke lawan
            st.session_state.battle_current_player = 1 - st.session_state.battle_current_player
            st.session_state.battle_time_left = st.session_state.battle_total_time
            st.session_state.battle_last_update = time.time()
            st.session_state.battle_timer_running = True
            st.rerun()
        
        # Tampilkan soal
        current_q = st.session_state.battle_questions[st.session_state.battle_current_q_index]
        
        st.markdown(f"### 📝 {current_q['text']}")
        display_type = "🇮🇩 Nasionalisme" if current_q.get('type') == "Nasionalisme" else f"🧠 {current_q.get('type', 'Unknown')}"
        st.info(display_type)
        
        selected = st.radio("Pilih jawabanmu:", current_q['options'], key=f"battle_ans", index=None)
        
        if st.button("✅ JAWAB", use_container_width=True):
            if selected is None:
                st.warning("Pilih jawaban terlebih dahulu!")
            else:
                # Hitung poin
                points = 0
                if current_q.get("type") in ["EQ_scale", "AQ_scale"]:
                    points = int(selected)
                else:
                    if selected == current_q.get('correct'):
                        q_type = current_q.get('type')
                        if q_type == "Nasionalisme":
                            points = 5
                        elif q_type == "IQ":
                            points = 10
                        elif q_type == "EQ":
                            points = 10
                        elif q_type == "SQ":
                            points = 5
                        elif q_type == "AQ":
                            points = 5
                        else:
                            points = 10
                
                # Simpan jawaban
                st.session_state.battle_answers.append({
                    "player": st.session_state.battle_current_player,
                    "question": current_q['text'][:50],
                    "answer": selected,
                    "correct": selected == current_q.get('correct') if current_q.get('type') not in ["EQ_scale", "AQ_scale"] else True,
                    "points": points
                })
                
                # Tambah skor
                st.session_state.battle_scores[st.session_state.battle_current_player] += points
                
                # Cek apakah pertandingan selesai
                if st.session_state.battle_current_q_index + 1 >= len(st.session_state.battle_questions):
                    st.session_state.battle_active = False
                    st.session_state.battle_finished = True
                else:
                    st.session_state.battle_current_q_index += 1
                    st.session_state.battle_current_player = 1 - st.session_state.battle_current_player
                    st.session_state.battle_time_left = st.session_state.battle_total_time
                    st.session_state.battle_last_update = time.time()
                    st.session_state.battle_timer_running = True
                st.rerun()
    
    # ========== PERTANDINGAN SELESAI ==========
    elif st.session_state.battle_finished:
        st.balloons()
        st.markdown("## 🏆 HASIL PERTANDINGAN 🏆")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"👤 {st.session_state.battle_players[0]}", f"{st.session_state.battle_scores[0]} poin")
        with col2:
            st.metric(f"👤 {st.session_state.battle_players[1]}", f"{st.session_state.battle_scores[1]} poin")
        
        if st.session_state.battle_scores[0] > st.session_state.battle_scores[1]:
            st.success(f"🎉 PEMENANG: **{st.session_state.battle_players[0]}**! 🎉")
        elif st.session_state.battle_scores[1] > st.session_state.battle_scores[0]:
            st.success(f"🎉 PEMENANG: **{st.session_state.battle_players[1]}**! 🎉")
        else:
            st.success("🎉 HASIL SERI! Kedua pemain sama kuat! 🎉")
        
        with st.expander("📋 Riwayat Jawaban"):
            for i, ans in enumerate(st.session_state.battle_answers):
                player_name = st.session_state.battle_players[ans['player']]
                status = "✅" if ans['correct'] else "❌"
                st.write(f"{i+1}. {status} **{player_name}**: {ans['question']} → {ans['answer']} (+{ans['points']} poin)")
        
        if st.button("🔄 PERTANDINGAN BARU", use_container_width=True):
            reset_battle()
            st.rerun()
