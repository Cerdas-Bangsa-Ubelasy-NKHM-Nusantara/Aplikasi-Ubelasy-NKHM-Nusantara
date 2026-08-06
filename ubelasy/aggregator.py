# ubelasy/aggregator.py
import json
import os
import streamlit as st
import logging
from datetime import datetime
import uuid
from ubelasy.notifications import send_email, send_whatsapp
from ubelasy.bank_api import submit_to_bank

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        try:
            with open(BANKS_FILE, "w", encoding="utf-8") as f:
                json.dump(contoh_bank, f, indent=2)
            logging.info("File banks.json berhasil dibuat.")
        except Exception as e:
            logging.error(f"Gagal membuat banks.json: {e}")
            return []
    try:
        with open(BANKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Gagal membaca banks.json: {e}")
        return []

def save_banks(banks):
    try:
        with open(BANKS_FILE, "w", encoding="utf-8") as f:
            json.dump(banks, f, indent=2)
        logging.info("banks.json berhasil disimpan.")
    except Exception as e:
        logging.error(f"Gagal menyimpan banks.json: {e}")

def load_applications():
    if not os.path.exists(APPS_FILE):
        return []
    try:
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Gagal membaca applications.json: {e}")
        return []

def save_applications(apps):
    try:
        with open(APPS_FILE, "w", encoding="utf-8") as f:
            json.dump(apps, f, indent=2)
        logging.info("applications.json berhasil disimpan.")
    except Exception as e:
        logging.error(f"Gagal menyimpan applications.json: {e}")

def get_recommendations(profil):
    banks = load_banks()
    cocok = []
    
    # Hitung skor kredit sederhana berdasarkan NKHM
    nkhm_score = profil.get("nkhm_score", 0)
    if nkhm_score >= 320:
        credit_score = 100
        credit_grade = "A (Sangat Baik)"
    elif nkhm_score >= 240:
        credit_score = 75
        credit_grade = "B (Baik)"
    elif nkhm_score >= 160:
        credit_score = 50
        credit_grade = "C (Cukup)"
    elif nkhm_score >= 80:
        credit_score = 25
        credit_grade = "D (Kurang)"
    else:
        credit_score = 10
        credit_grade = "E (Sangat Kurang)"
    
    for bank in banks:
        if not bank.get("aktif", True):
            continue
        if profil["sektor"] not in bank["sektor"] and "lainnya" not in bank["sektor"]:
            continue
        if profil["tenor"] < bank["tenor_min"] or profil["tenor"] > bank["tenor_max"]:
            continue
        bunga = bank["bunga_min"]
        # Penyesuaian bunga berdasarkan skor kredit
        if credit_score >= 80:
            bunga = max(bank["bunga_min"], bunga - 1.5)
        elif credit_score <= 30:
            bunga = min(bank["bunga_max"], bunga + 2.0)
        estimasi_angsuran = (profil["jumlah_pinjaman"] * (bunga/100)) / 12
        cocok.append({
            "id": bank["id"],
            "bank": bank["nama"],
            "bunga": round(bunga, 2),
            "estimasi_angsuran": estimasi_angsuran,
            "biaya_admin": bank["biaya_admin"],
            "komisi": bank["komisi_persen"],
            "credit_score": credit_score,
            "credit_grade": credit_grade
        })
    
    # Urutkan berdasarkan credit_score tertinggi dan bunga terendah
    cocok.sort(key=lambda x: (-x["credit_score"], x["bunga"]))
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
        try:
            send_email(email, "Pengajuan Pinjaman Diterima", f"ID {app_id} telah kami terima.")
        except Exception as e:
            logging.error(f"Gagal kirim email ke {email}: {e}")
    if phone:
        try:
            send_whatsapp(phone, f"Pengajuan pinjaman ID {app_id} telah diterima.")
        except Exception as e:
            logging.error(f"Gagal kirim WA ke {phone}: {e}")
    
    # NOTIFIKASI REAL-TIME
    try:
        st.toast(f"✅ Pengajuan ID {app_id} berhasil dikirim ke bank!", icon="🎉")
    except Exception as e:
        logging.error(f"Gagal menampilkan toast: {e}")
    
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
                try:
                    send_email(email, f"Status Pinjaman {app_id}", f"Status berubah menjadi {status}\nCatatan: {catatan}")
                except Exception as e:
                    logging.error(f"Gagal kirim email ke {email}: {e}")
            if phone:
                try:
                    send_whatsapp(phone, f"Status pinjaman {app_id}: {status}. Catatan: {catatan}")
                except Exception as e:
                    logging.error(f"Gagal kirim WA ke {phone}: {e}")
            break
    save_applications(apps)
    # NOTIFIKASI REAL-TIME
    try:
        st.toast(f"📢 Status pengajuan {app_id} diupdate menjadi {status}", icon="🔄")
    except Exception as e:
        logging.error(f"Gagal menampilkan toast: {e}")

def get_application(app_id):
    apps = load_applications()
    for app in apps:
        if app["id"] == app_id:
            return app
    return None

def get_all_applications_for_user(profil_hash=None):
    return load_applications()