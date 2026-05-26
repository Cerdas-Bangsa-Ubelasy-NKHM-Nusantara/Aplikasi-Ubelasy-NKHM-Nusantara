# ubelasy/aggregator.py
import json
import os
import streamlit as st
from datetime import datetime
import uuid
from ubelasy.notifications import send_email, send_whatsapp
from ubelasy.bank_api import submit_to_bank

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BANKS_FILE = os.path.join(DATA_DIR, "banks.json")
APPS_FILE = os.path.join(DATA_DIR, "applications.json")
os.makedirs(DATA_DIR, exist_ok=True)

def load_banks():
    if not os.path.exists(BANKS_FILE):
        contoh_bank = [
            {"id": "bss_babel", "nama": "Bank Sumsel Babel", "bunga_min": 10.0, "bunga_max": 12.0,
             "tenor_min": 1, "tenor_max": 5, "biaya_admin": 500000, "sektor": ["pangan", "energi"],
             "komisi_persen": 1.0, "aktif": True},
            {"id": "mandiri_umkm", "nama": "Bank Mandiri UMKM", "bunga_min": 10.5, "bunga_max": 13.0,
             "tenor_min": 1, "tenor_max": 4, "biaya_admin": 750000, "sektor": ["pangan"],
             "komisi_persen": 1.2, "aktif": True},
            {"id": "bri_bogor", "nama": "BRI Bogor", "bunga_min": 9.5, "bunga_max": 12.0,
             "tenor_min": 1, "tenor_max": 5, "biaya_admin": 400000, "sektor": ["pangan", "energi", "lainnya"],
             "komisi_persen": 0.9, "aktif": True}
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
    Mengembalikan tuple: (cocok, credit_score, credit_grade)
    """
    banks = load_banks()
    cocok = []
    for bank in banks:
        if not bank.get("aktif", True):
            continue
        if profil["sektor"] not in bank["sektor"] and "lainnya" not in bank["sektor"]:
            continue
        if profil["tenor"] < bank["tenor_min"] or profil["tenor"] > bank["tenor_max"]:
            continue
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
    
    # Hitung skor kredit sederhana berdasarkan NKHM (jika ada)
    nkhm_score = profil.get("nkhm_score", 0)
    if nkhm_score >= 80:
        credit_score = 85
        credit_grade = "A (Sangat Baik)"
    elif nkhm_score >= 60:
        credit_score = 70
        credit_grade = "B (Baik)"
    elif nkhm_score >= 40:
        credit_score = 55
        credit_grade = "C (Cukup)"
    else:
        credit_score = 30
        credit_grade = "D (Kurang)"
    
    return cocok, credit_score, credit_grade

def submit_application(profil, bank_id):
    apps = load_applications()
    app_id = str(uuid.uuid4())[:8]
    new_app = {
        "id": app_id,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "profil": profil,
        "bank_id": bank_id,
        "status": "Dikirim",
        "catatan": ""
    }
    apps.append(new_app)
    save_applications(apps)
    
    # Kirim notifikasi email/WA jika ada
    email = profil.get("email", "")
    phone = profil.get("phone", "")
    if email:
        send_email(email, "Pengajuan Pinjaman Diterima", f"ID {app_id} telah kami terima.")
    if phone:
        send_whatsapp(phone, f"Pengajuan pinjaman ID {app_id} telah diterima.")
    
    # NOTIFIKASI REAL-TIME
    st.toast(f"✅ Pengajuan ID {app_id} berhasil dikirim ke bank!", icon="🎉")
    
    return app_id

def update_application_status(app_id, status, catatan=""):
    apps = load_applications()
    for app in apps:
        if app["id"] == app_id:
            app["status"] = status
            app["catatan"] = catatan
            profil = app.get("profil", {})
            email = profil.get("email", "")
            phone = profil.get("phone", "")
            if email:
                send_email(email, f"Status Pinjaman {app_id}", f"Status berubah menjadi {status}\nCatatan: {catatan}")
            if phone:
                send_whatsapp(phone, f"Status pinjaman {app_id}: {status}. Catatan: {catatan}")
            break
    save_applications(apps)
    # NOTIFIKASI REAL-TIME
    st.toast(f"📢 Status pengajuan {app_id} diupdate menjadi {status}", icon="🔄")

def get_application(app_id):
    apps = load_applications()
    for app in apps:
        if app["id"] == app_id:
            return app
    return None

def get_all_applications_for_user(profil_hash=None):
    return load_applications()
