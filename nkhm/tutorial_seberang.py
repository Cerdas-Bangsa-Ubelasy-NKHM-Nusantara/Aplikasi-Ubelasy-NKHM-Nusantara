# nkhm/tutorial_seberang.py
import streamlit as st

def show_tutorial_seberang():
    st.markdown("## 🚣‍♂️ Tutorial: Pahlawan Menyeberang Sungai")
    
    # Pengantar
    st.markdown("""
    ### 📖 Cerita
    Seorang pahlawan ingin menyeberangi sungai dengan membawa:
    - **Tawanan Perang** (⛓️)
    - **Perbekalan Pangan** (🍞)
    - **Anak Buah** (👤)
    
    Ia hanya memiliki sebuah **perahu kecil** yang sangat terbatas kapasitasnya hanya bisa dimuat 2 entitas saja.
    """)
    
    # Aturan Dasar
    st.markdown("""
    ### ⚠️ Aturan Permainan
    1. **Perahu hanya bisa memuat maksimal 2 entitas** (termasuk pahlawan).
       - Contoh: Pahlawan + Tawanan, Pahlawan + Perbekalan, atau Pahlawan sendirian.
    2. **Tawanan dan perbekalan tidak boleh ditinggal berdua tanpa pengawasan pahlawan**.
       - Jika terjadi, tawanan akan merusak perbekalan → PERMAINAN GAGAL!
    3. **Tujuan**: Memindahkan semua entitas (pahlawan, tawanan, perbekalan, anak buah) ke seberang sungai dengan selamat.
    """)
    
    # Solusi Langkah demi Langkah
    st.markdown("### 🎯 Solusi Langkah demi Langkah")
    
    st.markdown("""
    Berikut adalah urutan langkah yang **paling aman** dan **pasti berhasil**:
    
    | Langkah | Aksi | Penjelasan |
    |:---:|:---|:---|
    | **1** | 🦸 + ⛓️ → 🏝️ seberang | Bawa tawanan terlebih dahulu |
    | **2** | 🦸 sendiri ← 🏝️ awal | Kembali ambil perbekalan |
    | **3** | 🦸 + 🍞 → 🏝️ seberang | Bawa perbekalan |
    | **4** | 🦸 + ⛓️ ← 🏝️ awal | Bawa tawanan kembali (agar tidak ditinggal dengan perbekalan) |
    | **5** | 🦸 + 👤 → 🏝️ seberang | Bawa anak buah |
    | **6** | 🦸 sendiri ← 🏝️ awal | Kembali ambil tawanan |
    | **7** | 🦸 + ⛓️ → 🏝️ seberang | Bawa tawanan terakhir |
    
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
        - Gunakan pahlawan sebagai agen 'antar-jemput'
        """)
    
    # Tips Tambahan
    st.markdown("### 💡 Tips Tambahan")
    st.markdown("""
    - Jangan terburu-buru. Pikirkan setiap langkah.
    - Perhatikan siapa yang ada di sisi awal dan di seberang sebelum memilih.
    - Jika gagal, klik **Reset Permainan** dan coba lagi dengan urutan yang benar.
    - Gunakan tombol **"Sendirian (hanya pahlawan)"** untuk memindahkan pahlawan tanpa entitas lain.
    """)
    
    # Simulasi Interaktif Sederhana
    st.markdown("### 🎮 Coba Langsung!")
    st.markdown("""
    Setelah memahami tutorial ini, buka tab **HADIAH → Pahlawan Menyeberang Sungai** untuk bermain langsung.
    
    Jangan lupa, ikuti langkah-langkah di atas jika ingin menang dengan mudah!
    """)
    
    # Tombol untuk langsung menuju permainan (jika diinginkan)
    if st.button("🚀 Buka Permainan Sekarang", use_container_width=True):
        st.switch_page("nkhm/main.py")  # Catatan: ini hanya berfungsi di lingkungan Streamlit dengan multi-page apps
        # Alternatif: beri pesan
        st.info("Buka tab **HADIAH** dan pilih subtab **Pahlawan Menyeberang Sungai**")

if __name__ == "__main__":
    show_tutorial_seberang()