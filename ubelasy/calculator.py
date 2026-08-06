# ubelasy/calculator.py
import logging

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_loan(K, r1_percent, delta_percent, n, tp, m_years, bank_type, cost_funds_percent):
    """
    Hitung simulasi pinjaman Ubelasy.
    K: pinjaman per periode (Rp)
    r1_percent: suku bunga awal (%)
    delta_percent: penurunan per periode (%)
    n: jumlah periode
    tp: tenor per periode (tahun)
    m_years: tahun bayar di periode terakhir
    bank_type: 'desa' atau 'kota'
    cost_funds_percent: biaya dana+overhead (%)
    """
    # ========== VALIDASI INPUT ==========
    if K <= 0:
        logging.error("Pinjaman per periode (K) harus lebih besar dari 0.")
        raise ValueError("Pinjaman per periode (K) harus lebih besar dari 0.")
    if tp <= 0:
        logging.error("Tenor per periode (tp) harus lebih besar dari 0.")
        raise ValueError("Tenor per periode (tp) harus lebih besar dari 0.")
    if m_years < 0 or m_years > tp:
        logging.error(f"Tahun bayar (m_years) harus antara 0 dan {tp}.")
        raise ValueError(f"Tahun bayar (m_years) harus antara 0 dan {tp}.")
    if n <= 0:
        logging.error("Jumlah periode (n) harus lebih besar dari 0.")
        raise ValueError("Jumlah periode (n) harus lebih besar dari 0.")
    if bank_type not in ['desa', 'kota']:
        logging.error("bank_type harus 'desa' atau 'kota'.")
        raise ValueError("bank_type harus 'desa' atau 'kota'.")

    # ========== PERHITUNGAN ==========
    r = []
    for i in range(n):
        rate = r1_percent - i * delta_percent
        rate = max(0, rate)
        r.append(rate / 100)
    
    T = n * tp
    dPSH = T / 25
    total_pokok = n * K
    TSH = [K * (1 + r[i] * tp) for i in range(n)]
    TSH_last = TSH[-1]
    SHA = TSH_last * (1 - m_years / tp)
    if SHA < 0:
        SHA = 0
    
    total_bayar_sebelum_psh = 0
    for i in range(n-1):
        total_bayar_sebelum_psh += TSH[i]
    total_bayar_sebelum_psh += TSH_last * (m_years / tp)
    
    faktor_psh = T / 50 if bank_type == 'desa' else T / 60
    PSH = SHA * faktor_psh
    total_bayar_sesudah_psh = total_bayar_sebelum_psh + (SHA - PSH)
    
    laba_nominal = total_bayar_sesudah_psh - total_pokok
    laba_persen = (laba_nominal / total_pokok) * 100
    return_tahunan = laba_persen / T if T > 0 else 0
    
    weighted_bunga = sum(r[i] * tp for i in range(n))
    rata_bunga = (weighted_bunga / T) * 100 if T > 0 else 0
    spread = rata_bunga - cost_funds_percent
    
    psh_persen_total = (PSH / total_pokok) * 100
    
    detail = []
    for i in range(n):
        bunga_persen = r[i] * 100
        tsh = TSH[i]
        angsuran_bulan = tsh / (tp * 12) if tp > 0 else 0
        is_last = (i == n-1)
        total_dibayar = tsh if not is_last else tsh * (m_years / tp)
        sisa_akhir = 0 if not is_last else SHA
        detail.append({
            "Periode": i+1,
            "Suku Bunga (%)": round(bunga_persen, 2),
            "Total Kewajiban (Rp)": f"Rp {tsh:,.0f}".replace(",", "."),
            "Angsuran/bln (Rp)": f"Rp {angsuran_bulan:,.0f}".replace(",", "."),
            "Total Dibayar (Rp)": f"Rp {total_dibayar:,.0f}".replace(",", "."),
            "Sisa Hutang Akhir (Rp)": f"Rp {sisa_akhir:,.0f}".replace(",", ".")
        })
    
    if dPSH <= 0.20:
        status = "🟢 Pemula (Beginner)"
    elif dPSH <= 0.50:
        status = "🔵 Berkembang (Developing)"
    elif dPSH <= 1.00:
        status = "🟡 Madya (Intermediate)"
    elif dPSH <= 1.80:
        status = "🟠 Lanjut (Advanced)"
    else:
        status = "🔴 Yobel (Jubilee)"
    
    return {
        "T": T,
        "dPSH": dPSH,
        "total_pokok": total_pokok,
        "SHA": SHA,
        "PSH": PSH,
        "psh_persen_total": psh_persen_total,
        "laba_persen": laba_persen,
        "return_tahunan": return_tahunan,
        "rata_bunga": rata_bunga,
        "spread": spread,
        "detail": detail,
        "status": status,
        "faktor_psh": faktor_psh
    }