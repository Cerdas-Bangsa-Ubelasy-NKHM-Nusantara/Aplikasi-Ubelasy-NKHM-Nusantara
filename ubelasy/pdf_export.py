# ubelasy/pdf_export.py
from fpdf import FPDF
from datetime import datetime
import tempfile
import re

def clean_text(text):
    """Membersihkan teks dari karakter yang tidak didukung FPDF (emoji, simbol aneh)"""
    if not isinstance(text, str):
        text = str(text)
    # Ganti emoji dan simbol umum dengan teks biasa
    replacements = {
        "🔵": "[Diproses]",
        "🟡": "[Diproses]",
        "✅": "[Disetujui]",
        "❌": "[Ditolak]",
        "⚪": "[Dikirim]",
        "🌾": "[Ubelasy]",
        "📊": "[Statistik]",
        "📅": "[Tanggal]",
        "🏦": "[Bank]",
        "🆓": "[PSH]",
        "💰": "[Keuntungan]",
        "📈": "[Return]",
        "📉": "[Bunga]",
        "📋": "[Detail]",
        "📌": "[Info]",
        "🧠": "[IQ]",
        "❤️": "[EQ]",
        "🙏": "[SQ]",
        "💪": "[AQ]",
        "🇮🇩": "[NKHM]",
        "🎮": "[Kuis]",
        "🏆": "[Prestasi]",
        "⚔️": "[Tanding]",
        "🎁": "[Karunia]",
        "📘": "[Tutorial]",
        "💖": "[Stomata]",
        "🌿": "[NKHM]",
        "🌟": "[Level]",
        "📚": "[Level]",
        "🌱": "[Level]",
        "Rp": "Rp",  # aman
    }
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    # Hapus karakter non-ASCII lainnya (opsional, untuk berjaga-jaga)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'UBELASY - Simulasi Pinjaman Berkelanjutan', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

def export_simulation_to_pdf(hasil, rekomendasi=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 10)
    
    # Header laporan
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Laporan Simulasi Pinjaman Ubelasy', 0, 1, 'C')
    pdf.ln(5)
    
    # Tanggal
    pdf.set_font('Helvetica', 'I', 9)
    pdf.cell(0, 6, f'Tanggal: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}', 0, 1)
    pdf.ln(5)
    
    # Parameter
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, 'Parameter Simulasi:', 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, clean_text(f'Pinjaman per Periode: Rp {hasil["total_pokok"]:,.0f}').replace(',', '.'), 0, 1)
    pdf.cell(0, 6, clean_text(f'Total Tenor: {hasil["T"]} tahun'), 0, 1)
    pdf.cell(0, 6, clean_text(f'dPSH: {hasil["dPSH"]:.4f}'), 0, 1)
    tipe_bank = "Pedesaan" if hasil.get("faktor_psh") == hasil["T"]/50 else "Perkotaan"
    pdf.cell(0, 6, clean_text(f'Tipe Bank: {tipe_bank}'), 0, 1)
    pdf.ln(5)
    
    # Hasil simulasi
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, 'Hasil Simulasi:', 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, clean_text(f'Total Pinjaman Akumulasi: Rp {hasil["total_pokok"]:,.0f}').replace(',', '.'), 0, 1)
    pdf.cell(0, 6, clean_text(f'PSH Diterima: Rp {hasil["PSH"]:,.0f} ({hasil["psh_persen_total"]:.2f}%)').replace(',', '.'), 0, 1)
    pdf.cell(0, 6, clean_text(f'Keuntungan Bank: {hasil["laba_persen"]:.2f}%'), 0, 1)
    pdf.cell(0, 6, clean_text(f'Return Tahunan Setara: {hasil["return_tahunan"]:.2f}% p.a'), 0, 1)
    pdf.cell(0, 6, clean_text(f'Rata-rata Suku Bunga: {hasil["rata_bunga"]:.2f}%'), 0, 1)
    pdf.cell(0, 6, clean_text(f'Spread: {hasil["spread"]:.2f}%'), 0, 1)
    pdf.ln(5)
    
    # Status debitur
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, 'Status Debitur:', 0, 1)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, clean_text(hasil['status']), 0, 1)
    pdf.ln(5)
    
    # Tabel detail per periode
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, 'Detail per Periode:', 0, 1)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(25, 8, 'Periode', 1, 0, 'C')
    pdf.cell(30, 8, 'Suku Bunga (%)', 1, 0, 'C')
    pdf.cell(45, 8, 'Total Kewajiban (Rp)', 1, 0, 'C')
    pdf.cell(45, 8, 'Angsuran/bln (Rp)', 1, 0, 'C')
    pdf.cell(45, 8, 'Sisa Hutang Akhir', 1, 1, 'C')
    
    pdf.set_font('Helvetica', '', 8)
    for d in hasil['detail']:
        pdf.cell(25, 6, str(d['Periode']), 1, 0, 'C')
        pdf.cell(30, 6, str(d['Suku Bunga (%)']), 1, 0, 'C')
        pdf.cell(45, 6, clean_text(d['Total Kewajiban (Rp)'].replace('Rp ', '')), 1, 0, 'R')
        pdf.cell(45, 6, clean_text(d['Angsuran/bln (Rp)'].replace('Rp ', '')), 1, 0, 'R')
        pdf.cell(45, 6, clean_text(d['Sisa Hutang Akhir (Rp)'].replace('Rp ', '')), 1, 1, 'R')
    
    pdf.ln(5)
    
    # Rekomendasi bank (jika ada)
    if rekomendasi and len(rekomendasi) > 0:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, 'Rekomendasi Bank Mitra:', 0, 1)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(50, 8, 'Bank', 1, 0, 'C')
        pdf.cell(30, 8, 'Bunga (%)', 1, 0, 'C')
        pdf.cell(50, 8, 'Estimasi Angsuran/bln', 1, 0, 'C')
        pdf.cell(40, 8, 'Biaya Admin', 1, 1, 'C')
        
        pdf.set_font('Helvetica', '', 9)
        for r in rekomendasi:
            pdf.cell(50, 6, clean_text(r['bank']), 1, 0, 'L')
            pdf.cell(30, 6, str(r['bunga']), 1, 0, 'C')
            pdf.cell(50, 6, f"Rp {r['estimasi_angsuran']:,.0f}".replace(',', '.'), 1, 0, 'R')
            pdf.cell(40, 6, f"Rp {r['biaya_admin']:,.0f}".replace(',', '.'), 1, 1, 'R')
    
    # Simpan ke file sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name
