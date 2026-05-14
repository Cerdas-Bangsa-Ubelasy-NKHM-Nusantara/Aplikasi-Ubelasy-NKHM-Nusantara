# Tim Cerdas Bangsa Berkarya: Aplikasi-Ubelasy-NKHM-Nusantara
Aplikasi Keuangan Ubelasy Sistem Pinjaman Berbasis PSH, dan Aplikasi Gaming NKHM Nusantara Model 4 Kecerdasan + Nasionalisme  Berbasis Data Personal

Two in One dalam Satu Aplikasi yang memiliki dua mode di sidebar kiri (Aplikasi 🌾 Sistem Ubelasy: Agregator & Simulasi pinjaman keuangan berkelanjutan, dan  🌿 NKHM Nusantara: Game asah 4 Kecerdasan + Nasionalisme.

Klik Lencana di bawah sini:
<p align="center">
  <a href="https://ubelasy-nkhm-nusantara.streamlit.app">
    <img src="https://img.shields.io/badge/🚀_Coba_Sekarang-Ubelasy + NKHM Nusantara-2e7d32?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit App">
  </a>
  <a href="https://github.com/SRPakpahanSST/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara">
    <img src="https://img.shields.io/badge/📁_Source_Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</p>

📄 File README.md

```markdown
# 🌾 Sistem Keuangan Berkelanjutan Nusantara

**Two-in-One Platform: Sistem Pinjaman Ubelasy + NKHM Nusantara**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sistem-keuangan-nusantara.streamlit.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-SRPakpahanSST%2FSistem--Keuangan--Nusantara-181717?logo=github)](https://github.com/SRPakpahanSST/Sistem-Keuangan-Nusantara)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Tentang Aplikasi

Repository ini berisi **dua aplikasi keuangan berkelanjutan** yang dapat diakses melalui satu platform dengan pilihan di sidebar:

| Aplikasi | Fungsi | Landasan |
|----------|--------|----------|
| 🌾 **Sistem Ubelasy** | Simulasi pinjaman dengan skema pembebasan sisa hutang (PSH) berbasis Tahun Yobel | Imamat 25:8-10 |
| 🌿 **NKHM Nusantara** | Game asah 4 kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme dengan AI Asisten | Rumus NKHM & nilai kebangsaan |

Kedua aplikasi dirancang untuk mendukung **ketahanan pangan dan energi** serta **pengembangan sumber daya manusia** di Sumatera Selatan.

---

## 🚀 Akses Aplikasi

Aplikasi telah dideploy ke **Streamlit Cloud** dan dapat diakses publik melalui:

👉 [**https://sistem-keuangan-nusantara.streamlit.app**](https://sistem-keuangan-nusantara.streamlit.app)

### Cara Penggunaan:
1. Buka URL di atas
2. Pilih aplikasi di **sidebar kiri**:
   - 🌾 **Sistem Ubelasy** – untuk simulasi pinjaman
   - 🌿 **NKHM Nusantara** – untuk game 4 kecerdasan
3. Ikuti petunjuk di masing-masing aplikasi

---

## 📁 Struktur Repository

```

Sistem-Keuangan-Nusantara/
│
├── app.py                    # MAIN ENTRY (pemilih aplikasi)
├── ubelasy.py                # Modul Sistem Ubelasy
├── nkhm.py                   # Modul NKHM Nusantara
├── requirements.txt          # Dependensi Python
├── README.md                 # Dokumentasi ini
│
├── .streamlit/
│   └── secrets.toml          # API Key (OpenAI)
│
├── assets/
│   ├── .gitkeep
│   └── pmd_logo.jpg          # Logo Pakpahan Ministry
│
└── soal_mentah/              # Bank soal NKHM
├── IQ/
│   └── iq_1.json
├── EQ/
│   └── eq_1.json
├── SQ/
│   └── sq_1.json
├── AQ/
│   └── aq_1.json
└── Nasionalisme/
└── nasionalisme_1.json

```

---

## 🌾 Sistem Ubelasy (Pinjaman Yobel)

### Konsep
Terinspirasi dari **Kitab Imamat 25:8-10** (Tahun Yobel), Sistem Ubelasy menawarkan skema pinjaman dengan:
- Penurunan suku bunga 0,5% per periode
- Pembebasan Sisa Hutang (PSH) proporsional
- Skala dPSH (Derajat Pembebasan Sisa Hutang) 0–2

### Parameter Input
| Parameter | Simbol | Contoh |
|-----------|--------|--------|
| Jumlah Pinjaman per Periode | K | Rp 36.000.000 |
| Suku bunga awal | r₁ | 11% |
| Penurunan per periode | Δr | 0,5% |
| Jumlah periode | n | 2 |
| Tenor per periode | tₚ | 3 tahun |
| Tahun bayar di periode terakhir | m | 2 tahun |
| Tipe bank | - | Pedesaan / Perkotaan |
| Biaya dana + overhead | - | 9% |

### Rumus Inti
```

T = n × tₚ
dPSH = T / 25
TSHᵢ = K × (1 + rᵢ × tₚ)
SHA = TSHₙ × (1 – m/tₚ)
PSH desa = SHA × (T/50)
PSH kota = SHA × (T/60)

```

### Status Debitur (berdasarkan dPSH)
| dPSH | Status | PSH (% dari SHA) |
|------|--------|------------------|
| 0 – 0,20 | 🟢 Pemula | 0 – 10% |
| 0,21 – 0,50 | 🔵 Berkembang | 10,5 – 25% |
| 0,51 – 1,00 | 🟡 Madya | 25,5 – 50% |
| 1,01 – 1,80 | 🟠 Lanjut | 50,5 – 90% |
| 1,81 – 2,00 | 🔴 Yobel | 90,5 – 100% |

---

## 🌿 NKHM Nusantara

### Konsep
Aplikasi gaming yang mengasah **4 kecerdasan** + **Nasionalisme**:
- 🧠 **IQ** – Kecerdasan Intelektual
- ❤️ **EQ** – Kecerdasan Emosi
- 🙏 **SQ** – Kecerdasan Spiritual
- 💪 **AQ** – Kecerdasan Daya Juang
- 🇮🇩 **Nasionalisme** – Nilai kebangsaan dan sejarah Indonesia

### Rumus NKHM
```

NKHM = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))

