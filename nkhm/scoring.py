# nkhm/scoring.py
"""
Modul ini berisi konstanta dan fungsi terkait penilaian:
- Standar jumlah soal
- Increment per jawaban benar (poin mentah)
- Konversi poin mentah ke persentase (0-100)
- Perhitungan NKHM_Q dan NKHM_Total
"""

# ========== STANDAR JUMLAH SOAL UNTUK PENILAIAN (PILIHAN GANDA) ==========
STANDAR_IQ = 32
STANDAR_EQ = 38
STANDAR_SQ = 14
STANDAR_AQ = 14
STANDAR_NASIONALISME = 20

# ========== TOTAL POIN MAKSIMAL PER KATEGORI ==========
MAX_POIN_IQ = 320
MAX_POIN_EQ = 380
MAX_POIN_SQ = 140
MAX_POIN_AQ = 140
MAX_POIN_NASIONALISME = 200

# ========== INCREMENT PER JAWABAN BENAR (POIN MENTAH) ==========
INCREMENT_IQ = MAX_POIN_IQ // STANDAR_IQ              # 10
INCREMENT_EQ = MAX_POIN_EQ // STANDAR_EQ              # 10
INCREMENT_SQ = MAX_POIN_SQ // (2 * STANDAR_SQ)        # 140 / 28 = 5
INCREMENT_AQ = MAX_POIN_AQ // (2 * STANDAR_AQ)        # 140 / 28 = 5
INCREMENT_NASIONALISME = MAX_POIN_NASIONALISME // (2 * STANDAR_NASIONALISME)  # 200 / 40 = 5

MAX_SCORE = 100   # batas akhir persentase

# ========== MAPPING TIPE SOAL KE INCREMENT (POIN MENTAH) ==========
def get_increment(question_type):
    """Mengembalikan increment (poin mentah) per jawaban benar berdasarkan tipe soal"""
    increments = {
        "IQ": INCREMENT_IQ,
        "EQ": INCREMENT_EQ,
        "SQ": INCREMENT_SQ,
        "AQ": INCREMENT_AQ,
        "Nasionalisme": INCREMENT_NASIONALISME
    }
    return increments.get(question_type, 0)

# ========== FUNGSI UNTUK MENDAPATKAN PERSENTASE DARI POIN MENTAH ==========
def get_normalized_score(raw_points, max_points):
    """
    Mengkonversi poin mentah ke persentase (0-100).
    raw_points: total poin yang diperoleh
    max_points: total poin maksimal untuk kategori tersebut
    """
    if max_points == 0:
        return 0
    return min(MAX_SCORE, (raw_points / max_points) * 100)

# ========== FUNGSI PENILAIAN SKOR TANGGAPAN ==========
def get_column_index(selected_value, options_order):
    """
    Mengkonversi nilai yang dipilih ke indeks kolom (0-3).
    options_order: list of string misal ["3","2","1","0"] atau ["0","1","2","3"]
    """
    try:
        pos = options_order.index(str(selected_value))
        return pos
    except ValueError:
        return 0

def calculate_section_value(section_answers):
    """Menghitung nilai bagian dari [col1, col2, col3, col4]"""
    return sum(section_answers)

# ========== FUNGSI NKHM (MENGGUNAKAN NILAI PERSENTASE) ==========
def calculate_nkhm_q(iq_percent, eq_percent, sq_percent, aq_percent):
    """
    Rumus NKHM_Q = ((IQ+EQ) × (SQ+AQ)) / ((IQ+EQ) + (SQ+AQ))
    Semua parameter dalam persen (0-100)
    """
    pembilang = (iq_percent + eq_percent) * (sq_percent + aq_percent)
    penyebut = (iq_percent + eq_percent) + (sq_percent + aq_percent)
    if penyebut == 0:
        return 0
    return round(pembilang / penyebut, 2)

def calculate_nkhm_total(nkhm_q, nasionalisme_percent):
    """Rumus NKHM_Total = (NKHM_Q + Nasionalisme) / 2"""
    return round((nkhm_q + nasionalisme_percent) / 2, 2)

def get_nkhm_level(nkhm_total):
    if nkhm_total >= 80:
        return "🌟 Pahlawan Cerdas", "green"
    elif nkhm_total >= 60:
        return "📚 Cendekia Muda", "blue"
    elif nkhm_total >= 40:
        return "🌱 Penjelajah Ilmu", "orange"
    else:
        return "🌿 Perintis Jalan", "gray"
