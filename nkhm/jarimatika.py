import streamlit as st
from pathlib import Path

def show_jarimatika():
    st.markdown("## 🖐️ Jarimatika App")
    st.markdown("Belajar berhitung dengan jari menggunakan AI dan kamera.")
    
    # Cek apakah folder jarimatika-app ada di root
    jarimatika_dir = Path(__file__).parent.parent / "jarimatika-app"
    index_path = jarimatika_dir / "index.html"
    
    if not index_path.exists():
        st.error("❌ Folder 'jarimatika-app' tidak ditemukan. Pastikan folder tersebut ada di root proyek Ubelasy + NKHM.")
        st.info("📁 Struktur yang diharapkan:\n```\nUbelasy-NKHM-Nusantara/\n├── jarimatika-app/\n│   ├── index.html\n│   ├── css/\n│   ├── js/\n│   └── ...\n├── nkhm/\n│   └── jarimatika.py\n└── ...\n```")
        return
    
    # Tampilkan iframe yang mengarah ke index.html
    # Asumsikan server melayani folder jarimatika-app sebagai statis
    jarimatika_url = "/jarimatika-app/index.html"
    
    st.markdown(f"""
    <div style="width:100%; height:80vh; border-radius:12px; overflow:hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <iframe 
            src="{jarimatika_url}" 
            style="width:100%; height:100%; border:none;" 
            allow="camera; microphone; autoplay; encrypted-media"
            allowfullscreen
        ></iframe>
    </div>
    """, unsafe_allow_html=True)
    
    # Info tambahan
    with st.expander("ℹ️ Cara Menggunakan Jarimatika App"):
        st.markdown("""
        1. **Mulai Kamera** – Klik tombol "🎥 Mulai Kamera" dan izinkan akses kamera.
        2. **Deteksi Jari** – Tunjukkan jari di depan kamera, aplikasi akan menghitung jumlah jari terbuka.
        3. **Perkalian Jarimatika (6-10)** – Pilih dua angka (6–10) dan klik "Hitung" untuk melihat hasil perkalian dengan metode jari.
        4. **Kalkulator** – Gunakan tombol angka untuk berhitung biasa.
        5. **AI Chatbot** – Tanyakan soal matematika atau tentang Jarimatika.
        """)