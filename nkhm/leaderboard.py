# nkhm/leaderboard.py
import streamlit as st
import pandas as pd

def show_leaderboard():
    st.subheader("🏆 Leaderboard Antar Sekolah")
    data = {
        "Sekolah": ["SMK Maarif NU 1 Purwokerto", "MI BAIPAS Malang", "SMA Negeri 1 Surabaya", "MAN 1 Medan"],
        "Rata-rata NKHM": [68, 72, 65, 70],
        "Jumlah Peserta": [45, 30, 60, 25]
    }
    df = pd.DataFrame(data)
    st.dataframe(df.sort_values("Rata-rata NKHM", ascending=False), use_container_width=True)
