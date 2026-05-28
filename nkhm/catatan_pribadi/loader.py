# nkhm/catatan_pribadi/loader.py
import streamlit as st
from pathlib import Path

    """Menampilkan aplikasi React Catatan Pribadi"""
def show_catatan_pribadi():
    st.markdown("### 📝 Catatan Pribadi")
    st.components.v1.iframe("https://your-react-app.vercel.app", height=600, scrolling=True)
    
    # Baca file index.html
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Perbaiki path asset relatif menjadi absolut (menggunakan base path)
    # Karena asset dipanggil dari dalam iframe, kita perlu mengganti src="./assets/..." menjadi src="./assets/..."
    # Tapi jika di dalam iframe, base path adalah direktori saat ini.
    # Solusi sederhana: gunakan iframe dengan srcdoc
    
    # Tampilkan dalam iframe (srcdoc agar lebih aman)
    st.components.v1.html(html_content, height=600, scrolling=True)
    
    # Alternatif: jika ingin menggunakan iframe dengan src ke file lokal (tidak bisa di Streamlit Cloud)
    # Kita gunakan srcdoc di atas.