# ubelasy/ai_kredit.py
"""
Fitur AI Penilaian Kredit – Ubelasy.
Menghasilkan skor kredit (0-1000) berdasarkan data keuangan dan riwayat pinjaman.
"""

import streamlit as st
import logging
from datetime import datetime

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_rerun():
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di ai_kredit: {e}")

# ========== FUNGSI SKORING ==========
def hitung_skor_kredit(data_keuangan, riwayat_pinjaman):
    """
    Menghitung skor kredit Ubelasy (0-1000) berdasarkan data keuangan dan riwayat.
    """
    skor = 0
    komponen = {}

    # 1. DTI (Debt-to-Income Ratio) – bobot 40%
    total_pemasukan = sum(data_keuangan.get("pendapatan", {}).values())
    total_cicilan = data_keuangan.get("pengeluaran", {}).get("cicilan", 0)
    dti = (total_cicilan / total_pemasukan * 100) if total_pemasukan > 0 else 100

    if dti < 30:
        dti_score = 100
        komponen["DTI"] = {"skor": 100, "keterangan": "Rasio utang sehat (<30%)"}
    elif dti < 50:
        dti_score = 50
        komponen["DTI"] = {"skor": 50, "keterangan": "Rasio utang cukup (30-50%)"}
    else:
        dti_score = 0
        komponen["DTI"] = {"skor": 0, "keterangan": "Rasio utang tinggi (>50%)"}

    skor += dti_score * 0.4

    # 2. Surplus bulanan – bobot 30%
    surplus = sum(data_keuangan.get("pendapatan", {}).values()) - sum(data_keuangan.get("pengeluaran", {}).values())
    if surplus > 0:
        surplus_score = 100
        komponen["Surplus"] = {"skor": 100, "keterangan": f"Surplus Rp {surplus:,.0f} per bulan"}
    else:
        surplus_score = 0
        komponen["Surplus"] = {"skor": 0, "keterangan": f"Defisit Rp {abs(surplus):,.0f} per bulan"}

    skor += surplus_score * 0.3

    # 3. Diversifikasi pendapatan – bobot 20%
    pendapatan = data_keuangan.get("pendapatan", {})
    sumber_aktif = [k for k, v in pendapatan.items() if v > 0]
    if len(sumber_aktif) >= 3:
        diversifikasi_score = 100
        komponen["Diversifikasi"] = {"skor": 100, "keterangan": "Pendapatan beragam (3+ sumber)"}
    elif len(sumber_aktif) == 2:
        diversifikasi_score = 60
        komponen["Diversifikasi"] = {"skor": 60, "keterangan": "Pendapatan cukup beragam (2 sumber)"}
    else:
        diversifikasi_score = 20
        komponen["Diversifikasi"] = {"skor": 20, "keterangan": "Pendapatan kurang beragam"}

    skor += diversifikasi_score * 0.2

    # 4. Riwayat pinjaman – bobot 10% (dummy, bisa dikembangkan dengan data real)
    if riwayat_pinjaman:
        # Asumsi riwayat berisi daftar transaksi pinjaman
        # Kita bisa hitung jumlah pelunasan tepat waktu
        on_time = sum(1 for x in riwayat_pinjaman if x.get("status") == "lunas")
        total = len(riwayat_pinjaman)
        if total > 0:
            rasio_tepat_waktu = on_time / total
            if rasio_tepat_waktu >= 0.9:
                riwayat_score = 100
                komponen["Riwayat"] = {"skor": 100, "keterangan": "Riwayat pembayaran sangat baik"}
            elif rasio_tepat_waktu >= 0.7:
                riwayat_score = 60
                komponen["Riwayat"] = {"skor": 60, "keterangan": "Riwayat pembayaran cukup baik"}
            else:
                riwayat_score = 20
                komponen["Riwayat"] = {"skor": 20, "keterangan": "Riwayat pembayaran perlu perbaikan"}
        else:
            riwayat_score = 50
            komponen["Riwayat"] = {"skor": 50, "keterangan": "Belum ada riwayat pinjaman"}
    else:
        riwayat_score = 50
        komponen["Riwayat"] = {"skor": 50, "keterangan": "Belum ada riwayat pinjaman"}

    skor += riwayat_score * 0.1

    # Skor akhir (0-1000)
    skor_akhir = round(skor * 10, 2)  # skala 0-1000
    # Pastikan dalam rentang 0-1000
    skor_akhir = max(0, min(1000, skor_akhir))

    return skor_akhir, komponen

