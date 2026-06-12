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
            "last_direction": None,
            "score": 0,
            "has_played": False,
            "game_over": False,
        }

# Cek jenis pelanggaran (kembalikan kode)
def check_violation_type(side):
    if not side["pahlawan"]:
        if side["tawanan"] and side["perbekalan"]:
            return "rule1"  # tawanan + perbekalan
        if side["tawanan"] and side["anak"]:
            return "rule2"  # tawanan + anak
    return None

# Pesan untuk kegagalan aturan 1 di sisi awal/seberang
def get_failure_rule1_message(location):
    if location == "awal":
        return """
❌ GAGAL! Di sisi awal, tawanan merusak perbekalan!

😔 **KARAKTER PAHLAWAN YANG CEROBOH** 😔
Pahlawan ini terlalu terburu-buru meninggalkan tawanan bersama perbekalan tanpa pengawasan.
Akibatnya, tawanan merusak perbekalan yang sangat berharga untuk perjalanan.
Seorang pahlawan sejati harus memikirkan konsekuensi dari setiap keputusan.
Jangan tinggalkan situasi berbahaya tanpa pengawasan!
*"Kecerobohan adalah musuh terbesar seorang pemimpin. Selalu pikirkan risiko sebelum bertindak."*
"""
    else:  # seberang
        return """
❌ GAGAL! Di seberang, tawanan merusak perbekalan!

😔 **KARAKTER PAHLAWAN YANG CEROBOH** 😔
Pahlawan ini terlalu terburu-buru meninggalkan tawanan bersama perbekalan tanpa pengawasan.
Akibatnya, tawanan merusak perbekalan yang sangat berharga untuk perjalanan.
Seorang pahlawan sejati harus memikirkan konsekuensi dari setiap keputusan.
Jangan tinggalkan situasi berbahaya tanpa pengawasan!
*"Kecerobohan adalah musuh terbesar seorang pemimpin. Selalu pikirkan risiko sebelum bertindak."*
"""

# Pesan untuk kegagalan aturan 2 di sisi awal/seberang
def get_failure_rule2_message(location):
    if location == "awal":
        return """
❌ GAGAL! Di sisi awal, tawanan dan anak buah bertarung duel!

😔 **KARAKTER PAHLAWAN YANG TIDAK SIAGA** 😔
Pahlawan ini meninggalkan tawanan bersama anak buahnya tanpa pengawasan.
Akibatnya, terjadi duel antara tawanan dan anak buah yang berakhir dengan cedera di kedua belah pihak.
Seorang pemimpin harus selalu hadir untuk mencegah konflik di antara anggota timnya.
Kehadiran pemimpin adalah perekat yang menjaga keharmonisan tim.
*"Seorang pemimpin harus selalu hadir untuk mencegah perselisihan di antara anak buahnya."*
"""
    else:
        return """
❌ GAGAL! Di seberang, tawanan dan anak buah bertarung duel!

😔 **KARAKTER PAHLAWAN YANG TIDAK SIAGA** 😔
Pahlawan ini meninggalkan tawanan bersama anak buahnya tanpa pengawasan.
Akibatnya, terjadi duel antara tawanan dan anak buah yang berakhir dengan cedera di kedua belah pihak.
Seorang pemimpin harus selalu hadir untuk mencegah konflik di antara anggota timnya.
Kehadiran pemimpin adalah perekat yang menjaga keharmonisan tim.
*"Seorang pemimpin harus selalu hadir untuk mencegah perselisihan di antara anak buahnya."*
"""

# Pesan untuk langkah pertama salah (bawa Anak Buah)
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

# Pesan untuk langkah pertama salah (bawa Perbekalan)
def get_failure_first_step_perbekalan_message():
    return """
❌ GAGAL! Di sisi awal, tawanan dan anak buah bertarung duel!

😔 **KARAKTER PAHLAWAN YANG TIDAK SIAGA** 😔
Pahlawan ini meninggalkan tawanan bersama anak buahnya tanpa pengawasan.
Akibatnya, terjadi duel antara tawanan dan anak buah yang berakhir dengan cedera di kedua belah pihak.
Seorang pemimpin harus selalu hadir untuk mencegah konflik di antara anggota timnya.
Kehadiran pemimpin adalah perekat yang menjaga keharmonisan tim.
*"Seorang pemimpin harus selalu hadir untuk mencegah perselisihan di antara anak buahnya."*
"""

