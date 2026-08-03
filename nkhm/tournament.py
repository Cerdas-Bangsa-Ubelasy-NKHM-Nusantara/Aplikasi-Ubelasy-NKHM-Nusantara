# nkhm/tournament.py
import streamlit as st
import random
import logging

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di tournament: {e}")

# ========== INISIALISASI STATE ==========
def init_tournament_state():
    try:
        defaults = {
            "players": [],               # Daftar nama peserta
            "bracket": [],              # Struktur bracket (list of tuples)
            "current_match": None,      # Pertandingan yang sedang berlangsung
            "winner": None,             # Pemenang turnamen
            "is_active": False,         # Status turnamen
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    except Exception as e:
        logging.error(f"Error init_tournament_state: {e}")

def create_bracket(players):
    """Membuat bracket turnamen sistem gugur."""
    try:
        shuffled = players.copy()
        random.shuffle(shuffled)
        bracket = []
        for i in range(0, len(shuffled), 2):
            if i+1 < len(shuffled):
                bracket.append((shuffled[i], shuffled[i+1]))
            else:
                bracket.append((shuffled[i], "BYE"))
        return bracket
    except Exception as e:
        logging.error(f"Error create_bracket: {e}")
        return []

def start_tournament(players):
    """Memulai turnamen dengan daftar peserta."""
    try:
        st.session_state.players = players
        st.session_state.bracket = create_bracket(players)
        st.session_state.current_match = 0
        st.session_state.winner = None
        st.session_state.is_active = True
        logging.info(f"Turnamen dimulai dengan {len(players)} peserta")
    except Exception as e:
        logging.error(f"Error start_tournament: {e}")
        st.error(f"Error memulai turnamen: {e}")

def advance_tournament(winner):
    """Memajukan turnamen berdasarkan pemenang pertandingan."""
    try:
        current_match = st.session_state.current_match
        st.session_state.bracket[current_match] = (winner, "WIN")  # Tandai pemenang
        st.session_state.current_match += 1

        if st.session_state.current_match >= len(st.session_state.bracket):
            st.session_state.is_active = False
            st.session_state.winner = winner
            logging.info(f"Turnamen selesai! Pemenang: {winner}")
    except Exception as e:
        logging.error(f"Error advance_tournament: {e}")
        st.error(f"Error memajukan turnamen: {e}")

def reset_tournament():
    """Reset semua state turnamen."""
    try:
        st.session_state.players = []
        st.session_state.bracket = []
        st.session_state.current_match = None
        st.session_state.winner = None
        st.session_state.is_active = False
        logging.info("Turnamen direset")
    except Exception as e:
        logging.error(f"Error reset_tournament: {e}")

# ========== KOMPONEN UI ==========
def show_tournament_setup():
    """Menampilkan UI untuk menyiapkan turnamen."""
    try:
        st.subheader("🏆 Siapkan Turnamen Kelas")
        
        # Gunakan form untuk setup
        with st.form(key="tournament_setup_form"):
            players_input = st.text_area(
                "Masukkan nama peserta (pisahkan dengan koma):",
                placeholder="Ani, Budi, Cici, Dadang",
                key="tournament_players_input"
            )
            start_btn = st.form_submit_button("Mulai Turnamen!", use_container_width=True)
            
            if start_btn:
                try:
                    players = [p.strip() for p in players_input.split(",") if p.strip()]
                    if len(players) < 2:
                        st.error("Minimal 2 peserta.")
                    else:
                        start_tournament(players)
                        safe_rerun()
                except Exception as e:
                    logging.error(f"Error starting tournament: {e}")
                    st.error(f"Error memulai turnamen: {e}")
    except Exception as e:
        logging.error(f"Error show_tournament_setup: {e}")
        st.error(f"Error: {e}")

def show_tournament_bracket():
    """Menampilkan bracket dan mengelola jalannya turnamen."""
    try:
        st.subheader("🏆 Bracket Turnamen")
        
        if not st.session_state.bracket:
            st.info("Belum ada bracket. Silakan mulai turnamen.")
            return
        
        for i, (p1, p2) in enumerate(st.session_state.bracket):
            col1, col2, col3 = st.columns([2, 1, 2])
            col1.write(p1)
            col3.write(p2)

            if p2 != "WIN" and p1 != "WIN":
                if i == st.session_state.current_match and st.session_state.is_active:
                    # Pertandingan sedang berlangsung - gunakan form
                    with st.form(key=f"match_form_{i}"):
                        # Tentukan pilihan yang tersedia
                        options = [p1]
                        if p2 != "BYE":
                            options.append(p2)
                        
                        winner = st.radio(
                            f"Pemenang {p1} vs {p2}",
                            options,
                            key=f"match_{i}"
                        )
                        confirm_btn = st.form_submit_button(f"✅ Konfirmasi Pemenang", use_container_width=True)
                        
                        if confirm_btn:
                            try:
                                advance_tournament(winner)
                                safe_rerun()
                            except Exception as e:
                                logging.error(f"Error confirming winner: {e}")
                                st.error(f"Error konfirmasi pemenang: {e}")
            elif p2 == "WIN" or p1 == "WIN":
                col2.markdown("🏆 **WINNER**")
    except Exception as e:
        logging.error(f"Error show_tournament_bracket: {e}")
        st.error(f"Error menampilkan bracket: {e}")

def show_tournament():
    """Fungsi utama untuk ditampilkan di tab Tanding."""
    try:
        init_tournament_state()
        
        if not st.session_state.is_active:
            show_tournament_setup()
            
            # Tampilkan tombol reset jika ada data turnamen sebelumnya
            if st.session_state.players and not st.session_state.is_active:
                if st.button("🔄 Reset Turnamen", use_container_width=True, key="reset_tournament_btn"):
                    reset_tournament()
                    safe_rerun()
        else:
            st.info(f"Peserta: {', '.join(st.session_state.players)}")
            show_tournament_bracket()
            
            if st.session_state.winner:
                st.balloons()
                st.success(f"🏆 JUARA: {st.session_state.winner} 🎉")
                st.markdown(f"""
                ### 📊 Hasil Akhir
                - **Juara 1:** 🥇 {st.session_state.winner}
                - **Total Peserta:** {len(st.session_state.players)}
                - **Jumlah Pertandingan:** {len(st.session_state.bracket)}
                """)
                
                if st.button("🔄 Turnamen Baru", use_container_width=True, key="new_tournament_btn"):
                    reset_tournament()
                    safe_rerun()
            else:
                # Tampilkan progress
                total_matches = len(st.session_state.bracket)
                current = st.session_state.current_match
                if total_matches > 0:
                    st.progress(current / total_matches, text=f"Progress: {current}/{total_matches} pertandingan")
                
                # Tombol reset selama turnamen berlangsung
                if st.button("❌ Batalkan Turnamen", use_container_width=True, key="cancel_tournament_btn"):
                    reset_tournament()
                    safe_rerun()
    
    except Exception as e:
        logging.error(f"Error di show_tournament: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Mode Turnamen: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_tournament()