# nkhm/catatan_pribadi/loader.py
import streamlit as st

def show_catatan_pribadi():
    st.markdown("### 📝 Catatan Pribadi")
    st.markdown("Catatan Anda disimpan secara online. Buka di tab baru jika perlu.")
    
    # Ganti dengan URL Vercel milik Anda
    vercel_url = "https://my-personal-notes-app-187q.vercel.app"
    
    st.components.v1.iframe(vercel_url, height=600, scrolling=True)
    
    # Opsional: tautan langsung
    st.markdown(f"[🔗 Buka di tab baru]({vercel_url})")