# nkhm/tiang_bendera.py
import streamlit as st

# ========== INISIALISASI STATE ==========
def init_game_state():
    if "tiang_bendera" not in st.session_state:
        st.session_state.tiang_bendera = {
            "A": ["biru", "hijau", "kuning", "merah_putih"],
            "B": [],
            "C": [],
            "selected": None,
            "message": "",
            "win": False,
            "moves": 0,
        }

# ========== CEK KONDISI MENANG ==========
def check_win():
    state = st.session_state.tiang_bendera
    goal = ["biru", "kuning", "hijau", "merah_putih"]
    if state["C"] == goal:
        state["win"] = True
        state["message"] = "🎉 SELAMAT! Anda berhasil memindahkan semua cakram dan bendera ke tiang C! 🎉"
        return True
    return False

# ========== ATURAN PERMAINAN ==========
def is_valid_move(from_tower, to_tower):
    state = st.session_state.tiang_bendera
    if not state[from_tower]:
        return False, "Tiang asal kosong!"
    top_from = state[from_tower][-1]
    if not state[to_tower]:
        return True, ""
    top_to = state[to_tower][-1]
    size_order = {"merah_putih": 1, "kuning": 2, "hijau": 3, "biru": 4}
    if size_order[top_from] < size_order[top_to]:
        return True, ""
    return False, f"Cakram {top_from} tidak boleh diletakkan di atas {top_to}!"

# ========== PROSES PERPINDAHAN ==========
def move_disk(from_tower, to_tower):
    state = st.session_state.tiang_bendera
    if state["win"]:
        return
    valid, msg = is_valid_move(from_tower, to_tower)
    if not valid:
        state["message"] = f"❌ {msg}"
        return
    disk = state[from_tower].pop()
    state[to_tower].append(disk)
    state["moves"] += 1
    state["message"] = f"✅ Memindahkan {disk} dari tiang {from_tower} ke tiang {to_tower}"
    state["selected"] = None
    check_win()

# ========== RESET PERMAINAN ==========
def reset_game():
    if "tiang_bendera" in st.session_state:
        del st.session_state.tiang_bendera
    init_game_state()

# ========== FUNGSI MENAMPILKAN TIANG ==========
def draw_tower(tower_name, disks):
    disk_icons = {"biru": "🔵", "hijau": "🟢", "kuning": "🟡", "merah_putih": "🚩"}
    st.markdown(f"### 🏗️ Tiang {tower_name}")
    if not disks:
        st.markdown("*Kosong*")
    else:
        for disk in disks:
            icon = disk_icons.get(disk, "⬤")
            st.markdown(f"{icon} {disk.capitalize()}")
    st.markdown("⬇️ **|**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📥 Ambil dari {tower_name}", key=f"take_{tower_name}", use_container_width=True):
            state = st.session_state.tiang_bendera
            if state["win"]:
                state["message"] = "Permainan sudah selesai! Klik Reset untuk bermain lagi."
            elif state["selected"] == tower_name:
                state["selected"] = None
                state["message"] = f"Batal memilih tiang {tower_name}"
            elif state["selected"] is None:
                if state[tower_name]:
                    state["selected"] = tower_name
                    state["message"] = f"Tiang {tower_name} dipilih. Klik tiang tujuan untuk meletakkan."
                else:
                    state["message"] = f"Tiang {tower_name} kosong!"
            else:
                move_disk(state["selected"], tower_name)
            st.rerun()
    
    with col2:
        if st.button(f"📤 Letakkan ke {tower_name}", key=f"place_{tower_name}", use_container_width=True):
            state = st.session_state.tiang_bendera
            if state["win"]:
                state["message"] = "Permainan sudah selesai! Klik Reset untuk bermain lagi."
            elif state["selected"] is not None:
                move_disk(state["selected"], tower_name)
            else:
                state["message"] = "Pilih tiang asal terlebih dahulu (klik 'Ambil dari ...')"
            st.rerun()

# ========== FUNGSI UTAMA ==========
def show_tiang_bendera():
    st.markdown("## 🏗️ Permainan Tiang & Bendera Merah Putih")
    st.markdown("""
    **Aturan:**
    - Ada 3 tiang: **A**, **B**, dan **C**.
    - Tiang A memiliki 3 cakram (biru 🔵, hijau 🟢, kuning 🟡) dan bendera merah putih 🚩 di atasnya.
    - Tujuan: "Merdeka", pindahkan semua cakram dan bendera ke tiang **C** dengan susunan: biru → kuning → hijau → merah putih.
    - **Aturan:** Cakram yang lebih kecil tidak boleh berada di bawah cakram yang lebih besar.
    - **Langkah:** Klik "Ambil dari [tiang]" lalu "Letakkan ke [tiang]".
    """)
    
    init_game_state()
    state = st.session_state.tiang_bendera
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Langkah", state["moves"])
    with col2:
        status = "✅ Selesai" if state["win"] else "🔄 Berjalan"
        st.metric("📊 Status", status)
    with col3:
        if st.button("🔄 Reset Permainan", use_container_width=True):
            reset_game()
            st.rerun()
    
    st.markdown("---")
    
    if state["message"]:
        if "SELAMAT" in state["message"]:
            st.success(state["message"])
        elif "❌" in state["message"]:
            st.error(state["message"])
        else:
            st.info(state["message"])
    
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        draw_tower("A", state["A"])
    with col_b:
        draw_tower("B", state["B"])
    with col_c:
        draw_tower("C", state["C"])
    
    st.markdown("---")
    st.caption("💡 Urutan ukuran (kecil ke besar): Bendera 🚩 → Kuning 🟡 → Hijau 🟢 → Biru 🔵")
    
    if state["win"]:
        st.balloons()
        st.success("🎉 SELAMAT! Anda berhasil menyelesaikan permainan! 🎉")

if __name__ == "__main__":
    show_tiang_bendera()
