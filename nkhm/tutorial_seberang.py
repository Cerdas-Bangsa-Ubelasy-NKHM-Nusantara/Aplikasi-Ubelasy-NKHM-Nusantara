# nkhm/seberang_sungai.py
import streamlit as st

# Inisialisasi state permainan
def init_game_state():
    if "river_game" not in st.session_state:
        st.session_state.river_game = {
            "left": {
                "pahlawan": True,
                "tawanan": True,
                "perbekalan": True,
                "anak": True
            },
            "right": {
                "pahlawan": False,
                "tawanan": False,
                "perbekalan": False,
                "anak": False
            },
            "message": "",
            "win": False,
        }

# Cek apakah ada yang melanggar aturan di suatu sisi
def check_violation(side):
    if not side["pahlawan"]:
        if side["tawanan"] and side["perbekalan"]:
            return True
    return False

# Cek kondisi di kedua sisi setelah perjalanan
def check_all_sides():
    state = st.session_state.river_game
    if check_violation(state["left"]):
        state["message"] = "❌ GAGAL! Di sisi awal, tawanan merusak perbekalan!"
        return False
    if check_violation(state["right"]):
        state["message"] = "❌ GAGAL! Di seberang, tawanan merusak perbekalan!"
        return False
    state["message"] = "✅ Aman. Silakan lanjutkan."
    return True

# Cek apakah semua sudah di seberang
def check_win():
    state = st.session_state.river_game
    if (state["right"]["pahlawan"] and state["right"]["tawanan"] and 
        state["right"]["perbekalan"] and state["right"]["anak"]):
        state["win"] = True
        state["message"] = "🎉 SELAMAT! Semua entitas berhasil menyeberang dengan selamat! 🎉"
        return True
    return False

# Fungsi untuk melakukan perjalanan
def travel(entitas):
    state = st.session_state.river_game
    
    if state["win"]:
        state["message"] = "Permainan sudah selesai. Klik 'Reset Permainan' untuk bermain lagi."
        return
    
    # Tentukan arah perjalanan
    if state["left"]["pahlawan"]:
        from_side = "left"
        to_side = "right"
        arah = "Sisi Awal → Seberang"
    elif state["right"]["pahlawan"]:
        from_side = "right"
        to_side = "left"
        arah = "Seberang → Sisi Awal"
    else:
        state["message"] = "❌ ERROR: Pahlawan tidak ditemukan!"
        return
    
    # Kumpulkan entitas yang akan dipindahkan
    to_move = ["pahlawan"]
    if entitas:
        to_move.append(entitas)
    
    # Perahu maksimal 2 entitas
    if len(to_move) > 2:
        state["message"] = f"⚠️ Perahu hanya bisa memuat maksimal 2 entitas!"
        return
    
    # Pastikan entitas ada di sisi asal
    for e in to_move:
        if not state[from_side].get(e, False):
            state["message"] = f"❌ {e.capitalize()} tidak berada di sisi asal!"
            return
    
    # Pindahkan entitas
    for e in to_move:
        state[from_side][e] = False
        state[to_side][e] = True
    
    # Beri pesan sukses
    if len(to_move) == 1:
        state["message"] = f"🚣 {arah}: Pahlawan menyeberang sendirian."
    else:
        nama = "Tawanan" if entitas == "tawanan" else "Perbekalan" if entitas == "perbekalan" else "Anak Buah"
        state["message"] = f"🚣 {arah}: Pahlawan membawa {nama}."
    
    # Cek pelanggaran
    if check_all_sides():
        check_win()
    else:
        # Batalkan perpindahan
        for e in to_move:
            state[from_side][e] = True
            state[to_side][e] = False

# Tombol untuk memilih entitas
def show_buttons():
    state = st.session_state.river_game
    
    if state["win"]:
        st.balloons()
        st.success(state["message"])
        st.markdown("### 🎈 SELAMAT! ANDA BERHASIL! 🎈")
        if st.button("🔄 Main Lagi", key="main_lagi"):
            del st.session_state.river_game
            st.rerun()
        return
    
    # Tentukan arah dan entitas yang tersedia
    if state["left"]["pahlawan"]:
        arah = "🚣 Arah: Sisi Awal → Seberang"
        tersedia = []
        if state["left"]["tawanan"]: tersedia.append("tawanan")
        if state["left"]["perbekalan"]: tersedia.append("perbekalan")
        if state["left"]["anak"]: tersedia.append("anak")
    else:
        arah = "🚣 Arah: Seberang → Sisi Awal"
        tersedia = []
        if state["right"]["tawanan"]: tersedia.append("tawanan")
        if state["right"]["perbekalan"]: tersedia.append("perbekalan")
        if state["right"]["anak"]: tersedia.append("anak")
    
    # Tampilkan arah
    st.info(arah)
    
    # Tombol pilihan
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⛓️ Tawanan", use_container_width=True, disabled=("tawanan" not in tersedia)):
            travel("tawanan")
            st.rerun()
    with col2:
        if st.button("🍞 Perbekalan", use_container_width=True, disabled=("perbekalan" not in tersedia)):
            travel("perbekalan")
            st.rerun()
    with col3:
        if st.button("👤 Anak Buah", use_container_width=True, disabled=("anak" not in tersedia)):
            travel("anak")
            st.rerun()
    
    if st.button("🚣 Sendirian", use_container_width=True):
        travel(None)
        st.rerun()
    
    st.divider()
    
    # Tampilkan peta
    st.markdown("### 🗺️ Peta Penyeberangan")
    
    colA, colRiver, colB = st.columns([2, 1, 2])
    
    with colA:
        st.markdown("**🏝️ SISI AWAL**")
        if state["left"]["pahlawan"]: st.write("- 🦸 Pahlawan")
        if state["left"]["tawanan"]: st.write("- ⛓️ Tawanan")
        if state["left"]["perbekalan"]: st.write("- 🍞 Perbekalan")
        if state["left"]["anak"]: st.write("- 👤 Anak Buah")
        if not any(state["left"].values()): st.write("*Kosong*")
    
    with colRiver:
        st.markdown("### 🌊🌊🌊")
        st.markdown("### 🚣")
        st.markdown("### 🌊🌊🌊")
    
    with colB:
        st.markdown("**🏝️ SEBERANG**")
        if state["right"]["pahlawan"]: st.write("- 🦸 Pahlawan")
        if state["right"]["tawanan"]: st.write("- ⛓️ Tawanan")
        if state["right"]["perbekalan"]: st.write("- 🍞 Perbekalan")
        if state["right"]["anak"]: st.write("- 👤 Anak Buah")
        if not any(state["right"].values()): st.write("*Kosong*")
    
    st.divider()
    
    # Tampilkan pesan
    if state["message"]:
        if "GAGAL" in state["message"]:
            st.error(state["message"])
        elif "SELAMAT" in state["message"]:
            st.success(state["message"])
        else:
            st.info(state["message"])

# Fungsi utama
def show_river_game():
    st.markdown("## 🚣‍♂️ Pahlawan Menyeberang Sungai")
    st.markdown("""
    **Aturan:**
    - Perahu hanya muat **2 entitas** (termasuk pahlawan).
    - **Tawanan dan perbekalan tidak boleh ditinggal berdua tanpa pahlawan.**
    - Tujuan: Pindahkan semua ke seberang.
    """)
    init_game_state()
    show_buttons()
    
    if st.button("🔄 Reset Permainan", use_container_width=True):
        if "river_game" in st.session_state:
            del st.session_state.river_game
        st.rerun()

if __name__ == "__main__":
    show_river_game()