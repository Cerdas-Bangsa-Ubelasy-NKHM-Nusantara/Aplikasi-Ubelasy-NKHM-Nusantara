# ubelasy/kredit_report.py
import streamlit as st
import pandas as pd
from datetime import datetime

def show_kredit_report():
    st.markdown("## 📊 Rapor Kredit Internal")
    st.markdown("Ringkasan riwayat pinjaman dan kesehatan kredit Anda di platform Ubelasy.")
    
    # Contoh data dummy (nanti diganti dengan data nyata dari database/session)
    # Untuk demo, kita buat data contoh
    if "kredit_data" not in st.session_state:
        # Buat data dummy
        st.session_state.kredit_data = {
            "pinjaman_aktif": [
                {"id": "P001", "bank": "Bank Desa Sejahtera", "jumlah": 36_000_000, 
                 "tenor": 6, "sisa_cicilan": 12_000_000, "status": "Aktif", "jatuh_tempo": "2025-12-31"},
                {"id": "P002", "bank": "Bank Kota Makmur", "jumlah": 50_000_000, 
                 "tenor": 12, "sisa_cicilan": 35_000_000, "status": "Aktif", "jatuh_tempo": "2026-06-30"}
            ],
            "riwayat_pinjaman": [
                {"id": "P000", "bank": "Bank Desa Sejahtera", "jumlah": 20_000_000, 
                 "tenor": 3, "tanggal_lunas": "2024-05-15", "status": "Lunas"},
                {"id": "P001", "bank": "Bank Kota Makmur", "jumlah": 15_000_000, 
                 "tenor": 2, "tanggal_lunas": "2023-12-01", "status": "Lunas"}
            ],
            "skor_kredit": 720,  # skor internal (0-1000)
            "total_pinjaman": 86_000_000,
            "total_terbayar": 35_000_000,
            "total_sisa": 51_000_000,
            "rasio_utang": 0.35  # 35% dari pendapatan (contoh)
        }
    
    data = st.session_state.kredit_data
    
    # ========== METRIK UTAMA ==========
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏦 Skor Kredit", f"{data['skor_kredit']}", delta="👍 Baik" if data['skor_kredit'] >= 700 else "⚠️ Perlu Perbaikan")
    col2.metric("💰 Total Pinjaman", f"Rp {data['total_pinjaman']:,.0f}".replace(",", "."))
    col3.metric("✅ Total Terbayar", f"Rp {data['total_terbayar']:,.0f}".replace(",", "."))
    col4.metric("📉 Sisa Pinjaman", f"Rp {data['total_sisa']:,.0f}".replace(",", "."))
    
    st.markdown("---")
    
    # ========== PINJAMAN AKTIF ==========
    st.subheader("📌 Pinjaman Aktif")
    if data['pinjaman_aktif']:
        df_aktif = pd.DataFrame(data['pinjaman_aktif'])
        df_aktif['sisa_cicilan'] = df_aktif['sisa_cicilan'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        df_aktif['jumlah'] = df_aktif['jumlah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        st.dataframe(df_aktif[['id', 'bank', 'jumlah', 'tenor', 'sisa_cicilan', 'status', 'jatuh_tempo']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada pinjaman aktif saat ini.")
    
    # ========== RIWAYAT PINJAMAN ==========
    st.subheader("📜 Riwayat Pinjaman (Lunas)")
    if data['riwayat_pinjaman']:
        df_riwayat = pd.DataFrame(data['riwayat_pinjaman'])
        df_riwayat['jumlah'] = df_riwayat['jumlah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        st.dataframe(df_riwayat[['id', 'bank', 'jumlah', 'tenor', 'tanggal_lunas', 'status']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada riwayat pinjaman yang lunas.")
    
    st.markdown("---")
    
    # ========== GRAFIK / ANALISIS ==========
    st.subheader("📊 Analisis Kredit")
    # Rasio utang terhadap pendapatan
    st.metric("📉 Rasio Utang terhadap Pendapatan", f"{data['rasio_utang']*100:.1f}%", 
              delta="Sehat" if data['rasio_utang'] < 0.3 else "Perlu Perhatian")
    
    # Visualisasi sederhana
    df_chart = pd.DataFrame({
        "Kategori": ["Total Pinjaman", "Total Terbayar", "Sisa Pinjaman"],
        "Nilai": [data['total_pinjaman'], data['total_terbayar'], data['total_sisa']]
    })
    st.bar_chart(df_chart.set_index("Kategori"), height=300)
    
    st.caption("💡 Rapor kredit ini membantu Anda memantau kesehatan keuangan dan riwayat pinjaman di Ubelasy.")