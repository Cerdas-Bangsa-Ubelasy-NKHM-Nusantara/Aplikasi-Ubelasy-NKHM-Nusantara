# ubelasy/aggregator.py
import json
import os
import streamlit as st
from datetime import datetime
import uuid

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
    """Simpan pengajuan ke file JSON"""
    apps = load_applications()
    new_app = {
        "id": str(uuid.uuid4())[:8],
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "profil": profil,
        "bank_id": bank_id,
        "status": "Dikirim",  # Dikirim, Diproses, Disetujui, Ditolak
        "catatan": ""
    }
    apps.append(new_app)
    save_applications(apps)
    return new_app["id"]
    
    # Di aggregator.py, setelah menyimpan pengajuan
    from ubelasy.notifications import send_email, send_whatsapp
    # asumsikan profil punya 'email' dan 'phone'
    send_email(profil.get('email', ''), "Pengajuan Pinjaman Diterima", f"ID {app_id} telah kami terima.")
    # Untuk status update:
    send_email(profil.get('email', ''), f"Status Pinjaman {app_id}", f"Status berubah menjadi {status}")

def update_application_status(app_id, status, catatan=""):
    apps = load_applications()
    for app in apps:
        if app["id"] == app_id:
            app["status"] = status
            app["catatan"] = catatan
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
