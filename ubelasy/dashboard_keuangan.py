# ubelasy/dashboard_keuangan.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def show_dashboard_keuangan():
    st.markdown("## 📊 Dashboard Keuangan Pribadi")
    st.markdown("Gambaran kesehatan finansial Anda secara keseluruhan.")
    
    # ========== INISIALISASI DATA ==========
    if "keuangan_data" not in st.session_state:
        st.session_state.keuangan_data = {
            "pemasukan": [],
            "pengeluaran": []
        }
    
    if "aset_kewajiban" not in st.session_state:
        st.session_state.aset_kewajiban = {
            "aset": [],
            "kewajiban": []
        }
    
    # ========== DATA TRANSAKSI ==========
    pemasukan = st.session_state.keuangan_data["pemasukan"]
    pengeluaran = st.session_state.keuangan_data["pengeluaran"]
    
    if not pemasukan and not pengeluaran:
        st.info("📋 Belum ada data keuangan. Silakan tambahkan transaksi di tab **Perencanaan Keuangan** terlebih dahulu.")
        return
    
    # ========== RINGKASAN ==========
    total_pemasukan = sum([i["nominal"] for i in pemasukan])
    total_pengeluaran = sum([i["nominal"] for i in pengeluaran])
    saldo = total_pemasukan - total_pengeluaran
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Pemasukan", f"Rp {total_pemasukan:,.0f}".replace(",", "."))
    col2.metric("💸 Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
    col3.metric("📊 Saldo", f"Rp {saldo:,.0f}".replace(",", "."), 
                delta="Positif" if saldo >= 0 else "Negatif")
    
    if total_pemasukan > 0:
        rasio = total_pengeluaran / total_pemasukan
        status = "Sehat" if rasio < 0.7 else "Perlu Perhatian"
        col4.metric("📈 Rasio Pengeluaran/Pemasukan", f"{rasio*100:.1f}%", delta=status)
    else:
        col4.metric("📈 Rasio Pengeluaran/Pemasukan", "N/A", delta="Tambah pemasukan")
    
    st.markdown("---")
    
    # ========== GRAFIK ARUS KAS BULANAN ==========
    st.subheader("📉 Arus Kas Bulanan")
    
    all_trans = []
    for p in pemasukan:
        all_trans.append({"tanggal": p["tanggal"], "tipe": "Pemasukan", "nominal": p["nominal"], "deskripsi": p["deskripsi"]})
    for p in pengeluaran:
        all_trans.append({"tanggal": p["tanggal"], "tipe": "Pengeluaran", "nominal": p["nominal"], "deskripsi": p["deskripsi"]})
    
    if all_trans:
        df = pd.DataFrame(all_trans)
        df["tanggal"] = pd.to_datetime(df["tanggal"])
        df["bulan"] = df["tanggal"].dt.to_period("M")
        
        bulanan = df.groupby(["bulan", "tipe"])["nominal"].sum().unstack().fillna(0)
        if not bulanan.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            bulanan.plot(kind="bar", ax=ax, color=["#2ecc71", "#e74c3c"])
            ax.set_title("Arus Kas Bulanan")
            ax.set_xlabel("Bulan")
            ax.set_ylabel("Nominal (Rp)")
            ax.legend(["Pemasukan", "Pengeluaran"])
            ax.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)
        else:
            st.info("Data belum cukup untuk grafik bulanan.")
    
    # ========== GRAFIK PENGELUARAN PER KATEGORI ==========
    st.subheader("🧾 Pengeluaran Berdasarkan Kategori")
    
    if pengeluaran:
        df_peng = pd.DataFrame(pengeluaran)
        if not df_peng.empty:
            kategori = df_peng.groupby("deskripsi")["nominal"].sum().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 6))
            kategori.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90)
            ax.set_title("Persentase Pengeluaran per Kategori")
            ax.set_ylabel("")
            st.pyplot(fig)
        else:
            st.info("Belum ada data pengeluaran.")
    
    st.markdown("---")
    
    # ========== ASET & KEWAJIBAN ==========
    st.subheader("🏦 Aset & Kewajiban")
    
    # Form untuk menambah aset
    with st.expander("➕ Tambah Aset", expanded=False):
        nama_aset = st.text_input("Nama Aset", placeholder="Misal: Tabungan, Emas, Properti", key="nama_aset_input")
        nilai_aset = st.number_input("Nilai (Rp)", min_value=0, value=0, step=100_000, key="nilai_aset_input")
        if st.button("✅ Tambah Aset", use_container_width=True, key="tambah_aset_btn"):
            if nama_aset.strip() and nilai_aset > 0:
                st.session_state.aset_kewajiban["aset"].append({
                    "nama": nama_aset,
                    "nilai": nilai_aset,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Aset berhasil ditambahkan!")
                st.rerun()
            else:
                st.warning("Isi nama dan nilai aset.")
    
    # Form untuk menambah kewajiban
    with st.expander("➕ Tambah Kewajiban (Utang)", expanded=False):
        nama_kewajiban = st.text_input("Nama Kewajiban", placeholder="Misal: Sisa Utang, Pinjaman", key="nama_kewajiban_input")
        nilai_kewajiban = st.number_input("Nilai (Rp)", min_value=0, value=0, step=100_000, key="nilai_kewajiban_input")
        if st.button("✅ Tambah Kewajiban", use_container_width=True, key="tambah_kewajiban_btn"):
            if nama_kewajiban.strip() and nilai_kewajiban > 0:
                st.session_state.aset_kewajiban["kewajiban"].append({
                    "nama": nama_kewajiban,
                    "nilai": nilai_kewajiban,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Kewajiban berhasil ditambahkan!")
                st.rerun()
            else:
                st.warning("Isi nama dan nilai kewajiban.")
    
    # Tampilkan ringkasan aset dan kewajiban
    total_aset = sum([a["nilai"] for a in st.session_state.aset_kewajiban["aset"]])
    total_kewajiban = sum([k["nilai"] for k in st.session_state.aset_kewajiban["kewajiban"]])
    net_worth = total_aset - total_kewajiban
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏦 Total Aset", f"Rp {total_aset:,.0f}".replace(",", "."))
    col2.metric("📉 Total Kewajiban", f"Rp {total_kewajiban:,.0f}".replace(",", "."))
    col3.metric("💎 Net Worth", f"Rp {net_worth:,.0f}".replace(",", "."),
                delta="Positif" if net_worth >= 0 else "Negatif")
    
    # Tabel aset
    if st.session_state.aset_kewajiban["aset"]:
        st.markdown("#### Aset")
        df_aset = pd.DataFrame(st.session_state.aset_kewajiban["aset"])
        df_aset["nilai"] = df_aset["nilai"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        st.dataframe(df_aset[["nama", "nilai", "tanggal"]], use_container_width=True, hide_index=True)
    
    if st.session_state.aset_kewajiban["kewajiban"]:
        st.markdown("#### Kewajiban")
        df_kewajiban = pd.DataFrame(st.session_state.aset_kewajiban["kewajiban"])
        df_kewajiban["nilai"] = df_kewajiban["nilai"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        st.dataframe(df_kewajiban[["nama", "nilai", "tanggal"]], use_container_width=True, hide_index=True)
    
    # Tombol reset data aset & kewajiban
    if st.button("🗑️ Reset Semua Data Aset & Kewajiban", use_container_width=True, key="reset_aset_btn"):
        st.session_state.aset_kewajiban = {"aset": [], "kewajiban": []}
        st.rerun()
    
    st.markdown("---")
    st.caption("💡 Dashboard ini memberikan gambaran kesehatan finansial Anda. Tambahkan data secara rutin untuk pemantauan yang lebih baik.")