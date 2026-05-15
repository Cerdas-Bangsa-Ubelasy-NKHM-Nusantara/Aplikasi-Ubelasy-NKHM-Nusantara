# ubelasy/credit_score.py
def calculate_credit_score(nkhm_scores, history=None):
    """
    nkhm_scores: dict dengan kunci IQ, EQ, SQ, AQ
    history: list of dict riwayat pinjaman (opsional)
    return skor kredit 0-100
    """
    # 1. Hitung total NKHM (jumlah 4 skor)
    total_nkhm = sum(nkhm_scores.values())
    # Normalisasi ke 100 (max total 400)
    nkhm_score = min(total_nkhm / 4, 100)  # karena masing-masing max 100
    
    # 2. Faktor riwayat (jika ada)
    history_factor = 0
    if history:
        # Misal: jika pernah ada pinjaman yang disetujui dan dilunasi
        # Untuk demo, kita asumsikan ada faktor
        history_factor = 10  # contoh
    # 3. Faktor lain (misal usia usaha, agunan) bisa ditambah
    
    final_score = nkhm_score + history_factor
    return min(final_score, 100)
