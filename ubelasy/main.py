# ubelasy/main.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
from ubelasy.calculator import calculate_loan
from ubelasy.aggregator import get_recommendations, submit_application, get_all_applications_for_user
from ubelasy.pdf_export import export_simulation_to_pdf
from shared.notifications import show_toast
from ubelasy.edukasi import show_edukasi
from ubelasy.kredit_report import show_kredit_report

# ========== KONTEN DOKUMEN SISTEM UBELASY (LENGKAP) ==========
def get_ubelasy_document():
    """Mengembalikan konten dokumen lengkap Sistem Ubelasy dalam format HTML"""
    return """
    <div class="ubelasy-document">
    
    <!-- ===== HEADER UTAMA ===== -->
    <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #2e7daf; margin-bottom: 30px;">
        <h1 style="color: #1a3c6e; font-size: 32px; margin-bottom: 5px;">
            SISTEM PINJAMAN/KREDIT MODEL UBELASY
        </h1>
        <h2 style="color: #2e7daf; font-size: 20px; font-weight: normal; margin-top: 0;">
            UNTUK UMKM SEKTOR PANGAN DAN ENERGI
        </h2>
        <p style="color: #666; font-size: 14px; margin-top: 10px;">
            (Ubelasy Versi 2 Periode, dPSH Maks = 2 untuk tₚ = 25 Tahun, dan Penurunan Suku Bunga 0,5% per Periode)
        </p>
        <p style="color: #888; font-size: 14px;">
            <em>Oleh: SR.Pakpahan, SST</em>
        </p>
    </div>
    
    <!-- ===== DAFTAR ISI ===== -->
    <div style="background-color: #f5f8fc; padding: 15px 20px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #dce4ec;">
        <p style="font-weight: bold; margin-top: 0; color: #1a3c6e;">📑 DAFTAR ISI</p>
        <ul style="columns: 2; list-style: none; padding-left: 0; margin-bottom: 0;">
            <li><a href="#teori" style="text-decoration: none; color: #2e7daf;">I. Teori, Definisi & Konsep</a></li>
            <li><a href="#ekonomi" style="text-decoration: none; color: #2e7daf;">II. Ekonomi Perkotaan vs Pedesaan</a></li>
            <li><a href="#rumus" style="text-decoration: none; color: #2e7daf;">III. Struktur Rumus Model Ubelasy</a></li>
            <li><a href="#keuntungan" style="text-decoration: none; color: #2e7daf;">IV. Keuntungan Bank</a></li>
            <li><a href="#simulasi" style="text-decoration: none; color: #2e7daf;">V. Simulasi Penghitungan Varian</a></li>
            <li><a href="#varian-d" style="text-decoration: none; color: #2e7daf;">VI. Simulasi Varian D</a></li>
            <li><a href="#kesimpulan" style="text-decoration: none; color: #2e7daf;">VII. Kesimpulan Final</a></li>
            <li><a href="#status" style="text-decoration: none; color: #2e7daf;">VIII. Status Debitur Berdasarkan dPSH</a></li>
        </ul>
    </div>
    
    <!-- ===== I. TEORI ===== -->
    <h2 id="teori" style="color: #1a3c6e; border-left: 5px solid #2e7daf; padding-left: 15px; margin-top: 30px;">
        I. TEORI, DEFENISI & KONSEP
    </h2>
    
    <h3 style="color: #2e7daf;">1.1. Konsep Tahun Yobel dan Keuangan Berkelanjutan</h3>
    
    <p style="text-align: justify; line-height: 1.8;">
        Kitab Imamat 25:8-17 mengajarkan Tahun Yobel (tahun ke-50) sebagai pembebasan sisa hutang dan pengembalian tanah. Prinsip ini diadopsi dalam keuangan berkelanjutan (<em>sustainable finance</em>) yang menekankan pilar ekonomi, sosial, dan lingkungan. Ubelasy menerapkan pembebasan sisa hutang secara proporsional: 
        <strong>PSH = SHA × (T / 50) untuk pedesaan</strong> (risiko tinggi) dan 
        <strong>PSH = SHA × (T / 60) untuk perkotaan</strong> (batas keuntungan 16,67% dari usaha bisnis).
    </p>
    
    <h3 style="color: #2e7daf;">1.2. Struktur Permodelan Ubelasy 2 Periode, dPSH Maks = 2</h3>
    
    <p><strong>Parameter dasar (untuk T = 6 tahun):</strong></p>
    
    <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
        <thead>
            <tr style="background-color: #1a3c6e; color: white;">
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Simbol</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Keterangan</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Satuan</th>
            </tr>
        </thead>
        <tbody>
            <tr><td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>T</strong></td><td style="padding: 8px 12px; border: 1px solid #ddd;">Total masa pinjaman (tenor keseluruhan)</td><td style="padding: 8px 12px; border: 1px solid #ddd;">tahun</td></tr>
            <tr style="background-color: #f5f8fc;"><td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>n</strong></td><td style="padding: 8px 12px; border: 1px solid #ddd;">Jumlah periode pinjaman</td><td style="padding: 8px 12px; border: 1px solid #ddd;">-</td></tr>
            <tr><td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>tₚ</strong></td><td style="padding: 8px 12px; border: 1px solid #ddd;">Tenor per periode (T = n × tₚ)</td><td style="padding: 8px 12px; border: 1px solid #ddd;">tahun</td></tr>
            <tr style="background-color: #f5f8fc;"><td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>K</strong></td><td style="padding: 8px 12px; border: 1px solid #ddd;">Nilai pinjaman per periode</td><td style="padding: 8px 12px; border: 1px solid #ddd;">Rupiah</td></tr>
            <tr><td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>rᵢ</strong></td><td style="padding: 8px 12px; border: 1px solid #ddd;">Suku bunga pada periode ke-i</td><td style="padding: 8px 12px; border: 1px solid #ddd;">% per tahun</td></tr>
            <tr style="background-color: #f5f8fc;"><td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>Δr</strong></td><td style="padding: 8px 12px; border: 1px solid #ddd;">Penurunan suku bunga per periode (0,5%)</td><td style="padding: 8px 12px; border: 1px solid #ddd;">%</td></tr>
        </tbody>
    </table>
    
    <p><strong>Hubungan:</strong> T = n × tₚ</p>
    
    <div style="background-color: #e8f0fe; border: 1px solid #2e7daf; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <p style="font-weight: bold; margin-top: 0; color: #1a3c6e;">📌 Contoh:</p>
        <ul style="line-height: 1.8;">
            <li>Pinjaman per periode (K) = Rp 36 juta</li>
            <li>Jumlah periode (n) = 2</li>
            <li>Tenor per periode (tp) = 3 tahun</li>
            <li>Total tenor T = n × tₚ = 6 tahun</li>
            <li>Suku bunga awal r₁ = 11% per tahun</li>
            <li>Penurunan bunga per periode, Δr = 0,5% → r₂ = 10,5%</li>
            <li>Biaya dana + overhead = 9% (HPDK 7% + overhead 2%)</li>
        </ul>
    </div>
    
    <h4 style="color: #3a5a7a;">Rumus Derajat PSH (dPSH) skala 0–2</h4>
    
    <p>Berdasarkan inspirasi Kitab Imamat 25:8-12, Tahun Yobel penuh terjadi pada tahun ke-50 dengan pembebasan total sisa hutang. Dalam sistem Ubelasy, patokan absolut tetap 50 tahun. Derajat Pembebasan Sisa Hutang (dPSH) didefinisikan dalam skala 0–2. Nilai dPSH = 2 dicapai ketika total tenor pinjaman T = 50 tahun.</p>
    
    <div style="background-color: #f5f8fc; padding: 15px 20px; margin: 10px 0; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 16px; text-align: center; border: 1px solid #dce4ec;">
        dPSH = 2 × (T / 50) = T / 25
    </div>
    
    <p>dimana T adalah total tenor pinjaman.</p>
    <p>Untuk T=6 tahun, dPSH = 6/25 = 0,24.</p>
    
    <h4 style="color: #3a5a7a;">Rumus Total Sisa Hutang (TSH) per periode (metode flat)</h4>
    
    <p>Dalam sistem Ubelasy, skema pembayaran kredit menggunakan asumsi metode cicilan flat (bunga dihitung dari pokok awal dan tetap setiap bulan).</p>
    
    <div style="background-color: #f5f8fc; padding: 15px 20px; margin: 10px 0; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 16px; text-align: center; border: 1px solid #dce4ec;">
        TSH_i = K × (1 + r_i × t_p)
    </div>
    
    <p>dimana K adalah jumlah pinjaman per periode, r_i adalah suku bunga pinjaman di periode ke-i, tₚ adalah tenor pinjaman per periode dalam satuan tahun.</p>
    
    <p><strong>Contoh:</strong> K = 36 juta, r₁ = 11%, tₚ = 3 tahun → TSH₁ = 36 × (1 + 0,11×3) = 47,88 juta.</p>
    
    <h4 style="color: #3a5a7a;">Rumus Sisa Hutang Akhir di Periode Terakhir</h4>
    
    <p>Pada periode ke-n, debitur membayar angsuran selama periode tersebut. Jika diasumsikan debitur membayar selama m tahun (dengan 0 &lt; m ≤ tₚ), maka Sisa Hutang Akhir (SHA):</p>
    
    <div style="background-color: #f5f8fc; padding: 15px 20px; margin: 10px 0; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 16px; text-align: center; border: 1px solid #dce4ec;">
        SHA = TSH_n - (TSH_n / t_p) × m = TSH_n × (1 - m/t_p)
    </div>
    
    <p>dimana m adalah tahun pembayaran dalam periode terakhir (m ≤ tₚ).</p>
    
    <p><strong>Contoh (T=6 tahun, tₚ=3 tahun, m=2 tahun):</strong></p>
    <p>Sisa Hutang Akhir (SHA) = 47,34 × (1 - 2/3) = 47,34 × 1/3 = 15,78 juta</p>
    
    <h4 style="color: #3a5a7a;">Rumus PSH pedesaan dan perkotaan</h4>
    
    <p>PSH diberikan dua kali pada debitur yaitu setengah bagian PSH diberikan di akhir tahun periode kesatu, dan setengah bagian lagi di akhir tahun periode kedua. Besarnya PSH dihitung dari sisa hutang yang masih tersisa di tahun akhir periode terakhir pinjaman (periode ke-2), bukan dari total TSHₙ.</p>
    
    <div style="background-color: #f5f8fc; padding: 15px 20px; margin: 10px 0; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 16px; text-align: center; border: 1px solid #dce4ec;">
        PSH<sub>desa</sub> = SHA × (T / 50)
    </div>
    <div style="background-color: #f5f8fc; padding: 15px 20px; margin: 10px 0; border-radius: 5px; font-family: 'Courier New', monospace; font-size: 16px; text-align: center; border: 1px solid #dce4ec;">
        PSH<sub>kota</sub> = SHA × (T / 60)
    </div>
    
    <p><strong>Contoh (T=6 tahun, SHA = 15,78 juta):</strong></p>
    <ul>
        <li>PSH desa = 15,78 × (6/50) = 15,78 × 0,12 = 1,8936 juta</li>
        <li>PSH kota = 15,78 × (6/60) = 15,78 × 0,10 = 1,578 juta</li>
    </ul>
    
    <hr style="border: none; border-top: 2px solid #dce4ec; margin: 30px 0;">
    
    <!-- ===== II. EKONOMI ===== -->
    <h2 id="ekonomi" style="color: #1a3c6e; border-left: 5px solid #2e7daf; padding-left: 15px; margin-top: 30px;">
        II. EKONOMI PERKOTAAN VS PEDESAAN DALAM KONTEKS TAHUN YOBEL
    </h2>
    
    <h3 style="color: #2e7daf;">2.1. Landasan Teologis</h3>
    
    <blockquote style="border-left: 4px solid #2e7daf; padding: 10px 20px; margin: 15px 0; background-color: #f0f5fa; border-radius: 0 5px 5px 0;">
        <p>"Beban yang lebih ringan (PSH lebih besar) diberikan kepada mereka yang memiliki kapasitas ekonomi lebih rapuh dan akses terbatas terhadap sumber daya pemulihan."</p>
    </blockquote>
    
    <h3 style="color: #2e7daf;">2.2. Perbandingan Karakteristik Wilayah</h3>
    
    <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
        <thead>
            <tr style="background-color: #1a3c6e; color: white;">
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Karakteristik</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Perkotaan</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Pedesaan</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>Akses &amp; Diversifikasi</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Akses tinggi ke lembaga keuangan, peluang kerja beragam</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Akses terbatas, sangat tergantung 1-2 komoditas</td>
            </tr>
            <tr style="background-color: #f5f8fc;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>Profil Risiko</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Lebih terukur dan beragam; suku bunga cenderung lebih rendah</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Risiko tinggi (cuaca, hama, fluktuasi harga); NPL pertanian hingga 5%</td>
            </tr>
            <tr>
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>Kapasitas Pemulihan</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Pendapatan lebih stabil, jaring pengaman sosial lebih kuat</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Pendapatan tidak menentu, bergantung musim dan komunitas</td>
            </tr>
        </tbody>
    </table>
    
    <hr style="border: none; border-top: 2px solid #dce4ec; margin: 30px 0;">
    
    <!-- ===== III. RUMUS ===== -->
    <h2 id="rumus" style="color: #1a3c6e; border-left: 5px solid #2e7daf; padding-left: 15px; margin-top: 30px;">
        III. STRUKTUR RUMUS MODEL UBELASY
    </h2>
    
    <h3 style="color: #2e7daf;">3.8. Ringkasan Tiga Varian Ubelasy untuk Total Tenor T=6 Tahun</h3>
    
    <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
        <thead>
            <tr style="background-color: #1a3c6e; color: white;">
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Varian</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Wilayah</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">N × t_p</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Keuntungan Bank</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">PSH</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Sifat</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #d4edda;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>C</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Desa &amp; Kota</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">2 × 3 tahun</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">29,62% / 30,06%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">2,63% / 2,19%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">✅ Win-win solution</td>
            </tr>
            <tr>
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>A</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Desa</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">3 × 2 tahun</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">18,60%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">2,40%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Alternatif pro-debitur</td>
            </tr>
            <tr style="background-color: #f5f8fc;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>B</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Kota</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">6 × 1 tahun</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">7,94%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">1,81%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Alternatif pro-bank</td>
            </tr>
        </tbody>
    </table>
    
    <hr style="border: none; border-top: 2px solid #dce4ec; margin: 30px 0;">
    
    <!-- ===== VIII. STATUS DEBITUR ===== -->
    <h2 id="status" style="color: #1a3c6e; border-left: 5px solid #2e7daf; padding-left: 15px; margin-top: 30px;">
        VIII. STATUS DEBITUR BERDASARKAN dPSH
    </h2>
    
    <h3 style="color: #2e7daf;">8.2. SKALA STATUS DEBITUR (dPSH 0 – 2)</h3>
    
    <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px;">
        <thead>
            <tr style="background-color: #1a3c6e; color: white;">
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">dPSH</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Status</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">T (tahun)</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">PSH Desa</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">PSH Kota</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Makna</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #d4edda;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;">0,00 – 0,20</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">🟢 Pemula</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">0 – 5 th</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">0 – 10%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">0 – 8,33%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Edukasi keuangan</td>
            </tr>
            <tr style="background-color: #d1ecf1; font-weight: bold;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;">0,21 – 0,50</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">🔵 Berkembang</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">5 – 12,5 th</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">10,5 – 25%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">8,75 – 20,8%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Target implementasi awal</td>
            </tr>
            <tr style="background-color: #fff3cd;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;">0,51 – 1,00</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">🟡 Madya</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">12,5 – 25 th</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">25,5 – 50%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">21,25 – 41,7%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">PSH signifikan</td>
            </tr>
            <tr style="background-color: #f8d7da;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;">1,01 – 1,80</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">🟠 Lanjut</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">25 – 45 th</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">50,5 – 90%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">42,1 – 75%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Mendekati Yobel</td>
            </tr>
            <tr style="background-color: #f5c6cb;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;">1,81 – 2,00</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">🔴 Yobel</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">45 – 50 th</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">90,5 – 100%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">75,4 – 83,3%</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Pembebasan total</td>
            </tr>
        </tbody>
    </table>
    
    <h3 style="color: #2e7daf;">8.3. Status Debitur Varian C (T=6 tahun)</h3>
    
    <div style="background-color: #d1ecf1; border: 2px solid #17a2b8; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <p style="font-size: 18px; font-weight: bold; color: #0c5460; margin-top: 0;">
            🔵 Debitur pada Varian C termasuk dalam status <strong>BERKEMBANG (Developing)</strong> dengan dPSH = 0,24
        </p>
        <ul style="line-height: 1.8;">
            <li><strong>Total tenor (T):</strong> 6 tahun</li>
            <li><strong>dPSH:</strong> 6/25 = 0,24</li>
            <li><strong>PSH Desa:</strong> 12% dari SHA (1,8936 juta)</li>
            <li><strong>PSH Kota:</strong> 10% dari SHA (1,578 juta)</li>
            <li><strong>Keuntungan bank desa:</strong> 29,62% (return tahunan 4,94%)</li>
            <li><strong>Keuntungan bank kota:</strong> 30,06% (return tahunan 5,01%)</li>
        </ul>
    </div>
    
    <hr style="border: none; border-top: 2px solid #dce4ec; margin: 30px 0;">
    
    <!-- ===== KESIMPULAN ===== -->
    <h2 id="kesimpulan" style="color: #1a3c6e; border-left: 5px solid #2e7daf; padding-left: 15px; margin-top: 30px;">
        VII. KESIMPULAN FINAL & REKOMENDASI
    </h2>
    
    <h3 style="color: #2e7daf;">7.3. Rekomendasi Final</h3>
    
    <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px;">
        <thead>
            <tr style="background-color: #1a3c6e; color: white;">
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Varian</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Status</th>
                <th style="padding: 10px 12px; border: 1px solid #ddd; text-align: left;">Alasan</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color: #d4edda;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>C (2×3 tahun)</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">✅ PILIHAN UTAMA</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Return 4,94–5,01%, penurunan bunga, PSH signifikan</td>
            </tr>
            <tr>
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>A (3×2 tahun)</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">✅ PEMBANDING</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Return 3,10–3,17%, tenor lebih pendek</td>
            </tr>
            <tr style="background-color: #f5f8fc;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>B (6×1 tahun)</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">✅ PEMBANDING</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Return 1,26–1,32%, fleksibilitas tahunan</td>
            </tr>
            <tr style="background-color: #f8d7da;">
                <td style="padding: 8px 12px; border: 1px solid #ddd;"><strong>D (1×6 tahun)</strong></td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">❌ TIDAK DIREKOMENDASIKAN</td>
                <td style="padding: 8px 12px; border: 1px solid #ddd;">Return terlalu tinggi, tidak ada penurunan bunga</td>
            </tr>
        </tbody>
    </table>
    
    <hr style="border: none; border-top: 2px solid #dce4ec; margin: 30px 0;">
    
    <!-- ===== FOOTER ===== -->
    <div style="background-color: #e8f0fe; border: 1px solid #2e7daf; border-radius: 8px; padding: 15px; margin: 15px 0;">
        <p style="font-weight: bold; margin-top: 0; color: #1a3c6e;">📌 Informasi Penulis</p>
        <p><strong>Nama Penulis:</strong> SR Pakpahan SST</p>
        <p><strong>Email:</strong> pakpahan.ministry@gmail.com</p>
        <p><strong>No. Telepon/HP:</strong> 082170814310</p>
        <p><strong>Pangkalan Kerinci, Mei 2026</strong></p>
    </div>
    
    <hr style="border: none; border-top: 2px solid #dce4ec; margin: 30px 0;">
    
    <p style="text-align: center; font-size: 12px; color: #999;">
        <em>Dokumen ini dikonversi dari format DOCX untuk aplikasi Ubelasy + NKHM Nusantara</em>
    </p>
    
    </div>
    """


