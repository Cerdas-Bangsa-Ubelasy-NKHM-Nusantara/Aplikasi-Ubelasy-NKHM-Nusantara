# nkhm/seberang_sungai.py
import streamlit as st

# ========== STATE PERMANEN (SKOR HANYA SEKALI) ==========
def init_permanent_state():
    if "seberang_score" not in st.session_state:
        st.session_state.seberang_score = 0
    if "seberang_has_played" not in st.session_state:
        st.session_state.seberang_has_played = False

# ========== STATE PERMAINAN (POSISI, PELANGGARAN) ==========
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
            "last_direction": None,
            "game_over": False,
            "violated_rule2": False,
        }

def reset_game():
    if "river_game" in st.session_state:
        del st.session_state.river_game
    init_game_state()

# ========== FUNGSI PENGECEKAN ==========
def check_violation_type(side):
    if not side["pahlawan"]:
        if side["tawanan"] and side["perbekalan"]:
            return "rule1"
    return None

def check_rule2_violation(side):
    if not side["pahlawan"]:
        if side["tawanan"] and side["anak"]:
            return True
    return False

# ========== PESAN-PESAN ==========
def get_failure_rule1_message(location):
    if location == "awal":
        return """
❌ GAGAL! Di sisi awal, tawanan merusak perbekalan, atau tawanan dan anak buah bertarung duel!

😔 **KARAKTER PAHLAWAN YANG CEROBOH DAN EGOIS** 😔
Pahlawan ini terlalu terburu-buru meninggalkan tawanan bersama perbekalan tanpa pengawasan.
Akibatnya, tawanan merusak perbekalan yang sangat berharga untuk perjalanan.
Seorang pahlawan sejati harus memikirkan konsekuensi dari setiap keputusan.
Jangan tinggalkan situasi berbahaya tanpa pengawasan!
*"Kecerobohan adalah musuh terbesar seorang pemimpin. Selalu pikirkan risiko sebelum bertindak."*

😔 **KARAKTER PAHLAWAN YANG TIDAK SIAGA** 😔
Pahlawan ini meninggalkan tawanan bersama anak buahnya tanpa pengawasan.
Akibatnya, terjadi duel antara tawanan dan anak buah yang berakhir dengan cedera di kedua belah pihak.
Seorang pemimpin harus selalu hadir untuk mencegah konflik di antara anggota timnya.
Kehadiran pemimpin adalah perekat yang menjaga keharmonisan tim.
*"Seorang pemimpin harus selalu hadir untuk mencegah perselisihan di antara anak buahnya."*

😔 **KARAKTER PAHLAWAN YANG TIDAK STRATEGIS** 😔
Pahlawan ini juga memilih meninggalkan tawanan bersama perbekalan tanpa pengawasan.
Tawanan yang tidak diawasi segera merusak perbekalan yang sangat berharga.
Seorang pemimpin strategis akan memprioritaskan 'ancaman terbesar' terlebih dahulu.
Tawanan adalah entitas paling berbahaya yang harus selalu diawasi atau dipindahkan pertama kali.
*"Prioritaskan yang paling berbahaya terlebih dahulu. Jangan biarkan ancaman menguasai situasi."*
"""
    else:
        return """
❌ GAGAL! Di seberang, tawanan merusak perbekalan!

😔 **KARAKTER PAHLAWAN YANG CEROBOH** 😔
Pahlawan ini terlalu terburu-buru meninggalkan tawanan bersama perbekalan tanpa pengawasan.
Akibatnya, tawanan merusak perbekalan yang sangat berharga untuk perjalanan.
Seorang pahlawan sejati harus memikirkan konsekuensi dari setiap keputusan.
Jangan tinggalkan situasi berbahaya tanpa pengawasan!
*"Kecerobohan adalah musuh terbesar seorang pemimpin. Selalu pikirkan risiko sebelum bertindak."*
"""

def get_rule2_violation_message(location):
    if location == "awal":
        return "⚠️ PERINGATAN: Di sisi awal, tawanan dan anak buah ditinggal berdua! (aturan ke-2 dilanggar, tetapi permainan lanjut)"
    else:
        return "⚠️ PERINGATAN: Di seberang, tawanan dan anak buah ditinggal berdua! (aturan ke-2 dilanggar, tetapi permainan lanjut)"

