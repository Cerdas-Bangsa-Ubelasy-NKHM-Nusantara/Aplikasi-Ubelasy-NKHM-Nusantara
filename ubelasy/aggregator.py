# ubelasy/aggregator.py
import json
import os
import streamlit as st
from datetime import datetime
import uuid
# Import notifikasi
from ubelasy.notifications import send_email, send_whatsapp
# Import API bank untuk integrasi dengan bank mitra
from ubelasy.bank_api import submit_to_bank

# Path ke file data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BANKS_FILE = os.path.join(DATA_DIR, "banks.json")
APPS_FILE = os.path.join(DATA_DIR, "applications.json")

# Inisialisasi folder data jika belum ada
os.makedirs(DATA_DIR, exist_ok=True)

def load_banks():
    """Muat daftar bank dari file JSON"""
    if not os.path.exists(BANKS_FILE):
        # Buat file contoh jika belum ada
        contoh_bank = [
            {"id": "bss_babel", "nama": "Bank Sumsel Babel", "bunga_min": 10.0, "bunga_max": 12.0,
             "tenor_min": 1, "tenor_max": 5, "biaya_admin": 500000, "sektor": ["pangan", "energi"],
             "komisi_persen": 1.0, "aktif": True},
            {"id": "mandiri_umkm", "nama": "Bank Mandiri UMKM", "bunga_min": 10.5, "bunga_max": 13.0,
             "tenor_min": 1, "tenor_max": 4, "biaya_admin": 750000, "sektor": ["pangan"],
             "komisi_persen": 1.2, "aktif": True}
        ]
        with open(BANKS_FILE, "w") as f:
            json.dump(contoh_bank, f, indent=2)
    with open(BANKS_FILE, "r") as f:
        return json.load(f)

def save_banks(banks):
    with open(BANKS_FILE, "w") as f:
        json.dump(banks, f, indent=2)

def load_applications():
    if not os.path.exists(APPS_FILE):
        return []
    with open(APPS_FILE, "r") as f:
        return json.load(f)

def save_applications(apps):
    with open(APPS_FILE, "w") as f:
        json.dump(apps, f, indent=2)

def get_recommendations(profil):
    """
    Mencari bank yang sesuai berdasarkan profil debitur.
    profil = {"jumlah_pinjaman": int, "sektor": str, "tenor": int, "nkhm_score": int (opsional)}
    """
    banks = load_banks()
    cocok = []
    for bank in banks:
        if not bank.get("aktif", True):
            continue
        # Cek sektor
        if profil["sektor"] not in bank["sektor"] and "lainnya" not in bank["sektor"]:
            continue
        # Cek tenor
        if profil["tenor"] < bank["tenor_min"] or profil["tenor"] > bank["tenor_max"]:
            continue
        # Estimasi suku bunga (dapat disesuaikan dengan NKHM score nanti)
        bunga = bank["bunga_min"]  # default minimal
        estimasi_angsuran = (profil["jumlah_pinjaman"] * (bunga/100)) / 12
        cocok.append({
            "id": bank["id"],
            "bank": bank["nama"],
            "bunga": bunga,
            "estimasi_angsuran": estimasi_angsuran,
            "biaya_admin": bank["biaya_admin"],
            "komisi": bank["komisi_persen"]
        })
    return cocok

def submit_application(profil, bank_id):
    # 1. Simpan pengajuan ke file internal terlebih dahulu
    apps = load_applications()
    app_id = str(uuid.uuid4())[:8]
    new_app = {
        "id": app_id,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "profil": profil,
        "bank_id": bank_id,
        "status": "Dikirim",  # status awal
        "catatan": ""
    }
    apps.append(new_app)
    save_applications(apps)
    
    # 2. Siapkan data untuk dikirim ke bank via API
    bank_data = {
        "app_id": app_id,
        "jumlah_pinjaman": profil.get("jumlah_pinjaman"),
        "tenor": profil.get("tenor"),
        "sektor": profil.get("sektor"),
        "nama_debitur": profil.get("nama", "Tidak ada nama"),
        "email": profil.get("email", ""),
        "phone": profil.get("phone", ""),
        "nkhm_score": profil.get("nkhm_score", 0)
    }
    
    # 3. Panggil API bank
    try:
        api_response = submit_to_bank(bank_data, bank_id)
        if api_response.get("status") == "success":
            # Jika API berhasil, update status menjadi "Diproses" atau "Disetujui"
            update_application_status(app_id, "Diproses", f"Pengajuan diterima bank. Ref: {api_response.get('reference', '')}")
            # Notifikasi tambahan bisa ditambahkan di sini jika perlu
        else:
            # Jika API gagal, status tetap "Dikirim" tapi catatan ditambahkan
            update_application_status(app_id, "Dikirim", f"Gagal mengirim ke bank: {api_response.get('message', '')}")
    except Exception as e:
        # Jika terjadi error (misal koneksi timeout), catat error
        update_application_status(app_id, "Dikirim", f"Error API: {str(e)}")
    
    # 4. Kirim notifikasi ke debitur (email/WA)
    email = profil.get("email", "")
    phone = profil.get("phone", "")
    if email:
        send_email(email, "Pengajuan Pinjaman Diterima", f"ID {app_id} telah kami terima.")
    if phone:
        send_whatsapp(phone, f"Pengajuan pinjaman ID {app_id} telah diterima.")
    
    return app_id

def update_application_status(app_id, status, catatan=""):
    apps = load_applications()
    for app in apps:
        if app["id"] == app_id:
            app["status"] = status
            app["catatan"] = catatan
            # Ambil profil dari data aplikasi
            profil = app.get("profil", {})
            email = profil.get("email", "")
            phone = profil.get("phone", "")
            if email:
                send_email(email, f"Status Pinjaman {app_id}", f"Status berubah menjadi {status}\nCatatan: {catatan}")
            if phone:
                send_whatsapp(phone, f"Status pinjaman {app_id}: {status}. Catatan: {catatan}")
            break
    save_applications(apps)
    
def get_application(app_id):
    apps = load_applications()
    for app in apps:
        if app["id"] == app_id:
            return app
    return None

def get_all_applications_for_user(profil_hash=None):
    """Untuk demo, kita kembalikan semua pengajuan (karena tidak ada login)"""
    return load_applications()
    
