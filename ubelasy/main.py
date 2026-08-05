# ubelasy/main.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import logging
import time
from pathlib import Path
from ubelasy.keuangan_real import show_keuangan_real
from ubelasy.dashboard_keuangan_real import show_dashboard_keuangan_real
from ubelasy.gamifikasi import show_gamifikasi_ubelasy
from ubelasy.ai_kredit import show_ai_kredit  # ✅ Import sudah ada

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di ubelasy: {e}")

# ========== IMPORT MODUL DENGAN ERROR HANDLING ==========
try:
    from ubelasy.calculator import calculate_loan
except ImportError as e:
    logging.error(f"Gagal import ubelasy.calculator: {e}")
    st.error("❌ Modul 'calculator' tidak ditemukan.")
    st.stop()

try:
    from ubelasy.aggregator import get_recommendations, submit_application, get_all_applications_for_user
except ImportError as e:
    logging.error(f"Gagal import ubelasy.aggregator: {e}")
    st.error("❌ Modul 'aggregator' tidak ditemukan.")
    st.stop()

try:
    from ubelasy.pdf_export import export_simulation_to_pdf
except ImportError:
    logging.warning("Modul pdf_export tidak ditemukan, fitur PDF dinonaktifkan")
    export_simulation_to_pdf = None

try:
    from shared.notifications import show_toast
except ImportError:
    logging.warning("Modul shared.notifications tidak ditemukan, notifikasi dinonaktifkan")
    show_toast = lambda msg, type="info", duration=3000: st.info(msg)

try:
    from ubelasy.edukasi import show_edukasi
except ImportError:
    show_edukasi = lambda: st.info("Fitur edukasi belum tersedia.")

try:
    from ubelasy.kredit_report import show_kredit_report
except ImportError:
    show_kredit_report = lambda: st.info("Fitur laporan kredit belum tersedia.")

try:
    from ubelasy.keuangan import show_keuangan
except ImportError:
    show_keuangan = lambda: st.info("Fitur perencanaan keuangan belum tersedia.")

try:
    from ubelasy.dashboard_keuangan import show_dashboard_keuangan
except ImportError:
    show_dashboard_keuangan = lambda: st.info("Fitur dashboard keuangan belum tersedia.")

# ========== DOKUMEN UBELASY (BARU: MEMBACA DARI FILE) ==========
def load_ubelasy_document():
    """Memuat dokumen Sistem Ubelasy dari file markdown."""
    doc_path = Path(__file__).parent.parent / "assets" / "dokumen" / "Sistem Pinjaman Ubelasy.md"
    if doc_path.exists():
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error membaca dokumen: {e}")
            return None
    return None

def get_ubelasy_document():
    """Mengembalikan konten dokumen atau pesan fallback."""
    content = load_ubelasy_document()
    if content:
        return content
    else:
        return """
        <div class="ubelasy-document">
        <h1>Sistem Pinjaman/Kredit Model Ubelasy</h1>
        <p>Dokumen belum tersedia. Silakan upload file <strong>Sistem Pinjaman Ubelasy.md</strong> ke folder <strong>assets/dokumen/</strong>.</p>
        </div>
        """