def get_failure_first_step_anak_message():
    return """
❌ GAGAL! Anda membawa Anak Buah terlebih dahulu!

😔 **KARAKTER PAHLAWAN YANG TIDAK STRATEGIS** 😔
Pahlawan ini memilih membawa anak buah terlebih dahulu, meninggalkan tawanan bersama perbekalan.
Tawanan yang tidak diawasi segera merusak perbekalan yang sangat berharga.
Seorang pemimpin strategis akan memprioritaskan 'ancaman terbesar' terlebih dahulu.
Tawanan adalah entitas paling berbahaya yang harus selalu diawasi atau dipindahkan pertama kali.
*"Prioritaskan yang paling berbahaya terlebih dahulu. Jangan biarkan ancaman menguasai situasi."*
"""

def get_first_step_perbekalan_warning():
    return """
⚠️ PERINGATAN! Anda membawa Perbekalan terlebih dahulu. Ini melanggar aturan ke-2, tetapi permainan tetap lanjut.
😔 Namun, Anda telah mencatat pelanggaran. Jika tetap berhasil menyelesaikan, Anda TIDAK akan mendapat poin.
"""

def get_first_step_sendiri_warning():
    return """
⚠️ PERINGATAN! Anda menyeberang sendirian di langkah pertama. Ini melanggar aturan ke-2, tetapi permainan tetap lanjut.
😔 Namun, Anda telah mencatat pelanggaran. Jika tetap berhasil menyelesaikan, Anda TIDAK akan mendapat poin.
"""

def get_success_normal_message(is_first_game):
    if is_first_game:
        return """
🎉 SELAMAT! Anda berhasil menyeberangkan semua entitas dengan selamat! 🎉

🏆 Anda mendapatkan 10 POIN! 🏆

🌟 **KARAKTER PAHLAWAN YANG BIJAKSANA** 🌟
Seorang pahlawan sejati tidak hanya mengandalkan kekuatan fisik, tetapi juga kebijaksanaan dan strategi.
Dengan merencanakan setiap langkah, mempertimbangkan risiko, dan melindungi semua yang menjadi tanggung jawabnya,
pahlawan ini menunjukkan bahwa kepemimpinan sejati adalah tentang menjaga keseimbangan dan keselamatan semua pihak.
*"Kebijaksanaan lebih berharga daripada kekuatan. Seorang pemimpin yang baik melindungi semua yang dipimpinnya."*
"""
    else:
        return """
🎉 SELAMAT! Semua entitas berhasil menyeberang dengan selamat! 🎉

📝 Ini adalah permainan latihan. Skor tetap = {} poin.

🌟 **KARAKTER PAHLAWAN YANG BIJAKSANA** 🌟
...""".format(st.session_state.seberang_score)

def get_success_tricked_message():
    return """
🎉 CURANG! Meski Anda berhasil menyeberangkan semua entitas dengan selamat, namun Anda telah melanggar aturan ke-2! 🎉

🏆 Anda tidak dapat POIN! 🏆

🌟 **KARAKTER PAHLAWAN YANG TERKECOH** 🌟
Pahlawan ini memang berhasil mencapai tujuan, tetapi dengan cara yang ceroboh karena meninggalkan tawanan bersama anak buah tanpa pengawasan (meski tidak berakibat fatal kali ini).
Seorang pemimpin sejati tidak hanya fokus pada hasil akhir, tetapi juga pada proses dan keselamatan semua pihak sepanjang perjalanan.
Pelanggaran aturan menunjukkan kelemahan dalam strategi dan kewaspadaan. Untuk mendapatkan poin, cobalah lagi dengan mematuhi semua aturan!
*"Kemenangan tanpa integritas hanyalah kemenangan semu. Patuhi setiap aturan untuk menjadi pahlawan sejati."*
"""

# ========== PROSES PERJALANAN ==========
def check_all_sides():
    state = st.session_state.river_game
    v_left = check_violation_type(state["left"])
    if v_left:
        state["message"] = get_failure_rule1_message("awal")
        state["game_over"] = True
        return False
    if check_rule2_violation(state["left"]):
        state["violated_rule2"] = True
        state["message"] = get_rule2_violation_message("awal")
    v_right = check_violation_type(state["right"])
    if v_right:
        state["message"] = get_failure_rule1_message("seberang")
        state["game_over"] = True
        return False
    if check_rule2_violation(state["right"]):
        state["violated_rule2"] = True
        state["message"] = get_rule2_violation_message("seberang")
    if not state["message"] or "Peringatan" not in state["message"]:
        state["message"] = "✅ Aman. Silakan lanjut pilih (tekan tombol) entitas."
    return True

