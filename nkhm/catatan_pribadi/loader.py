# nkhm/catatan_pribadi/loader.py
import streamlit as st
from pathlib import Path

def show_catatan_pribadi():
    """Menampilkan aplikasi React Catatan Pribadi"""
    st.markdown("### 📝 Catatan Pribadi")
    
    # Path ke folder dist
    dist_path = Path(__file__).parent / "dist"
    index_path = dist_path / "index.html"
    
    if not index_path.exists():
        st.error(f"❌ Aplikasi catatan pribadi belum di-build. Pastikan folder `dist` ada di {dist_path}")
        st.info("Jalankan `npm run build` di folder `nkhm/catatan_pribadi`, lalu upload folder `dist` ke GitHub.")
        return
    
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