def inject_ubelasy_document_css():
    """Menambahkan CSS untuk tampilan dokumen."""
    st.markdown("""
    <style>
        .ubelasy-document {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px 30px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            line-height: 1.8;
        }
        .ubelasy-document h1 {
            color: #1a3c6e;
            border-bottom: 3px solid #2e7daf;
            padding-bottom: 10px;
        }
        .ubelasy-document h2 {
            color: #1a3c6e;
            border-left: 5px solid #2e7daf;
            padding-left: 15px;
            margin-top: 30px;
        }
        .ubelasy-document h3 {
            color: #2e7daf;
            margin-top: 25px;
        }
        .ubelasy-document table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
        }
        .ubelasy-document th {
            background-color: #1a3c6e;
            color: white;
            padding: 10px 12px;
            border: 1px solid #ddd;
        }
        .ubelasy-document td {
            padding: 8px 12px;
            border: 1px solid #ddd;
        }
        .ubelasy-document tr:nth-child(even) {
            background-color: #f5f8fc;
        }
        .ubelasy-document tr:hover {
            background-color: #e8f0fe;
        }
        .ubelasy-document blockquote {
            border-left: 4px solid #2e7daf;
            padding: 10px 20px;
            margin: 15px 0;
            background-color: #f0f5fa;
            border-radius: 0 5px 5px 0;
        }
        .ubelasy-document ul, .ubelasy-document ol {
            padding-left: 25px;
            line-height: 1.8;
        }
        .ubelasy-document p {
            text-align: justify;
            line-height: 1.8;
        }
        .ubelasy-document hr {
            border: none;
            border-top: 2px solid #dce4ec;
            margin: 30px 0;
        }
        /* Dark mode support */
        .dark-mode .ubelasy-document {
            background-color: #1a1a2e;
            color: #d0d0e0;
        }
        .dark-mode .ubelasy-document h1,
        .dark-mode .ubelasy-document h2 {
            color: #7ab7e0;
        }
        .dark-mode .ubelasy-document h3 {
            color: #5a9acf;
        }
        .dark-mode .ubelasy-document th {
            background-color: #2a3a5a;
            color: #e0e0e0;
        }
        .dark-mode .ubelasy-document tr:nth-child(even) {
            background-color: #22223a;
        }
        .dark-mode .ubelasy-document tr:hover {
            background-color: #2a2a4a;
        }
        .dark-mode .ubelasy-document blockquote {
            background-color: #1a1a3a;
            border-left-color: #4a8abf;
            color: #d0d0e0;
        }
        .dark-mode .ubelasy-document p,
        .dark-mode .ubelasy-document li {
            color: #d0d0e0;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #f5f8fc"] {
            background-color: #1a1a3a !important;
            border-color: #444 !important;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #e8f0fe"] {
            background-color: #1a1a4a !important;
            border-color: #3a6a8a !important;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #d1ecf1"] {
            background-color: #0a2a3a !important;
            border-color: #2a6a8a !important;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #d4edda"] {
            background-color: #0a2a1a !important;
            border-color: #2a6a3a !important;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #fff3cd"] {
            background-color: #2a2a0a !important;
            border-color: #6a6a2a !important;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #f8d7da"] {
            background-color: #3a1a1a !important;
            border-color: #6a2a2a !important;
        }
        .dark-mode .ubelasy-document div[style*="background-color: #f5c6cb"] {
            background-color: #3a0a0a !important;
            border-color: #6a1a1a !important;
        }
        /* Responsif */
        @media (max-width: 600px) {
            .ubelasy-document {
                padding: 15px;
            }
            .ubelasy-document table {
                font-size: 12px;
            }
            .ubelasy-document ul[style*="columns: 2"] {
                columns: 1 !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ========== MAIN ==========
def main():
    try:
        # Inisialisasi session state
        if "simulasi_hasil" not in st.session_state:
            st.session_state.simulasi_hasil = None
        if "rekomendasi" not in st.session_state:
            st.session_state.rekomendasi = None
        if "profil_terakhir" not in st.session_state:
            st.session_state.profil_terakhir = None
        if "credit_score" not in st.session_state:
            st.session_state.credit_score = None
        if "credit_grade" not in st.session_state:
            st.session_state.credit_grade = None

        # ========== HEADER ==========
        script_dir = Path(__file__).parent.parent
        image_path = script_dir / "assets" / "ubelasy.jpg"

        st.markdown("""
        <style>
        .full-width-image img { width: 100%; height: auto; }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if image_path.exists():
                with st.container():
                    st.markdown('<div class="full-width-image">', unsafe_allow_html=True)
                    st.image(str(image_path))
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Gambar ubelasy.jpg tidak ditemukan di folder assets/")
            st.markdown(
                "<h1 style='text-align: center;'>🌾 Ubelasy – Agregator Pinjaman Berkelanjutan</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='text-align: center;'><strong>Skema PSH & Penurunan Suku Bunga 0,5% per Periode</strong></p>",
                unsafe_allow_html=True
            )
        st.markdown("---")

        # ========== SIDEBAR ==========
        with st.sidebar:
            if "nkhm_scores" in st.session_state:
                nkhm_total = sum(st.session_state.nkhm_scores.values())
                st.metric("🧠 Skor NKHM", nkhm_total)
                st.caption("(Semakin tinggi skor, semakin baik peluang mendapat pinjaman)")
                st.markdown("---")
            else:
                st.info("Mainkan game NKHM untuk meningkatkan skor Anda!")
                st.markdown("---")

            st.header("📑 Navigasi Ubelasy")
            tab_mode = st.radio(
                "Pilih Tab",
                [
                    "📖 Sistem Ubelasy",
                    "⚙️ Simulasi & Agregator",
                    "📚 Edukasi",
                    "📊 Rapor Kredit",
                    "💰 Perencanaan Keuangan",
                    "💰 Perencanaan Keuangan Real",
                    "📊 Dashboard Keuangan",
                    "📊 Dashboard Keuangan Real",
                    "🎮 Gamifikasi Ubelasy",
                    "🤖 AI Penilaian Kredit"   # <--- TAMBAHKAN INI
                ],
                index=1,
                label_visibility="collapsed"
            )
            st.markdown("---")

            if tab_mode == "⚙️ Simulasi & Agregator":
                st.header("⚙️ Simulasi Pinjaman")
                K = st.number_input("Pinjaman per Periode (Rp)", value=36_000_000, step=1_000_000, format="%d")
                r1 = st.number_input("Suku bunga awal (%)", value=11.0, step=0.5)
                delta = st.number_input("Penurunan per periode (%)", value=0.5, step=0.1)
                n = st.number_input("Jumlah periode", min_value=1, max_value=10, value=2, step=1)
                tp = st.number_input("Tenor per periode (tahun)", min_value=0.5, max_value=30.0, value=3.0, step=0.5)
                m = st.number_input("Tahun bayar di periode terakhir", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
                bank_type = st.selectbox("Tipe Bank", ["desa", "kota"], format_func=lambda x: "🏡 Pedesaan" if x=="desa" else "🏙️ Perkotaan")
                biaya_dana = st.number_input("Biaya Dana+Overhead (%)", value=9.0, step=0.5)
                hitung = st.button("🚀 Hitung Simulasi", type="primary")

        # ========== INJECT CSS ==========
        inject_ubelasy_document_css()

        # ========== TAMPILKAN KONTEN ==========
        if tab_mode == "📖 Sistem Ubelasy":
            doc_content = get_ubelasy_document()
            st.markdown(doc_content)
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.caption("💡 Untuk menyimpan dokumen ini, gunakan fitur 'Print' di browser Anda (Ctrl+P) dan pilih 'Save as PDF'.")
                if st.button("📄 Download Dokumen (PDF)", use_container_width=True):
                    st.info("Fitur download PDF akan segera tersedia. Saat ini silakan gunakan Print > Save as PDF.")

        elif tab_mode == "📚 Edukasi":
            show_edukasi()

        elif tab_mode == "📊 Rapor Kredit":
            show_kredit_report()

        elif tab_mode == "💰 Perencanaan Keuangan":
            show_keuangan()

        elif tab_mode == "💰 Perencanaan Keuangan Real":
            show_keuangan_real()

        elif tab_mode == "📊 Dashboard Keuangan":
            show_dashboard_keuangan()

        elif tab_mode == "📊 Dashboard Keuangan Real":
            show_dashboard_keuangan_real()

        elif tab_mode == "🎮 Gamifikasi Ubelasy":
            show_gamifikasi_ubelasy()

        elif tab_mode == "🤖 AI Penilaian Kredit":   # <--- TAMBAHKAN INI
            show_ai_kredit()

        else:
            # ========== TAB SIMULASI & AGREGATOR ==========
            if 'hitung' in locals() and hitung:
                if m > tp:
                    st.error(f"⚠️ m ({m}) tidak boleh > tp ({tp})")
                    return
                try:
                    hasil = calculate_loan(K, r1, delta, n, tp, m, bank_type, biaya_dana)
                    st.session_state.simulasi_hasil = hasil
                    if show_toast:
                        show_toast("📊 Simulasi pinjaman berhasil dihitung!", type="success")
                except Exception as e:
                    logging.error(f"Error menghitung simulasi: {e}")
                    st.error(f"Error menghitung simulasi: {e}")

            if st.session_state.simulasi_hasil is not None:
                try:
                    hasil = st.session_state.simulasi_hasil
                    st.markdown("## 📊 Ubelasy - Simulasi Hitungan Pinjaman")

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("📅 Total Tenor", f"{hasil['T']} tahun")
                    col1.metric("⚖️ dPSH", f"{hasil['dPSH']:.4f} / 2")
                    col2.metric("🏦 Total Pinjaman", f"Rp {hasil['total_pokok']:,.0f}".replace(",", "."))
                    col2.metric("🆓 PSH Diterima", f"Rp {hasil['PSH']:,.0f}".replace(",", ".") + f" ({hasil['psh_persen_total']:.2f}%)")
                    col3.metric("💰 Keuntungan Bank", f"{hasil['laba_persen']:.2f}%")
                    col3.metric("📈 Return Tahunan", f"{hasil['return_tahunan']:.2f}% p.a")
                    col4.metric("📉 Rata-rata Bunga", f"{hasil['rata_bunga']:.2f}%")
                    col4.metric("📊 Spread", f"{hasil['spread']:.2f}%")

                    st.subheader("📋 Detail per Periode")
                    df_detail = pd.DataFrame(hasil['detail'])
                    st.dataframe(df_detail, use_container_width=True, hide_index=True)

                    st.subheader("📌 Status Debitur")
                    st.info(f"**{hasil['status']}** (dPSH = {hasil['dPSH']:.4f})")

                    bunga = [hasil['detail'][i]['Suku Bunga (%)'] for i in range(n)]
                    fig, ax = plt.subplots()
                    ax.plot(range(1, n+1), bunga, marker='o', color='#2e7d32')
                    ax.set_xlabel("Periode")
                    ax.set_ylabel("Suku Bunga (%)")
                    ax.set_title("Penurunan Suku Bunga 0.5% per Periode")
                    ax.grid(True, linestyle='--', alpha=0.5)
                    st.pyplot(fig)

                    # EKSPOR PDF
                    if export_simulation_to_pdf is not None:
                        try:
                            rekom = st.session_state.get("rekomendasi", None)
                            pdf_path = export_simulation_to_pdf(hasil, rekom)
                            with open(pdf_path, "rb") as f:
                                if st.download_button(
                                    label="📄 Download Laporan PDF",
                                    data=f,
                                    file_name=f"ubelasy_simulasi_{hasil['T']}tahun.pdf",
                                    mime="application/pdf",
                                    key="download_pdf_btn"
                                ):
                                    if show_toast:
                                        show_toast("✅ Laporan berhasil diunduh!", type="success")
                            os.unlink(pdf_path)
                        except Exception as e:
                            logging.error(f"Error membuat PDF: {e}")
                            st.error(f"Gagal membuat PDF: {e}")
                    else:
                        st.info("Fitur PDF tidak tersedia karena modul pdf_export tidak ditemukan.")
                except Exception as e:
                    logging.error(f"Error menampilkan hasil simulasi: {e}")
                    st.error(f"Error menampilkan hasil simulasi: {e}")

            # ========== AGREGATOR ==========
            st.markdown("---")
            st.subheader("🏦 Cari Pinjaman dari Bank Mitra")

            with st.form("form_cari_pinjaman"):
                col_a, col_b = st.columns(2)
                with col_a:
                    jumlah_pinjaman = st.number_input("Jumlah pinjaman (Rp)", value=50_000_000, step=10_000_000)
                    sektor_usaha = st.selectbox("Sektor usaha", ["pangan", "energi", "lainnya"])
                    email = st.text_input("Email (untuk notifikasi)", placeholder="email@domain.com")
                with col_b:
                    tenor = st.slider("Tenor (tahun)", 1, 5, 3)
                    phone = st.text_input("Nomor WhatsApp (untuk notifikasi)", placeholder="08123456789")
                submitted = st.form_submit_button("🔍 Cari Rekomendasi")

                if submitted:
                    try:
                        nkhm_total = 0
                        if "nkhm_scores" in st.session_state:
                            nkhm_total = sum(st.session_state.nkhm_scores.values())
                        profil = {
                            "jumlah_pinjaman": jumlah_pinjaman,
                            "sektor": sektor_usaha,
                            "tenor": tenor,
                            "email": email.strip(),
                            "phone": phone.strip(),
                            "nkhm_score": nkhm_total,
                            "riwayat_pinjaman": []
                        }
                        rekom, credit_score, credit_grade = get_recommendations(profil)
                        st.session_state.rekomendasi = rekom
                        st.session_state.profil_terakhir = profil
                        st.session_state.credit_score = credit_score
                        st.session_state.credit_grade = credit_grade
                        if show_toast:
                            show_toast(f"🏦 Ditemukan {len(rekom)} bank mitra yang cocok!", type="success")
                        safe_rerun()
                    except Exception as e:
                        logging.error(f"Error mencari rekomendasi: {e}")
                        st.error(f"Error mencari rekomendasi: {e}")

            if "credit_score" in st.session_state:
                st.info(f"📊 **Skor Kredit Anda: {st.session_state.credit_score}** ({st.session_state.credit_grade}) - Semakin tinggi skor, semakin rendah bunga yang ditawarkan.")

            if "rekomendasi" in st.session_state and st.session_state.rekomendasi:
                try:
                    rekom = st.session_state.rekomendasi
                    st.success(f"Ditemukan {len(rekom)} bank yang cocok:")
                    for r in rekom:
                        with st.expander(f"🏦 {r['bank']}"):
                            st.write(f"**Estimasi bunga:** {r['bunga']}% per tahun")
                            st.write(f"**Estimasi angsuran/bulan:** Rp {r['estimasi_angsuran']:,.0f}".replace(",", "."))
                            st.write(f"**Biaya admin:** Rp {r['biaya_admin']:,.0f}".replace(",", "."))
                            st.caption(f"📈 Skor kredit Anda: {r.get('credit_score', 'N/A')} ({r.get('credit_grade', 'N/A')}) → bunga disesuaikan")
                            if st.button(f"Ajukan ke {r['bank']}", key=r['id']):
                                try:
                                    app_id = submit_application(st.session_state.profil_terakhir, r['id'])
                                    if show_toast:
                                        show_toast(f"✅ Pengajuan ke {r['bank']} terkirim! ID: {app_id}", type="success", duration=5000)
                                    st.success(f"Pengajuan berhasil dikirim! ID: {app_id}")
                                    st.info("Bank akan menghubungi Anda dalam 1x24 jam.")
                                    safe_rerun()
                                except Exception as e:
                                    logging.error(f"Error submit aplikasi: {e}")
                                    st.error(f"Error submit aplikasi: {e}")
                except Exception as e:
                    logging.error(f"Error menampilkan rekomendasi: {e}")
                    st.error(f"Error menampilkan rekomendasi: {e}")
            elif "rekomendasi" in st.session_state:
                st.warning("Belum ada bank yang cocok. Coba ubah kriteria pinjaman.")

            # ========== STATUS PENGAJUAN ==========
            st.markdown("---")
            st.subheader("📋 Status Pengajuan Anda")
            try:
                apps = get_all_applications_for_user()
                if not apps:
                    st.info("Belum ada pengajuan. Silakan cari pinjaman di atas.")
                else:
                    for app in apps[-5:]:
                        status_color = {
                            "Dikirim": "🔵",
                            "Diproses": "🟡",
                            "Disetujui": "✅",
                            "Ditolak": "❌"
                        }.get(app["status"], "⚪")
                        with st.expander(f"{status_color} {app['id']} - {app['tanggal']} - {app['status']}"):
                            st.write(f"**Bank:** {app['bank_id']}")
                            st.write(f"**Jumlah pinjaman:** Rp {app['profil']['jumlah_pinjaman']:,.0f}".replace(",", "."))
                            st.write(f"**Sektor:** {app['profil']['sektor']}, **Tenor:** {app['profil']['tenor']} tahun")
                            if app.get('catatan'):
                                st.write(f"**Catatan:** {app['catatan']}")
            except Exception as e:
                logging.error(f"Error menampilkan status pengajuan: {e}")
                st.warning("Gagal memuat status pengajuan.")

            # ========== ADMIN PANEL ==========
            try:
                if st.query_params.get("admin") == "1":
                    try:
                        from ubelasy.admin import admin_page
                        admin_page()
                    except ImportError:
                        st.error("Modul admin tidak ditemukan.")
                    st.stop()

                if st.query_params.get("bank"):
                    bank_id = st.query_params.get("bank")
                    try:
                        from ubelasy.bank_admin import bank_admin_page
                        bank_admin_page(bank_id)
                    except ImportError:
                        st.error("Modul bank_admin tidak ditemukan.")
                    st.stop()
            except Exception as e:
                logging.error(f"Error admin panel: {e}")

    except Exception as e:
        logging.error(f"Error di Ubelasy: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di aplikasi Ubelasy: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()