def tentukan_produk(skor):
    """Menentukan plafon dan suku bunga berdasarkan skor."""
    if skor >= 800:
        plafon = 100_000_000
        bunga = 8.0
        grade = "A"
        rekomendasi = "💎 Anda memiliki profil kredit sangat baik. Nikmati plafon tertinggi dan bunga rendah."
    elif skor >= 600:
        plafon = 75_000_000
        bunga = 10.0
        grade = "B"
        rekomendasi = "📊 Profil kredit baik. Anda berhak atas plafon dan bunga yang kompetitif."
    elif skor >= 400:
        plafon = 50_000_000
        bunga = 12.0
        grade = "C"
        rekomendasi = "🌱 Profil kredit cukup. Perbaiki beberapa aspek untuk mendapatkan bunga lebih rendah."
    else:
        plafon = 25_000_000
        bunga = 15.0
        grade = "D"
        rekomendasi = "⚠️ Profil kredit perlu perbaikan. Fokus pada pengurangan utang dan peningkatan pendapatan."

    return plafon, bunga, grade, rekomendasi

def generate_rekomendasi_perbaikan(komponen):
    """Memberikan rekomendasi perbaikan skor berdasarkan komponen yang lemah."""
    rekomendasi_list = []
    if komponen["DTI"]["skor"] < 50:
        rekomendasi_list.append("📉 **Kurangi rasio utang** – lunasi sebagian cicilan atau tingkatkan pendapatan.")
    if komponen["Surplus"]["skor"] < 50:
        rekomendasi_list.append("💰 **Tingkatkan surplus bulanan** – kurangi pengeluaran atau cari tambahan pemasukan.")
    if komponen["Diversifikasi"]["skor"] < 60:
        rekomendasi_list.append("📈 **Diversifikasi pendapatan** – coba tambahkan sumber penghasilan lain (usaha sampingan, investasi).")
    if komponen["Riwayat"]["skor"] < 60:
        rekomendasi_list.append("✅ **Jaga riwayat pembayaran** – bayar cicilan tepat waktu untuk meningkatkan skor.")

    if not rekomendasi_list:
        rekomendasi_list.append("🌟 Anda sudah dalam kondisi prima! Pertahankan.")

    return rekomendasi_list

# ========== UI UTAMA ==========
def show_ai_kredit():
    """Menampilkan halaman AI Penilaian Kredit."""
    try:
        st.markdown("## 🤖 AI Penilaian Kredit Ubelasy")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
            padding: 15px 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">🧠</div>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">Skor Kredit Cerdas</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Dapatkan skor kredit 0-1000 berdasarkan data keuangan Anda, beserta rekomendasi perbaikan.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Ambil data dari session state
        data_keuangan = st.session_state.get("keuangan_real_data")
        hasil_keuangan = st.session_state.get("keuangan_real_hasil")
        riwayat_pinjaman = st.session_state.get("riwayat_pinjaman", [])  # dummy, bisa dikembangkan

        if not data_keuangan or not hasil_keuangan:
            st.warning("⚠️ Data keuangan belum lengkap. Isi data di **Perencanaan Keuangan Real** terlebih dahulu.")
            if st.button("🔗 Buka Perencanaan Keuangan Real", use_container_width=True):
                st.info("Silakan pilih tab '💰 Perencanaan Keuangan Real' di sidebar kiri.")
            return

        # Hitung skor
        skor, komponen = hitung_skor_kredit(data_keuangan, riwayat_pinjaman)
        plafon, bunga, grade, rekomendasi_umum = tentukan_produk(skor)

        # ===== TAMPILAN =====
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🧠 Skor Kredit", f"{skor:.0f} / 1000", delta=f"Grade {grade}")
        with col2:
            st.metric("💰 Plafon Maksimal", f"Rp {plafon:,.0f}".replace(",", "."))
        with col3:
            st.metric("📉 Suku Bunga", f"{bunga:.1f}% per tahun")

        st.markdown("---")
        st.markdown("### 💡 Rekomendasi")
        st.info(rekomendasi_umum)

        # Detail komponen
        with st.expander("📊 Detail Komponen Skor"):
            for komponen_nama, data in komponen.items():
                st.markdown(f"**{komponen_nama}**: {data['skor']:.0f}% – {data['keterangan']}")

        # Rekomendasi perbaikan
        st.markdown("---")
        st.markdown("### 🛠️ Rekomendasi Perbaikan Skor")
        rekom_perbaikan = generate_rekomendasi_perbaikan(komponen)
        for item in rekom_perbaikan:
            st.markdown(f"- {item}")

        # Tombol refresh (jika ada update data)
        if st.button("🔄 Refresh Data", use_container_width=True):
            safe_rerun()

    except Exception as e:
        logging.error(f"Error di show_ai_kredit: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_ai_kredit()