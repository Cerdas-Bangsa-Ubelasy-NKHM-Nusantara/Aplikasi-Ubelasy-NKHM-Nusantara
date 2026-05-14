import streamlit as st
from ubelasy.aggregator import load_applications, update_application_status

def admin_page():
    st.title("🔐 Admin Panel - Update Status Pengajuan")
    
    # Proteksi dengan kata sandi sederhana
    password = st.text_input("Masukkan kode admin:", type="password")
    if password != "admin123":  # Ganti dengan kata sandi yang lebih aman
        st.warning("Kode salah. Akses ditolak.")
        return
    
    apps = load_applications()
    if not apps:
        st.info("Belum ada pengajuan.")
        return
    
    for app in apps:
        with st.expander(f"{app['id']} - {app['tanggal']} - {app['status']}"):
            st.write(f"**Jumlah pinjaman:** Rp {app['profil']['jumlah_pinjaman']:,.0f}".replace(",", "."))
            st.write(f"**Sektor:** {app['profil']['sektor']}, **Tenor:** {app['profil']['tenor']} tahun")
            st.write(f"**Bank ID:** {app['bank_id']}")
            
            status_baru = st.selectbox(
                "Ubah status",
                ["Dikirim", "Diproses", "Disetujui", "Ditolak"],
                index=["Dikirim", "Diproses", "Disetujui", "Ditolak"].index(app["status"]),
                key=f"status_{app['id']}"
            )
            catatan = st.text_area("Catatan (opsional)", value=app.get("catatan", ""), key=f"catatan_{app['id']}")
            if st.button(f"Update {app['id']}", key=f"update_{app['id']}"):
                update_application_status(app["id"], status_baru, catatan)
                st.success(f"Status pengajuan {app['id']} diupdate menjadi {status_baru}")
                st.rerun()