# Pesan untuk langkah pertama salah (sendirian) – gabungan
def get_failure_first_step_sendiri_message():
    return """
❌ GAGAL! Di sisi awal, tawanan dan anak buah bertarung duel!, atau tawanan merusak perbekalan pangan!

😔 **KARAKTER PAHLAWAN YANG TIDAK SIAGA** DAN **TIDAK STRATEGIS** 😔
Pahlawan ini meninggalkan tawanan bersama anak buahnya tanpa pengawasan.
Akibatnya, terjadi duel antara tawanan dan anak buah yang berakhir dengan cedera di kedua belah pihak.
Seorang pemimpin harus selalu hadir untuk mencegah konflik di antara anggota timnya.
Kehadiran pemimpin adalah perekat yang menjaga keharmonisan tim.
*"Seorang pemimpin harus selalu hadir untuk mencegah perselisihan di antara anak buahnya."*

😔 Pahlawan ini juga memilih meninggalkan tawanan bersama perbekalan tanpa pengawasan.
Tawanan yang tidak diawasi segera merusak perbekalan yang sangat berharga.
Seorang pemimpin strategis akan memprioritaskan 'ancaman terbesar' terlebih dahulu.
Tawanan adalah entitas paling berbahaya yang harus selalu diawasi atau dipindahkan pertama kali.
*"Prioritaskan yang paling berbahaya terlebih dahulu. Jangan biarkan ancaman menguasai situasi."*
"""

# Pesan sukses
def get_success_message(is_first_game):
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

📝 Ini adalah permainan latihan. Skor tetap = """ + str(st.session_state.river_game["score"]) + """ poin.

