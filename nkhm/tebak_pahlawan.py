# nkhm/tebak_pahlawan.py
import streamlit as st
import random
from datetime import datetime

# ======================= DAFTAR 12 PAHLAWAN + FAKTA =======================
PAHLAWAN_DATA = {
    1: {"nama": "Ir. Soekarno", "fakta": "Proklamator Kemerdekaan RI, Presiden pertama Indonesia."},
    2: {"nama": "Drs. Mohammad Hatta", "fakta": "Proklamator, Wakil Presiden pertama, Bapak Koperasi."},
    3: {"nama": "Jenderal Sudirman", "fakta": "Panglima Besar TNI, memimpin gerilya meski sakit paru-paru."},
    4: {"nama": "Pangeran Diponegoro", "fakta": "Pahlawan nasional yang memimpin Perang Jawa (1825-1830)."},
    5: {"nama": "Cut Nyak Dien", "fakta": "Pahlawan wanita dari Aceh, gigih melawan Belanda."},
    6: {"nama": "R.A. Kartini", "fakta": "Pelopor emansipasi wanita Indonesia."},
    7: {"nama": "Ki Hajar Dewantara", "fakta": "Bapak Pendidikan Indonesia, pendiri Taman Siswa."},
    8: {"nama": "Kapten Pattimura", "fakta": "Pahlawan asal Maluku, memimpin perlawanan terhadap VOC."},
    9: {"nama": "Dewi Sartika", "fakta": "Pelopor pendidikan bagi perempuan di Jawa Barat."},
    10: {"nama": "Sultan Hasanuddin", "fakta": "Pahlawan dari Makassar, dijuluki 'Ayam Jantan dari Timur'."},
    11: {"nama": "Martha Christina Tiahahu", "fakta": "Pahlawan wanita dari Maluku, ikut perang Pattimura."},
    12: {"nama": "Dr. Soetomo", "fakta": "Pendiri organisasi Boedi Oetomo, pelopor kebangkitan nasional."}
}

SEMUA_NAMA = [data["nama"] for data in PAHLAWAN_DATA.values()]

# ======================= INISIALISASI STATE =======================
def init_game_state():
    if "pahlawan_target" not in st.session_state:
        st.session_state.pahlawan_target = random.choice(SEMUA_NAMA)
    if "pahlawan_options" not in st.session_state:
        st.session_state.pahlawan_options = []
    if "pahlawan_score" not in st.session_state:
        st.session_state.pahlawan_score = 0
    if "pahlawan_attempts" not in st.session_state:
        st.session_state.pahlawan_attempts = 0
    if "pahlawan_history" not in st.session_state:
        st.session_state.pahlawan_history = []
    if "pahlawan_user_name" not in st.session_state:
        st.session_state.pahlawan_user_name = st.session_state.get("nkhm_user", "Pemain")
    if "pahlawan_feedback" not in st.session_state:
        st.session_state.pahlawan_feedback = None
    if "pahlawan_game_ended" not in st.session_state:
        st.session_state.pahlawan_game_ended = False  # Menandai apakah sudah 5 tebakan
    # Generate pilihan awal jika kosong
    if not st.session_state.pahlawan_options:
        _generate_new_round()

def _generate_new_round():
    """Buat ronde baru: target acak + 2 distraktor unik, lalu acak urutan."""
    new_target = random.choice(SEMUA_NAMA)
    candidates = [n for n in SEMUA_NAMA if n != new_target]
    distractors = random.sample(candidates, 2)
    options = [new_target] + distractors
    random.shuffle(options)
    st.session_state.pahlawan_target = new_target
    st.session_state.pahlawan_options = options

def _save_attempt(tebakan_nama, hasil_teks, poin_didapat):
    data = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "nama": st.session_state.pahlawan_user_name,
        "tebakan": tebakan_nama,
        "hasil": hasil_teks,
        "poin": poin_didapat
    }
    st.session_state.pahlawan_history.insert(0, data)
    if len(st.session_state.pahlawan_history) > 20:
        st.session_state.pahlawan_history.pop()

