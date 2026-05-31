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
    st.markdown("Tebak pahlawan mana yang muncul secara acak. Setiap tebakan benar mendapat +10 poin.")
    
    user_name = st.text_input("Nama Anda:", value=st.session_state.pahlawan_user_name, key="pahlawan_nama")
    st.session_state.pahlawan_user_name = user_name
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏆 Skor Anda", st.session_state.pahlawan_score)
    with col2:
        st.metric("📊 Jumlah Tebakan", len(st.session_state.pahlawan_history))
    
    st.markdown("---")
    st.markdown("### Pilih Pahlawan (tekan tombol):")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("1️⃣\nJenderal Sudirman", use_container_width=True):
            tebakan = 1
            tebakan_nama = PAHLAWAN[1]["nama"]
            rahasia = random.randint(1, 3)
            rahasia_nama = PAHLAWAN[rahasia]["nama"]
            if tebakan == rahasia:
                st.session_state.pahlawan_score += 10
                hasil = f"Benar! ✅ ({rahasia_nama})"
                st.balloons()
                st.success(f"🎉 Selamat! Tebakan Anda benar: {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
                poin = 10
            else:
                hasil = f"Salah ❌ (Yang benar: {rahasia_nama})"
                st.error(f"❌ Maaf, yang benar adalah {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
                poin = 0
            save_attempt(user_name, tebakan, tebakan_nama, hasil, poin)
            st.rerun()
    with col_b:
        if st.button("2️⃣\nPangeran Diponegoro", use_container_width=True):
            tebakan = 2
            tebakan_nama = PAHLAWAN[2]["nama"]
            rahasia = random.randint(1, 3)
            rahasia_nama = PAHLAWAN[rahasia]["nama"]
            if tebakan == rahasia:
                st.session_state.pahlawan_score += 10
                hasil = f"Benar! ✅ ({rahasia_nama})"
                st.balloons()
                st.success(f"🎉 Selamat! Tebakan Anda benar: {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
                poin = 10
            else:
                hasil = f"Salah ❌ (Yang benar: {rahasia_nama})"
                st.error(f"❌ Maaf, yang benar adalah {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
                poin = 0
            save_attempt(user_name, tebakan, tebakan_nama, hasil, poin)
            st.rerun()
    with col_c:
        if st.button("3️⃣\nKapten Pattimura", use_container_width=True):
            tebakan = 3
            tebakan_nama = PAHLAWAN[3]["nama"]
            rahasia = random.randint(1, 3)
            rahasia_nama = PAHLAWAN[rahasia]["nama"]
            if tebakan == rahasia:
                st.session_state.pahlawan_score += 10
                hasil = f"Benar! ✅ ({rahasia_nama})"
                st.balloons()
                st.success(f"🎉 Selamat! Tebakan Anda benar: {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
                poin = 10
            else:
                hasil = f"Salah ❌ (Yang benar: {rahasia_nama})"
                st.error(f"❌ Maaf, yang benar adalah {rahasia_nama}")
                st.info(f"📖 Fakta: {PAHLAWAN[rahasia]['fakta']}")
                poin = 0
            save_attempt(user_name, tebakan, tebakan_nama, hasil, poin)
            st.rerun()
    
    st.markdown("---")
    st.subheader("📜 Riwayat Tebakan (5 terakhir)")
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
        st.info("Belum ada tebakan. Coba tebak pahlawan!")
    
    if st.button("🔄 Reset Skor", use_container_width=True):
        st.session_state.pahlawan_score = 0
        st.session_state.pahlawan_history = []
        st.success("Skor dan riwayat direset!")
        st.rerun()

if __name__ == "__main__":
    show_tebak_pahlawan()
