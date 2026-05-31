# nkhm/tebak_pahlawan.py
import streamlit as st
import random
from datetime import datetime

# Data pahlawan
PAHLAWAN = {
    1: {"nama": "Jenderal Sudirman", "fakta": "Panglima besar TNI, memimpin gerilya, wafat di usia muda."},
    2: {"nama": "Pangeran Diponegoro", "fakta": "Pahlawan nasional yang memimpin Perang Jawa (1825-1830)."},
    3: {"nama": "Kapten Pattimura", "fakta": "Pahlawan asal Maluku yang memimpin perlawanan terhadap VOC."}
}

def init_game_state():
    if "pahlawan_history" not in st.session_state:
        st.session_state.pahlawan_history = []
    if "pahlawan_score" not in st.session_state:
        st.session_state.pahlawan_score = 0
    if "pahlawan_user_name" not in st.session_state:
        st.session_state.pahlawan_user_name = st.session_state.get("nkhm_user", "Pemain")
    if "pahlawan_attempts" not in st.session_state:
        st.session_state.pahlawan_attempts = 0
    if "pahlawan_game_over" not in st.session_state:
        st.session_state.pahlawan_game_over = False

def reset_game():
    st.session_state.pahlawan_history = []
    st.session_state.pahlawan_score = 0
    st.session_state.pahlawan_attempts = 0
    st.session_state.pahlawan_game_over = False

def save_attempt(nama, tebakan_angka, tebakan_nama, hasil, poin):
    data = {
        "nama": nama,
        "tebakan": f"{tebakan_angka}. {tebakan_nama}",
        "hasil": hasil,
        "poin": poin,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.pahlawan_history.insert(0, data)
    if len(st.session_state.pahlawan_history) > 5:
        st.session_state.pahlawan_history.pop()

def show_tebak_pahlawan():
    init_game_state()
    st.markdown("## 🦅 Game Tebak Pahlawan Nasional")
    st.markdown("Anda hanya diberi **5 kesempatan** menebak. Setiap tebakan benar mendapat +10 poin. Maksimal skor 50.")
    
    user_name = st.text_input("Nama Anda:", value=st.session_state.pahlawan_user_name, key="pahlawan_nama")
    st.session_state.pahlawan_user_name = user_name
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏆 Skor", st.session_state.pahlawan_score)
    with col2:
        sisa = max(0, 5 - st.session_state.pahlawan_attempts)
        st.metric("🎯 Kesempatan Tersisa", sisa)
    with col3:
        st.metric("📊 Tebakan Dilakukan", f"{st.session_state.pahlawan_attempts}/5")
    
    st.markdown("---")
    
    # Tampilkan tombol hanya jika game belum berakhir dan kesempatan masih ada
    if not st.session_state.pahlawan_game_over and st.session_state.pahlawan_attempts < 5:
        st.markdown("### Pilih Pahlawan (tekan tombol):")
        col_a, col_b, col_c = st.columns(3)
        
        def proses_tebakan(tebakan_angka, tebakan_nama):
            # Cegah jika game sudah berakhir atau melebihi batas
            if st.session_state.pahlawan_game_over or st.session_state.pahlawan_attempts >= 5:
                return
            rahasia = random.randint(1, 3)
            rahasia_nama = PAHLAWAN[rahasia]["nama"]
            benar = (tebakan_angka == rahasia)
            poin = 10 if benar else 0
            
            if benar:
                st.session_state.pahlawan_score += poin
            
            hasil = f"Benar! ✅ ({rahasia_nama})" if benar else f"Salah ❌ (Yang benar: {rahasia_nama})"
            save_attempt(user_name, tebakan_angka, tebakan_nama, hasil, poin)
            st.session_state.pahlawan_attempts += 1
            
            if benar:
                st.balloons()
                st.success(f"🎉 Selamat! Tebakan Anda benar: {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
            else:
                st.error(f"❌ Maaf, yang benar adalah {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
            
            if st.session_state.pahlawan_attempts >= 5:
                st.session_state.pahlawan_game_over = True
                st.warning("⚠️ Anda telah menggunakan 5 kesempatan. Game berakhir!")
            
            st.rerun()
        
        with col_a:
            if st.button("1️⃣\nJenderal Sudirman", use_container_width=True):
                proses_tebakan(1, PAHLAWAN[1]["nama"])
        with col_b:
            if st.button("2️⃣\nPangeran Diponegoro", use_container_width=True):
                proses_tebakan(2, PAHLAWAN[2]["nama"])
        with col_c:
            if st.button("3️⃣\nKapten Pattimura", use_container_width=True):
                proses_tebakan(3, PAHLAWAN[3]["nama"])
    
    elif st.session_state.pahlawan_game_over or st.session_state.pahlawan_attempts >= 5:
        st.warning("🏁 Game telah berakhir! Anda sudah menggunakan 5 kesempatan.")
        st.info(f"Skor akhir Anda: {st.session_state.pahlawan_score} dari maksimal 50.")
        if st.button("🔄 Mulai Game Baru", use_container_width=True):
            reset_game()
            st.rerun()
    else:
        st.warning("Game belum dimulai? Silakan refresh atau reset.")
    
    st.markdown("---")
    st.subheader("📜 Riwayat Tebakan (Anda Hanya Bisa Menebak Sebanyak 5 Kali)")
    if st.session_state.pahlawan_history:
        history_data = []
        for h in st.session_state.pahlawan_history:
            history_data.append({
                "Waktu": h["timestamp"],
                "Nama": h["nama"],
                "Tebakan": h["tebakan"],
                "Hasil": h["hasil"],
                "Poin": h["poin"]
            })
        st.dataframe(history_data, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada tebakan. Mulai tebak pahlawan!")
    
    # Tombol reset manual (opsional)
    if st.button("🔄 Reset Game (Mulai dari awal)", use_container_width=True):
        reset_game()
        st.rerun()

if __name__ == "__main__":
    show_tebak_pahlawan()
