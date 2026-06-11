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
            "boat": [],
            "message": "",
            "win": False,
        }

# Cek apakah ada yang melanggar aturan di suatu sisi
def check_violation(side):
    if not side["pahlawan"]:
        if side["tawanan"] and side["perbekalan"]:
            return "tawanan merusak perbekalan!"
    return None

# Cek kondisi di kedua sisi setelah perjalanan
def check_all_sides():
    state = st.session_state.river_game
    violation_left = check_violation(state["left"])
    if violation_left:
        state["message"] = f"❌ GAGAL! Di sisi awal, {violation_left}"
        return False
    violation_right = check_violation(state["right"])
    if violation_right:
        state["message"] = f"❌ GAGAL! Di seberang, {violation_right}"
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
def travel(entitas1, entitas2):
    state = st.session_state.river_game
    if state["win"]:
        state["message"] = "Permainan sudah selesai. Klik 'Reset Permainan' untuk bermain lagi."
        return
    
    if state["left"]["pahlawan"]:
        from_side = "left"
        to_side = "right"
    elif state["right"]["pahlawan"]:
        from_side = "right"
        to_side = "left"
    else:
        state["message"] = "❌ ERROR: Pahlawan tidak ditemukan!"
        return
    
    to_move = []
    for e in ["pahlawan", entitas1, entitas2]:
        if e:
            to_move.append(e)
    to_move = list(set(to_move))
    
    if len(to_move) > 2:
        state["message"] = "⚠️ Perahu hanya bisa memuat maksimal 2 entitas (termasuk pahlawan)."
        return
    
    for e in to_move:
        if not state[from_side].get(e, False):
            state["message"] = f"❌ {e.capitalize()} tidak berada di sisi {'asal' if from_side=='left' else 'seberang'}!"
            return
    
    for e in to_move:
        state[from_side][e] = False
        state[to_side][e] = True
    
    state["boat"] = to_move
    
    if check_all_sides():
        check_win()
    else:
        for e in to_move:
            state[from_side][e] = True
            state[to_side][e] = False
        state["boat"] = []

# Tombol untuk memilih entitas
def show_buttons():
    state = st.session_state.river_game
    if state["win"]:
        st.success(state["message"])
        if st.button("🔄 Main Lagi", key="main_lagi_seberang"):
            for key in list(st.session_state.keys()):
                if key == "river_game":
                    del st.session_state[key]
            st.rerun()
        return
    
    if state["left"]["pahlawan"]:
        available = [e for e in ["tawanan", "perbekalan", "anak"] if state["left"][e]]
        posisi = "sisi awal"
    else:
        available = [e for e in ["tawanan", "perbekalan", "anak"] if state["right"][e]]
        posisi = "seberang"
    
    nama_entitas = {
        "tawanan": "⛓️ Tawanan Perang",
        "perbekalan": "🍞 Perbekalan Pangan",
        "anak": "👤 Anak Buah"
    }
    
    st.markdown(f"**Pahlawan berada di {posisi} bersama:** " + 
                (", ".join([nama_entitas[e] for e in available]) if available else "tidak ada entitas lain"))
    st.caption("Pilih satu entitas (selain pahlawan) untuk ikut menyeberang. Pahlawan akan selalu ikut.")
    
    if not available:
        st.info("Tidak ada entitas lain di sisi ini. Pahlawan akan menyeberang sendiri.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⛓️ Tawanan Perang", use_container_width=True, disabled=("tawanan" not in available), key="btn_tawanan"):
            travel("tawanan", None)
            st.rerun()
    with col2:
        if st.button("🍞 Perbekalan Pangan", use_container_width=True, disabled=("perbekalan" not in available), key="btn_perbekalan"):
            travel("perbekalan", None)
            st.rerun()
    with col3:
        if st.button("👤 Anak Buah", use_container_width=True, disabled=("anak" not in available), key="btn_anak"):
            travel("anak", None)
            st.rerun()
    
    if st.button("🚣 Sendirian (hanya pahlawan)", use_container_width=True, key="btn_sendiri"):
        travel(None, None)
        st.rerun()
    
    st.divider()
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**🏝️ Sisi Awal**")
        left_items = []
        if state["left"]["pahlawan"]: left_items.append("🦸 Pahlawan")
        if state["left"]["tawanan"]: left_items.append("⛓️ Tawanan")
        if state["left"]["perbekalan"]: left_items.append("🍞 Perbekalan")
        if state["left"]["anak"]: left_items.append("👤 Anak Buah")
        st.write(", ".join(left_items) if left_items else "Kosong")
    with colB:
        st.markdown("**🏝️ Seberang**")
        right_items = []
        if state["right"]["pahlawan"]: right_items.append("🦸 Pahlawan")
        if state["right"]["tawanan"]: right_items.append("⛓️ Tawanan")
        if state["right"]["perbekalan"]: right_items.append("🍞 Perbekalan")
        if state["right"]["anak"]: right_items.append("👤 Anak Buah")
        st.write(", ".join(right_items) if right_items else "Kosong")
    
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
    - Perahu hanya bisa memuat **maksimal 2 entitas** (termasuk pahlawan).
    - **Tawanan perang dan perbekalan pangan tidak boleh ditinggal berdua tanpa pengawasan pahlawan** (tawanan akan merusak perbekalan).
    - Tujuan: memindahkan semua entitas (pahlawan, tawanan, perbekalan, anak buah) ke seberang.
    """)
    init_game_state()
    show_buttons()
    if st.button("🔄 Reset Permainan", use_container_width=True, key="reset_seberang"):
        for key in list(st.session_state.keys()):
            if key == "river_game":
                del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    show_river_game()
