# nkhm/gamifikasi.py
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

# ========== DATA MISI ==========
MISSIONS = [
    {
        "id": "jawab_5",
        "nama": "📝 Jawab 5 Soal",
        "deskripsi": "Jawab 5 soal kuis (IQ, EQ, SQ, AQ, atau Nasionalisme)",
        "target": 5,
        "reward": 5,
        "type": "total_questions"
    },
    {
        "id": "jawab_10",
        "nama": "📝 Jawab 10 Soal",
        "deskripsi": "Jawab 10 soal kuis",
        "target": 10,
        "reward": 10,
        "type": "total_questions"
    },
    {
        "id": "iq_50",
        "nama": "🧠 IQ 50+",
        "deskripsi": "Capai skor IQ minimal 50",
        "target": 50,
        "reward": 10,
        "type": "iq_score"
    },
    {
        "id": "eq_50",
        "nama": "❤️ EQ 50+",
        "deskripsi": "Capai skor EQ minimal 50",
        "target": 50,
        "reward": 10,
        "type": "eq_score"
    },
    {
        "id": "sq_50",
        "nama": "🙏 SQ 50+",
        "deskripsi": "Capai skor SQ minimal 50",
        "target": 50,
        "reward": 10,
        "type": "sq_score"
    },
    {
        "id": "aq_50",
        "nama": "💪 AQ 50+",
        "deskripsi": "Capai skor AQ minimal 50",
        "target": 50,
        "reward": 10,
        "type": "aq_score"
    },
    {
        "id": "nas_50",
        "nama": "🇮🇩 Nasionalisme 50+",
        "deskripsi": "Capai skor Nasionalisme minimal 50",
        "target": 50,
        "reward": 10,
        "type": "nas_score"
    },
    {
        "id": "nkhm_30",
        "nama": "🌟 NKHM Total 30+",
        "deskripsi": "Capai NKHM Total minimal 30",
        "target": 30,
        "reward": 15,
        "type": "nkhm_total"
    },
    {
        "id": "nkhm_50",
        "nama": "🌟 NKHM Total 50+",
        "deskripsi": "Capai NKHM Total minimal 50",
        "target": 50,
        "reward": 20,
        "type": "nkhm_total"
    }
]

# ========== FUNGSI LEADERBOARD ==========
def get_leaderboard_file():
    data_dir = Path(__file__).parent.parent / "data"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "leaderboard.json"

def load_leaderboard():
    """Muat data leaderboard dari file JSON dengan error handling"""
    file_path = get_leaderboard_file()
    
    # Jika file belum ada, buat dengan data kosong
    if not file_path.exists():
        save_leaderboard([])  # buat file dengan list kosong
        return []
    
    # Coba baca file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Pastikan data adalah list
            if not isinstance(data, list):
                data = []
                save_leaderboard(data)
            return data
    except (json.JSONDecodeError, ValueError) as e:
        # Jika file corrupt, buat ulang
        st.warning("⚠️ Data leaderboard rusak, dibuat ulang.")
        save_leaderboard([])
        return []

