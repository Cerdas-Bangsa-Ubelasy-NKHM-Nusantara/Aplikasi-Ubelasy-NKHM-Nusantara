# ubelasy/main.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from ubelasy.calculator import calculate_loan
from ubelasy.aggregator import get_recommendations, submit_application, get_all_applications_for_user

def main():
    st.title("🌾 Ubelasy – Agregator Pinjaman Berkelanjutan")
    st.markdown("**Skema PSH & Penurunan Suku Bunga 0,5% per Periode**")
    st.markdown("---")
    
    # ========== SIDEBAR UNTUK SIMULASI ==========
    with st.sidebar:
        # Tampilkan skor NKHM jika tersedia dari session state
        if "nkhm_scores" in st.session_state:
            nkhm_total = sum(st.session_state.nkhm_scores.values())
            st.metric("🧠 Skor NKHM", nkhm_total)
            st.caption("(Semakin tinggi skor, semakin baik peluang mendapat pinjaman)")
            st.markdown("---")
        else:
            st.info("Mainkan game NKHM untuk meningkatkan skor Anda!")
            st.markdown("---")        
        
        st.header("⚙️ Simulasi Pinjaman")
        K = st.number_input("Pinjaman per Periode (Rp)", value=36_000_000, step=1_000_000, format="%d")
        r1 = st.number_input("Suku bunga awal (%)", value=11.0, step=0.5)
        delta = st.number_input("Penurunan per periode (%)", value=0.5, step=0.1)
        n = st.number_input("Jumlah periode", min_value=1, max_value=10, value=2, step=1)
        tp = st.number_input("Tenor per periode (tahun)", min_value=0.5, max_value=30.0, value=3.0, step=0.5)
        m = st.number_input("Tahun bayar di periode terakhir", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
        bank_type = st.selectbox("Tipe Bank", ["desa", "kota"], format_func=lambda x: "🏡 Pedesaan" if x=="desa" else "🏙️ Perkotaan")
        biaya_dana = st.number_input("Biaya Dana+Overhead (%)", value=9.0, step=0.5)
        hitung = st.button("🚀 Hitung Simulasi", type="primary", use_container_width=True)
    
    # Simulasi (kalkulator)
    if hitung:
        if m > tp:
            st.error(f"⚠️ m ({m}) tidak boleh > tp ({tp})")
            return
        hasil = calculate_loan(K, r1, delta, n, tp, m, bank_type, biaya_dana)
        
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
        st.dataframe(pd.DataFrame(hasil['detail']), use_container_width=True, hide_index=True)
        
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
    
    # ========== AGREGATOR: Cari Pinjaman ==========
    st.markdown("---")
    st.subheader("🏦 Cari Pinjaman dari Bank Mitra")
    
    # Form untuk input kriteria (termasuk email dan phone)
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
    
    # Simpan hasil pencarian di session state agar tidak hilang
    if submitted:
        # Hitung total NKHM jika ada (untuk skor kredit)
        nkhm_total = 0
        if "nkhm_scores" in st.session_state:
            nkhm_total = sum(st.session_state.nkhm_scores.values())
        
        profil = {
            "jumlah_pinjaman": jumlah_pinjaman,
            "sektor": sektor_usaha,
            "tenor": tenor,
            "email": email.strip(),
            "phone": phone.strip(),
            "nkhm_score": nkhm_total,      # kirim skor NKHM untuk perhitungan kredit
            "riwayat_pinjaman": []          # bisa diisi dari database nanti
        }
        # Panggil get_recommendations yang mengembalikan 3 nilai
        rekom, credit_score, credit_grade = get_recommendations(profil)
        st.session_state.rekomendasi = rekom
        st.session_state.profil_terakhir = profil
        st.session_state.credit_score = credit_score
        st.session_state.credit_grade = credit_grade
        st.rerun()
    
    # ========== TAMPILAN SKOR KREDIT DEBITUR ==========
    # Tampilkan skor kredit debitur jika tersedia
    if "credit_score" in st.session_state:
        st.info(f"📊 **Skor Kredit Anda: {st.session_state.credit_score}** ({st.session_state.credit_grade}) - Semakin tinggi skor, semakin rendah bunga yang ditawarkan.")
    
    # Tampilkan rekomendasi jika ada (di luar form)
    if "rekomendasi" in st.session_state and st.session_state.rekomendasi:
        rekom = st.session_state.rekomendasi
        st.success(f"Ditemukan {len(rekom)} bank yang cocok:")
        for r in rekom:
            with st.expander(f"🏦 {r['bank']}"):
                st.write(f"**Estimasi bunga:** {r['bunga']}% per tahun")
                st.write(f"**Estimasi angsuran/bulan:** Rp {r['estimasi_angsuran']:,.0f}".replace(",", "."))
                st.write(f"**Biaya admin:** Rp {r['biaya_admin']:,.0f}".replace(",", "."))
                # Tampilkan skor kredit dan grade untuk rekomendasi ini
                st.caption(f"📈 Skor kredit Anda: {r.get('credit_score', 'N/A')} ({r.get('credit_grade', 'N/A')}) → bunga disesuaikan")
                # Tombol Ajukan
                if st.button(f"Ajukan ke {r['bank']}", key=r['id']):
                    app_id = submit_application(st.session_state.profil_terakhir, r['id'])
                    st.success(f"Pengajuan berhasil dikirim! ID: {app_id}")
                    st.info("Bank akan menghubungi Anda dalam 1x24 jam.")
    elif "rekomendasi" in st.session_state:
        st.warning("Belum ada bank yang cocok. Coba ubah kriteria pinjaman.")
    
    # ========== STATUS PENGAJUAN ==========
    st.markdown("---")
    st.subheader("📋 Status Pengajuan Anda")
    apps = get_all_applications_for_user()
    if not apps:
        st.info("Belum ada pengajuan. Silakan cari pinjaman di atas.")
    else:
        for app in apps[-5:]:  # tampilkan 5 terakhir
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
                    
    # ========== ADMIN PANEL GLOBAL ==========
    if st.query_params.get("admin") == "1":
        from ubelasy.admin import admin_page
        admin_page()
        st.stop()
        
    # ========== BANK ADMIN PANEL (per bank) ==========
    if st.query_params.get("bank"):
        bank_id = st.query_params.get("bank")
        from ubelasy.bank_admin import bank_admin_page
        bank_admin_page(bank_id)
        st.stop()

if __name__ == "__main__":
    main()
    