🌟 **KARAKTER PAHLAWAN YANG BIJAKSANA** 🌟
Seorang pahlawan sejati tidak hanya mengandalkan kekuatan fisik, tetapi juga kebijaksanaan dan strategi.
Dengan merencanakan setiap langkah, mempertimbangkan risiko, dan melindungi semua yang menjadi tanggung jawabnya,
pahlawan ini menunjukkan bahwa kepemimpinan sejati adalah tentang menjaga keseimbangan dan keselamatan semua pihak.
*"Kebijaksanaan lebih berharga daripada kekuatan. Seorang pemimpin yang baik melindungi semua yang dipimpinnya."*
"""

# Cek kondisi di kedua sisi setelah perjalanan
def check_all_sides():
    state = st.session_state.river_game
    # Cek sisi kiri
    v_left = check_violation_type(state["left"])
    if v_left:
        if v_left == "rule1":
            state["message"] = get_failure_rule1_message("awal")
        else:
            state["message"] = get_failure_rule2_message("awal")
        state["game_over"] = True
        return False
    # Cek sisi kanan
    v_right = check_violation_type(state["right"])
    if v_right:
        if v_right == "rule1":
            state["message"] = get_failure_rule1_message("seberang")
        else:
            state["message"] = get_failure_rule2_message("seberang")
        state["game_over"] = True
        return False
    state["message"] = "✅ Aman. Silakan lanjutkan."
    return True

# Cek apakah semua sudah di seberang
def check_win():
    state = st.session_state.river_game
    if (state["right"]["pahlawan"] and state["right"]["tawanan"] and 
        state["right"]["perbekalan"] and state["right"]["anak"]):
        state["win"] = True
        state["game_over"] = True
        if not state["has_played"]:
            state["score"] = 10
            state["has_played"] = True
            state["message"] = get_success_message(True)
        else:
            state["message"] = get_success_message(False)
        return True
    return False

# Fungsi untuk melakukan perjalanan (menyeberang)
def travel(entitas1, entitas2):
    state = st.session_state.river_game
    
    if state["win"] or state["game_over"]:
        state["message"] = "Permainan sudah selesai. Klik 'Reset Permainan' untuk bermain lagi."
        return
    
    # Tentukan arah perjalanan
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
    
    # Pengecekan langkah pertama
    is_first_step = (state["left"]["pahlawan"] and state["left"]["tawanan"] and 
                     state["left"]["perbekalan"] and state["left"]["anak"] and 
                     not any(state["right"].values()))
    
    if is_first_step and entitas1 != "tawanan":
        if entitas1 == "anak":
            state["message"] = get_failure_first_step_anak_message()
        elif entitas1 == "perbekalan":
            state["message"] = get_failure_first_step_perbekalan_message()
        else:  # sendirian
            state["message"] = get_failure_first_step_sendiri_message()
        state["game_over"] = True
        return
    
    # Simpan arah untuk ditampilkan
    state["last_direction"] = arah
    
    # Pindahkan entitas
    for e in to_move:
        state[from_side][e] = False
        state[to_side][e] = True
    
    state["boat"] = to_move
    
    # Beri pesan sukses pergerakan
    if len(to_move) == 1:
        state["message"] = f"🚣 {arah}: Pahlawan menyeberang sendirian."
    else:
        nama_entitas = []
        for e in to_move:
            if e == "tawanan": nama_entitas.append("Tawanan")
            elif e == "perbekalan": nama_entitas.append("Perbekalan")
            elif e == "anak": nama_entitas.append("Anak Buah")
            elif e == "pahlawan": continue
        state["message"] = f"🚣 {arah}: Pahlawan membawa {', '.join(nama_entitas)}."
    
    if check_all_sides():
        check_win()
    else:
        # Batalkan perpindahan jika melanggar aturan
        for e in to_move:
            state[from_side][e] = True
            state[to_side][e] = False
        state["boat"] = []
        state["last_direction"] = None

# Tombol untuk memilih entitas
def show_buttons():
    state = st.session_state.river_game
    
    # Tampilkan skor jika sudah ada
    if state["has_played"]:
        st.metric("🏆 Skor Resmi", f"{state['score']} / 10")
    else:
        st.metric("🏆 Skor", "Belum ada (permainan pertama)")
    
    if state["win"] or state["game_over"]:
        if state["win"]:
            st.balloons()
            st.success(state["message"])
        else:
            st.error(state["message"])
        
        if st.button("🔄 Main Lagi", key="main_lagi_seberang"):
            for key in list(st.session_state.keys()):
                if key == "river_game":
                    del st.session_state[key]
            st.rerun()
        return
    
    # Tentukan arah yang akan terjadi jika pengguna memilih
    if state["left"]["pahlawan"]:
        arah_yang_akan_datang = "🚣 Arah: Sisi Awal → Seberang"
        available = [e for e in ["tawanan", "perbekalan", "anak"] if state["left"][e]]
    else:
        arah_yang_akan_datang = "🚣 Arah: Seberang → Sisi Awal"
        available = [e for e in ["tawanan", "perbekalan", "anak"] if state["right"][e]]
    
    # Tampilkan arah yang akan terjadi
    st.info(arah_yang_akan_datang)
    
    nama_entitas = {
        "tawanan": "⛓️ Tawanan Perang",
        "perbekalan": "🍞 Perbekalan Pangan",
        "anak": "👤 Anak Buah"
    }
    
    st.markdown(f"**Pahlawan siap menyeberang. Pilih siapa yang akan dibawa:**")
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
    
    # Tampilkan status dengan ikon sungai di tengah
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
    
    # Tampilkan pesan jika tidak dalam kondisi game over (sudah ditampilkan di atas)
    if not state["game_over"] and state["message"]:
        st.info(state["message"])

# Fungsi utama untuk menampilkan permainan
def show_river_game():
    st.markdown("## 🚣‍♂️ Pahlawan Menyeberang Sungai")
    st.markdown("""
    **Aturan:**
    - Perahu hanya bisa memuat **maksimal 2 entitas** (termasuk pahlawan).
    - **Tawanan perang dan perbekalan pangan tidak boleh ditinggal berdua tanpa pengawasan pahlawan** (tawanan akan merusak perbekalan).
    - **Tawanan dan Anak Buah tidak boleh ditinggal berdua tanpa bersama pahlawan** (tawanan dan anak buah akan bertarung duel).
    - **Langkah pertama HARUS membawa Tawanan** (jika tidak, permainan GAGAL dengan pesan karakter).
    - **Poin:** Berhasil menyelesaikan permainan pada **permainan pertama** mendapat **10 poin**. Permainan berikutnya hanya latihan (skor tetap).
    - Tujuan: memindahkan semua entitas (pahlawan, tawanan, perbekalan, anak buah) ke seberang.
    
    > **💡 Petunjuk:** Perhatikan arah panah di atas tombol. Itu menunjukkan arah perjalanan yang akan terjadi.
    """)
    init_game_state()
    show_buttons()
    
    # Tombol reset
    if st.button("🔄 Reset Permainan", use_container_width=True, key="reset_seberang"):
        for key in list(st.session_state.keys()):
            if key == "river_game":
                del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    show_river_game()