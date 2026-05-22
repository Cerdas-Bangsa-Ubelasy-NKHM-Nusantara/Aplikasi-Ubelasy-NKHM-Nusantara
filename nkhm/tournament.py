# nkhm/tournament.py
import streamlit as st
import random

# --- Inisialisasi State ---
def init_tournament_state():
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

def create_bracket(players):
    """Membuat bracket turnamen sistem gugur."""
    random.shuffle(players)
    bracket = []
    for i in range(0, len(players), 2):
        if i+1 < len(players):
            bracket.append((players[i], players[i+1]))
        else:
            bracket.append((players[i], "BYE"))
    return bracket

def start_tournament(players):
    """Memulai turnamen dengan daftar peserta."""
    st.session_state.players = players
    st.session_state.bracket = create_bracket(players)
    st.session_state.current_match = 0
    st.session_state.winner = None
    st.session_state.is_active = True

def advance_tournament(winner):
    """Memajukan turnamen berdasarkan pemenang pertandingan."""
    current_match = st.session_state.current_match
    st.session_state.bracket[current_match] = (winner, "WIN") # Tandai pemenang
    st.session_state.current_match += 1

    if st.session_state.current_match >= len(st.session_state.bracket):
        st.session_state.is_active = False
        st.session_state.winner = winner

# --- Komponen UI ---
def show_tournament_setup():
    """Menampilkan UI untuk menyiapkan turnamen."""
    st.subheader("🏆 Siapkan Turnamen Kelas")
    players_input = st.text_area(
        "Masukkan nama peserta (pisahkan dengan koma):",
        placeholder="Ani, Budi, Cici, Dadang",
        key="tournament_players_input"
    )
    if st.button("Mulai Turnamen!"):
        players = [p.strip() for p in players_input.split(",") if p.strip()]
        if len(players) < 2:
            st.error("Minimal 2 peserta.")
        else:
            start_tournament(players)
            st.rerun()

def show_tournament_bracket():
    """Menampilkan bracket dan mengelola jalannya turnamen."""
    st.subheader("🏆 Bracket Turnamen")
    for i, (p1, p2) in enumerate(st.session_state.bracket):
        col1, col2, col3 = st.columns([2,1,2])
        col1.write(p1)
        col3.write(p2)

        if p2 != "WIN" and p1 != "WIN":
            if i == st.session_state.current_match and st.session_state.is_active:
                # Pertandingan sedang berlangsung
                winner = st.radio(
                    f"Pemenang {p1} vs {p2}",
                    [p1, p2] if p2 != "BYE" else [p1],
                    key=f"match_{i}"
                )
                if st.button(f"✅ Konfirmasi Pemenang", key=f"confirm_{i}"):
                    advance_tournament(winner)
                    st.rerun()
        elif p2 == "WIN" or p1 == "WIN":
            col2.markdown("🏆 **WINNER**")

def show_tournament():
    """Fungsi utama untuk ditampilkan di tab Tanding."""
    init_tournament_state()
    if not st.session_state.is_active:
        show_tournament_setup()
    else:
        st.info(f"Peserta: {', '.join(st.session_state.players)}")
        show_tournament_bracket()
        if st.session_state.winner:
            st.success(f"🏆 JUARA: {st.session_state.winner} 🎉")
