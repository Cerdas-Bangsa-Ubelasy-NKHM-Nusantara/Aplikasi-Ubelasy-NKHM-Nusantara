# ubelasy/keuangan_real.py
"""
Fitur Perencanaan Keuangan Real - Ubelasy.
Membantu pengguna mengelola keuangan, menghitung rasio utang, dan mensimulasikan kemampuan pinjaman.
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU ==========
def safe_rerun():
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di keuangan_real: {e}")

def init_keuangan_real_state():
    """Inisialisasi session state untuk Perencanaan Keuangan Real."""
    defaults = {
        "keuangan_real_data": {
            "pendapatan": {
                "gaji": 0.0,
                "usaha": 0.0,
                "investasi": 0.0,
                "lainnya": 0.0
            },
            "pengeluaran": {
                "makanan": 0.0,
                "transport": 0.0,
                "cicilan": 0.0,
                "listrik_air": 0.0,
                "sewa": 0.0,
                "pendidikan": 0.0,
                "kesehatan": 0.0,
                "hiburan": 0.0,
                "tabungan": 0.0,
                "lainnya": 0.0
            },
            "simulasi_pinjaman": {
                "jumlah": 0.0,
                "tenor": 12,
                "bunga": 11.0
            }
        },
        "keuangan_real_hasil": None,
        "keuangan_real_counter": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def hitung_dti(total_cicilan, total_pemasukan):
    if total_pemasukan == 0:
        return 0.0
    return (total_cicilan / total_pemasukan) * 100

def get_rekomendasi(dti, surplus):
    if dti < 30 and surplus > 0:
        return {
            "status": "✅ Sehat",
            "warna": "green",
            "pesan": "Keuangan Anda sehat. Anda layak mengajukan pinjaman baru.",
            "rekomendasi": "Anda dapat mengajukan pinjaman dengan tenang. Pastikan tetap menjaga rasio ini."
        }
    elif dti < 50:
        return {
            "status": "⚠️ Perlu Evaluasi",
            "warna": "orange",
            "pesan": "Rasio utang Anda cukup tinggi. Pertimbangkan untuk mengurangi beban utang terlebih dahulu.",
            "rekomendasi": "Jika tetap ingin mengajukan pinjaman, pilih tenor lebih panjang atau jumlah lebih kecil."
        }
    else:
        return {
            "status": "❌ Tidak Layak",
            "warna": "red",
            "pesan": "Rasio utang Anda sudah terlalu tinggi. Segera kurangi beban utang.",
            "rekomendasi": "Lunasi sebagian utang Anda terlebih dahulu sebelum mengajukan pinjaman baru."
        }

def show_keuangan_real():
    """Menampilkan halaman Perencanaan Keuangan Real."""
    try:
        init_keuangan_real_state()

        st.markdown("## 💰 Perencanaan Keuangan Real")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
            padding: 15px 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">📊</div>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">Analisis Keuangan & Kemampuan Pinjaman</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Masukkan data pendapatan dan pengeluaran Anda untuk mendapatkan gambaran kesehatan keuangan.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== TAB =====
        tab1, tab2, tab3 = st.tabs(["📥 Data Keuangan", "📊 Analisis", "💡 Simulasi Pinjaman"])

        with tab1:
            show_data_keuangan()

        with tab2:
            show_analisis()

        with tab3:
            show_simulasi()

    except Exception as e:
        logging.error(f"Error di show_keuangan_real: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

def show_data_keuangan():
    """Tab input data pendapatan dan pengeluaran."""
    st.markdown("### 📥 Data Pendapatan & Pengeluaran")

    # Ambil data dari session state
    data = st.session_state.keuangan_real_data

    with st.form(key="form_keuangan_real"):
        st.markdown("#### 💵 Pendapatan Bulanan")
        col1, col2 = st.columns(2)
        with col1:
            gaji = st.number_input("💼 Gaji / Upah (Rp)", min_value=0.0, step=100000.0, format="%.0f", value=data["pendapatan"]["gaji"])
            usaha = st.number_input("🏪 Pendapatan Usaha (Rp)", min_value=0.0, step=100000.0, format="%.0f", value=data["pendapatan"]["usaha"])
        with col2:
            investasi = st.number_input("📈 Pendapatan Investasi (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pendapatan"]["investasi"])
            lainnya = st.number_input("💰 Pendapatan Lainnya (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pendapatan"]["lainnya"])

        st.markdown("---")
        st.markdown("#### 📤 Pengeluaran Bulanan")
        col3, col4 = st.columns(2)
        with col3:
            makanan = st.number_input("🍽️ Makanan (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["makanan"])
            transport = st.number_input("🚗 Transport (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["transport"])
            cicilan = st.number_input("🏦 Cicilan / Angsuran (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["cicilan"])
            listrik_air = st.number_input("💡 Listrik & Air (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["listrik_air"])
        with col4:
            sewa = st.number_input("🏠 Sewa / KPR (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["sewa"])
            pendidikan = st.number_input("📚 Pendidikan (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["pendidikan"])
            kesehatan = st.number_input("🏥 Kesehatan (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["kesehatan"])
            hiburan = st.number_input("🎬 Hiburan (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["hiburan"])
            tabungan = st.number_input("🏦 Tabungan (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["tabungan"])
            lainnya_pengeluaran = st.number_input("📦 Lainnya (Rp)", min_value=0.0, step=50000.0, format="%.0f", value=data["pengeluaran"]["lainnya"])

        st.markdown("---")
        submitted = st.form_submit_button("💾 Simpan & Analisis", use_container_width=True, type="primary")

        if submitted:
            # Update data di session state
            data["pendapatan"] = {
                "gaji": gaji,
                "usaha": usaha,
                "investasi": investasi,
                "lainnya": lainnya
            }
            data["pengeluaran"] = {
                "makanan": makanan,
                "transport": transport,
                "cicilan": cicilan,
                "listrik_air": listrik_air,
                "sewa": sewa,
                "pendidikan": pendidikan,
                "kesehatan": kesehatan,
                "hiburan": hiburan,
                "tabungan": tabungan,
                "lainnya": lainnya_pengeluaran
            }
            st.session_state.keuangan_real_data = data
            st.session_state.keuangan_real_counter += 1

            # Hitung analisis
            total_pemasukan = sum(data["pendapatan"].values())
            total_pengeluaran = sum(data["pengeluaran"].values())
            total_cicilan = data["pengeluaran"]["cicilan"]
            dti = hitung_dti(total_cicilan, total_pemasukan)
            surplus = total_pemasukan - total_pengeluaran

            rekom = get_rekomendasi(dti, surplus)

            st.session_state.keuangan_real_hasil = {
                "total_pemasukan": total_pemasukan,
                "total_pengeluaran": total_pengeluaran,
                "surplus": surplus,
                "dti": dti,
                "rekomendasi": rekom,
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            safe_rerun()

        # Tampilkan info jika data sudah disimpan
        if st.session_state.keuangan_real_hasil:
            st.success("✅ Data keuangan berhasil disimpan! Buka tab **Analisis** untuk melihat hasil.")

def show_analisis():
    """Tab analisis keuangan."""
    st.markdown("### 📊 Analisis Keuangan")

    hasil = st.session_state.keuangan_real_hasil
    if not hasil:
        st.info("Belum ada data. Silakan isi data keuangan di tab **Data Keuangan** terlebih dahulu.")
        return

    # ===== METRIK UTAMA =====
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Pemasukan", f"Rp {hasil['total_pemasukan']:,.0f}".replace(",", "."))
    with col2:
        st.metric("📤 Total Pengeluaran", f"Rp {hasil['total_pengeluaran']:,.0f}".replace(",", "."))
    with col3:
        surplus = hasil['surplus']
        st.metric("💵 Surplus / Defisit", f"Rp {surplus:,.0f}".replace(",", "."), delta_color="normal")
    with col4:
        dti = hasil['dti']
        st.metric("📊 Rasio Utang (DTI)", f"{dti:.1f}%", delta=f"{dti:.1f}%", delta_color="inverse")

    # ===== REKOMENDASI =====
    rekom = hasil['rekomendasi']
    st.markdown("---")
    st.markdown("### 💡 Rekomendasi Kelayakan Pinjaman")
    st.markdown(
        f"""
        <div style="
            background-color: {'#d4edda' if rekom['warna'] == 'green' else '#fff3cd' if rekom['warna'] == 'orange' else '#f8d7da'};
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 4px solid {'#28a745' if rekom['warna'] == 'green' else '#ffc107' if rekom['warna'] == 'orange' else '#dc3545'};
            margin: 10px 0;
        ">
            <div style="font-size: 20px; font-weight: bold;">{rekom['status']}</div>
            <div style="margin: 8px 0;">{rekom['pesan']}</div>
            <div style="font-size: 14px; color: #555;"><strong>Rekomendasi:</strong> {rekom['rekomendasi']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ===== GRAFIK PENGELUARAN =====
    st.markdown("---")
    st.markdown("### 📊 Distribusi Pengeluaran")

    data = st.session_state.keuangan_real_data
    pengeluaran = data["pengeluaran"]

    # Buat DataFrame
    df_pengeluaran = pd.DataFrame({
        "Kategori": list(pengeluaran.keys()),
        "Nominal": list(pengeluaran.values())
    })
    df_pengeluaran = df_pengeluaran[df_pengeluaran["Nominal"] > 0]

    if not df_pengeluaran.empty:
        st.bar_chart(df_pengeluaran.set_index("Kategori"), height=300, use_container_width=True)
        with st.expander("📋 Detail Pengeluaran"):
            st.dataframe(df_pengeluaran, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada pengeluaran yang dicatat.")

    # ===== GRAFIK PENDAPATAN =====
    st.markdown("### 📊 Distribusi Pendapatan")

    pendapatan = data["pendapatan"]
    df_pendapatan = pd.DataFrame({
        "Sumber": list(pendapatan.keys()),
        "Nominal": list(pendapatan.values())
    })
    df_pendapatan = df_pendapatan[df_pendapatan["Nominal"] > 0]

    if not df_pendapatan.empty:
        st.bar_chart(df_pendapatan.set_index("Sumber"), height=250, use_container_width=True)
    else:
        st.info("Belum ada pendapatan yang dicatat.")

def show_simulasi():
    """Tab simulasi pinjaman."""
    st.markdown("### 💡 Simulasi Pinjaman")

    hasil = st.session_state.keuangan_real_hasil
    if not hasil:
        st.info("Isi data keuangan terlebih dahulu di tab **Data Keuangan** untuk simulasi yang akurat.")
        return

    data = st.session_state.keuangan_real_data
    total_pemasukan = hasil['total_pemasukan']
    total_pengeluaran = hasil['total_pengeluaran']
    surplus = hasil['surplus']
    dti = hasil['dti']

    st.markdown("#### 🎯 Kemampuan Bayar Anda")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💵 Surplus Bulanan", f"Rp {surplus:,.0f}".replace(",", "."))
    with col2:
        st.metric("📊 Rasio Utang (DTI)", f"{dti:.1f}%")

    st.markdown("---")
    st.markdown("#### 📝 Masukkan Detail Pinjaman yang Diinginkan")

    with st.form(key="form_simulasi_pinjaman"):
        jumlah_pinjaman = st.number_input("💰 Jumlah Pinjaman (Rp)", min_value=1_000_000, step=1_000_000, value=50_000_000, format="%.0f")
        tenor = st.selectbox("📅 Tenor (bulan)", [6, 12, 24, 36, 48, 60], index=2)
        bunga = st.number_input("📈 Suku Bunga (% per tahun)", min_value=0.0, max_value=30.0, step=0.5, value=11.0)

        submitted = st.form_submit_button("🔍 Hitung Kemampuan", use_container_width=True, type="primary")

        if submitted:
            # Hitung angsuran per bulan (metode flat sederhana)
            bunga_bulanan = bunga / 100 / 12
            angsuran_per_bulan = jumlah_pinjaman * (bunga_bulanan * (1 + bunga_bulanan) ** tenor) / ((1 + bunga_bulanan) ** tenor - 1) if tenor > 0 else 0
            total_bayar = angsuran_per_bulan * tenor
            total_bunga = total_bayar - jumlah_pinjaman

            # Cek kemampuan bayar
            if surplus <= 0:
                kemampuan = "Tidak mampu"
                warna = "red"
                pesan = "Anda tidak memiliki surplus bulanan. Lunasi utang atau kurangi pengeluaran terlebih dahulu."
            elif angsuran_per_bulan > surplus:
                kemampuan = "Mampu, tapi berisiko"
                warna = "orange"
                pesan = f"Angsuran (Rp {angsuran_per_bulan:,.0f}) melebihi surplus bulanan Anda (Rp {surplus:,.0f}). Risiko keuangan tinggi."
            else:
                kemampuan = "Mampu"
                warna = "green"
                pesan = f"Anda mampu membayar angsuran sebesar Rp {angsuran_per_bulan:,.0f} per bulan. Selamat!"

            st.markdown("---")
            st.markdown("### 📋 Hasil Simulasi")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💵 Angsuran / Bulan", f"Rp {angsuran_per_bulan:,.0f}".replace(",", "."))
            with col2:
                st.metric("💰 Total Bayar", f"Rp {total_bayar:,.0f}".replace(",", "."))
            with col3:
                st.metric("📈 Total Bunga", f"Rp {total_bunga:,.0f}".replace(",", "."))

            st.markdown(
                f"""
                <div style="
                    background-color: {'#d4edda' if warna == 'green' else '#fff3cd' if warna == 'orange' else '#f8d7da'};
                    padding: 15px 20px;
                    border-radius: 8px;
                    border-left: 4px solid {'#28a745' if warna == 'green' else '#ffc107' if warna == 'orange' else '#dc3545'};
                    margin: 10px 0;
                ">
                    <div style="font-size: 18px; font-weight: bold;">Kemampuan: {kemampuan}</div>
                    <div>{pesan}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if warna == "green":
                st.balloons()
                st.success("🎉 Anda layak mengajukan pinjaman ini!")
            elif warna == "orange":
                st.warning("⚠️ Pertimbangkan kembali jumlah pinjaman atau tenor.")
            else:
                st.error("❌ Anda belum layak mengajukan pinjaman saat ini.")

    # ===== RIWAYAT =====
    st.markdown("---")
    if st.button("🔄 Reset Data Keuangan", use_container_width=True):
        st.session_state.keuangan_real_hasil = None
        st.session_state.keuangan_real_data = {
            "pendapatan": {k: 0.0 for k in st.session_state.keuangan_real_data["pendapatan"].keys()},
            "pengeluaran": {k: 0.0 for k in st.session_state.keuangan_real_data["pengeluaran"].keys()},
            "simulasi_pinjaman": st.session_state.keuangan_real_data["simulasi_pinjaman"]
        }
        st.session_state.keuangan_real_counter += 1
        safe_rerun()

if __name__ == "__main__":
    show_keuangan_real()