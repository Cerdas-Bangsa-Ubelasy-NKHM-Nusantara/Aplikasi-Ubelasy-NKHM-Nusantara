‎# nkhm/scoring.py
‎"""
‎Modul ini berisi semua konstanta dan fungsi terkait penilaian:
‎- Standar jumlah soal
‎- Increment per jawaban benar
‎- Perhitungan skor tanggapan (EQ_scale, AQ_scale)
‎- Perhitungan NKHM_Q dan NKHM_Total
‎"""
‎
‎# ========== STANDAR JUMLAH SOAL UNTUK PENILAIAN (PILIHAN GANDA) ==========
‎STANDAR_IQ = 32
‎STANDAR_EQ = 38
‎STANDAR_SQ = 14
‎STANDAR_AQ = 14
‎STANDAR_NASIONALISME = 20
‎
‎# ========== INCREMENT PER JAWABAN BENAR ==========
‎# IQ: biasa
‎INCREMENT_IQ = 320 / STANDAR_IQ                                    # 3.125
‎# EQ: biasa
‎INCREMENT_EQ = 380 / STANDAR_EQ                                    # ≈ 2.6316
‎# SQ: strategis (2× standar)
‎INCREMENT_SQ = 140 / (2 * STANDAR_SQ)                              # ≈ 3.5714
‎# AQ: strategis (2× standar)
‎INCREMENT_AQ = 140 / (2 * STANDAR_AQ)                              # ≈ 3.5714
‎# Nasionalisme: strategis (2× standar)
‎INCREMENT_NASIONALISME = 200 / (2 * STANDAR_NASIONALISME)          # 2.5
‎
‎MAX_SCORE = 100
‎
‎# ========== MAPPING TIPE SOAL KE INCREMENT ==========
‎def get_increment(question_type):
‎    """Mengembalikan increment per jawaban benar berdasarkan tipe soal"""
‎    increments = {
‎        "IQ": INCREMENT_IQ,
‎        "EQ": INCREMENT_EQ,
‎        "SQ": INCREMENT_SQ,
‎        "AQ": INCREMENT_AQ,
‎        "Nasionalisme": INCREMENT_NASIONALISME
‎    }
‎    return increments.get(question_type, 0)
‎
‎# ========== FUNGSI PENILAIAN SKOR TANGGAPAN ==========
‎def get_column_index(selected_value, options_order):
‎    """
‎    Mengkonversi nilai yang dipilih ke indeks kolom (0-3).
‎    options_order: list of string misal ["3","2","1","0"] atau ["0","1","2","3"]
‎    """
‎    # Cari posisi selected_value dalam options_order
‎    try:
‎        pos = options_order.index(str(selected_value))
‎        return pos
‎    except ValueError:
‎        return 0
‎
‎def calculate_section_value(section_answers):
‎    """
‎    Menghitung nilai bagian dari [col1, col2, col3, col4]
‎    """
‎    return sum(section_answers)
‎
‎# ========== FUNGSI NKHM ==========
‎def calculate_nkhm_q(iq, eq, sq, aq):
‎    """Rumus NKHM_Q = ((IQ+EQ) × (SQ+AQ)) / ((IQ+EQ) + (SQ+AQ))"""
‎    pembilang = (iq + eq) * (sq + aq)
‎    penyebut = (iq + eq) + (sq + aq)
‎    if penyebut == 0:
‎        return 0
‎    return round(pembilang / penyebut, 2)
‎
‎def calculate_nkhm_total(nkhm_q, nasionalisme):
‎    """Rumus NKHM_Total = (NKHM_Q + Nasionalisme) / 2"""
‎    return round((nkhm_q + nasionalisme) / 2, 2)
‎
‎def get_nkhm_level(nkhm_total):
‎    if nkhm_total >= 80:
‎        return "🌟 Pahlawan Cerdas", "green"
‎    elif nkhm_total >= 60:
‎        return "📚 Cendekia Muda", "blue"
‎    elif nkhm_total >= 40:
‎        return "🌱 Penjelajah Ilmu", "orange"
‎    else:
‎        return "🌿 Perintis Jalan", "gray"
‎
