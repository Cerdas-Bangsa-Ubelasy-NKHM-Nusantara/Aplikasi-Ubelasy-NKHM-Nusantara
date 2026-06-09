# nkhm/stomata.py
import streamlit as st
from nkhm.stomata_tanggapan import show_tanggapan
from nkhm.stomata_pilihan_benar_salah import show_pilihan_benar_salah
from nkhm.stomata_pilihan_ganda import show_pilihan_ganda

def show_stomata():
    st.markdown("## 💖 Sto-mata Hati")
    tab1, tab2, tab3 = st.tabs(["📝 Tanggapan (Skala Likert)", "✅ Pilihan Benar/Salah", "🔢 Pilihan Ganda (a,b,c,d)"])
    with tab1:
        show_tanggapan()
    with tab2:
        show_pilihan_benar_salah()
    with tab3:
        show_pilihan_ganda()