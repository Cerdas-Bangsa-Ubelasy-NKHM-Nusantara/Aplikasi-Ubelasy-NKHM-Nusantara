# ubelasy.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    """Halaman utama Sistem Ubelasy"""
    
    st.title("🌾 Sistem Pinjaman Digital Ubelasy")
    st.markdown("**Versi 2 Periode · dPSH Maks = 2 · Penurunan Suku Bunga 0,5% per Periode**")
    st.markdown("Keuangan Berkelanjutan untuk Ketahanan Pangan & Energi Nusantara")
    st.markdown("---")
    
    # Sidebar input parameter
    with st.sidebar:
        st.header("⚙️ Parameter Pinjaman")
        K = st.number_input("Jumlah Pinjaman per Periode (Rp)", value=36_000_000, step=1_000_000, format="%d")
        r1 = st.number_input("Suku bunga awal (r₁) %", value=11.0, step=0.5)
        delta = st.number_input("Penurunan suku bunga per periode (Δr) %", value=0.5, step=0.1)
        n = st.number_input("Jumlah periode (n)", min_value=1, max_value=10, value=2, step=1)
        tp = st.number_input("Tenor per periode (tₚ) tahun", min_value=0.5, max_value=30.0, value=3.0, step=0.5)
        m = st.number_input("Tahun bayar di periode terakhir (m)", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
        tipe = st.selectbox("Tipe Bank / Wilayah", ["desa", "kota"], format_func=lambda x: "🏡 Pedesaan (PSH = SHA × T/50)" if x=="desa" else "🏙️ Perkotaan (PSH = SHA × T/60)")
        biaya_dana = st.number_input("Biaya Dana + Overhead (%)", value=9.0, step=0.5)
        
        if m > tp:
            st.error(f"⚠️ m ({m}) tidak boleh lebih besar dari tₚ ({tp})")
            return
        
        hitung = st.button("🚀 Hitung Simulasi", type="primary", use_container_width=True)
    
    # Fungsi hitung Ubelasy
    def hitung_ubelasy(K, r1, delta, n, tp, m, tipe, biaya_dana):
        r = []
        for i in range(n):
            rate = r1 - i * delta
            rate = max(0, rate)
            r.append(rate / 100)
        
        T = n * tp
        dPSH = T / 25
        total_pokok = n * K
        TSH = [K * (1 + r[i] * tp) for i in range(n)]
        TSH_last = TSH[-1]
        SHA = max(0, TSH_last * (1 - m / tp))
        
        bayar_sebelum_psh = 0
        for i in range(n-1):
            bayar_sebelum_psh += TSH[i]
        bayar_sebelum_psh += TSH_last * (m / tp)
        
        faktor_psh = T / 50 if tipe == "desa" else T / 60
        PSH = SHA * faktor_psh
        bayar_sesudah_psh = bayar_sebelum_psh + (SHA - PSH)
        
        laba_nominal = bayar_sesudah_psh - total_pokok
        laba_persen = (laba_nominal / total_pokok) * 100
        return_tahunan = laba_persen / T
        
        weighted_bunga = sum(r[i] * tp for i in range(n))
        rata_bunga = (weighted_bunga / T) * 100
        spread = rata_bunga - biaya_dana
        
        psh_persen_total = (PSH / total_pokok) * 100
        
        detail = []
        for i in range(n):
            bunga_persen = r[i] * 100
            tsh = TSH[i]
            angsuran_bulan = tsh / (tp * 12)
            is_last = (i == n-1)
            dibayar = tsh if not is_last else tsh * (m / tp)
            sisa = 0 if not is_last else SHA
            detail.append({
                "Periode": i+1,
                "Suku Bunga (%)": round(bunga_persen, 2),
                "Total Kewajiban (Rp)": f"Rp {tsh:,.0f}".replace(",","."),
                "Angsuran/bln (Rp)": f"Rp {angsuran_bulan:,.0f}".replace(",","."),
                "Total Dibayar (Rp)": f"Rp {dibayar:,.0f}".replace(",","."),
                "Sisa Hutang Akhir (Rp)": f"Rp {sisa:,.0f}".replace(",",".")
            })
        
        if dPSH <= 0.20:
            status = "🟢 Pemula (Beginner)"
        elif dPSH <= 0.50:
            status = "🔵 Berkembang (Developing)"
        elif dPSH <= 1.00:
            status = "🟡 Madya (Intermediate)"
        elif dPSH <= 1.80:
            status = "🟠 Lanjut (Advanced)"
        else:
            status = "🔴 Yobel (Jubilee)"
        
        return {
            "T": T, "dPSH": dPSH, "total_pokok": total_pokok,
            "SHA": SHA, "PSH": PSH, "psh_persen_total": psh_persen_total,
            "laba_persen": laba_persen, "return_tahunan": return_tahunan,
            "rata_bunga": rata_bunga, "spread": spread,
            "detail": detail, "status": status, "faktor_psh": faktor_psh
        }
    
    if hitung:
        with st.spinner("Menghitung..."):
            h = hitung_ubelasy(K, r1, delta, n, tp, m, tipe, biaya_dana)
        
        # Tampilkan hasil
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📅 Total Tenor (T)", f"{h['T']} tahun")
        col1.metric("⚖️ dPSH", f"{h['dPSH']:.4f} / 2")
        col2.metric("🏦 Total Pinjaman", f"Rp {h['total_pokok']:,.0f}".replace(",","."))
        col2.metric("🆓 PSH Diterima", f"Rp {h['PSH']:,.0f}".replace(",",".") + f" ({h['psh_persen_total']:.2f}%)")
        col3.metric("💰 Keuntungan Bank", f"{h['laba_persen']:.2f}%")
        col3.metric("📈 Return Tahunan", f"{h['return_tahunan']:.2f}% p.a")
        col4.metric("📉 Rata-rata Bunga", f"{h['rata_bunga']:.2f}%")
        col4.metric("📊 Spread", f"{h['spread']:.2f}%")
        
        st.subheader("📋 Detail per Periode")
        st.dataframe(pd.DataFrame(h['detail']), use_container_width=True, hide_index=True)
        
        st.subheader("📌 Status Debitur")
        st.info(f"**{h['status']}** (dPSH = {h['dPSH']:.4f})")
        
        # Grafik suku bunga
        bunga = [h['detail'][p]['Suku Bunga (%)'] for p in range(n)]
        fig, ax = plt.subplots()
        ax.plot(range(1, n+1), bunga, marker='o', color='#2e7d32')
        ax.set_xlabel("Periode"); ax.set_ylabel("Suku Bunga (%)")
        ax.set_title("Penurunan Suku Bunga 0.5% per Periode")
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
    else:
        st.info("👈 Masukkan parameter di sidebar dan tekan tombol **Hitung Simulasi**")

if __name__ == "__main__":
    main()
