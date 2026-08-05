# ubelasy/dashboard_keuangan_real.py
"""
Fitur Dashboard Keuangan Real untuk Ubelasy.
Menampilkan visualisasi interaktif kesehatan keuangan berdasarkan data dari Perencanaan Keuangan Real.
"""

import streamlit as st
import pandas as pd
import logging
import matplotlib.pyplot as plt

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_rerun():
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di dashboard_keuangan_real: {e}")

# Cek ketersediaan plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def show_dashboard_keuangan_real():
    """Menampilkan Dashboard Keuangan Real dengan visualisasi interaktif."""
    try:
        st.markdown("## 📊 Dashboard Keuangan Real")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
            padding: 15px 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">📈</div>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">Analisis Keuangan Interaktif</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Visualisasi lengkap dari data Perencanaan Keuangan Anda.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== AMBIL DATA DARI SESSION STATE =====
        hasil = st.session_state.get("keuangan_real_hasil")
        data = st.session_state.get("keuangan_real_data")

        if not hasil or not data:
            st.info("📝 Belum ada data keuangan. Silakan isi data di tab **Perencanaan Keuangan Real** terlebih dahulu.")
            if st.button("🔗 Buka Perencanaan Keuangan Real", use_container_width=True):
                st.info("Silakan pilih tab '💰 Perencanaan Keuangan Real' di sidebar kiri.")
            return

        # Ekstrak data
        total_pemasukan = hasil.get("total_pemasukan", 0)
        total_pengeluaran = hasil.get("total_pengeluaran", 0)
        surplus = hasil.get("surplus", 0)
        dti = hasil.get("dti", 0)
        rekom = hasil.get("rekomendasi", {})
        status = rekom.get("status", "❓ Tidak Diketahui")
        warna = rekom.get("warna", "gray")

        pendapatan = data.get("pendapatan", {})
        pengeluaran = data.get("pengeluaran", {})

        # ===== 1. METRIK UTAMA =====
        st.markdown("### 📊 Ringkasan Keuangan")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Pemasukan", f"Rp {total_pemasukan:,.0f}".replace(",", "."))
        with col2:
            st.metric("📤 Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}".replace(",", "."))
        with col3:
            st.metric("💵 Surplus / Defisit", f"Rp {surplus:,.0f}".replace(",", "."), delta_color="normal")
        with col4:
            st.metric("📊 Rasio Utang (DTI)", f"{dti:.1f}%", delta=f"{dti:.1f}%", delta_color="inverse")

        # ===== 2. STATUS KESEHATAN =====
        st.markdown("---")
        st.markdown("### 💡 Status Kesehatan Keuangan")
        color_map = {"green": "#d4edda", "orange": "#fff3cd", "red": "#f8d7da"}
        border_map = {"green": "#28a745", "orange": "#ffc107", "red": "#dc3545"}
        bg = color_map.get(warna, "#e9ecef")
        border = border_map.get(warna, "#6c757d")
        st.markdown(
            f"""
            <div style="
                background-color: {bg};
                padding: 15px 20px;
                border-radius: 8px;
                border-left: 4px solid {border};
                margin: 10px 0;
            ">
                <div style="font-size: 20px; font-weight: bold;">{status}</div>
                <div style="margin: 8px 0;">{rekom.get('pesan', '')}</div>
                <div style="font-size: 14px; color: #555;"><strong>Rekomendasi:</strong> {rekom.get('rekomendasi', '')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ===== 3. GRAFIK DISTRIBUSI (Plotly jika tersedia) =====
        st.markdown("---")
        st.markdown("### 📊 Distribusi Pendapatan & Pengeluaran")

        # Siapkan data untuk pie chart
        df_pendapatan = pd.DataFrame({
            "Sumber": list(pendapatan.keys()),
            "Nominal": list(pendapatan.values())
        })
        df_pendapatan = df_pendapatan[df_pendapatan["Nominal"] > 0]

        df_pengeluaran = pd.DataFrame({
            "Kategori": list(pengeluaran.keys()),
            "Nominal": list(pengeluaran.values())
        })
        df_pengeluaran = df_pengeluaran[df_pengeluaran["Nominal"] > 0]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 💵 Pendapatan")
            if not df_pendapatan.empty:
                if PLOTLY_AVAILABLE:
                    fig = px.pie(df_pendapatan, values="Nominal", names="Sumber", hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
                    fig.update_layout(height=300, margin=dict(l=10, r=10, t=20, b=10), showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.pie(df_pendapatan["Nominal"], labels=df_pendapatan["Sumber"], autopct='%1.1f%%', startangle=90)
                    ax.set_title("Sumber Pendapatan")
                    st.pyplot(fig)
            else:
                st.caption("Tidak ada data pendapatan.")

        with col2:
            st.markdown("#### 📤 Pengeluaran")
            if not df_pengeluaran.empty:
                if PLOTLY_AVAILABLE:
                    fig = px.pie(df_pengeluaran, values="Nominal", names="Kategori", hole=0.4, color_discrete_sequence=px.colors.sequential.Reds_r)
                    fig.update_layout(height=300, margin=dict(l=10, r=10, t=20, b=10), showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.pie(df_pengeluaran["Nominal"], labels=df_pengeluaran["Kategori"], autopct='%1.1f%%', startangle=90)
                    ax.set_title("Kategori Pengeluaran")
                    st.pyplot(fig)
            else:
                st.caption("Tidak ada data pengeluaran.")

        # ===== 4. BAR CHART PERBANDINGAN =====
        st.markdown("---")
        st.markdown("### 📊 Perbandingan Pendapatan vs Pengeluaran per Kategori")

        # Buat DataFrame gabungan untuk bar chart perbandingan (hanya yang ada)
        semua_kategori = list(set(pendapatan.keys()) | set(pengeluaran.keys()))
        df_perbandingan = pd.DataFrame({
            "Kategori": semua_kategori,
            "Pendapatan": [pendapatan.get(k, 0) for k in semua_kategori],
            "Pengeluaran": [pengeluaran.get(k, 0) for k in semua_kategori]
        })
        df_perbandingan = df_perbandingan[(df_perbandingan["Pendapatan"] > 0) | (df_perbandingan["Pengeluaran"] > 0)]

        if not df_perbandingan.empty and PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_perbandingan["Kategori"],
                y=df_perbandingan["Pendapatan"],
                name='Pendapatan',
                marker_color='#2e7daf'
            ))
            fig.add_trace(go.Bar(
                x=df_perbandingan["Kategori"],
                y=df_perbandingan["Pengeluaran"],
                name='Pengeluaran',
                marker_color='#dc3545'
            ))
            fig.update_layout(height=350, barmode='group', margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        elif not df_perbandingan.empty:
            # Fallback matplotlib
            fig, ax = plt.subplots(figsize=(8, 4))
            x = df_perbandingan["Kategori"]
            width = 0.35
            ax.bar(x - width/2, df_perbandingan["Pendapatan"], width, label='Pendapatan', color='#2e7daf')
            ax.bar(x + width/2, df_perbandingan["Pengeluaran"], width, label='Pengeluaran', color='#dc3545')
            ax.set_ylabel('Nominal (Rp)')
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("Tidak ada data untuk perbandingan.")

        # ===== 5. TABEL DETAIL =====
        st.markdown("---")
        st.markdown("### 📋 Detail Transaksi")

        detail_data = []
        for k, v in pendapatan.items():
            if v > 0:
                detail_data.append({"Kategori / Sumber": k.capitalize(), "Jenis": "💵 Pendapatan", "Nominal (Rp)": v})
        for k, v in pengeluaran.items():
            if v > 0:
                detail_data.append({"Kategori / Sumber": k.capitalize(), "Jenis": "📤 Pengeluaran", "Nominal (Rp)": v})

        if detail_data:
            df_detail = pd.DataFrame(detail_data)
            st.dataframe(df_detail, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada transaksi yang dicatat.")

        # ===== 6. TOMBOL REFRESH =====
        st.markdown("---")
        if st.button("🔄 Refresh Data", use_container_width=True):
            safe_rerun()

    except Exception as e:
        logging.error(f"Error di show_dashboard_keuangan_real: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_dashboard_keuangan_real()