def check_win():
    state = st.session_state.river_game
    if (state["right"]["pahlawan"] and state["right"]["tawanan"] and 
        state["right"]["perbekalan"] and state["right"]["anak"]):
        state["win"] = True
        state["game_over"] = True
        if not st.session_state.seberang_has_played:
            if not state["violated_rule2"]:
                st.session_state.seberang_score = 10
                st.session_state.seberang_has_played = True
                state["message"] = get_success_normal_message(True)
            else:
                st.session_state.seberang_has_played = True
                state["message"] = get_success_tricked_message()
        else:
            if state["violated_rule2"]:
                state["message"] = get_success_tricked_message() + "\n\n📝 (Ini permainan latihan, skor tetap)"
            else:
                state["message"] = get_success_normal_message(False)
        return True
    return False

def travel(entitas1, entitas2):
    state = st.session_state.river_game
    if state["win"] or state["game_over"]:
        state["message"] = "Permainan sudah selesai. Klik 'Reset Permainan' untuk bermain lagi."
        return
    if state["left"]["pahlawan"]:
        from_side = "left"
        to_side = "right"
        arah = "Dari Sisi Awal → Seberang"
    elif state["right"]["pahlawan"]:
        from_side = "right"
        to_side = "left"
        arah = "Dari Seberang → Sisi Awal"
    else:
        state["message"] = "❌ ERROR: Pahlawan tidak ditemukan!"
        return
    to_move = []
    for e in ["pahlawan", entitas1, entitas2]:
        if e:
            to_move.append(e)
    to_move = list(set(to_move))
    if len(to_move) > 2:
        state["message"] = f"⚠️ Perahu hanya bisa memuat maksimal 2 entitas (termasuk pahlawan). {arah} dibatalkan."
        return
    for e in to_move:
        if not state[from_side].get(e, False):
            state["message"] = f"❌ {e.capitalize()} tidak berada di sisi {'asal' if from_side=='left' else 'seberang'}! {arah} dibatalkan."
            return
    is_first_step = (state["left"]["pahlawan"] and state["left"]["tawanan"] and 
                     state["left"]["perbekalan"] and state["left"]["anak"] and 
                     not any(state["right"].values()))
    if is_first_step:
        if entitas1 == "anak":
            state["message"] = get_failure_first_step_anak_message()
            state["game_over"] = True
            return
        elif entitas1 == "perbekalan":
            state["violated_rule2"] = True
            state["message"] = get_first_step_perbekalan_warning()
        elif entitas1 is None:
            state["violated_rule2"] = True
            state["message"] = get_first_step_sendiri_warning()
    state["last_direction"] = arah
    for e in to_move:
        state[from_side][e] = False
        state[to_side][e] = True
    state["boat"] = to_move
    if len(to_move) == 1:
        state["message"] = f"🚣 {arah}: Pahlawan menyeberang sendirian."
    else:
        nama_entitas = []
        for e in to_move:
            if e == "tawanan": nama_entitas.append("Tawanan")
            elif e == "perbekalan": nama_entitas.append("Perbekalan")
            elif e == "anak": nama_entitas.append("Anak Buah")
        state["message"] = f"🚣 {arah}: Pahlawan membawa {', '.join(nama_entitas)}."
    if check_all_sides():
        check_win()
    else:
        if "GAGAL" in state["message"]:
            for e in to_move:
                state[from_side][e] = True
                state[to_side][e] = False
            state["boat"] = []
            state["last_direction"] = None

