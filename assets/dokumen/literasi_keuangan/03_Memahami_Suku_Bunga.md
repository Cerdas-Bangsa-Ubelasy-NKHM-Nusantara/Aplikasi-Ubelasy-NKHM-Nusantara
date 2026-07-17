# Memahami Suku Bunga

> "Hikmat lebih baik dari pada permata, dan segala yang diinginkan orang tidak dapat menyamainya." - Amsal 8:11

## Pendahuluan

Suku bunga adalah "harga" yang harus dibayar untuk menggunakan uang orang lain. Memahami suku bunga adalah kunci untuk membuat keputusan keuangan yang bijak, terutama saat mengajukan pinjaman. Dalam sistem keuangan, suku bunga berfungsi sebagai:

1. **Balas jasa** bagi pemberi pinjaman (bank/kreditur)
2. **Biaya risiko** yang mencerminkan kemungkinan gagal bayar
3. **Kompensasi inflasi** yang menggerus nilai uang seiring waktu

> "Setiap orang yang bijaksana bertindak dengan pengetahuan, tetapi orang bebal menyiarkan kebodohan." - Amsal 13:16

---

## 1. Jenis-Jenis Suku Bunga

### a. Suku Bunga Flat (Bunga Tetap)

**Karakteristik:**
- Bunga dihitung dari **pokok pinjaman awal** sepanjang masa pinjaman
- Jumlah cicilan tetap setiap bulan
- Mudah dipahami dan dihitung

**Rumus:**

Bunga = Pokok Pinjaman × Suku Bunga × Tenor (tahun)
Total Angsuran = Pokok + Bunga
Angsuran per Bulan = Total Angsuran / (Tenor × 12)


**Contoh** (seperti yang digunakan dalam sistem Ubelasy):

| **Parameter** | **Nilai** |
|---------------|-----------|
| Pinjaman (K) | Rp 36.000.000 |
| Suku Bunga (r₁) | 11% per tahun |
| Tenor (tₚ) | 3 tahun |
| Total Bunga | 36.000.000 × 11% × 3 = Rp 11.880.000 |
| Total Angsuran | 36.000.000 + 11.880.000 = Rp 47.880.000 |
| Angsuran/Bulan | 47.880.000 / 36 = Rp 1.330.000 |

> "Orang benar memberi pinjaman dan tidak meminta kembali, tetapi orang fasik tidak membayar hutang." - Mazmur 37:21

### b. Suku Bunga Efektif (Bunga Menurun)

**Karakteristik:**
- Bunga dihitung dari **sisa pokok pinjaman** yang tersisa
- Bunga semakin menurun seiring waktu
- Total bunga lebih kecil dibandingkan flat

**Perbedaan Flat vs Efektif:**

| **Aspek** | **Flat** | **Efektif** |
|-----------|----------|-------------|
| Dasar perhitungan | Pokok awal | Sisa pokok |
| Cicilan per bulan | Tetap | Menurun |
| Total bunga | Lebih tinggi | Lebih rendah |
| Kompleksitas | Sederhana | Kompleks |
| Transparansi | Mudah dipahami | Perlu kalkulator |

> **Catatan Ubelasy:** Sistem Ubelasy menggunakan **metode flat** untuk transparansi dan kemudahan perhitungan. Debitur dapat dengan mudah memperkirakan kewajiban mereka.

### c. Suku Bunga Anuitas

**Karakteristik:**
- Cicilan total per bulan tetap
- Komposisi bunga dan pokok berubah (bunga semakin kecil, pokok semakin besar)
- Paling umum digunakan di perbankan konvensional

---

## 2. Komponen Suku Bunga Pinjaman

### Memecah SBDK (Suku Bunga Dasar Kredit)

Bank menentukan suku bunga pinjaman berdasarkan tiga komponen utama:

| **Komponen** | **Kisaran** | **Keterangan** |
|--------------|-------------|----------------|
| **Harga Pokok Dana untuk Kredit (HPDK)** | 1,97% – 5,17% | Biaya yang bank bayar untuk dana (deposito, tabungan) |
| **Biaya Overhead** | 2,13% – 7,53% | Biaya operasional (gaji, sewa, IT, dll) |
| **Margin Keuntungan Bank** | 1,32% – 3,48% | Laba kotor bank |
| **Total SBDK** | **7,5% – 13,7%** | Suku bunga yang dibayar debitur |

> "Kekayaan orang kaya adalah kota bentengnya, tetapi kehancuran orang miskin adalah kemiskinan mereka." - Amsal 10:15

### Margin Keuntungan Bank Indonesia (Data 2026)

| **Bank & Segmen** | **Margin Keuntungan (% p.a.)** |
|-------------------|--------------------------------|
| Bank Mandiri-Korporasi | 1,99% |
| Bank Mandiri-UMKM Menengah | 2,57% |
| Bank Mandiri-UMKM Kecil | 3,07% |
| Bank Mandiri-UMKM Mikro | 3,37% |
| Bankaltimtara Korporasi | 1,39% |
| Bank BTN Korporasi | 1,57% |
| Bank INA-Seluruh Segmen | 1,50% |

**Kesimpulan:** Margin keuntungan bank untuk UMKM berkisar **1,32% – 3,48%** per tahun. Debitur mikro/UMKM kecil dikenakan margin lebih tinggi karena risiko lebih besar.

---

## 3. Faktor-Faktor yang Mempengaruhi Suku Bunga

### a. Faktor Internal (Debitur)

| **Faktor** | **Pengaruh** |
|------------|--------------|
| Skor kredit / Riwayat pembayaran | Semakin baik → Bunga lebih rendah |
| Jaminan/Agunan | Ada agunan → Bunga lebih rendah |
| Jumlah pinjaman | Semakin besar → Potensi bunga lebih rendah |
| Tenor pinjaman | Semakin pendek → Bunga lebih rendah |
| Sektor usaha | Prioritas (pangan/energi) → Bunga lebih rendah |

### b. Faktor Eksternal (Makro)

| **Faktor** | **Pengaruh** |
|------------|--------------|
| BI Rate (Suku Bunga Acuan) | Naik → Bunga pinjaman naik |
| Inflasi | Tinggi → Bunga pinjaman tinggi |
| Risiko negara (Country Risk) | Stabil → Bunga lebih rendah |
| Likuiditas perbankan | Longgar → Bunga lebih rendah |

> "Orang yang bijak melihat dan menjauhkan diri dari kejahatan, tetapi orang bebal terus berjalan dan tidak peduli." - Amsal 14:16

---

## 4. Suku Bunga dalam Sistem Ubelasy

### Keunikan Ubelasy: Penurunan Suku Bunga per Periode

Sistem Ubelasy menerapkan **penurunan suku bunga 0,5% per periode**. Ini adalah salah satu fitur utama yang membedakan Ubelasy dari sistem pinjaman konvensional.

**Varian C (Model Utama 2 × 3 tahun):**

| **Periode** | **Suku Bunga** | **Keterangan** |
|-------------|----------------|----------------|
| Periode 1 (3 tahun) | 11,0% | Bunga awal |
| Periode 2 (3 tahun) | 10,5% | Turun 0,5% |
| **Rata-rata** | **10,75%** | Total 6 tahun |

**Perhitungan Spread:**