def save_leaderboard(data):
    """Simpan data leaderboard ke file JSON"""
    file_path = get_leaderboard_file()
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_leaderboard(username, total_reward):
    data = load_leaderboard()
    found = False
    for entry in data:
        if entry["username"] == username:
            entry["total_reward"] = total_reward
            entry["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            found = True
            break
    if not found:
        data.append({
            "username": username,
            "total_reward": total_reward,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
    data.sort(key=lambda x: x["total_reward"], reverse=True)
    save_leaderboard(data)

# ========== FUNGSI MISI ==========
def init_mission_progress():
    if "nkhm_mission_progress" not in st.session_state:
        st.session_state.nkhm_mission_progress = {}
        for mission in MISSIONS:
            st.session_state.nkhm_mission_progress[mission["id"]] = {
                "completed": False,
                "claimed": False
            }

def check_mission_progress():
    """Periksa progress misi, import get_current_nkhm lokal untuk hindari circular"""
    init_mission_progress()
    
    # Import lokal agar tidak circular
    try:
        from nkhm.main import get_current_nkhm
    except ImportError:
        # Jika belum bisa import, skip
        return
    
    nkhm_q, nkhm_total, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct = get_current_nkhm()
    total_q = st.session_state.get("nkhm_total_questions", 0)
    
    progress = st.session_state.nkhm_mission_progress
    any_completed = False
    
    for mission in MISSIONS:
        if progress[mission["id"]]["completed"]:
            continue
        m_type = mission["type"]
        target = mission["target"]
        completed = False
        if m_type == "total_questions":
            if total_q >= target:
                completed = True
        elif m_type == "iq_score":
            if iq_pct >= target:
                completed = True
        elif m_type == "eq_score":
            if eq_pct >= target:
                completed = True
        elif m_type == "sq_score":
            if sq_pct >= target:
                completed = True
        elif m_type == "aq_score":
            if aq_pct >= target:
                completed = True
        elif m_type == "nas_score":
            if nas_pct >= target:
                completed = True
        elif m_type == "nkhm_total":
            if nkhm_total >= target:
                completed = True
        if completed:
            progress[mission["id"]]["completed"] = True
            any_completed = True
    if any_completed:
        st.rerun()

def get_total_reward():
    progress = st.session_state.get("nkhm_mission_progress", {})
    total = 0
    for mission in MISSIONS:
        if progress.get(mission["id"], {}).get("claimed", False):
            total += mission["reward"]
    return total

def show_missions():
    init_mission_progress()
    check_mission_progress()
    
    st.markdown("## 🎯 Misi & Tantangan")
    st.markdown("Selesaikan misi untuk mengumpulkan koin! 🪙")
    
    progress = st.session_state.nkhm_mission_progress
    total_reward = get_total_reward()
    st.metric("🪙 Total Koin", total_reward)
    st.markdown("---")
    
    for mission in MISSIONS:
        status = progress[mission["id"]]
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            if status["claimed"]:
                st.markdown(f"✅ ~~{mission['nama']}~~ *(selesai)*")
            elif status["completed"]:
                st.markdown(f"✨ {mission['nama']} *(siap diklaim!)*")
            else:
                st.markdown(f"⬜ {mission['nama']}")
            st.caption(mission["deskripsi"])
        with col2:
            st.caption(f"🎁 {mission['reward']} koin")
        with col3:
            if status["completed"] and not status["claimed"]:
                if st.button("Klaim", key=f"claim_{mission['id']}"):
                    progress[mission["id"]]["claimed"] = True
                    username = st.session_state.get("nkhm_user", "Anonymous")
                    new_total = get_total_reward() + mission["reward"]
                    update_leaderboard(username, new_total)
                    st.rerun()
            elif status["claimed"]:
                st.button("✅", disabled=True, key=f"done_{mission['id']}")
            else:
                # tampilkan progress bar sederhana
                if mission["type"] == "total_questions":
                    current = st.session_state.get("nkhm_total_questions", 0)
                    st.progress(min(current / mission["target"], 1.0), text=f"{current}/{mission['target']}")
                else:
                    st.caption("🔒 Belum tercapai")

def show_leaderboard():
    st.markdown("## 🏆 Leaderboard")
    st.markdown("Peringkat berdasarkan total koin yang dikumpulkan.")
    data = load_leaderboard()
    if not data:
        st.info("Belum ada peserta. Mulailah mengumpulkan koin!")
        return
    df = pd.DataFrame(data)
    df = df[["username", "total_reward", "last_update"]]
    df.columns = ["Pengguna", "🪙 Koin", "Terakhir Update"]
    st.dataframe(df, use_container_width=True, hide_index=True)
    if len(data) >= 1:
        st.success(f"👑 Juara saat ini: **{data[0]['username']}** dengan {data[0]['total_reward']} koin!")