def show_buttons():
    state = st.session_state.river_game
    if st.session_state.seberang_has_played:
        st.metric("🏆 Skor Resmi", f"{st.session_state.seberang_score} / 10")
    else:
        st.metric("🏆 Skor", "Belum ada (permainan pertama)")
    if state["win"] or state["game_over"]:
        if state["win"]:
            st.balloons()
            st.success(state["message"])
        else:
            st.error(state["message"])
        if st.button("🔄 Main Lagi", key="main_lagi_seberang"):
            reset_game()
            st.rerun()
        return
    if state["left"]["pahlawan"]:
        arah_yang_akan_datang = "🚣 Arah: Sisi Awal → Seberang"
        available = [e for e in ["tawanan", "perbekalan", "anak"] if state["left"][e]]
    else:
        arah_yang_akan_datang = "🚣 Arah: Seberang → Sisi Awal"
        available = [e for e in ["tawanan", "perbekalan", "anak"] if state["right"][e]]
    st.info(arah_yang_akan_datang)
    nama_entitas = {
        "tawanan": "⛓️ Tawanan Perang",
        "perbekalan": "🍞 Perbekalan Pangan",
        "anak": "👤 Anak Buah"
    }
    st.markdown(f"**Pahlawan siap menyeberang. Pilih siapa (entitas) yang akan dibawa:**")
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
    st.markdown("### 🗺️ Peta Penyeberangan")
    colA, colRiver, colB = st.columns([2, 1, 2])
    with colA:
        st.markdown("**🏝️ SISI AWAL**")
        left_items = []
        if state["left"]["pahlawan"]: left_items.append("🦸 Pahlawan")
        if state["left"]["tawanan"]: left_items.append("⛓️ Tawanan")
        if state["left"]["perbekalan"]: left_items.append("🍞 Perbekalan")
        if state["left"]["anak"]: left_items.append("👤 Anak Buah")
        if left_items:
            for item in left_items:
                st.markdown(f"- {item}")
        else:
            st.markdown("*Kosong*")
    with colRiver:
        st.markdown("### 🌊🌊🌊")
        st.markdown("### 🚣‍♂️")
        st.markdown("### 🌊🌊🌊")
        st.caption("Sungai")
    with colB:
        st.markdown("**🏝️ SEBERANG**")
        right_items = []
        if state["right"]["pahlawan"]: right_items.append("🦸 Pahlawan")
        if state["right"]["tawanan"]: right_items.append("⛓️ Tawanan")
        if state["right"]["perbekalan"]: right_items.append("🍞 Perbekalan")
        if state["right"]["anak"]: right_items.append("👤 Anak Buah")
        if right_items:
            for item in right_items:
                st.markdown(f"- {item}")
        else:
            st.markdown("*Kosong*")
    st.divider()
    if not state["game_over"] and state["message"]:
        if "Peringatan" in state["message"]:
            st.warning(state["message"])
        else:
            st.info(state["message"])

def show_river_game():
    init_permanent_state()
    init_game_state()
    st.markdown("## 🚣‍♂️ Pahlawan Menyeberang Sungai")
    st.markdown("""
    **Aturan:**
    - Perahu hanya bisa memuat **maksimal 2 entitas** (termasuk pahlawan).
    - **Tawanan perang dan perbekalan pangan tidak boleh ditinggal berdua tanpa pengawasan pahlawan** (aturan 1) → LANGSUNG GAGAL.
    - **Tawanan dan Anak Buah tidak boleh ditinggal berdua tanpa bersama pahlawan** (aturan 2) → TIDAK GAGAL, tetapi dicatat. Jika aturan 2 dilanggar, Anda TIDAK akan mendapat poin meskipun berhasil menyelesaikan permainan.
    - **Langkah pertama HARUS membawa Tawanan**? Tidak harus. Jika membawa Perbekalan atau Sendirian, Anda melanggar aturan 2 (tidak gagal). Membawa Anak langsung gagal (aturan 1).
    - **Poin:** Berhasil menyelesaikan permainan pada **permainan pertama** mendapat **10 poin**, **ASALKAN tidak pernah melanggar aturan ke-2**. Jika melanggar aturan ke-2, tetap berhasil tetapi tidak mendapat poin (terkecoh). Permainan berikutnya hanya latihan (skor tetap).
    - Tujuan: memindahkan semua entitas (pahlawan, tawanan, perbekalan, anak buah) ke seberang.
    
    > **💡 Petunjuk:** Perhatikan arah panah di atas tombol. Itu menunjukkan arah perjalanan yang akan terjadi.
    """)
    show_buttons()
    if st.button("🔄 Reset Permainan", use_container_width=True, key="reset_seberang"):
        reset_game()
        st.rerun()

if __name__ == "__main__":
    show_river_game()