# ========== CSS KUSTOM UNTUK DOKUMEN ==========
def inject_ubelasy_document_css():
    """Menambahkan CSS kustom untuk tampilan dokumen Sistem Ubelasy"""
    st.markdown("""
    <style>
        /* Container dokumen */
        .ubelasy-document {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px 30px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.08);
        }
        
        .ubelasy-document h2 {
            color: #1a3c6e;
            border-left: 5px solid #2e7daf;
            padding-left: 15px;
            margin-top: 35px;
            font-size: 24px;
        }
        
        .ubelasy-document h3 {
            color: #2e7daf;
            margin-top: 25px;
            font-size: 20px;
        }
        
        .ubelasy-document h4 {
            color: #3a5a7a;
            margin-top: 20px;
            font-size: 18px;
        }
        
        .ubelasy-document table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
        }
        
        .ubelasy-document th {
            background-color: #1a3c6e;
            color: white;
            padding: 10px 12px;
            text-align: left;
            border: 1px solid #ddd;
        }
        
        .ubelasy-document td {
            padding: 8px 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        
        .ubelasy-document tr:nth-child(even) {
            background-color: #f5f8fc;
        }
        
        .ubelasy-document tr:hover {
            background-color: #e8f0fe;
        }
        
        .ubelasy-document blockquote {
            border-left: 4px solid #2e7daf;
            padding: 10px 20px;
            margin: 15px 0;
            background-color: #f0f5fa;
            border-radius: 0 5px 5px 0;
        }
        
        .ubelasy-document hr {
            border: none;
            border-top: 2px solid #e8edf2;
            margin: 30px 0;
        }
        
        .ubelasy-document ul, .ubelasy-document ol {
            padding-left: 25px;
            line-height: 1.8;
        }
        
        .ubelasy-document p {
            line-height: 1.8;
            text-align: justify;
        }
        
        /* Dark Mode Support */
        .dark-mode .ubelasy-document {
            background-color: #1a1a2e;
            box-shadow: 0 2px 15px rgba(255,255,255,0.05);
        }
        
        .dark-mode .ubelasy-document h2,
        .dark-mode .ubelasy-document h3,
        .dark-mode .ubelasy-document h4 {
            color: #7ab7e0;
        }
        
        .dark-mode .ubelasy-document th {
            background-color: #2a3a5a;
            color: #e0e0e0;
        }
        
        .dark-mode .ubelasy-document td {
            border-color: #444;
        }
        
        .dark-mode .ubelasy-document tr:nth-child(even) {
            background-color: #22223a;
        }
        
        .dark-mode .ubelasy-document tr:hover {
            background-color: #2a2a4a;
        }
        
        .dark-mode .ubelasy-document blockquote {
            background-color: #1a1a3a;
            border-left-color: #4a8abf;
            color: #d0d0e0;
        }
        
        .dark-mode .ubelasy-document hr {
            border-top-color: #333;
        }
        
        .dark-mode .ubelasy-document p,
        .dark-mode .ubelasy-document li {
            color: #d0d0e0;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #f5f8fc"] {
            background-color: #1a1a3a !important;
            border-color: #444 !important;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #e8f0fe"] {
            background-color: #1a1a4a !important;
            border-color: #3a6a8a !important;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #d1ecf1"] {
            background-color: #0a2a3a !important;
            border-color: #2a6a8a !important;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #d4edda"] {
            background-color: #0a2a1a !important;
            border-color: #2a6a3a !important;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #fff3cd"] {
            background-color: #2a2a0a !important;
            border-color: #6a6a2a !important;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #f8d7da"] {
            background-color: #3a1a1a !important;
            border-color: #6a2a2a !important;
        }
        
        .dark-mode .ubelasy-document div[style*="background-color: #f5c6cb"] {
            background-color: #3a0a0a !important;
            border-color: #6a1a1a !important;
        }
        
        /* Daftar isi 2 kolom responsif */
        @media (max-width: 600px) {
            .ubelasy-document ul[style*="columns: 2"] {
                columns: 1 !important;
            }
            .ubelasy-document {
                padding: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)


def main():
    # Inisialisasi session state
    if "simulasi_hasil" not in st.session_state:
        st.session_state.simulasi_hasil = None

    # ========== HEADER ==========
    script_dir = Path(__file__).parent.parent
    image_path = script_dir / "assets" / "ubelasy.jpg"
    
    # CSS untuk membuat gambar selebar kolom
    st.markdown("""
    <style>
    .full-width-image img {
        width: 100%;
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if image_path.exists():
            with st.container():
                st.markdown('<div class="full-width-image">', unsafe_allow_html=True)
                st.image(str(image_path))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Gambar ubelasy.jpg tidak ditemukan di folder assets/")
        st.markdown(
            "<h1 style='text-align: center;'>🌾 Ubelasy – Agregator Pinjaman Berkelanjutan</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center;'><strong>Skema PSH & Penurunan Suku Bunga 0,5% per Periode</strong></p>",
            unsafe_allow_html=True
        )
    st.markdown("---")
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        if "nkhm_scores" in st.session_state:
            nkhm_total = sum(st.session_state.nkhm_scores.values())
            st.metric("🧠 Skor NKHM", nkhm_total)
            st.caption("(Semakin tinggi skor, semakin baik peluang mendapat pinjaman)")
            st.markdown("---")
        else:
            st.info("Mainkan game NKHM untuk meningkatkan skor Anda!")
            st.markdown("---")
        
        # ========== TAB SELECTOR DI SIDEBAR ==========
        st.header("📑 Navigasi Ubelasy")
        tab_mode = st.radio(
            "Pilih Tab",
            ["📖 Sistem Ubelasy", "⚙️ Simulasi & Agregator", "📚 Edukasi", "📊 Rapor Kredit"],
            index=1,
            label_visibility="collapsed"
        )
        st.markdown("---")
        
        if tab_mode == "⚙️ Simulasi & Agregator":
            st.header("⚙️ Simulasi Pinjaman")
            K = st.number_input("Pinjaman per Periode (Rp)", value=36_000_000, step=1_000_000, format="%d")
            r1 = st.number_input("Suku bunga awal (%)", value=11.0, step=0.5)
            delta = st.number_input("Penurunan per periode (%)", value=0.5, step=0.1)
            n = st.number_input("Jumlah periode", min_value=1, max_value=10, value=2, step=1)
            tp = st.number_input("Tenor per periode (tahun)", min_value=0.5, max_value=30.0, value=3.0, step=0.5)
            m = st.number_input("Tahun bayar di periode terakhir", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
            bank_type = st.selectbox("Tipe Bank", ["desa", "kota"], format_func=lambda x: "🏡 Pedesaan" if x=="desa" else "🏙️ Perkotaan")
            biaya_dana = st.number_input("Biaya Dana+Overhead (%)", value=9.0, step=0.5)
            hitung = st.button("🚀 Hitung Simulasi", type="primary")
    
    # ========== INJECT CSS DOKUMEN ==========
    inject_ubelasy_document_css()
    
    # ========== TAMPILKAN KONTEN BERDASARKAN TAB ==========
    if tab_mode == "📖 Sistem Ubelasy":
        # Tampilkan dokumen lengkap
        st.markdown(get_ubelasy_document(), unsafe_allow_html=True)
        
        # Tombol aksi
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            st.caption("💡 Untuk menyimpan dokumen ini, gunakan fitur 'Print' di browser Anda (Ctrl+P) dan pilih 'Save as PDF'.")
            if st.button("📄 Download Dokumen (PDF)"):
                st.info("Fitur download PDF akan segera tersedia. Saat ini silakan gunakan Print > Save as PDF.")
    
    elif tab_mode == "📚 Edukasi":
        show_edukasi()
    
    elif tab_mode == "📊 Rapor Kredit":
        show_kredit_report()
    
    else:
        # ========== TAB SIMULASI & AGREGATOR ==========
        # PROSES SIMULASI
        if 'hitung' in locals() and hitung:
            if m > tp:
                st.error(f"⚠️ m ({m}) tidak boleh > tp ({tp})")
                return
            hasil = calculate_loan(K, r1, delta, n, tp, m, bank_type, biaya_dana)
            st.session_state.simulasi_hasil = hasil
            show_toast("📊 Simulasi pinjaman berhasil dihitung!", type="success")
        
        # TAMPILKAN HASIL SIMULASI
        if st.session_state.simulasi_hasil is not None:
            hasil = st.session_state.simulasi_hasil
            st.markdown("## 📊 Ubelasy - Simulasi Hitungan Pinjaman")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📅 Total Tenor", f"{hasil['T']} tahun")
            col1.metric("⚖️ dPSH", f"{hasil['dPSH']:.4f} / 2")
            col2.metric("🏦 Total Pinjaman", f"Rp {hasil['total_pokok']:,.0f}".replace(",", "."))
            col2.metric("🆓 PSH Diterima", f"Rp {hasil['PSH']:,.0f}".replace(",", ".") + f" ({hasil['psh_persen_total']:.2f}%)")
            col3.metric("💰 Keuntungan Bank", f"{hasil['laba_persen']:.2f}%")
            col3.metric("📈 Return Tahunan", f"{hasil['return_tahunan']:.2f}% p.a")
            col4.metric("📉 Rata-rata Bunga", f"{hasil['rata_bunga']:.2f}%")
            col4.metric("📊 Spread", f"{hasil['spread']:.2f}%")
        
            st.subheader("📋 Detail per Periode")
            st.dataframe(pd.DataFrame(hasil['detail']), width='stretch', hide_index=True)
        
            st.subheader("📌 Status Debitur")
            st.info(f"**{hasil['status']}** (dPSH = {hasil['dPSH']:.4f})")
        
            bunga = [hasil['detail'][i]['Suku Bunga (%)'] for i in range(n)]
            fig, ax = plt.subplots()
            ax.plot(range(1, n+1), bunga, marker='o', color='#2e7d32')
            ax.set_xlabel("Periode")
            ax.set_ylabel("Suku Bunga (%)")
            ax.set_title("Penurunan Suku Bunga 0.5% per Periode")
            ax.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)
        
            # EKSPOR PDF
            rekom = st.session_state.get("rekomendasi", None)
            try:
                pdf_path = export_simulation_to_pdf(hasil, rekom)
                with open(pdf_path, "rb") as f:
                    if st.download_button(
                        label="📄 Download Laporan PDF",
                        data=f,
                        file_name=f"ubelasy_simulasi_{hasil['T']}tahun.pdf",
                        mime="application/pdf",
                        width='stretch',
                        key="download_pdf_btn"
                    ):
                        show_toast("✅ Laporan berhasil diunduh!", type="success")
                os.unlink(pdf_path)
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")
        
        # ========== AGREGATOR: CARI PINJAMAN ==========
        st.markdown("---")
        st.subheader("🏦 Cari Pinjaman dari Bank Mitra")
        
        with st.form("form_cari_pinjaman"):
            col_a, col_b = st.columns(2)
            with col_a:
                jumlah_pinjaman = st.number_input("Jumlah pinjaman (Rp)", value=50_000_000, step=10_000_000)
                sektor_usaha = st.selectbox("Sektor usaha", ["pangan", "energi", "lainnya"])
                email = st.text_input("Email (untuk notifikasi)", placeholder="email@domain.com")
            with col_b:
                tenor = st.slider("Tenor (tahun)", 1, 5, 3)
                phone = st.text_input("Nomor WhatsApp (untuk notifikasi)", placeholder="08123456789")
            submitted = st.form_submit_button("🔍 Cari Rekomendasi")
        
        if submitted:
            nkhm_total = 0
            if "nkhm_scores" in st.session_state:
                nkhm_total = sum(st.session_state.nkhm_scores.values())
            profil = {
                "jumlah_pinjaman": jumlah_pinjaman,
                "sektor": sektor_usaha,
                "tenor": tenor,
                "email": email.strip(),
                "phone": phone.strip(),
                "nkhm_score": nkhm_total,
                "riwayat_pinjaman": []
            }
            rekom, credit_score, credit_grade = get_recommendations(profil)
            st.session_state.rekomendasi = rekom
            st.session_state.profil_terakhir = profil
            st.session_state.credit_score = credit_score
            st.session_state.credit_grade = credit_grade
            show_toast(f"🏦 Ditemukan {len(rekom)} bank mitra yang cocok!", type="success")
            st.rerun()
        
        if "credit_score" in st.session_state:
            st.info(f"📊 **Skor Kredit Anda: {st.session_state.credit_score}** ({st.session_state.credit_grade}) - Semakin tinggi skor, semakin rendah bunga yang ditawarkan.")
        
        if "rekomendasi" in st.session_state and st.session_state.rekomendasi:
            rekom = st.session_state.rekomendasi
            st.success(f"Ditemukan {len(rekom)} bank yang cocok:")
            for r in rekom:
                with st.expander(f"🏦 {r['bank']}"):
                    st.write(f"**Estimasi bunga:** {r['bunga']}% per tahun")
                    st.write(f"**Estimasi angsuran/bulan:** Rp {r['estimasi_angsuran']:,.0f}".replace(",", "."))
                    st.write(f"**Biaya admin:** Rp {r['biaya_admin']:,.0f}".replace(",", "."))
                    st.caption(f"📈 Skor kredit Anda: {r.get('credit_score', 'N/A')} ({r.get('credit_grade', 'N/A')}) → bunga disesuaikan")
                    if st.button(f"Ajukan ke {r['bank']}", key=r['id']):
                        app_id = submit_application(st.session_state.profil_terakhir, r['id'])
                        show_toast(f"✅ Pengajuan ke {r['bank']} terkirim! ID: {app_id}", type="success", duration=5000)
                        st.success(f"Pengajuan berhasil dikirim! ID: {app_id}")
                        st.info("Bank akan menghubungi Anda dalam 1x24 jam.")
        elif "rekomendasi" in st.session_state:
            st.warning("Belum ada bank yang cocok. Coba ubah kriteria pinjaman.")
        
        # ========== STATUS PENGAJUAN ==========
        st.markdown("---")
        st.subheader("📋 Status Pengajuan Anda")
        apps = get_all_applications_for_user()
        if not apps:
            st.info("Belum ada pengajuan. Silakan cari pinjaman di atas.")
        else:
            for app in apps[-5:]:
                status_color = {
                    "Dikirim": "🔵",
                    "Diproses": "🟡",
                    "Disetujui": "✅",
                    "Ditolak": "❌"
                }.get(app["status"], "⚪")
                with st.expander(f"{status_color} {app['id']} - {app['tanggal']} - {app['status']}"):
                    st.write(f"**Bank:** {app['bank_id']}")
                    st.write(f"**Jumlah pinjaman:** Rp {app['profil']['jumlah_pinjaman']:,.0f}".replace(",", "."))
                    st.write(f"**Sektor:** {app['profil']['sektor']}, **Tenor:** {app['profil']['tenor']} tahun")
                    if app.get('catatan'):
                        st.write(f"**Catatan:** {app['catatan']}")
                        
        # ========== ADMIN PANEL ==========
        if st.query_params.get("admin") == "1":
            from ubelasy.admin import admin_page
            admin_page()
            st.stop()
            
        if st.query_params.get("bank"):
            bank_id = st.query_params.get("bank")
            from ubelasy.bank_admin import bank_admin_page
            bank_admin_page(bank_id)
            st.stop()


if __name__ == "__main__":
    main()
