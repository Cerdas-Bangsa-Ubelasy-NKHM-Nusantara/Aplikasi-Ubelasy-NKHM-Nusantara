# ubelasy/keuangan.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def show_keuangan():
    st.markdown("## 💰 Simulasi & Perencanaan Keuangan")
    st.markdown("Kelola keuangan pribadi dan simulasikan pelunasan utang lebih cepat.")
    
    # ===== SUB-TAB =====
    sub_tab1, sub_tab2 = st.tabs(["📉 Simulasi Pelunasan Utang", "📊 Perencanaan Keuangan Pribadi"])
    
    # ============================================================
    # SUB-TAB 1: SIMULASI PELUNASAN UTANG
    # ============================================================
    with sub_tab1:
        st.markdown("### Simulasi Pelunasan Utang dengan Pembayaran Ekstra")
        st.markdown("Masukkan data pinjaman Anda dan lihat dampak menambah angsuran bulanan.")
        
        with st.form("form_simulasi_pelunasan"):
            col1, col2 = st.columns(2)
            with col1:
                saldo = st.number_input("Sisa Pokok Pinjaman (Rp)", min_value=0, value=50_000_000, step=1_000_000, format="%d")
                bunga_tahunan = st.number_input("Suku Bunga (% per tahun)", min_value=0.0, max_value=30.0, value=11.0, step=0.5)
                angsuran_saat_ini = st.number_input("Angsuran Bulanan Saat Ini (Rp)", min_value=0, value=1_500_000, step=100_000, format="%d")
            with col2:
                tambahan_bayar = st.number_input("Tambahan Pembayaran Bulanan (Rp)", min_value=0, value=500_000, step=50_000, format="%d")
                durasi_saat_ini = st.number_input("Durasi Saat Ini (bulan)", min_value=1, value=48, step=1)
            
            submitted = st.form_submit_button("💡 Hitung Simulasi", use_container_width=True)
        
        if submitted:
            if saldo <= 0 or angsuran_saat_ini <= 0 or durasi_saat_ini <= 0:
                st.error("Pastikan semua nilai > 0.")
            else:
                # Konversi bunga bulanan
                bunga_bulanan = bunga_tahunan / 100 / 12
                
                # Skenario saat ini (tanpa tambahan)
                total_bunga_saat_ini = (angsuran_saat_ini * durasi_saat_ini) - saldo
                total_bayar_saat_ini = angsuran_saat_ini * durasi_saat_ini
                
                # Skenario dengan tambahan
                angsuran_baru = angsuran_saat_ini + tambahan_bayar
                # Hitung durasi baru dengan rumus anuitas (aproksimasi)
                # Untuk sederhana, kita hitung dengan simulasi bulanan
                saldo_sim = saldo
                bulan = 0
                total_bunga_baru = 0
                while saldo_sim > 0 and bulan < 600:  # max 50 tahun
                    bunga_bulan = saldo_sim * bunga_bulanan
                    pokok_bayar = min(angsuran_baru - bunga_bulan, saldo_sim)
                    if pokok_bayar <= 0:
                        break
                    saldo_sim -= pokok_bayar
                    total_bunga_baru += bunga_bulan
                    bulan += 1
                    if saldo_sim < 0:
                        saldo_sim = 0
                
                if bulan == 0:
                    st.error("Simulasi gagal, periksa input.")
                else:
                    durasi_baru = bulan
                    total_bayar_baru = angsuran_baru * durasi_baru
                    
                    st.markdown("---")
                    st.markdown("#### 📊 Hasil Simulasi")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Durasi Saat Ini", f"{durasi_saat_ini} bulan", delta=None)
                        st.metric("Total Bunga Saat Ini", f"Rp {total_bunga_saat_ini:,.0f}".replace(",", "."))
                        st.metric("Total Bayar Saat Ini", f"Rp {total_bayar_saat_ini:,.0f}".replace(",", "."))
                    with col2:
                        st.metric("Durasi Baru", f"{durasi_baru} bulan", delta=f"-{durasi_saat_ini - durasi_baru} bulan" if durasi_baru < durasi_saat_ini else f"+{durasi_baru - durasi_saat_ini} bulan")
                        st.metric("Total Bunga Baru", f"Rp {total_bunga_baru:,.0f}".replace(",", "."), delta=f"-Rp {total_bunga_saat_ini - total_bunga_baru:,.0f}".replace(",", ".") if total_bunga_baru < total_bunga_saat_ini else f"+Rp {total_bunga_baru - total_bunga_saat_ini:,.0f}".replace(",", "."))
                        st.metric("Total Bayar Baru", f"Rp {total_bayar_baru:,.0f}".replace(",", "."), delta=f"-Rp {total_bayar_saat_ini - total_bayar_baru:,.0f}".replace(",", ".") if total_bayar_baru < total_bayar_saat_ini else f"+Rp {total_bayar_baru - total_bayar_saat_ini:,.0f}".replace(",", "."))
                    
                    # Grafik perbandingan
                    fig, ax = plt.subplots(figsize=(8, 4))
                    labels = ['Saat Ini', 'Dengan Tambahan']
                    durasi_data = [durasi_saat_ini, durasi_baru]
                    bunga_data = [total_bunga_saat_ini / 1_000_000, total_bunga_baru / 1_000_000]
                    x = range(len(labels))
                    width = 0.35
                    ax.bar([i - width/2 for i in x], durasi_data, width, label='Durasi (bulan)', color='#1f77b4')
                    ax.bar([i + width/2 for i in x], bunga_data, width, label='Total Bunga (juta)', color='#ff7f0e')
                    ax.set_xticks(x)
                    ax.set_xticklabels(labels)
                    ax.set_ylabel('Nilai')
                    ax.set_title('Perbandingan Durasi & Bunga')
                    ax.legend()
                    st.pyplot(fig)
                    
                    # Simpan hasil ke session state untuk digunakan di tempat lain
                    st.session_state.simulasi_pelunasan = {
                        "durasi_baru": durasi_baru,
                        "total_bunga_baru": total_bunga_baru,
                        "total_bayar_baru": total_bayar_baru
                    }
    
    # ============================================================
    # SUB-TAB 2: PERENCANAAN KEUANGAN PRIBADI
    # ============================================================
    with sub_tab2:
        st.markdown("### Perencanaan Keuangan Pribadi")
        st.markdown("Catat pemasukan dan pengeluaran bulanan untuk melihat kemampuan bayar pinjaman.")
        
        # Inisialisasi data di session state
        if "keuangan_data" not in st.session_state:
            st.session_state.keuangan_data = {
                "pemasukan": [],
                "pengeluaran": []
            }
        
        # ===== TAMBAH DATA =====
        with st.expander("➕ Tambah Pemasukan / Pengeluaran", expanded=False):
            col_type, col_nominal, col_desc, col_act = st.columns([1, 1, 2, 1])
            with col_type:
                tipe = st.selectbox("Tipe", ["Pemasukan", "Pengeluaran"], key="tipe_transaksi")
            with col_nominal:
                nominal = st.number_input("Nominal (Rp)", min_value=0, value=1_000_000, step=100_000, key="nominal_transaksi")
            with col_desc:
                deskripsi = st.text_input("Deskripsi", placeholder="Misal: Gaji, Makanan, dll.", key="deskripsi_transaksi")
            with col_act:
                if st.button("✅ Tambah", key="tambah_transaksi"):
                    if nominal > 0 and deskripsi.strip():
                        item = {
                            "tipe": tipe,
                            "nominal": nominal,
                            "deskripsi": deskripsi,
                            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        if tipe == "Pemasukan":
                            st.session_state.keuangan_data["pemasukan"].append(item)
                        else:
                            st.session_state.keuangan_data["pengeluaran"].append(item)
                        st.success("Data berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("Isi nominal dan deskripsi.")
        
        # ===== TAMPILKAN DATA =====
        st.markdown("#### 📋 Ringkasan Transaksi")
        total_pemasukan = sum([i["nominal"] for i in st.session_state.keuangan_data["pemasukan"]])
        total_pengeluaran = sum([i["nominal"] for i in st.session_state.keuangan_data["pengeluaran"]])
        saldo = total_pemasukan - total_pengeluaran
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Pemasukan", f"Rp {total_pemasukan:,.0f}".replace(",", "."))
        col2.metric("💸 Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
        col3.metric("📊 Saldo", f"Rp {saldo:,.0f}".replace(",", "."), delta="Positif" if saldo >= 0 else "Negatif")
        
        # Tampilkan tabel
        if st.session_state.keuangan_data["pemasukan"] or st.session_state.keuangan_data["pengeluaran"]:
            all_trans = []
            for p in st.session_state.keuangan_data["pemasukan"]:
                all_trans.append({"Tipe": "💹 Pemasukan", "Nominal": p["nominal"], "Deskripsi": p["deskripsi"], "Tanggal": p["tanggal"]})
            for p in st.session_state.keuangan_data["pengeluaran"]:
                all_trans.append({"Tipe": "💸 Pengeluaran", "Nominal": p["nominal"], "Deskripsi": p["deskripsi"], "Tanggal": p["tanggal"]})
            df_trans = pd.DataFrame(all_trans)
            df_trans = df_trans.sort_values("Tanggal", ascending=False)
            st.dataframe(df_trans, use_container_width=True, hide_index=True)
            
            # Grafik
            fig, ax = plt.subplots(figsize=(8, 4))
            labels = ['Pemasukan', 'Pengeluaran']
            values = [total_pemasukan, total_pengeluaran]
            colors = ['#2ecc71', '#e74c3c']
            ax.bar(labels, values, color=colors)
            ax.set_title('Perbandingan Pemasukan & Pengeluaran')
            ax.set_ylabel('Nominal (Rp)')
            st.pyplot(fig)
        
        # ===== ANALISIS KEMAMPUAN BAYAR =====
        st.markdown("#### 💡 Analisis Kemampuan Bayar Pinjaman")
        if total_pemasukan > 0:
            rasio_utang = total_pengeluaran / total_pemasukan if total_pemasukan > 0 else 0
            st.metric("Rasio Pengeluaran terhadap Pemasukan", f"{rasio_utang*100:.1f}%", delta="Sehat" if rasio_utang < 0.7 else "Perlu Perhatian")
            
            # Rekomendasi sederhana
            if rasio_utang < 0.5:
                st.success("✅ Keuangan Anda sehat. Anda memiliki ruang untuk mengajukan pinjaman baru atau berinvestasi.")
            elif rasio_utang < 0.7:
                st.warning("⚠️ Pengeluaran cukup tinggi. Pertimbangkan untuk menekan pengeluaran atau menambah pemasukan.")
            else:
                st.error("❌ Pengeluaran sangat tinggi. Sebaiknya kurangi utang dan pengeluaran sebelum mengajukan pinjaman baru.")
        else:
            st.info("Tambahkan data pemasukan untuk melihat analisis.")
        
        # Tombol reset data
        if st.button("🗑️ Reset Semua Data Keuangan", use_container_width=True):
            st.session_state.keuangan_data = {"pemasukan": [], "pengeluaran": []}
            st.rerun()