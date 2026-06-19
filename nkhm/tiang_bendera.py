# nkhm/tiang_bendera.py
import streamlit as st

# ========== INISIALISASI STATE ==========
def init_game_state():
    if "tiang_bendera" not in st.session_state:
        st.session_state.tiang_bendera = {
            # Susunan dari BAWAH ke ATAS: Biru (bawah), Kuning, Hijau, Merah Putih (atas)
            # Artinya dari atas ke bawah: Merah Putih → Hijau → Kuning → Biru
            "A": ["biru", "kuning", "hijau", "merah_putih"],
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
    # Goal: tiang C berisi ["biru", "hijau", "kuning", "merah_putih"] (bawah ke atas)
    # Artinya dari atas ke bawah: Merah Putih → Kuning → Hijau → Biru
    goal = ["biru", "hijau", "kuning", "merah_putih"]
    if state["C"] == goal:
        state["win"] = True
        state["message"] = "🎉 SELAMAT! Anda berhasil memindahkan semua cakram dan bendera ke tiang C! 🎉"
        return True
    return False

# ========== ATURAN PERMAINAN ==========
def is_valid_move(from_tower, to_tower):
    state = st.session_state.tiang_bendera
    if not state[from_tower]:
        return False, "❌ Tiang asal kosong!"
    top_from = state[from_tower][-1]
    if not state[to_tower]:
        return True, ""
    top_to = state[to_tower][-1]
    # Urutan ukuran (dari kecil ke besar): merah_putih (1), kuning (2), hijau (3), biru (4)
    size_order = {"merah_putih": 1, "kuning": 2, "hijau": 3, "biru": 4}
    if size_order[top_from] < size_order[top_to]:
        return True, ""
    return False, f"❌ {top_from.capitalize()} tidak boleh diletakkan di atas {top_to.capitalize()}!"

# ========== PROSES PERPINDAHAN ==========
def move_disk(from_tower, to_tower):
    state = st.session_state.tiang_bendera
    if state["win"]:
        return
    valid, msg = is_valid_move(from_tower, to_tower)
    if not valid:
        state["message"] = msg
        return
    disk = state[from_tower].pop()
    state[to_tower].append(disk)
    state["moves"] += 1
    state["message"] = f"✅ Memindahkan {disk.capitalize()} dari tiang {from_tower} ke tiang {to_tower}"
    state["selected"] = None
    check_win()

# ========== RESET PERMAINAN ==========
def reset_game():
    if "tiang_bendera" in st.session_state:
        del st.session_state.tiang_bendera
    init_game_state()

# ========== FUNGSI MENAMPILKAN TIANG ==========
def draw_tower(tower_name, disks):
    disk_icons = {
        "biru": "🔵",
        "kuning": "🟡",
        "hijau": "🟢",
        "merah_putih": "🚩"
    }
    
    st.markdown(f"### 🏗️ Tiang {tower_name}")
    
    if not disks:
        st.markdown("*Kosong*")
    else:
        # Tampilkan dari ATAS ke BAWAH (agar visual sesuai)
        for disk in reversed(disks):
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
                    state["message"] = f"❌ Tiang {tower_name} kosong!"
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
                state["message"] = "❌ Pilih tiang asal terlebih dahulu (klik 'Ambil dari ...')"
            st.rerun()

# ========== FUNGSI UTAMA ==========
def show_tiang_bendera():
    st.markdown("## 🏗️ Permainan Tiang & Bendera")
    st.markdown("""
    **🎯 Tujuan:** Pindahkan semua cakram dan bendera ke tiang **C**.
    
    **📦 Susunan Awal (Tiang A - dari atas ke bawah):**
    🚩 Merah Putih → 🟢 Hijau → 🟡 Kuning → 🔵 Biru
    
    **🎯 Susunan Akhir (Tiang C - dari atas ke bawah):**
    🚩 Merah Putih → 🟡 Kuning → 🟢 Hijau → 🔵 Biru
    
    **📋 Aturan:**
    1. Hanya satu cakram yang bisa dipindahkan dalam satu langkah.
    2. Cakram yang lebih besar TIDAK boleh diletakkan di atas cakram yang lebih kecil.
    3. 🚩 Bendera adalah yang terkecil, 🔵 Biru adalah yang terbesar.
    4. 🟡 Kuning boleh diletakkan di atas 🟢 Hijau (karena Kuning lebih kecil dari Hijau).
    5. Anda bisa memindahkan cakram teratas dari satu tiang ke tiang lain.
    
    **💡 Cara Bermain:**
    1. Klik **"Ambil dari [tiang]"** untuk mengambil cakram paling atas.
    2. Klik **"Letakkan ke [tiang]"** untuk memindahkan ke tiang tujuan.
    3. Klik **"Reset Permainan"** untuk memulai dari awal.
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
        st.caption("📍 Tiang A (Awal)")
    with col_b:
        draw_tower("B", state["B"])
        st.caption("📍 Tiang B (Bantuan)")
    with col_c:
        draw_tower("C", state["C"])
        st.caption("📍 Tiang C (Tujuan)")
    
    st.markdown("---")
    st.markdown("**🔢 Urutan Ukuran (dari kecil ke besar):**")
    st.markdown("🚩 Merah Putih → 🟡 Kuning → 🟢 Hijau → 🔵 Biru")
    
    if state["win"]:
        st.balloons()
        st.success("🎉 **SELAMAT! Anda berhasil menyelesaikan permainan!** 🎉")
        st.markdown("""
        **✅ Goal State tercapai!**  
        Tiang C sekarang berisi (dari bawah ke atas):  
        🔵 Biru → 🟢 Hijau → 🟡 Kuning → 🚩 Merah Putih
        
        **(dari atas ke bawah):**  
        🚩 Merah Putih → 🟡 Kuning → 🟢 Hijau → 🔵 Biru
        """)

if __name__ == "__main__":
    show_tiang_bendera()