def reset_game():
    """Reset hanya attempts dan game_ended, skor TIDAK diubah"""
    st.session_state.pahlawan_attempts = 0
    st.session_state.pahlawan_game_ended = False
    st.session_state.pahlawan_history = []
    st.session_state.pahlawan_feedback = "🔄 Game telah direset! Kamu bisa bermain lagi dengan 5 kesempatan baru, tetapi skor tetap seperti sebelumnya."
    _generate_new_round()

# ======================= FUNGSI UTAMA =======================
def show_tebak_pahlawan():
    init_game_state()

    st.markdown("## 🦅 Tebak Pahlawan Nusantara")
    st.markdown("""
    **Aturan:**  
    - Kamu hanya punya **5 kesempatan** untuk mengumpulkan skor.  
    - Setiap tebakan **benar** = +10 poin.  
    - **Setelah menebak (benar/salah), pahlawan target akan berganti** secara acak dari 12 pahlawan nasional.  
    - Setelah 5 kali tebakan, skor tidak akan berubah lagi dan tombol Reset Game akan muncul.  
    - **Tombol Reset Game hanya mereset kesempatan tebakan menjadi 0, skor tetap seperti skor akhir Anda.**  
    """)

    # Input nama
    user_name = st.text_input(
        "Nama Anda:",
        value=st.session_state.pahlawan_user_name,
        key="pahlawan_nama_input"
    )
    if user_name.strip():
        st.session_state.pahlawan_user_name = user_name

    # Tentukan apakah game sudah berakhir (5 tebakan)
    if st.session_state.pahlawan_attempts >= 5:
        st.session_state.pahlawan_game_ended = True
    
    # Panel info
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏆 Skor AKHIR (Tetap)", st.session_state.pahlawan_score)
    with col2:
        if st.session_state.pahlawan_game_ended:
            st.metric("🎯 Status", "✅ Game Selesai (5 tebakan)")
            st.info(f"Skor akhir Anda: {st.session_state.pahlawan_score} dari maksimal 50")
        else:
            sisa = 5 - st.session_state.pahlawan_attempts
            st.metric("🎯 Kesempatan Tersisa", f"{sisa}/5")

    st.markdown("---")
    
    # Jika game sudah berakhir, tampilkan pesan dan tombol reset
    if st.session_state.pahlawan_game_ended:
        st.warning("🏁 **Game telah selesai!** Anda sudah menggunakan 5 kesempatan.")
        st.info(f"📊 Skor akhir Anda: **{st.session_state.pahlawan_score}** poin")
        
        # Tombol reset di tengah
        col_reset = st.columns([1, 2, 1])[1]
        with col_reset:
            if st.button("🔄 Reset Game (Main Lagi dengan Skor Sama)", use_container_width=True, key="reset_btn_pahlawan"):
                reset_game()
                st.rerun()
        
        # Tampilkan daftar pahlawan dan riwayat saja (tanpa tombol tebakan)
        with st.expander("📜 Daftar 12 Pahlawan Nasional"):
            cols_ref = st.columns(3)
            for i, data in enumerate(PAHLAWAN_DATA.values()):
                with cols_ref[i % 3]:
                    st.markdown(f"**{data['nama']}**  \n{data['fakta'][:80]}...")
        
        # Riwayat tebakan
        st.markdown("---")
        st.subheader("📋 Riwayat Tebakan (Game Sebelumnya)")
        if st.session_state.pahlawan_history:
            history_df = []
            for h in st.session_state.pahlawan_history[:10]:
                history_df.append({
                    "Waktu": h["timestamp"],
                    "Nama": h["nama"],
                    "Tebakan": h["tebakan"],
                    "Hasil": h["hasil"],
                    "Poin": h["poin"]
                })
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada tebakan.")
        return  # Keluar dari fungsi, tidak menampilkan tombol tebakan
    
    # ========== GAME MASIH BERJALAN (BELUM 5 TEBAKAN) ==========
    st.markdown("### Siapa pahlawan yang benar?")
    options = st.session_state.pahlawan_options
    if not options:
        _generate_new_round()
        options = st.session_state.pahlawan_options
    
    # Form untuk menangani tebakan
    with st.form(key="tebak_pahlawan_form"):
        cols = st.columns(3)
        submit_btn = None
        selected_hero = None
        
        for idx, hero_name in enumerate(options):
            with cols[idx]:
                if st.form_submit_button(f"📌 {hero_name}", use_container_width=True):
                    selected_hero = hero_name
                    submit_btn = True
        
        if submit_btn and selected_hero:
            # Proses tebakan
            benar = (selected_hero == st.session_state.pahlawan_target)
            poin = 0
            
            # Tambah skor hanya jika masih dalam batas 5 tebakan
            if st.session_state.pahlawan_attempts < 5:
                if benar:
                    poin = 10
                    st.session_state.pahlawan_score += poin
            
            # Catat riwayat
            if benar:
                hasil_teks = f"✅ Benar! (+{poin})" if poin > 0 else "✅ Benar! (skor tidak berubah)"
            else:
                hasil_teks = f"❌ Salah (target: {st.session_state.pahlawan_target})"
            _save_attempt(selected_hero, hasil_teks, poin)
            
            # Siapkan feedback
            fakta_target = next((d["fakta"] for d in PAHLAWAN_DATA.values() if d["nama"] == st.session_state.pahlawan_target), "")
            if benar:
                st.session_state.pahlawan_feedback = f"🎉 **BENAR!** {st.session_state.pahlawan_target}\n📖 *{fakta_target}*"
                if poin == 0 and st.session_state.pahlawan_attempts >= 5:
                    st.session_state.pahlawan_feedback += "\n\n⚠️ Skor tidak bertambah karena kamu sudah melewati 5 kesempatan."
            else:
                st.session_state.pahlawan_feedback = f"❌ **SALAH!** Pahlawan yang dimaksud adalah **{st.session_state.pahlawan_target}**.\n📖 *{fakta_target}*"
            
            # Tambah hitungan tebakan
            st.session_state.pahlawan_attempts += 1
            
            # Cek apakah setelah penambahan mencapai 5
            if st.session_state.pahlawan_attempts >= 5:
                st.session_state.pahlawan_game_ended = True
                st.session_state.pahlawan_feedback += "\n\n🏁 **Game selesai!** Klik tombol 'Reset Game' untuk bermain lagi dengan skor yang sama."
            
            # Generate ronde baru untuk tebakan berikutnya
            _generate_new_round()
            
            # Trigger rerun
            st.rerun()
    
    # Tampilkan feedback jika ada
    if st.session_state.pahlawan_feedback:
        st.markdown("---")
        st.info(st.session_state.pahlawan_feedback)
    
    # Referensi 12 pahlawan
    with st.expander("📜 Daftar 12 Pahlawan Nasional"):
        cols_ref = st.columns(3)
        for i, data in enumerate(PAHLAWAN_DATA.values()):
            with cols_ref[i % 3]:
                st.markdown(f"**{data['nama']}**  \n{data['fakta'][:80]}...")
    
    # Riwayat tebakan
    st.markdown("---")
    st.subheader("📋 Riwayat Tebakan")
    if st.session_state.pahlawan_history:
        history_df = []
        for h in st.session_state.pahlawan_history[:10]:
            history_df.append({
                "Waktu": h["timestamp"],
                "Nama": h["nama"],
                "Tebakan": h["tebakan"],
                "Hasil": h["hasil"],
                "Poin": h["poin"]
            })
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada tebakan. Mulai tebak pahlawan di atas!")