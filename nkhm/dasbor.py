# nkhm/dasbor.py
import streamlit as st
import pandas as pd
import os
import logging
from datetime import datetime, timedelta
from nkhm.scoring import calculate_nkhm_q, calculate_nkhm_total

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di dasbor: {e}")

def init_dasbor_state():
    """Inisialisasi state untuk dasbor."""
    try:
        if "simple_note" not in st.session_state:
            st.session_state.simple_note = ""
        if "dasbor_subtab" not in st.session_state:
            st.session_state.dasbor_subtab = "Ringkasan & Progres"
    except Exception as e:
        logging.error(f"Error init_dasbor_state: {e}")

def show_dasbor():
    try:
        init_dasbor_state()
        
        # Definisikan URL catatan pribadi
        vercel_url = "https://my-personal-notes-app-187q.vercel.app"
        
        st.markdown("## 👤 Dasbor Saya")
        st.markdown("Ringkasan perkembangan dan rekomendasi personal Anda.")
        
        # ========== SUBTAB DENGAN RADIO HORIZONTAL ==========
        # Tentukan subtab aktif dari query parameter atau session state
        try:
            if "subtab" in st.query_params and st.query_params["subtab"] == "catatan":
                default_subtab = "Catatan"
            else:
                default_subtab = "Ringkasan & Progres"
        except Exception as e:
            logging.warning(f"Error membaca query_params: {e}")
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
            try:
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
                
                st.markdown("---")
                
                # ===== GRAFIK PERKEMBANGAN =====
                if history:
                    st.markdown("### 📈 Perkembangan NKHM")
                    try:
                        df_history = pd.DataFrame(history)
                        if "nkhm_total" in df_history.columns and "timestamp" in df_history.columns:
                            df_history["timestamp"] = pd.to_datetime(df_history["timestamp"])
                            df_history = df_history.sort_values("timestamp")
                            st.line_chart(
                                df_history.set_index("timestamp")["nkhm_total"],
                                height=300,
                                use_container_width=True
                            )
                        else:
                            st.info("Data riwayat belum lengkap untuk ditampilkan.")
                    except Exception as e:
                        logging.error(f"Error membuat grafik perkembangan: {e}")
                        st.warning("Gagal menampilkan grafik perkembangan.")
                else:
                    st.info("Belum ada riwayat kuis. Mulai kerjakan soal untuk melihat perkembangan.")
                
                st.markdown("---")
                
                # ===== ANALISIS KECERDASAN =====
                st.markdown("### 🧠 Analisis Kecerdasan")
                col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)
                with col_a1:
                    st.metric("IQ", f"{scores['IQ']}")
                with col_a2:
                    st.metric("EQ", f"{scores['EQ']}")
                with col_a3:
                    st.metric("SQ", f"{scores['SQ']}")
                with col_a4:
                    st.metric("AQ", f"{scores['AQ']}")
                with col_a5:
                    st.metric("Nasionalisme", f"{scores['Nasionalisme']}")
                
                # ===== REKOMENDASI =====
                st.markdown("### 💡 Rekomendasi Personal")
                try:
                    rekomendasi = []
                    
                    # Analisis IQ
                    if scores["IQ"] < 50:
                        rekomendasi.append("🧠 **IQ**: Tingkatkan pengetahuan umum dengan banyak membaca dan belajar.")
                    elif scores["IQ"] < 80:
                        rekomendasi.append("🧠 **IQ**: Pertahankan dan terus asah kemampuan analitis dengan soal-soal logika.")
                    else:
                        rekomendasi.append("🧠 **IQ**: Luar biasa! Terus tantang diri dengan soal yang lebih kompleks.")
                    
                    # Analisis EQ
                    if scores["EQ"] < 50:
                        rekomendasi.append("❤️ **EQ**: Latih empati dengan lebih aktif mendengarkan orang lain.")
                    elif scores["EQ"] < 80:
                        rekomendasi.append("❤️ **EQ**: Kembangkan kecerdasan emosional dengan latihan kesadaran diri.")
                    else:
                        rekomendasi.append("❤️ **EQ**: Hebat! Gunakan kemampuan sosial untuk mempengaruhi positif.")
                    
                    # Analisis SQ
                    if scores["SQ"] < 50:
                        rekomendasi.append("🙏 **SQ**: Perkuat nilai spiritual dengan refleksi dan meditasi.")
                    elif scores["SQ"] < 80:
                        rekomendasi.append("🙏 **SQ**: Terus eksplorasi makna hidup dan tujuan jangka panjang.")
                    else:
                        rekomendasi.append("🙏 **SQ**: Visioner! Bagikan wawasan spiritual untuk menginspirasi.")
                    
                    # Analisis AQ
                    if scores["AQ"] < 50:
                        rekomendasi.append("💪 **AQ**: Bangun ketahanan mental dengan menghadapi tantangan.")
                    elif scores["AQ"] < 80:
                        rekomendasi.append("💪 **AQ**: Pertahankan semangat pantang menyerah dalam setiap situasi.")
                    else:
                        rekomendasi.append("💪 **AQ**: Tangguh! Jadilah teladan ketahanan bagi orang lain.")
                    
                    # Analisis Nasionalisme
                    if scores["Nasionalisme"] < 50:
                        rekomendasi.append("🇮🇩 **Nasionalisme**: Pelajari sejarah dan nilai-nilai kebangsaan.")
                    elif scores["Nasionalisme"] < 80:
                        rekomendasi.append("🇮🇩 **Nasionalisme**: Tingkatkan kontribusi pada masyarakat sekitar.")
                    else:
                        rekomendasi.append("🇮🇩 **Nasionalisme**: Patriot sejati! Terus jaga semangat kebangsaan.")
                    
                    for rec in rekomendasi:
                        st.markdown(f"- {rec}")
                        
                except Exception as e:
                    logging.error(f"Error membuat rekomendasi: {e}")
                    st.warning("Gagal menghasilkan rekomendasi.")
                
                st.markdown("---")
                
                # ===== RIWAYAT TERBARU =====
                if history:
                    st.markdown("### 📋 Riwayat Terbaru")
                    try:
                        df_latest = pd.DataFrame(history[-5:])
                        if all(col in df_latest.columns for col in ["timestamp", "type", "question", "correct", "nkhm_total"]):
                            df_latest = df_latest[["timestamp", "type", "question", "correct", "nkhm_total"]]
                            df_latest["correct"] = df_latest["correct"].map({True: "✅", False: "❌"})
                            df_latest.columns = ["Waktu", "Tipe", "Soal", "Hasil", "NKHM Total"]
                            st.dataframe(df_latest, use_container_width=True, hide_index=True)
                        else:
                            st.info("Data riwayat tidak lengkap.")
                    except Exception as e:
                        logging.error(f"Error menampilkan riwayat: {e}")
                        st.warning("Gagal menampilkan riwayat.")
                
                # ===== TARGET =====
                st.markdown("### 🎯 Target Berikutnya")
                try:
                    target = min(100, nkhm_total + 10)
                    st.progress(nkhm_total / 100, text=f"Menuju {target:.0f}")
                    if nkhm_total >= 100:
                        st.success("🎉 Selamat! Anda sudah mencapai NKHM Total 100!")
                    else:
                        st.caption(f"Target: mencapai NKHM Total {target:.0f} (sekarang {nkhm_total:.1f})")
                except Exception as e:
                    logging.error(f"Error menampilkan target: {e}")
                
                # ===== RESET =====
                st.markdown("---")
                if st.button("🔄 Reset Semua Data", use_container_width=True, type="secondary"):
                    try:
                        st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
                        st.session_state.nkhm_history = []
                        st.session_state.nkhm_total_questions = 0
                        st.success("✅ Semua data berhasil direset!")
                        safe_rerun()
                    except Exception as e:
                        logging.error(f"Error reset data: {e}")
                        st.error(f"Gagal reset data: {e}")
                        
            except Exception as e:
                logging.error(f"Error di subtab Ringkasan & Progres: {e}", exc_info=True)
                st.error(f"Terjadi error: {e}")
                st.exception(e)
        
        # ========== CATATAN ==========
        else:
            try:
                st.markdown("### 📝 Catatan Saya")
                st.markdown("Gunakan bagian di bawah untuk menulis catatan harian, ide, atau jurnal belajar.")
                
                col_left, col_right = st.columns(2)
                
                # KOLOM KIRI: CATATAN CEPAT
                with col_left:
                    st.markdown("#### ✏️ Catatan Cepat")
                    st.caption("Catatan disimpan di server. Simpan akan membersihkan kotak, buka untuk memuat catatan yang tersimpan.")
                    
                    note_filename = f"notes_{st.session_state.nkhm_user}.txt" if st.session_state.nkhm_user else "notes_default.txt"
                    
                    try:
                        if "simple_note" not in st.session_state:
                            try:
                                if os.path.exists(note_filename):
                                    with open(note_filename, "r", encoding="utf-8") as f:
                                        st.session_state.simple_note = f.read()
                                else:
                                    st.session_state.simple_note = ""
                            except Exception as e:
                                logging.error(f"Error membaca catatan awal: {e}")
                                st.session_state.simple_note = ""
                    except Exception as e:
                        logging.error(f"Error akses session_state simple_note: {e}")
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
                            try:
                                if st.session_state.simple_note.strip():
                                    with open(note_filename, "w", encoding="utf-8") as f:
                                        f.write(st.session_state.simple_note)
                                    st.success("✅ Catatan disimpan! Kotak teks sudah dibersihkan.")
                                    st.session_state.simple_note = ""
                                    safe_rerun()
                                else:
                                    st.warning("Catatan kosong, tidak disimpan.")
                            except Exception as e:
                                logging.error(f"Error menyimpan catatan: {e}")
                                st.error(f"Gagal menyimpan: {e}")
                    
                    with col_btn2:
                        if st.button("📂 Buka Catatan", use_container_width=True):
                            try:
                                if os.path.exists(note_filename):
                                    with open(note_filename, "r", encoding="utf-8") as f:
                                        saved_note = f.read()
                                    st.session_state.simple_note = saved_note
                                    st.success("📂 Catatan berhasil dimuat! Silakan edit dan simpan lagi jika perlu.")
                                    safe_rerun()
                                else:
                                    st.warning("Belum ada catatan yang tersimpan.")
                            except Exception as e:
                                logging.error(f"Error membuka catatan: {e}")
                                st.error(f"Gagal membuka catatan: {e}")
                    
                    if st.session_state.simple_note:
                        st.caption("📌 Catatan aktif saat ini:")
                        display_note = st.session_state.simple_note[:200]
                        if len(st.session_state.simple_note) > 200:
                            display_note += "..."
                        st.info(display_note)
                
                # KOLOM KANAN: CATATAN PRIBADI REACT
                with col_right:
                    st.markdown("#### 📱 Catatan Pribadi (React)")
                    st.markdown("Aplikasi catatan interaktif dengan fitur lengkap.")
                    try:
                        st.components.v1.iframe(vercel_url, height=450, scrolling=True)
                    except Exception as e:
                        logging.error(f"Error menampilkan iframe: {e}")
                        st.warning("Gagal menampilkan aplikasi catatan. Silakan buka di tab baru.")
                    
                    st.markdown("---")
                    nkhm_url = "https://tim-cerdas-bangsa-ubelasy-nkhm-nusantara.streamlit.app"
                    st.link_button("🔗 Buka di tab baru", vercel_url, use_container_width=True)
                    st.link_button("⬅️ Kembali ke NKHM", nkhm_url, use_container_width=True)
                    st.caption("💡 Tips: Gunakan tombol 'Kembali ke NKHM' untuk kembali ke aplikasi NKHM.")
                    
            except Exception as e:
                logging.error(f"Error di subtab Catatan: {e}", exc_info=True)
                st.error(f"Terjadi error: {e}")
                st.exception(e)
    
    except Exception as e:
        logging.error(f"Error di show_dasbor: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Dasbor: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_dasbor()