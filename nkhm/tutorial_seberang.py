# nkhm/tutorial_seberang.py
import streamlit as st

def show_tutorial_seberang():
    st.markdown("## 🚣‍♂️ Tutorial: Pahlawan Menyeberang Sungai")
    
    # Pengantar
    st.markdown("""
    ### 📖 Cerita
    Seorang pahlawan ingin menyeberangi sungai dengan membawa:
    - **Seorang Tawanan Perang** (⛓️)
    - **Perbekalan Pangan** (🍞)
    - **Seorang Anak Buah** (👤)
    
    Ia hanya memiliki sebuah **perahu kecil** yang sangat terbatas kapasitasnya, hanya bisa dimuati dua entitas.
    """)
    
    # Aturan Dasar
    st.markdown("""
    ### ⚠️ Aturan Permainan
    1. **Perahu hanya bisa memuat maksimal 2 entitas** (termasuk pahlawan).
       - Contoh: Pahlawan + Tawanan, Pahlawan + Perbekalan, atau Pahlawan sendirian.
    2. **Tawanan dan perbekalan tidak boleh ditinggal berdua tanpa pengawasan pahlawan**.
       - Jika terjadi, tawanan akan merusak perbekalan → PERMAINAN GAGAL!
    3. **Tawanan dan Anak Buah tidak boleh ditinggal berdua tanpa bersama pahlawan**
      - Jika terjadi, tawanan dan anak buah akan bertarung duel → PERMAINAN GAGAL!
    4. **Tujuan**: Memindahkan semua entitas (pahlawan, tawanan, perbekalan, anak buah) ke seberang sungai dengan selamat.
    """)
    
    # Solusi Langkah demi Langkah
    st.markdown("### 🎯 Solusi Langkah demi Langkah")
    
    st.markdown("""
    Tentukan urutan langkah yang **paling aman** dan **pasti berhasil** Untuk Aksi penyeberangan:
- Pahlawan membawa apa terlebih dahulu ke Sebetang, lalu Aksi kembali ke Sisi Awal,
- Kemudian Pahlawan membawa apa  berikutnya ke Sebetang, lalu Aksi kembali ke Sisi Awal, 
- Berikutnya Pahlawan membawa apa ke Sebetang, lalu Aksi kembali ke Sisi Awal,
- Terakhir Pahlawan membawa apa ke Seberang, hingga semuanya selamat sampai di seberang sungai.
    
    **SELESAI!** Semua entitas berhasil menyeberang dengan selamat. 🎉
    """)
    
    # Penjelasan Logika
    st.markdown("### 🧠 Mengapa Harus Begitu?")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **❌ Jika salah langkah:**
        - Meninggalkan tawanan dan perbekalan bersama tanpa pahlawan → **GAGAL**
        - Perahu kelebihan muatan → **Tidak bisa**
        """)
    with col2:
        st.success("""
        **✅ Kunci sukses:**
        - Tawanan harus selalu diawasi
        - Pahlawan menjadi 'penengah' yang aman
        - Gunakan pahlawan sebagai 'antar-jemput'
        """)
    
    # Tips Tambahan
    st.markdown("### 💡 Tips Tambahan")
    st.markdown("""
    - Jangan terburu-buru. Pikirkan setiap langkah.
    - Perhatikan siapa yang ada di sisi awal dan seberang sebelum memilih.
    - Jika gagal, klik **Reset Permainan** dan coba lagi dengan urutan yang benar.
    - Gunakan tombol **"Sendirian (hanya pahlawan)"** untuk memindahkan pahlawan tanpa entitas lain.
    """)
    
    # Simulasi Interaktif Sederhana
    st.markdown("### 🎮 Coba Langsung!")
    st.markdown("""
    Setelah memahami tutorial ini, buka tab **HADIAH → Pahlawan Menyeberang Sungai** untuk bermain langsung.
    
    Jangan lupa, ikuti langkah-langkah di atas jika ingin menang dengan mudah!
    """)
    
     # Tombol informasi (tanpa switch_page)
    if st.button("🎮 Buka Tab HADIAH untuk Bermain", use_container_width=True):
        st.info("📍 Buka tab **HADIAH** di menu utama, lalu pilih subtab **Pahlawan Menyeberang Sungai**")


if __name__ == "__main__":
    show_tutorial_seberang()
