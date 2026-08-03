# nkhm/angka_rahasia.py
import streamlit as st
import logging

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di angka_rahasia: {e}")

# ========== INISIALISASI STATE ==========
def init_game_state():
    try:
        defaults = {
            "angka_jawaban": None,
            "angka_rahasia_terbuka": False,
            "baris1": "",
            "baris2": "",
            "baris4": "",
            "angka_skor": 0,
            "angka_pernah_menang": False
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    except Exception as e:
        logging.error(f"Error init_game_state: {e}")
        st.error(f"Error inisialisasi game: {e}")

def hitung_pelengkap(angka_str):
    try:
        return ''.join(str(9 - int(d)) for d in angka_str if d.isdigit())
    except Exception as e:
        logging.error(f"Error hitung_pelengkap: {e}")
        return ""

def hitung_jawaban(angka_awal):
    try:
        angka = int(angka_awal)
        panjang = len(angka_awal)
        return 2 * (10**panjang) + (angka - 2)
    except Exception as e:
        logging.error(f"Error hitung_jawaban: {e}")
        return None

def reset_skor():
    """Reset skor permainan."""
    try:
        st.session_state.angka_skor = 0
        st.session_state.angka_pernah_menang = False
        logging.info("Skor angka rahasia direset")
    except Exception as e:
        logging.error(f"Error reset_skor: {e}")
        st.error(f"Error reset skor: {e}")

# ========== FUNGSI UTAMA ==========
def show_angka_rahasia():
    try:
        init_game_state()
        
        # CSS untuk styling
        st.markdown("""
        <style>
        div[data-testid="stTextInput"] input {
            height: 38px;
            font-size: 16px;
            padding: 6px 10px;
        }
        div[data-testid="stTextInput"] input:disabled {
            font-weight: bold;
            color: #0a0a0a;
            background-color: #f0f2f6;
        }
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
        
        # Tampilkan skor
        col_skor, _ = st.columns([1, 3])
        with col_skor:
            st.metric("🏆 Skor Anda", st.session_state.angka_skor)
        
        st.markdown("<p class='rata-kiri'><strong>Ayo, mulai:</strong></p>", unsafe_allow_html=True)
        
        # ========== BARIS 1 ==========
        col1, col2 = st.columns(2)
        with col1:
            baris1 = st.text_input(
                "Baris 1 (Tuliskan angka bebas, minimal 2 digit):",
                value=st.session_state.baris1,
                key="input_baris1"
            )
        
        if baris1:
            if not baris1.isdigit():
                st.error("Baris 1 harus berisi angka saja.")
            elif len(baris1) < 2:
                st.error("Baris 1 minimal 2 digit.")
            else:
                if baris1 != st.session_state.baris1:
                    try:
                        st.session_state.baris1 = baris1
                        st.session_state.angka_jawaban = hitung_jawaban(baris1)
                        st.session_state.angka_rahasia_terbuka = False
                        # Reset status menang saat angka baru
                        st.session_state.angka_pernah_menang = False
                    except Exception as e:
                        logging.error(f"Error memproses Baris 1: {e}")
                        st.error(f"Error memproses Baris 1: {e}")
        
        if st.session_state.angka_jawaban is None:
            st.info("Silakan isi Baris 1 terlebih dahulu.")
            return
        
        panjang = len(st.session_state.baris1)
        
        # ========== BARIS 2 ==========
        with col2:
            if st.session_state.angka_rahasia_terbuka:
                st.success(f"✨ Jawaban Rahasia: **{st.session_state.angka_jawaban}**")
            else:
                st.warning("🔒 Jawaban rahasia masih tersembunyi.")
            if st.button("🔓 Buka Rahasia", key="buka_rahasia"):
                st.session_state.angka_rahasia_terbuka = True
                safe_rerun()
        
        st.markdown("---")
        
        # ========== BARIS 2 ==========
        baris2 = st.text_input(
            f"Baris 2 (Tuliskan angka dengan {panjang} digit):",
            value=st.session_state.baris2,
            key="input_baris2"
        )
        valid2 = False
        if baris2:
            if not baris2.isdigit():
                st.error("Baris 2 harus angka.")
            elif len(baris2) != panjang:
                st.error(f"Baris 2 harus memiliki tepat {panjang} digit.")
            else:
                valid2 = True
                st.session_state.baris2 = baris2
        
        if valid2:
            baris3 = hitung_pelengkap(baris2)
            st.text_input("Baris 3 (otomatis, pelengkap angka)", value=baris3, disabled=True, key="baris3")
        else:
            st.text_input("Baris 3 (otomatis)", value="", disabled=True)
        
        # ========== BARIS 4 ==========
        baris4 = st.text_input(
            f"Baris 4 (Tuliskan angka dengan {panjang} digit):",
            value=st.session_state.baris4,
            key="input_baris4"
        )
        valid4 = False
        if baris4:
            if not baris4.isdigit():
                st.error("Baris 4 harus angka.")
            elif len(baris4) != panjang:
                st.error(f"Baris 4 harus memiliki tepat {panjang} digit.")
            else:
                valid4 = True
                st.session_state.baris4 = baris4
        
        if valid4:
            baris5 = hitung_pelengkap(baris4)
            st.text_input("Baris 5 (otomatis, pelengkap angka)", value=baris5, disabled=True, key="baris5")
        else:
            st.text_input("Baris 5 (otomatis)", value="", disabled=True)
        
        # ========== BARIS 6 ==========
        st.markdown("---")
        hasil_user = st.text_input("Baris 6 (Anda jumlahkan kelima baris):", key="hasil_user")
        
        # ========== TOMBOL COCOKKAN ==========
        if st.button("✅ Cocokkan dengan Jawaban Rahasia", key="cocokkan"):
            try:
                if not hasil_user or not hasil_user.isdigit():
                    st.error("Masukkan angka hasil penjumlahan yang valid.")
                else:
                    total_user = int(hasil_user)
                    if total_user == st.session_state.angka_jawaban:
                        # Skor ditambahkan hanya jika user belum pernah menang sebelumnya
                        if not st.session_state.angka_pernah_menang:
                            st.session_state.angka_skor += 10
                            st.session_state.angka_pernah_menang = True
                            st.success("🎉 BENAR! Anda mendapatkan +10 poin (hadiah pertama).")
                            st.balloons()
                        else:
                            st.success("🎉 BENAR! Anda telah mendapatkan poin sebelumnya. Skor tetap.")
                    else:
                        st.error(f"❌ SALAH. Jawaban rahasia adalah {st.session_state.angka_jawaban}. Coba periksa kembali penjumlahan Anda.")
            except Exception as e:
                logging.error(f"Error saat mencocokkan: {e}")
                st.error(f"Terjadi error: {e}")
        
        # ========== TOMBOL RESET SKOR ==========
        if st.button("🔄 Reset Skor Permainan", key="reset_skor"):
            reset_skor()
            safe_rerun()
        
        st.caption("Catatan: Baris 3 dan Baris 5 diisi otomatis oleh sistem berdasarkan aturan Angka Rahasia (Angka - Menguak Rahasia). Skor hanya diberikan satu kali (10 poin) saat pertama kali berhasil menebak dengan benar.")
    
    except Exception as e:
        logging.error(f"Error di show_angka_rahasia: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Angka Rahasia: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_angka_rahasia()