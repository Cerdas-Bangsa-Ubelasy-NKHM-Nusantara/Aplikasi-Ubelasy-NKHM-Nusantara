# nkhm/dasbor.py (bagian show_dasbor)
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from nkhm.scoring import calculate_nkhm_q, calculate_nkhm_total

def show_dasbor():
    # Definisikan URL catatan pribadi
    vercel_url = "https://my-personal-notes-app-187q.vercel.app"
    
    st.markdown("## 👤 Dasbor Saya")
    st.markdown("Ringkasan perkembangan dan rekomendasi personal Anda.")
    
    # ========== SUBTAB DENGAN RADIO HORIZONTAL ==========
    # Tentukan subtab aktif dari query parameter atau session state
    if "subtab" in st.query_params and st.query_params["subtab"] == "catatan":
        default_subtab = "Catatan"
    else:
        default_subtab = "Ringkasan & Progres"
    
    subtab = st.radio(
        "Pilih tampilan:",
        ["Ringkasan & Progres", "Catatan"],
        horizontal=True,
        index=0 if default_subtab == "Ringkasan & Progres" else 1,
        key="dasbor_subtab"
    )
    st.markdown("---")
    
    # ========== RINGKASAN & PROGRES ==========
    if subtab == "Ringkasan & Progres":
        # ... (semua kode ringkasan yang sudah ada, dari sub_tab1 sebelumnya) ...
        # Salin seluruh konten dari sub_tab1 (tanpa dengan sub_tab1)
        scores = st.session_state.nkhm_scores
        history = st.session_state.nkhm_history
        total_questions = st.session_state.nkhm_total_questions
        user_name = st.session_state.nkhm_user
        
        nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
        nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👤 Nama Pengguna", user_name)
        with col2:
            st.metric("📖 Total Soal Dikerjakan", total_questions)
        with col3:
            st.metric("🏆 NKHM Total", f"{nkhm_total:.1f}")
        
        # ... dan seterusnya (grafik, analisis, rekomendasi, riwayat, target, reset) ...
        # (salin persis dari kode sebelumnya)
    
    # ========== CATATAN ==========
    else:
        st.markdown("### 📝 Catatan Saya")
        st.markdown("Gunakan bagian di bawah untuk menulis catatan harian, ide, atau jurnal belajar.")
        
        col_left, col_right = st.columns(2)
        
        # KOLOM KIRI: CATATAN CEPAT
        with col_left:
            st.markdown("#### ✏️ Catatan Cepat")
            st.caption("Catatan disimpan di server. Simpan akan membersihkan kotak, buka untuk memuat catatan yang tersimpan.")
            
            note_filename = f"notes_{st.session_state.nkhm_user}.txt"
            if "simple_note" not in st.session_state:
                try:
                    with open(note_filename, "r") as f:
                        st.session_state.simple_note = f.read()
                except FileNotFoundError:
                    st.session_state.simple_note = ""
            
            note_text = st.text_area(
                "Tulis catatan di sini (teks biasa):",
                value=st.session_state.simple_note,
                height=250,
                key="simple_note_area",
                placeholder="Contoh: Hari ini belajar tentang NKHM..."
            )
            if note_text != st.session_state.simple_note:
                st.session_state.simple_note = note_text
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("💾 Simpan Catatan", use_container_width=True):
                    if st.session_state.simple_note.strip():
                        try:
                            with open(note_filename, "w") as f:
                                f.write(st.session_state.simple_note)
                            st.session_state.simple_note = ""
                            st.success("✅ Catatan disimpan! Kotak teks sudah dibersihkan.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menyimpan: {e}")
                    else:
                        st.warning("Catatan kosong, tidak disimpan.")
            with col_btn2:
                if st.button("📂 Buka Catatan", use_container_width=True):
                    try:
                        if os.path.exists(note_filename):
                            with open(note_filename, "r") as f:
                                saved_note = f.read()
                            st.session_state.simple_note = saved_note
                            st.success("📂 Catatan berhasil dimuat! Silakan edit dan simpan lagi jika perlu.")
                            st.rerun()
                        else:
                            st.warning("Belum ada catatan yang tersimpan.")
                    except Exception as e:
                        st.error(f"Gagal membuka catatan: {e}")
            
            if st.session_state.simple_note:
                st.caption("📌 Catatan aktif saat ini:")
                st.info(st.session_state.simple_note[:200] + ("..." if len(st.session_state.simple_note) > 200 else ""))
        
        # KOLOM KANAN: CATATAN PRIBADI REACT
        with col_right:
            st.markdown("#### 📱 Catatan Pribadi (React)")
            st.markdown("Aplikasi catatan interaktif dengan fitur lengkap.")
            st.components.v1.iframe(vercel_url, height=450, scrolling=True)
            st.markdown("---")
            nkhm_url = "https://tim-cerdas-bangsa-ubelasy-nkhm-nusantara.streamlit.app"
            st.link_button("🔗 Buka di tab baru", vercel_url, use_container_width=True)
            st.link_button("⬅️ Kembali ke NKHM", nkhm_url, use_container_width=True)
            st.caption("💡 Tips: Gunakan tombol 'Kembali ke NKHM' untuk kembali ke aplikasi NKHM.")
