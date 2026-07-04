import streamlit as st

def show_jarimatika():
    st.markdown("## 🖐️ Jarimatika App")
    st.markdown("Belajar berhitung dengan jari menggunakan AI dan kamera.")
    
    # URL aplikasi Jarimatika yang di-deploy di Netlify
    # Ganti dengan URL Netlify Anda
    jarimatika_url = "https://jarimatika-app.netlify.app"
    
    # Tampilkan iframe
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