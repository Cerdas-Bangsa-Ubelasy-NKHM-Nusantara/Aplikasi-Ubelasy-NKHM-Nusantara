# ubelasy/pdf_export.py
from fpdf import FPDF
import streamlit as st
from datetime import datetime
import tempfile
import os

class PDF(FPDF):
    def header(self):
        # Logo atau judul
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'UBELASY - Simulasi Pinjaman Berkelanjutan', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

def export_simulation_to_pdf(hasil, rekomendasi=None):
    """
    Mengekspor hasil simulasi Ubelasy ke PDF.
    hasil: dict dari calculate_loan
    rekomendasi: list dari get_recommendations (opsional)
    """
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    # Header
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Laporan Simulasi Pinjaman Ubelasy', 0, 1, 'C')
    pdf.ln(5)
    
    # Tanggal
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 6, f'Tanggal: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}', 0, 1)
    pdf.ln(5)
    
    # Parameter simulasi
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Parameter Simulasi:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f'Pinjaman per Periode: Rp {hasil["total_pokok"]:,.0f}'.replace(',', '.'), 0, 1)
    pdf.cell(0, 6, f'Total Tenor: {hasil["T"]} tahun', 0, 1)
    pdf.cell(0, 6, f'dPSH: {hasil["dPSH"]:.4f}', 0, 1)
    pdf.cell(0, 6, f'Tipe Bank: {"Pedesaan" if hasil.get("faktor_psh") == hasil["T"]/50 else "Perkotaan"}', 0, 1)
    pdf.ln(5)
    
    # Hasil utama
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Hasil Simulasi:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f'Total Pinjaman Akumulasi: Rp {hasil["total_pokok"]:,.0f}'.replace(',', '.'), 0, 1)
    pdf.cell(0, 6, f'PSH Diterima: Rp {hasil["PSH"]:,.0f} ({hasil["psh_persen_total"]:.2f}%)'.replace(',', '.'), 0, 1)
    pdf.cell(0, 6, f'Keuntungan Bank: {hasil["laba_persen"]:.2f}%', 0, 1)
    pdf.cell(0, 6, f'Return Tahunan Setara: {hasil["return_tahunan"]:.2f}% p.a', 0, 1)
    pdf.cell(0, 6, f'Rata-rata Suku Bunga: {hasil["rata_bunga"]:.2f}%', 0, 1)
    pdf.cell(0, 6, f'Spread: {hasil["spread"]:.2f}%', 0, 1)
    pdf.ln(5)
    
    # Status debitur
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Status Debitur:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, hasil['status'], 0, 1)
    pdf.ln(5)
    
    # Detail per periode
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Detail per Periode:', 0, 1)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(25, 8, 'Periode', 1, 0, 'C')
    pdf.cell(30, 8, 'Suku Bunga (%)', 1, 0, 'C')
    pdf.cell(45, 8, 'Total Kewajiban (Rp)', 1, 0, 'C')
    pdf.cell(45, 8, 'Angsuran/bln (Rp)', 1, 0, 'C')
    pdf.cell(45, 8, 'Sisa Hutang Akhir', 1, 1, 'C')
    
    pdf.set_font('Arial', '', 8)
    for d in hasil['detail']:
        pdf.cell(25, 6, str(d['Periode']), 1, 0, 'C')
        pdf.cell(30, 6, str(d['Suku Bunga (%)']), 1, 0, 'C')
        pdf.cell(45, 6, d['Total Kewajiban (Rp)'].replace('Rp ', ''), 1, 0, 'R')
        pdf.cell(45, 6, d['Angsuran/bln (Rp)'].replace('Rp ', ''), 1, 0, 'R')
        pdf.cell(45, 6, d['Sisa Hutang Akhir (Rp)'].replace('Rp ', ''), 1, 1, 'R')
    
    pdf.ln(5)
    
    # Jika ada rekomendasi bank
    if rekomendasi:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, 'Rekomendasi Bank Mitra:', 0, 1)
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(50, 8, 'Bank', 1, 0, 'C')
        pdf.cell(30, 8, 'Bunga (%)', 1, 0, 'C')
        pdf.cell(50, 8, 'Estimasi Angsuran/bln', 1, 0, 'C')
        pdf.cell(40, 8, 'Biaya Admin', 1, 1, 'C')
        
        pdf.set_font('Arial', '', 9)
        for r in rekomendasi:
            pdf.cell(50, 6, r['bank'], 1, 0, 'L')
            pdf.cell(30, 6, str(r['bunga']), 1, 0, 'C')
            pdf.cell(50, 6, f"Rp {r['estimasi_angsuran']:,.0f}".replace(',', '.'), 1, 0, 'R')
            pdf.cell(40, 6, f"Rp {r['biaya_admin']:,.0f}".replace(',', '.'), 1, 1, 'R')
    
    # Simpan ke file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
        pdf.output(tmpfile.name)
        tmp_path = tmpfile.name
    
    return tmp_path
