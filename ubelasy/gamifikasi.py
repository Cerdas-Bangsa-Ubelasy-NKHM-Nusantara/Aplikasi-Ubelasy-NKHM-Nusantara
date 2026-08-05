# ubelasy/gamifikasi.py
"""
Fitur Gamifikasi Ubelasy – Misi & Reward Pinjaman.
Mendorong pengguna untuk menyelesaikan misi keuangan dan mendapatkan poin reward.
"""

import streamlit as st
import logging
from datetime import datetime, timedelta

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_rerun():
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di gamifikasi_ubelasy: {e}")

# ========== INISIALISASI STATE ==========
def init_gamifikasi_state():
    """Inisialisasi session state untuk Gamifikasi Ubelasy."""
    defaults = {
        "gamifikasi_ubelasy_poin": 0,
        "gamifikasi_ubelasy_misi": {
            "bayar_cicilan": {
                "nama": "Bayar cicilan tepat waktu 3 bulan berturut-turut",
                "deskripsi": "Bayar cicilan pinjaman tepat waktu selama 3 bulan berturut-turut.",
                "target": 3,
                "progress": 0,
                "selesai": False,
                "reward": 15,
                "icon": "💳"
            },
            "lengkapi_data": {
                "nama": "Lengkapi data Perencanaan Keuangan",
                "deskripsi": "Isi data pendapatan dan pengeluaran di fitur Perencanaan Keuangan Real.",
                "target": 1,
                "progress": 0,
                "selesai": False,
                "reward": 10,
                "icon": "📊"
            },
            "pelajari_modul": {
                "nama": "Pelajari 3 modul literasi keuangan",
                "deskripsi": "Baca dan pahami 3 modul edukasi keuangan yang tersedia.",
                "target": 3,
                "progress": 0,
                "selesai": False,
                "reward": 20,
                "icon": "📚"
            }
        },
        "gamifikasi_ubelasy_riwayat": [],
        "gamifikasi_ubelasy_total_reward_diklaim": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_gamifikasi():
    """Reset semua state gamifikasi (untuk testing)."""
    st.session_state.gamifikasi_ubelasy_poin = 0
    for misi in st.session_state.gamifikasi_ubelasy_misi.values():
        misi["progress"] = 0
        misi["selesai"] = False
    st.session_state.gamifikasi_ubelasy_riwayat = []
    st.session_state.gamifikasi_ubelasy_total_reward_diklaim = 0
    safe_rerun()

# ========== FUNGSI MISI ==========
def cek_misi_lengkapi_data():
    """Cek apakah data Perencanaan Keuangan sudah diisi."""
    hasil = st.session_state.get("keuangan_real_hasil")
    return hasil is not None

def update_misi_lengkapi_data():
    """Update progress misi lengkapi data."""
    misi = st.session_state.gamifikasi_ubelasy_misi["lengkapi_data"]
    if not misi["selesai"]:
        if cek_misi_lengkapi_data():
            misi["progress"] = 1
            misi["selesai"] = True
            beri_reward("lengkapi_data")
            return True
    return False

def update_misi_bayar_cicilan():
    """Simulasi bayar cicilan (tambah progress)."""
    misi = st.session_state.gamifikasi_ubelasy_misi["bayar_cicilan"]
    if not misi["selesai"]:
        misi["progress"] = min(misi["progress"] + 1, misi["target"])
        if misi["progress"] >= misi["target"]:
            misi["selesai"] = True
            beri_reward("bayar_cicilan")
            return True
    return False

def update_misi_pelajari_modul():
    """Tambah progress misi pelajari modul."""
    misi = st.session_state.gamifikasi_ubelasy_misi["pelajari_modul"]
    if not misi["selesai"]:
        misi["progress"] = min(misi["progress"] + 1, misi["target"])
        if misi["progress"] >= misi["target"]:
            misi["selesai"] = True
            beri_reward("pelajari_modul")
            return True
    return False

def beri_reward(misi_key):
    """Beri reward poin untuk misi yang selesai."""
    misi = st.session_state.gamifikasi_ubelasy_misi[misi_key]
    reward = misi["reward"]
    st.session_state.gamifikasi_ubelasy_poin += reward
    st.session_state.gamifikasi_ubelasy_riwayat.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "misi": misi["nama"],
        "poin": reward,
        "jenis": "reward"
    })
    logging.info(f"✅ Misi '{misi['nama']}' selesai! +{reward} poin.")

