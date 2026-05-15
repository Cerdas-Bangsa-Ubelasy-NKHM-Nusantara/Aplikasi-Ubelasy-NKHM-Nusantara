
# ubelasy/bank_admin.py
import streamlit as st
from ubelasy.aggregator import load_applications, update_application_status

def bank_admin_page(bank_id):
    st.title(f"🏦 Admin Dashboard - {bank_id.upper()}")
    st.markdown("Kelola pengajuan pinjaman yang masuk ke bank Anda.")
    
    # Autentikasi sederhana (gunakan password dari secrets)
    bank_pass_key = f"bank_{bank_id}_password"
    if bank_pass_key not in st.secrets:
        st.error("Password bank belum dikonfigurasi di secrets.")
        return
    password = st.text_input("Masukkan password bank:", type="password")
    if password != st.secrets[bank_pass_key]:
        st.warning("Password salah.")
        return
    
    apps = load_applications()
    # Filter pengajuan berdasarkan bank_id
    bank_apps = [app for app in apps if app["bank_id"] == bank_id]
    if not bank_apps:
        st.info("Tidak ada pengajuan untuk bank ini.")
        return
    
    for app in bank_apps:
        with st.expander(f"{app['id']} - {app['tanggal']} - {app['status']}"):
            st.write(f"**Jumlah pinjaman:** Rp {app['profil']['jumlah_pinjaman']:,.0f}".replace(",", "."))
            st.write(f"**Sektor:** {app['profil']['sektor']}, **Tenor:** {app['profil']['tenor']} tahun")
            st.write(f"**Debitur:** {app['profil'].get('nama', 'Tidak ada nama')} (NKHM score: {app['profil'].get('nkhm_score', 0)})")
            new_status = st.selectbox("Status", ["Dikirim", "Diproses", "Disetujui", "Ditolak"], index=["Dikirim", "Diproses", "Disetujui", "Ditolak"].index(app["status"]), key=f"status_{app['id']}")
            catatan = st.text_area("Catatan internal", value=app.get("catatan", ""), key=f"catatan_{app['id']}")
            if st.button(f"Update", key=f"update_{app['id']}"):
                update_application_status(app["id"], new_status, catatan)
                st.success(f"Status diupdate menjadi {new_status}")
                st.rerun()
