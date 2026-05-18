# nkhm/leaderboard.py
import json
import os
import streamlit as st
from datetime import datetime

LEADERBOARD_FILE = "data/leaderboard.json"

def init_leaderboard():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump([], f)

# nkhm/leaderboard.py (bagian save_score)

def save_score(name, nkhm_total):
    """Menyimpan skor NKHM_Total ke leaderboard"""
    init_leaderboard()
    with open(LEADERBOARD_FILE, "r") as f:
        scores = json.load(f)
    
    # Cek apakah nama sudah ada
    found = False
    for item in scores:
        if item["name"] == name:
            if nkhm_total > item["score"]:
                item["score"] = nkhm_total
                item["timestamp"] = datetime.now().isoformat()
            found = True
            break
    
    if not found:
        scores.append({"name": name, "score": nkhm_total, "timestamp": datetime.now().isoformat()})
    
    # Urutkan berdasarkan skor tertinggi
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:100]
    
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f)

def get_leaderboard():
    init_leaderboard()
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def show_leaderboard():
    st.subheader("🏆 Peringkat NKHM Tertinggi")
    scores = get_leaderboard()
    if not scores:
        st.info("Belum ada peserta.")
        return
    import pandas as pd
    df = pd.DataFrame(scores[:10])
    df.index = range(1, len(df)+1)
    st.dataframe(df[["name", "score"]], use_container_width=True)