def tukar_poin(poin_dipakai):
    """Tukar poin dengan potongan biaya administrasi."""
    if poin_dipakai <= 0:
        return False, "Poin harus lebih dari 0."
    if st.session_state.gamifikasi_ubelasy_poin < poin_dipakai:
        return False, f"Poin tidak cukup. Anda punya {st.session_state.gamifikasi_ubelasy_poin} poin."
    
    # Simulasi potongan: setiap 50 poin = 1% potongan
    potongan_persen = (poin_dipakai // 50) * 1
    if potongan_persen == 0:
        return False, "Minimal 50 poin untuk mendapatkan potongan 1%."
    
    st.session_state.gamifikasi_ubelasy_poin -= poin_dipakai
    st.session_state.gamifikasi_ubelasy_riwayat.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "misi": f"Tukar {poin_dipakai} poin",
        "poin": -poin_dipakai,
        "jenis": "tukar"
    })
    st.session_state.gamifikasi_ubelasy_total_reward_diklaim += potongan_persen
    return True, f"✅ Berhasil menukar {poin_dipakai} poin untuk potongan {potongan_persen}% biaya administrasi!"

# ========== UI UTAMA ==========
def show_gamifikasi_ubelasy():
    """Menampilkan halaman Gamifikasi Ubelasy."""
    try:
        init_gamifikasi_state()

        st.markdown("## 🎮 Gamifikasi Ubelasy")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
            padding: 15px 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">🏆</div>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">Selesaikan Misi, Dapatkan Poin!</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Kumpulkan poin dan tukarkan dengan potongan biaya administrasi.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Cek misi lengkapi data secara otomatis
        update_misi_lengkapi_data()

        # ===== DASHBOARD =====
        col1, col2, col3 = st.columns(3)
        total_misi = len(st.session_state.gamifikasi_ubelasy_misi)
        selesai = sum(1 for m in st.session_state.gamifikasi_ubelasy_misi.values() if m["selesai"])
        with col1:
            st.metric("🏅 Total Poin", st.session_state.gamifikasi_ubelasy_poin)
        with col2:
            st.metric("✅ Misi Selesai", f"{selesai}/{total_misi}")
        with col3:
            st.metric("🎁 Potongan Diklaim", f"{st.session_state.gamifikasi_ubelasy_total_reward_diklaim:.1f}%")

        st.markdown("---")

        # ===== DAFTAR MISI =====
        st.markdown("### 📋 Daftar Misi")

        for key, misi in st.session_state.gamifikasi_ubelasy_misi.items():
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"<div style='font-size: 30px;'>{misi['icon']}</div>", unsafe_allow_html=True)
                with col2:
                    status = "✅ Selesai" if misi["selesai"] else "⏳ Dalam Progress"
                    st.markdown(f"**{misi['nama']}** – {status}")
                    st.caption(misi['deskripsi'])
                    progress = misi["progress"] / misi["target"] if misi["target"] > 0 else 0
                    st.progress(min(progress, 1.0), text=f"{misi['progress']}/{misi['target']}")
                    if not misi["selesai"]:
                        # Tombol aksi untuk misi tertentu
                        if key == "bayar_cicilan":
                            if st.button(f"💰 Bayar Cicilan (simulasi)", key=f"bayar_{key}"):
                                if update_misi_bayar_cicilan():
                                    st.success("✅ Progress misi bertambah! Cek status.")
                                    safe_rerun()
                                else:
                                    st.info("Progress misi ditambahkan.")
                                    safe_rerun()
                        elif key == "pelajari_modul":
                            if st.button(f"📖 Pelajari 1 Modul", key=f"modul_{key}"):
                                if update_misi_pelajari_modul():
                                    st.success("✅ Progress misi bertambah! Cek status.")
                                    safe_rerun()
                                else:
                                    st.info("Progress misi ditambahkan.")
                                    safe_rerun()
                st.markdown("---")

        # ===== TUKAR POIN =====
        st.markdown("### 🎁 Tukar Poin dengan Potongan")
        st.caption("Setiap 50 poin = 1% potongan biaya administrasi.")

        col1, col2 = st.columns([2, 1])
        with col1:
            poin_tukar = st.number_input("Masukkan jumlah poin yang ingin ditukar (kelipatan 50):", min_value=0, step=50, value=50)
        with col2:
            if st.button("🎯 Tukar Sekarang", use_container_width=True, type="primary"):
                success, msg = tukar_poin(poin_tukar)
                if success:
                    st.success(msg)
                    st.balloons()
                else:
                    st.warning(msg)
                safe_rerun()

        # ===== RIWAYAT =====
        st.markdown("---")
        st.markdown("### 📜 Riwayat Aktivitas")
        if st.session_state.gamifikasi_ubelasy_riwayat:
            import pandas as pd
            df = pd.DataFrame(st.session_state.gamifikasi_ubelasy_riwayat[-10:])
            df = df[["timestamp", "misi", "poin"]]
            df.columns = ["Waktu", "Aktivitas", "Poin"]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada aktivitas. Mulai selesaikan misi!")

        # ===== TOMBOL RESET =====
        if st.button("🔄 Reset Gamifikasi", use_container_width=True):
            reset_gamifikasi()

    except Exception as e:
        logging.error(f"Error di show_gamifikasi_ubelasy: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_gamifikasi_ubelasy()