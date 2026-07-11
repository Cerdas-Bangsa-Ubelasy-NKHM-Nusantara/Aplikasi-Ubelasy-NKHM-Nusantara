# nkhm/main.py - PERUBAHAN UNTUK TOMBOL

# Di bagian splash:
if st.button("🚀 MULAI BELAJAR"):  # <-- HAPUS width
    if name and name.strip():
        st.session_state.nkhm_user = name.strip()
        st.rerun()
    else:
        st.error("Masukkan nama dulu!")

# Di sidebar:
if st.button("🔄 Reset Skor"):  # <-- HAPUS width
    # ... kode reset

if st.button("🚪 Keluar / Ganti Pengguna"):  # <-- HAPUS width
    # ... kode keluar

# Di TAB 1 - KUIS:
if st.button("✅ JAWAB", disabled=disable_btn, key=f"jawab_{question_key}"):  # <-- HAPUS width
    # ... kode jawab

if q.get("type") in ["EQ_scale", "AQ_scale"] and st.session_state.current_section and st.session_state.nkhm_answered:
    if st.button("✅ Selesai Bagian Ini", key=f"selesai_{question_key}"):  # <-- HAPUS width
        # ... kode selesai bagian

# Tombol navigasi:
if st.button("⏩ SOAL BERIKUTNYA", key=f"next_{question_key}"):  # <-- HAPUS width
    # ... kode next

if st.button("🔄 KUIS BARU", key=f"reset_{question_key}"):  # <-- HAPUS width
    # ... kode reset