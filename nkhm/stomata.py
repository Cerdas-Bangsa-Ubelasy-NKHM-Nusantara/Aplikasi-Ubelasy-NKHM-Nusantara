# nkhm/stomata.py
import streamlit as st
from .stomata_tanggapan import show_tanggapan
from .stomata_pilihan_ganda import show_pilihan_ganda

def show_stomata():
    st.markdown("## 💖 Sto-mata Hati")
    st.markdown("Alat Uji Tingkat Iman, Kasih, dan Pengharapan (IKP)")
    tab1, tab2 = st.tabs(["📝 Tanggapan (Skala Likert)", "✅ Pilihan Ganda (Benar/Salah)"])
    with tab1:
        show_tanggapan()
    with tab2:
        show_pilihan_ganda()