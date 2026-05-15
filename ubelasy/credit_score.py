# ubelasy/credit_score.py

def calculate_credit_score(nkhm_scores, riwayat_pinjaman=None):
    """
    Hitung skor kredit berdasarkan NKHM dan riwayat pinjaman.
    nkhm_scores: dict dengan kunci IQ, EQ, SQ, AQ (masing-masing 0-100)
    riwayat_pinjaman: list of dict (opsional)
    return: skor 0-100
    """
    # Hitung total NKHM (maks 400)
    total_nkhm = sum(nkhm_scores.values())
    # Normalisasi ke skala 0-100
    nkhm_contribution = min(total_nkhm / 4, 100)
    
    # Faktor riwayat (jika ada)
    history_factor = 0
    if riwayat_pinjaman:
        # Contoh: pernah lunas tepat waktu +10, pernah telat -5, dll.
        for pinjaman in riwayat_pinjaman:
            if pinjaman.get("status") == "lunas_tepat_waktu":
                history_factor += 10
            elif pinjaman.get("status") == "telat":
                history_factor -= 5
    # Batasi history_factor
    history_factor = max(-20, min(history_factor, 20))
    
    skor = nkhm_contribution + history_factor
    return max(0, min(skor, 100))

def get_credit_grade(credit_score):
    """
    Mengembalikan grade kredit berdasarkan skor.
    """
    if credit_score >= 85:
        return "A (Sangat Baik)"
    elif credit_score >= 70:
        return "B (Baik)"
    elif credit_score >= 55:
        return "C (Cukup)"
    elif credit_score >= 40:
        return "D (Kurang)"
    else:
        return "E (Sangat Kurang)"

def adjust_interest_rate(base_rate, credit_grade):
    """
    Menyesuaikan suku bunga berdasarkan grade kredit.
    base_rate: suku bunga dasar bank (%)
    credit_grade: grade kredit (string)
    return: suku bunga yang disesuaikan
    """
    adjustment = {
        "A (Sangat Baik)": -1.5,
        "B (Baik)": -0.5,
        "C (Cukup)": 0,
        "D (Kurang)": 1.0,
        "E (Sangat Kurang)": 2.0
    }
    # Ambil adjustment berdasarkan grade
    for key, adj in adjustment.items():
        if key in credit_grade:
            return max(0, base_rate + adj)
    return base_rate
