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
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di dasbor: {e}")

def init_dasbor_state():
    try:
        if "simple_note" not in st.session_state:
            st.session_state.simple_note = ""
        if "dasbor_subtab" not in st.session_state:
            st.session_state.dasbor_subtab = "Ringkasan & Progres"
    except Exception as e:
        logging.error(f"Error init_dasbor_state: {e}")

# ========== FUNGSI BANTU UNTUK PARSING TIMESTAMP ==========
def parse_timestamp(timestamp_str):
    if not timestamp_str:
        return None
    formats = [
        '%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M',
        '%Y-%m-%dT%H:%M:%S',
        '%H:%M',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except (ValueError, TypeError):
            continue
    try:
        return pd.to_datetime(timestamp_str, errors='coerce')
    except Exception:
        return None

# ========== SUB FUNGSI ==========
def show_ringkasan_progres(scores, history, total_questions, user_name, nkhm_q, nkhm_total):
    """Menampilkan ringkasan dan progres."""
    try:
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
                    df_history['timestamp_parsed'] = df_history['timestamp'].apply(parse_timestamp)
                    df_history = df_history[df_history['timestamp_parsed'].notna()]
                    if not df_history.empty:
                        df_history = df_history.sort_values("timestamp_parsed")
                        st.line_chart(
                            df_history.set_index("timestamp_parsed")["nkhm_total"],
                            height=300,
                            use_container_width=True
                        )
                    else:
                        st.info("Data timestamp tidak valid untuk ditampilkan.")
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
            if scores["IQ"] < 50:
                rekomendasi.append("🧠 **IQ**: Tingkatkan pengetahuan umum dengan banyak membaca dan belajar.")
            elif scores["IQ"] < 80:
                rekomendasi.append("🧠 **IQ**: Pertahankan dan terus asah kemampuan analitis dengan soal-soal logika.")
            else:
                rekomendasi.append("🧠 **IQ**: Luar biasa! Terus tantang diri dengan soal yang lebih kompleks.")
            
            if scores["EQ"] < 50:
                rekomendasi.append("❤️ **EQ**: Latih empati dengan lebih aktif mendengarkan orang lain.")
            elif scores["EQ"] < 80:
                rekomendasi.append("❤️ **EQ**: Kembangkan kecerdasan emosional dengan latihan kesadaran diri.")
            else:
                rekomendasi.append("❤️ **EQ**: Hebat! Gunakan kemampuan sosial untuk mempengaruhi positif.")
            
            if scores["SQ"] < 50:
                rekomendasi.append("🙏 **SQ**: Perkuat nilai spiritual dengan refleksi dan meditasi.")
            elif scores["SQ"] < 80:
                rekomendasi.append("🙏 **SQ**: Terus eksplorasi makna hidup dan tujuan jangka panjang.")
            else:
                rekomendasi.append("🙏 **SQ**: Visioner! Bagikan wawasan spiritual untuk menginspirasi.")
            
            if scores["AQ"] < 50:
                rekomendasi.append("💪 **AQ**: Bangun ketahanan mental dengan menghadapi tantangan.")
            elif scores["AQ"] < 80:
                rekomendasi.append("💪 **AQ**: Pertahankan semangat pantang menyerah dalam setiap situasi.")
            else:
                rekomendasi.append("💪 **AQ**: Tangguh! Jadilah teladan ketahanan bagi orang lain.")
            
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
            if nkhm_total > 0:
                st.progress(min(nkhm_total / 100, 1.0), text=f"Menuju {target:.0f}")
            else:
                st.progress(0.0, text="Mulai kerjakan soal untuk memulai progress!")
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
        logging.error(f"Error show_ringkasan_progres: {e}")
        st.error(f"Terjadi error: {e}")

def show_analisis_mendalam(scores, history, nkhm_q, nkhm_total):
    """Menampilkan analisis mendalam dengan radar chart dan heatmap."""
    try:
        st.markdown("### 📊 Analisis Mendalam")
        
        # ===== RADAR CHART =====
        st.markdown("#### 🎯 Radar Kecerdasan")
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            
            categories = ['IQ', 'EQ', 'SQ', 'AQ', 'Nasionalisme']
            values = [scores.get('IQ', 0), scores.get('EQ', 0), scores.get('SQ', 0), 
                      scores.get('AQ', 0), scores.get('Nasionalisme', 0)]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                marker=dict(color='#2e7daf'),
                line=dict(color='#1a3c6e', width=2)
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(100, max(values) + 20)]
                    )
                ),
                showlegend=False,
                height=400,
                margin=dict(l=80, r=80, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.warning("⚠️ Plotly tidak terinstall. Radar chart tidak tersedia.")
        except Exception as e:
            logging.error(f"Error radar chart: {e}")
            st.warning("Gagal menampilkan radar chart.")
        
        st.markdown("---")
        
        # ===== STATISTIK BELAJAR =====
        st.markdown("#### 📚 Statistik Belajar")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_soal = len(history)
            st.metric("📝 Total Jawaban", total_soal)
        with col2:
            benar = sum(1 for h in history if isinstance(h.get('correct'), bool) and h['correct'])
            st.metric("✅ Benar", benar)
        with col3:
            salah = total_soal - benar
            st.metric("❌ Salah", salah)
        with col4:
            akurasi = (benar / total_soal * 100) if total_soal > 0 else 0
            st.metric("🎯 Akurasi", f"{akurasi:.1f}%")
        
        # ===== HEATMAP PER KATEGORI =====
        if history:
            st.markdown("#### 🔥 Heatmap Performa per Kategori")
            try:
                df_heat = pd.DataFrame(history)
                if 'type' in df_heat.columns and 'correct' in df_heat.columns:
                    # Konversi correct ke numerik
                    df_heat['correct_num'] = df_heat['correct'].apply(
                        lambda x: 1 if isinstance(x, bool) and x else 0
                    )
                    heatmap_data = df_heat.groupby('type')['correct_num'].mean().reset_index()
                    heatmap_data['correct_num'] = heatmap_data['correct_num'] * 100
                    
                    # Tampilkan sebagai bar chart
                    st.bar_chart(
                        heatmap_data.set_index('type'),
                        height=250,
                        use_container_width=True
                    )
                else:
                    st.info("Data tidak cukup untuk heatmap.")
            except Exception as e:
                logging.error(f"Error heatmap: {e}")
                st.warning("Gagal menampilkan heatmap.")
        
        # ===== KEKUATAN & KELEMAHAN =====
        st.markdown("#### 💪 Kekuatan & Kelemahan")
        try:
            if history:
                df_analysis = pd.DataFrame(history)
                if 'type' in df_analysis.columns and 'correct' in df_analysis.columns:
                    df_analysis['correct_num'] = df_analysis['correct'].apply(
                        lambda x: 1 if isinstance(x, bool) and x else 0
                    )
                    type_accuracy = df_analysis.groupby('type')['correct_num'].mean() * 100
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("##### 💪 Kekuatan (Akurasi ≥ 70%)")
                        kuat = type_accuracy[type_accuracy >= 70]
                        if not kuat.empty:
                            for tipe, akurasi in kuat.items():
                                st.success(f"✅ {tipe}: {akurasi:.1f}%")
                        else:
                            st.info("Belum ada kategori dengan akurasi ≥ 70%. Teruslah belajar!")
                    
                    with col2:
                        st.markdown("##### 📚 Perlu Ditingkatkan (Akurasi < 70%)")
                        lemah = type_accuracy[type_accuracy < 70]
                        if not lemah.empty:
                            for tipe, akurasi in lemah.items():
                                st.warning(f"📖 {tipe}: {akurasi:.1f}%")
                        else:
                            st.success("✨ Semua kategori sudah baik! Pertahankan!")
                else:
                    st.info("Data tidak cukup untuk analisis kekuatan & kelemahan.")
            else:
                st.info("Belum ada data. Mulai kerjakan soal untuk analisis.")
        except Exception as e:
            logging.error(f"Error kekuatan kelemahan: {e}")
            st.warning("Gagal menganalisis kekuatan & kelemahan.")
            
    except Exception as e:
        logging.error(f"Error show_analisis_mendalam: {e}")
        st.error(f"Terjadi error: {e}")

def show_tantangan_pencapaian(scores, history, nkhm_total):
    """Menampilkan tantangan dan pencapaian."""
    try:
        st.markdown("### 🎯 Tantangan & Pencapaian")
        
        # ===== BADGE =====
        st.markdown("#### 🏅 Badge yang Diperoleh")
        badges = []
        
        # Badge berdasarkan skor
        if nkhm_total >= 80:
            badges.append(("🌟", "Pahlawan Cerdas", "NKHM ≥ 80"))
        if nkhm_total >= 60:
            badges.append(("📚", "Cendekia Muda", "NKHM ≥ 60"))
        if nkhm_total >= 40:
            badges.append(("🌱", "Penjelajah Ilmu", "NKHM ≥ 40"))
        
        # Badge berdasarkan kategori
        if scores.get('IQ', 0) >= 80:
            badges.append(("🧠", "Cendekia IQ", "IQ ≥ 80"))
        if scores.get('EQ', 0) >= 80:
            badges.append(("❤️", "Empati EQ", "EQ ≥ 80"))
        if scores.get('SQ', 0) >= 80:
            badges.append(("🙏", "Spiritual SQ", "SQ ≥ 80"))
        if scores.get('AQ', 0) >= 80:
            badges.append(("💪", "Tangguh AQ", "AQ ≥ 80"))
        if scores.get('Nasionalisme', 0) >= 80:
            badges.append(("🇮🇩", "Patriot", "Nasionalisme ≥ 80"))
        
        # Badge jumlah soal
        total_soal = len(history)
        if total_soal >= 100:
            badges.append(("💯", "100 Soal", "Mengerjakan ≥ 100 soal"))
        elif total_soal >= 50:
            badges.append(("📖", "50 Soal", "Mengerjakan ≥ 50 soal"))
        elif total_soal >= 10:
            badges.append(("📝", "10 Soal", "Mengerjakan ≥ 10 soal"))
        
        if badges:
            cols = st.columns(min(4, len(badges)))
            for i, (icon, name, desc) in enumerate(badges):
                with cols[i % len(cols)]:
                    st.markdown(
                        f"""
                        <div style="text-align: center; padding: 10px; background-color: #f0f5fa; border-radius: 10px;">
                            <div style="font-size: 30px;">{icon}</div>
                            <div style="font-weight: bold;">{name}</div>
                            <div style="font-size: 11px; color: #666;">{desc}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.info("Belum ada badge. Teruslah belajar dan capai target!")
        
        st.markdown("---")
        
        # ===== TANTANGAN =====
        st.markdown("#### 🎯 Tantangan Berikutnya")
        
        challenges = []
        
        # Tantangan berdasarkan skor
        if nkhm_total < 40:
            challenges.append(("🌱", "Capai NKHM 40", "Menjadi Penjelajah Ilmu"))
        elif nkhm_total < 60:
            challenges.append(("📚", "Capai NKHM 60", "Menjadi Cendekia Muda"))
        elif nkhm_total < 80:
            challenges.append(("🌟", "Capai NKHM 80", "Menjadi Pahlawan Cerdas"))
        
        # Tantangan berdasarkan kategori
        if scores.get('IQ', 0) < 80:
            challenges.append(("🧠", "Tingkatkan IQ ke 80", "Fokus pada soal logika"))
        if scores.get('EQ', 0) < 80:
            challenges.append(("❤️", "Tingkatkan EQ ke 80", "Latih empati dan sosial"))
        if scores.get('SQ', 0) < 80:
            challenges.append(("🙏", "Tingkatkan SQ ke 80", "Perkuat nilai spiritual"))
        if scores.get('AQ', 0) < 80:
            challenges.append(("💪", "Tingkatkan AQ ke 80", "Bangun ketahanan mental"))
        
        # Tantangan jumlah soal
        total_soal = len(history)
        if total_soal < 10:
            challenges.append(("📝", "Kerjakan 10 Soal", "Mulai perjalanan belajar"))
        elif total_soal < 50:
            challenges.append(("📖", "Kerjakan 50 Soal", "Tingkatkan konsistensi"))
        elif total_soal < 100:
            challenges.append(("💯", "Kerjakan 100 Soal", "Capai milestone 100"))
        
        if challenges:
            for icon, title, desc in challenges[:5]:
                st.markdown(f"{icon} **{title}** – *{desc}*")
        else:
            st.success("🎉 Anda sudah mencapai semua tantangan! Luar biasa!")
            
    except Exception as e:
        logging.error(f"Error show_tantangan_pencapaian: {e}")
        st.error(f"Terjadi error: {e}")

def show_catatan(vercel_url, nkhm_url):
    """Menampilkan fitur catatan."""
    try:
        st.markdown("### 📝 Catatan Saya")
        st.markdown("Gunakan bagian di bawah untuk menulis catatan harian, ide, atau jurnal belajar.")
        
        col_left, col_right = st.columns(2)
        
        # KOLOM KIRI: CATATAN CEPAT
        with col_left:
            st.markdown("#### ✏️ Catatan Cepat")
            st.caption("Catatan disimpan di server. Simpan akan membersihkan kotak, buka untuk memuat catatan yang tersimpan.")
            
            user_name = st.session_state.get("nkhm_user", "pengguna")
            note_filename = f"notes_{user_name}.txt"
            
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
                iframe_html = f"""
                <iframe
                    src="{vercel_url}"
                    style="width: 100%; height: 450px; border: none; border-radius: 8px;"
                    sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                    loading="lazy"
                    allow="clipboard-read; clipboard-write"
                ></iframe>
                """
                try:
                    st.components.v1.html(iframe_html, height=470)
                except AttributeError:
                    try:
                        st.components.html(iframe_html, height=470)
                    except AttributeError:
                        st.markdown(iframe_html, unsafe_allow_html=True)
                    except Exception as e:
                        logging.error(f"Error dengan components.html: {e}")
                        st.markdown(iframe_html, unsafe_allow_html=True)
                except Exception as e:
                    logging.error(f"Error dengan components.v1.html: {e}")
                    try:
                        st.components.html(iframe_html, height=470)
                    except Exception as e2:
                        logging.error(f"Error dengan components.html fallback: {e2}")
                        st.markdown(iframe_html, unsafe_allow_html=True)
            except Exception as e:
                logging.error(f"Error menampilkan iframe: {e}")
                st.warning("⚠️ Gagal menampilkan aplikasi catatan. Silakan buka di tab baru.")
            
            st.markdown("---")
            st.link_button("🔗 Buka di tab baru", vercel_url, use_container_width=True)
            st.link_button("⬅️ Kembali ke NKHM", nkhm_url, use_container_width=True)
            st.caption("💡 Tips: Gunakan tombol 'Kembali ke NKHM' untuk kembali ke aplikasi NKHM.")
            
    except Exception as e:
        logging.error(f"Error show_catatan: {e}")
        st.error(f"Terjadi error: {e}")

# ========== MAIN ==========
def show_dasbor():
    try:
        init_dasbor_state()
        
        vercel_url = "https://my-personal-notes-app-187q.vercel.app"
        nkhm_url = "https://tim-cerdas-bangsa-ubelasy-nkhm-nusantara.streamlit.app"
        
        st.markdown("## 👤 Dasbor Saya")
        st.markdown("Ringkasan perkembangan dan rekomendasi personal Anda.")
        
        # ========== SUBTAB DENGAN MENU ==========
        try:
            if "subtab" in st.query_params and st.query_params.get("subtab") == "catatan":
                default_subtab = "Catatan"
            else:
                default_subtab = "Ringkasan & Progres"
        except Exception as e:
            logging.warning(f"Error membaca query_params: {e}")
            default_subtab = "Ringkasan & Progres"
        
        # ===== MENU DASBOR (DIPERLUAS) =====
        subtab = st.radio(
            "Pilih tampilan:",
            ["Ringkasan & Progres", "Analisis Mendalam", "Tantangan & Pencapaian", "Catatan"],
            horizontal=True,
            index=0 if default_subtab == "Ringkasan & Progres" else 1,
            key="dasbor_subtab"
        )
        st.markdown("---")
        
        # Ambil data
        scores = st.session_state.get("nkhm_scores", {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0})
        history = st.session_state.get("nkhm_history", [])
        total_questions = st.session_state.get("nkhm_total_questions", 0)
        user_name = st.session_state.get("nkhm_user", "Pengguna")
        
        nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
        nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
        
        # ========== TAMPILKAN SUBTAB ==========
        if subtab == "Ringkasan & Progres":
            show_ringkasan_progres(scores, history, total_questions, user_name, nkhm_q, nkhm_total)
        
        elif subtab == "Analisis Mendalam":
            show_analisis_mendalam(scores, history, nkhm_q, nkhm_total)
        
        elif subtab == "Tantangan & Pencapaian":
            show_tantangan_pencapaian(scores, history, nkhm_total)
        
        else:  # Catatan
            show_catatan(vercel_url, nkhm_url)
    
    except Exception as e:
        logging.error(f"Error di show_dasbor: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Dasbor: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_dasbor()