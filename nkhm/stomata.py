# nkhm/stomata.py
import streamlit as st
from nkhm.stomata_tanggapan import show_tanggapan
from nkhm.stomata_pilihan_benar_salah import show_pilihan_benar_salah

def show_stomata():
    st.markdown("## 💖 Sto-mata Hati")
    tab1, tab2 = st.tabs(["📝 Tanggapan (Skala Likert)", "✅ Pilihan Benar/Salah"])
    with tab1:
        show_tanggapan()
    with tab2:
        show_pilihan_benar_salah()