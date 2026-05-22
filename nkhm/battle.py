# nkhm/battle.py
import streamlit as st
import random
import time
from datetime import datetime
from nkhm.questions import load_all_questions
from nkhm.scoring import get_increment, MAX_POIN_IQ, MAX_POIN_EQ, MAX_POIN_SQ, MAX_POIN_AQ, MAX_POIN_NASIONALISME, get_normalized_score

# ========== INISIALISASI SESSION STATE ==========
def init_battle_state():
    if "battle_active" not in st.session_state:
        st.session_state.battle_active = False
    if "battle_players" not in st.session_state:
        st.session_state.battle_players = []
    if "battle_current_player" not in st.session_state:
        st.session_state.battle_current_player = 0
    if "battle_questions" not in st.session_state:
        st.session_state.battle_questions = []
    if "battle_current_q_index" not in st.session_state:
        st.session_state.battle_current_q_index = 0
    if "battle_scores" not in st.session_state:
        st.session_state.battle_scores = []
    if "battle_time_left" not in st.session_state:
        st.session_state.battle_time_left = 30
    if "battle_timer_running" not in st.session_state:
        st.session_state.battle_timer_running = False
    if "battle_last_update" not in st.session_state:
        st.session_state.battle_last_update = time.time()
    if "battle_answers" not in st.session_state:
        st.session_state.battle_answers = []  # menyimpan jawaban per soal
    if "battle_game_over" not in st.session_state:
        st.session_state.battle_game_over = False
    if "battle_winner" not in st.session_state:
        st.session_state.battle_winner = None
    if "battle_finished" not in st.session_state:
        st.session_state.battle_finished = False

def reset_battle():
    """Reset semua state battle"""
    st.session_state.battle_active = False
    st.session_state.battle_players = []
    st.session_state.battle_current_player = 0
    st.session_state.battle_questions = []
    st.session_state.battle_current_q_index = 0
    st.session_state.battle_scores = []
    st.session_state.battle_time_left = 30
    st.session_state.battle_timer_running = False
    st.session_state.battle_answers = []
    st.session_state.battle_game_over = False
    st.session_state.battle_winner = None
    st.session_state.battle_finished = False

def update_timer():
    """Update timer berdasarkan waktu yang berlalu"""
    if st.session_state.battle_timer_running and not st.session_state.battle_game_over:
        current_time = time.time()
        elapsed = current_time - st.session_state.battle_last_update
        if elapsed >= 1:
            st.session_state.battle_time_left -= int(elapsed)
            st.session_state.battle_last_update = current_time
            if st.session_state.battle_time_left <= 0:
                st.session_state.battle_time_left = 0
                st.session_state.battle_timer_running = False
                st.session_state.battle_game_over = True
                st.session_state.battle_winner = st.session_state.battle_players[1 - st.session_state.battle_current_player]
                st.rerun()

def calculate_battle_score(raw_points, max_points):
    """Konversi raw points ke skor 0-100 untuk battle"""
    if max_points == 0:
        return 0
    return min(100, (raw_points / max_points) * 100)

