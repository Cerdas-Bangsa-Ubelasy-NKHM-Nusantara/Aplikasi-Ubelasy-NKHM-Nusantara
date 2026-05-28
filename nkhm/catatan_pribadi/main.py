# nkhm/catatan_pribadi/main.py
import streamlit as st

def show_catatan_pribadi():
    """Fungsi yang dipanggil dari NKHM Dasbor Saya"""
    st.markdown("### 📝 Catatan Pribadi")
    st.markdown("Tulis jurnal belajar, ide, atau catatan pribadi Anda di sini.")
    
    # Inisialisasi session state untuk catatan (jika belum)
    if "personal_notes" not in st.session_state:
        st.session_state.personal_notes = ""
    
    # Text area untuk menulis catatan
    notes = st.text_area(
        "Tulis catatan Anda di sini:",
        value=st.session_state.personal_notes,
        height=300,
        key="personal_notes_area"
    )
    st.session_state.personal_notes = notes
    
    # Tombol simpan (sebenarnya sudah otomatis tersimpan di session state, tapi bisa ditambah tombol ekspor)
    if st.button("💾 Simpan Catatan ke File", use_container_width=True):
        try:
            with open(f"notes_{st.session_state.nkhm_user}.txt", "w") as f:
                f.write(notes)
            st.success("Catatan berhasil disimpan ke file!")
        except Exception as e:
            st.error(f"Gagal menyimpan: {e}")
    
    st.caption("Catatan Anda tersimpan selama sesi berlangsung. Untuk penyimpanan permanen, klik tombol simpan ke file.")

# Jika file ini dijalankan standalone, tetap bisa jalan
if __name__ == "__main__":
    show_catatan_pribadi()