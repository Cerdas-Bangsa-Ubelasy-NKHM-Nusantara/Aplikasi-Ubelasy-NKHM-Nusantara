# nkhm/utils.py

def calculate_nkhm_q(iq, eq, sq, aq):
    """
    Menghitung NKHM_Q berdasarkan 4 kecerdasan.
    Rumus: ((IQ+EQ) × (SQ+AQ)) / ((IQ+EQ) + (SQ+AQ))
    """
    pembilang = (iq + eq) * (sq + aq)
    penyebut = (iq + eq) + (sq + aq)
    if penyebut == 0:
        return 0
    return round(pembilang / penyebut, 2)

def calculate_nkhm_total(nkhm_q, nasionalisme):
    """
    Menghitung NKHM_Total berdasarkan NKHM_Q dan skor Nasionalisme.
    Rumus: (NKHM_Q + Nasionalisme) / 2
    """
    return round((nkhm_q + nasionalisme) / 2, 2)

def get_nkhm_level(nkhm_total):
    if nkhm_total >= 80:
        return "🌟 Pahlawan Cerdas", "green"
    elif nkhm_total >= 60:
        return "📚 Cendekia Muda", "blue"
    elif nkhm_total >= 40:
        return "🌱 Penjelajah Ilmu", "orange"
    else:
        return "🌿 Perintis Jalan", "gray"
        
