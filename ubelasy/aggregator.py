# ubelasy/aggregator.py
import streamlit as st

bank_products = [
    {
        "nama": "Bank Sumsel Babel",
        "bunga": 10.5,
        "tenor_min": 1,
        "tenor_max": 5,
        "biaya_admin": 500000,
        "sektor": ["pangan", "energi"],
        "komisi": 1.0
    },
    {
        "nama": "Bank Mandiri UMKM",
        "bunga": 11.0,
        "tenor_min": 1,
        "tenor_max": 4,
        "biaya_admin": 750000,
        "sektor": ["pangan"],
        "komisi": 1.2
    }
]

def get_recommendations(profil):
    rekomendasi = []
    for bank in bank_products:
        if profil['sektor'] in bank['sektor']:
            if bank['tenor_min'] <= profil['tenor'] <= bank['tenor_max']:
                estimasi_angsuran = (profil['jumlah_pinjaman'] * (bank['bunga']/100)) / 12
                rekomendasi.append({
                    "bank": bank['nama'],
                    "bunga": bank['bunga'],
                    "estimasi_angsuran": estimasi_angsuran,
                    "biaya_admin": bank['biaya_admin']
                })
    return rekomendasi
