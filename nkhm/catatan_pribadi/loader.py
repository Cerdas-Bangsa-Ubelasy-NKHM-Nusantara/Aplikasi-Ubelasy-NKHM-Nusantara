# nkhm/catatan_pribadi/loader.py
import streamlit as st

def show_catatan_pribadi():
    st.markdown("### 📝 Catatan Pribadi")
    st.markdown("Gunakan aplikasi catatan di bawah untuk menulis jurnal, ide, atau catatan belajar Anda.")
    
    # URL aplikasi React yang sudah dideploy di Vercel
    vercel_url = "https://my-personal-notes-app-187q.vercel.app"
    
    # Tampilkan dalam iframe
    st.components.v1.iframe(vercel_url, height=600, scrolling=True)
    
    # Opsional: tautan langsung jika iframe bermasalah
    st.markdown(f"[🔗 Buka Catatan Pribadi di tab baru]({vercel_url})")