# nkhm/angka_rahasia.py
import streamlit as st

def init_game_state():
    if "angka_jawaban" not in st.session_state:
        st.session_state.angka_jawaban = None
    if "angka_rahasia_terbuka" not in st.session_state:
        st.session_state.angka_rahasia_terbuka = False
    if "baris1" not in st.session_state:
        st.session_state.baris1 = ""
    if "baris2" not in st.session_state:
        st.session_state.baris2 = ""
    if "baris4" not in st.session_state:
        st.session_state.baris4 = ""

def hitung_pelengkap(angka_str):
    return ''.join(str(9 - int(d)) for d in angka_str if d.isdigit())

def hitung_jawaban(angka_awal):
    angka = int(angka_awal)
    panjang = len(angka_awal)
    return 2 * (10**panjang) + (angka - 2)

def show_angka_rahasia():
    init_game_state()
    
    # CSS untuk memperkecil tinggi input, bold pada input tertentu, dan rata kiri teks "Ayo, mulai:"
    st.markdown("""
    <style>
    /* Perkecil tinggi semua text input */
    div[data-testid="stTextInput"] input {
        height: 38px;
        font-size: 16px;
        padding: 6px 10px;
    }
    /* Input yang disabled (baris 3 dan 5) dibuat bold */
    div[data-testid="stTextInput"] input:disabled {
        font-weight: bold;
        color: #0a0a0a;
        background-color: #f0f2f6;
    }
    /* Rata kiri teks "Ayo, mulai:" tanpa margin kiri berlebih */
    .rata-kiri {
        text-align: left;
        margin-left: 0;
        padding-left: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔢 Angka - Menguak Rahasia")
    st.markdown("""
    **Aturan permainan:**  
    1. Anda menuliskan deretan angka di **Baris 1** (minimal 2 digit).  
    2. Aplikasi akan menyiapkan **jawaban rahasia** (tidak terlihat sampai Anda menekan tombol 'Buka Rahasia').  
    3. Anda menuliskan deretan angka lain di **Baris 2** (jumlah digit harus sama dengan Baris 1).  
    4. Aplikasi akan menuliskan **Baris 3** secara otomatis (pelengkap angka dari Baris 2).  
    5. Anda menuliskan deretan angka lain di **Baris 4** (jumlah digit harus sama).  
    6. Aplikasi akan menuliskan **Baris 5** secara otomatis (pelengkap angka dari Baris 4).  
    7. Anda jumlahkan kelima baris tersebut, tulis hasilnya di **Baris 6**, lalu cocokkan dengan jawaban rahasia.    
    """)
    
    # Teks "Ayo, mulai:" dengan class rata kiri (sejajar dengan poin 7)
    st.markdown("<p class='rata-kiri'><strong>Ayo, mulai:</strong></p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        baris1 = st.text_input("Baris 1 (Tuliskan angka bebas, minimal 2 digit):", value=st.session_state.baris1, key="input_baris1")
    if baris1:
        if not baris1.isdigit():
            st.error("Baris 1 harus berisi angka saja.")
        elif len(baris1) < 2:
            st.error("Baris 1 minimal 2 digit.")
        else:
            if baris1 != st.session_state.baris1:
                st.session_state.baris1 = baris1
                st.session_state.angka_jawaban = hitung_jawaban(baris1)
                st.session_state.angka_rahasia_terbuka = False
    
    if st.session_state.angka_jawaban is None:
        st.info("Silakan isi Baris 1 terlebih dahulu.")
        return
    
    panjang = len(st.session_state.baris1)
    
    with col2:
        if st.session_state.angka_rahasia_terbuka:
            st.success(f"✨ Jawaban Rahasia: **{st.session_state.angka_jawaban}**")
        else:
            st.warning("🔒 Jawaban rahasia masih tersembunyi.")
        if st.button("🔓 Buka Rahasia", key="buka_rahasia"):
            st.session_state.angka_rahasia_terbuka = True
            st.rerun()
    
    st.markdown("---")
    
    # Baris 2
    baris2 = st.text_input(f"Baris 2 (Tuliskan angka dengan {panjang} digit):", value=st.session_state.baris2, key="input_baris2")
    valid2 = False
    if baris2:
        if not baris2.isdigit():
            st.error("Baris 2 harus angka.")
        elif len(baris2) != panjang:
            st.error(f"Baris 2 harus memiliki tepat {panjang} digit.")
        else:
            valid2 = True
            st.session_state.baris2 = baris2
    
    # Baris 3 (otomatis, disabled, bold via CSS)
    if valid2:
        baris3 = hitung_pelengkap(baris2)
        st.text_input("Baris 3 (otomatis, pelengkap angka)", value=baris3, disabled=True, key="baris3")
    else:
        st.text_input("Baris 3 (otomatis)", value="", disabled=True)
    
    # Baris 4
    baris4 = st.text_input(f"Baris 4 (Tuliskan angka dengan {panjang} digit):", value=st.session_state.baris4, key="input_baris4")
    valid4 = False
    if baris4:
        if not baris4.isdigit():
            st.error("Baris 4 harus angka.")
        elif len(baris4) != panjang:
            st.error(f"Baris 4 harus memiliki tepat {panjang} digit.")
        else:
            valid4 = True
            st.session_state.baris4 = baris4
    
    # Baris 5 (otomatis, disabled, bold via CSS)
    if valid4:
        baris5 = hitung_pelengkap(baris4)
        st.text_input("Baris 5 (otomatis, pelengkap angka)", value=baris5, disabled=True, key="baris5")
    else:
        st.text_input("Baris 5 (otomatis)", value="", disabled=True)
    
    # Baris 6
    st.markdown("---")
    hasil_user = st.text_input("Baris 6 (Anda jumlahkan kelima baris):", key="hasil_user")
    if st.button("✅ Cocokkan dengan Jawaban Rahasia", key="cocokkan"):
        if not hasil_user.isdigit():
            st.error("Masukkan angka hasil penjumlahan.")
        else:
            total_user = int(hasil_user)
            if total_user == st.session_state.angka_jawaban:
                st.balloons()
                st.success("🎉 BENAR! Hasil penjumlahan Anda sesuai dengan jawaban rahasia!")
            else:
                st.error(f"❌ SALAH. Jawaban rahasia adalah {st.session_state.angka_jawaban}. Coba periksa kembali penjumlahan Anda.")
    
    st.caption("Catatan: Baris 3 dan Baris 5 diisi otomatis oleh sistem berdasarkan aturan Angka Rahasia (Angka - Menguak Rahasia).")

if __name__ == "__main__":
    show_angka_rahasia()