def show_battle():
    """Tampilan utama fitur Tanding"""
    init_battle_state()
    
    st.markdown("## ⚔️ Mode Tanding")
    st.markdown("Adu cepat dan tepat melawan lawan! Bergantian menjawab soal dengan timer.")
    st.markdown("---")
    
    # Jika battle belum dimulai, tampilkan form setup
    if not st.session_state.battle_active and not st.session_state.battle_finished:
        st.subheader("🏁 Atur Pertandingan")
        
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.text_input("👤 Nama Pemain 1", placeholder="Contoh: Budi", key="player1")
        with col2:
            player2 = st.text_input("👤 Nama Pemain 2", placeholder="Contoh: Ani", key="player2")
        
        col3, col4 = st.columns(2)
        with col3:
            num_questions = st.selectbox("📊 Jumlah Soal", [3, 5, 7, 10], index=1, key="num_q")
        with col4:
            time_limit = st.selectbox("⏱️ Batas Waktu per Giliran (detik)", [15, 30, 45, 60], index=1, key="time_limit")
        
        # Filter soal opsional
        st.markdown("---")
        st.markdown("### 🎯 Filter Soal (opsional)")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            kategori_filter = st.selectbox("Kategori", ["✨ Semua", "🇮🇩 Nasionalisme", "📚 Umum"], key="battle_kategori")
        with col_f2:
            fokus_filter = st.selectbox("Fokus", ["Semua", "IQ", "EQ", "SQ", "AQ", "Nasionalisme"], key="battle_fokus")
        
        if st.button("🚀 MULAI PERTANDINGAN", use_container_width=True):
            if not player1 or not player2:
                st.error("Masukkan nama kedua pemain!")
                return
            
            # Load bank soal
            QUESTION_BANK = load_all_questions()
            if not QUESTION_BANK:
                st.error("Bank soal kosong. Tidak bisa memulai pertandingan.")
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
                st.error(f"Soal dengan filter ini hanya {len(filtered)} buah. Kurangi jumlah soal atau ubah filter.")
                return
            
            # Pilih soal secara acak
            selected_questions = random.sample(filtered, num_questions)
            
            # Inisialisasi battle
            st.session_state.battle_players = [player1, player2]
            st.session_state.battle_questions = selected_questions
            st.session_state.battle_scores = [0, 0]
            st.session_state.battle_current_player = 0
            st.session_state.battle_current_q_index = 0
            st.session_state.battle_time_left = time_limit
            st.session_state.battle_timer_running = True
            st.session_state.battle_last_update = time.time()
            st.session_state.battle_answers = []
            st.session_state.battle_active = True
            st.session_state.battle_game_over = False
            st.session_state.battle_winner = None
            st.session_state.battle_finished = False
            st.rerun()
    
    # Jika battle sedang berlangsung
    elif st.session_state.battle_active and not st.session_state.battle_finished:
        # Update timer
        update_timer()
        
        # Tampilkan status pertandingan
        col_status1, col_status2, col_status3 = st.columns(3)
        with col_status1:
            st.metric(f"👤 {st.session_state.battle_players[0]}", f"{st.session_state.battle_scores[0]} poin")
        with col_status2:
            current_player_name = st.session_state.battle_players[st.session_state.battle_current_player]
            st.metric("🎯 Giliran", current_player_name)
        with col_status3:
            progress = f"{st.session_state.battle_current_q_index + 1} / {len(st.session_state.battle_questions)}"
            st.metric("📊 Soal", progress)
        
        # Timer progress bar
        time_limit = st.session_state.battle_time_left
        total_time = 30  # default, tapi sebaiknya simpan di session state
        # Ambil total waktu dari pengaturan (perlu disimpan)
        if "battle_total_time" not in st.session_state:
            st.session_state.battle_total_time = 30
        timer_progress = st.session_state.battle_time_left / st.session_state.battle_total_time
        st.progress(timer_progress, text=f"⏱️ Sisa waktu: {st.session_state.battle_time_left} detik")
        
        # Jika waktu habis
        if st.session_state.battle_time_left <= 0 and not st.session_state.battle_game_over:
            st.error(f"⏰ Waktu habis! {current_player_name} kehilangan giliran.")
            # Pindah giliran ke lawan
            st.session_state.battle_current_player = 1 - st.session_state.battle_current_player
            st.session_state.battle_time_left = st.session_state.battle_total_time
            st.session_state.battle_last_update = time.time()
            st.session_state.battle_timer_running = True
            st.rerun()
        
        # Tampilkan soal saat ini
        current_q = st.session_state.battle_questions[st.session_state.battle_current_q_index]
        
        st.markdown(f"### 📝 {current_q['text']}")
        
        # Tampilkan tipe soal
        display_type = "🇮🇩 Nasionalisme" if current_q.get('type') == "Nasionalisme" else f"🧠 {current_q.get('type', 'Unknown')}"
        st.info(f"{display_type}")
        
        # Pilihan jawaban
        selected = st.radio(
            "Pilih jawabanmu:",
            current_q['options'],
            key=f"battle_ans_{st.session_state.battle_current_q_index}",
            index=None
        )
        
        # Tombol Jawab
        if st.button("✅ JAWAB", use_container_width=True):
            if selected is None:
                st.warning("Pilih jawaban terlebih dahulu!")
            else:
                # Hitung poin
                points_earned = 0
                if current_q.get("type") in ["EQ_scale", "AQ_scale"]:
                    # Untuk skor tanggapan, nilai langsung dari pilihan
                    points_earned = int(selected)
                else:
                    # Untuk pilihan ganda
                    if selected == current_q.get('correct'):
                        # Dapatkan increment berdasarkan tipe
                        q_type = current_q.get('type')
                        if q_type == "Nasionalisme":
                            increment = 200 / (2 * 20)  # 5
                        elif q_type == "IQ":
                            increment = 320 / 32  # 10
                        elif q_type == "EQ":
                            increment = 380 / 38  # 10
                        elif q_type == "SQ":
                            increment = 140 / (2 * 14)  # 5
                        elif q_type == "AQ":
                            increment = 140 / (2 * 14)  # 5
                        else:
                            increment = 10
                        points_earned = increment
                
                # Tambahkan skor
                st.session_state.battle_scores[st.session_state.battle_current_player] += points_earned
                
                # Simpan jawaban
                st.session_state.battle_answers.append({
                    "player": st.session_state.battle_current_player,
                    "question": current_q['text'][:50],
                    "answer": selected,
                    "correct": selected == current_q.get('correct') if current_q.get('type') not in ["EQ_scale", "AQ_scale"] else True,
                    "points": points_earned
                })
                
                # Pindah ke soal berikutnya atau ganti pemain
                if st.session_state.battle_current_q_index + 1 >= len(st.session_state.battle_questions):
                    # Pertandingan selesai
                    st.session_state.battle_active = False
                    st.session_state.battle_finished = True
                    if st.session_state.battle_scores[0] > st.session_state.battle_scores[1]:
                        st.session_state.battle_winner = st.session_state.battle_players[0]
                    elif st.session_state.battle_scores[1] > st.session_state.battle_scores[0]:
                        st.session_state.battle_winner = st.session_state.battle_players[1]
                    else:
                        st.session_state.battle_winner = "SERI"
                else:
                    # Pindah ke soal berikutnya, ganti giliran pemain
                    st.session_state.battle_current_q_index += 1
                    st.session_state.battle_current_player = 1 - st.session_state.battle_current_player
                    st.session_state.battle_time_left = st.session_state.battle_total_time
                    st.session_state.battle_last_update = time.time()
                    st.session_state.battle_timer_running = True
                st.rerun()
    
    # Jika battle selesai, tampilkan hasil
    elif st.session_state.battle_finished:
        st.balloons()
        st.markdown("## 🏆 HASIL PERTANDINGAN 🏆")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"👤 {st.session_state.battle_players[0]}", f"{st.session_state.battle_scores[0]} poin")
        with col2:
            st.metric(f"👤 {st.session_state.battle_players[1]}", f"{st.session_state.battle_scores[1]} poin")
        
        if st.session_state.battle_winner == "SERI":
            st.success("🎉 HASIL SERI! Kedua pemain sama kuat! 🎉")
        else:
            st.success(f"🎉 PEMENANG: **{st.session_state.battle_winner}**! 🎉")
        
        # Tampilkan riwayat jawaban
        with st.expander("📋 Riwayat Jawaban"):
            for i, ans in enumerate(st.session_state.battle_answers):
                player_name = st.session_state.battle_players[ans['player']]
                status = "✅" if ans['correct'] else "❌"
                st.write(f"{i+1}. {status} **{player_name}**: {ans['question']} → {ans['answer']} (+{ans['points']} poin)")
        
        if st.button("🔄 PERTANDINGAN BARU", use_container_width=True):
            reset_battle()
            st.rerun()