```

### Level NKHM
| Nilai NKHM | Level |
|------------|-------|
| ≥ 80 | 🌟 Pahlawan Cerdas |
| 60 – 79 | 📚 Cendekia Muda |
| 40 – 59 | 🌱 Penjelajah Ilmu |
| < 40 | 🌿 Perintis Jalan |

### Fitur
- 📚 **Bank soal** (IQ, EQ, SQ, AQ, Nasionalisme) dari file JSON
- 🎮 **Kuis interaktif** dengan filter kategori & jenis kecerdasan
- 🤖 **Asisten AI "Ki Hajar"** (chatbot edukatif)
- 📊 **Dashboard** perkembangan skor
- 🏆 **Pencapaian & gelar** prestasi

---

## 🛠️ Instalasi & Menjalankan Secara Lokal

### Prasyarat
- Python 3.9 atau lebih baru
- pip

### Langkah-langkah

1. **Clone repository**
   ```bash
   git clone https://github.com/SRPakpahanSST/Sistem-Keuangan-Nusantara.git
   cd Sistem-Keuangan-Nusantara
```

1. Buat virtual environment (opsional)
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```
2. Install dependensi
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi
   ```bash
   streamlit run app.py
   ```
4. Buka browser di http://localhost:8501

---

☁️ Deploy ke Streamlit Cloud

1. Push repository ke GitHub
2. Buka Streamlit Cloud
3. Klik "New app"
4. Pilih repository SRPakpahanSST/Sistem-Keuangan-Nusantara
5. Branch: main
6. Main file path: app.py
7. Klik Deploy

---

📚 Landasan Teoritis

Ubelasy

· Kitab Imamat 25:8-10 – Tahun Yobel (pembebasan sisa hutang setiap 50 tahun)
· Pakpahan, SR (2025) – Sistem Pinjaman Model Tahun Yobel
· Data OJK 2025 – NPL pertanian 5,2%, pertambangan 5,8%

NKHM

· Rumus NKHM (4 kecerdasan) – Pengembangan model asesmen holistik
· Nilai kebangsaan & sejarah Indonesia (Sumpah Pemuda, Proklamasi, Pancasila)

---

🤝 Kontribusi

Kami menyambut kontribusi untuk pengembangan lebih lanjut:

· Penambahan bank soal NKHM
· Fitur ekspor PDF untuk Ubelasy
· Integrasi database untuk riwayat pengguna

Silakan buka issue atau kirim pull request.

---

📧 Kontak

Penulis & Pengembang: SR Pakpahan, SST
Email: pakpahan.ministry@gmail.com
Telepon: 082170814310

---

📜 Lisensi

Hak Cipta © 2026 – Pakpahan Ministry
Kode ini dirilis untuk tujuan pendidikan dan uji coba kebijakan keuangan berkelanjutan.

---

#KeuanganBerkelanjutan #TahunYobel #Ubelasy #NKHM #KetahananPangan #EnergiSumsel #SEF2026

```

---

## ✅ Langkah Selanjutnya

1. **Buat file `README.md`** di repository baru `Sistem-Keuangan-Nusantara`
2. **Salin isi di atas** ke file tersebut
3. **Commit** ke GitHub

Setelah itu, halaman utama repository GitHub Anda akan menampilkan dokumentasi yang rapi dan profesional, mencakup:
- Badge status aplikasi
- Penjelasan kedua sistem
- Cara penggunaan
- Instalasi lokal
- Landasan teoritis

Apakah ada yang ingin ditambahkan atau diubah di README? 🚀

