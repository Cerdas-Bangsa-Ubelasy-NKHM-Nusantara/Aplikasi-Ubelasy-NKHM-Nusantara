# nkhm/utils.py
def calculate_nkhm(iq, eq, sq, aq):
    pembilang = (iq + eq) * (sq + aq)
    penyebut = (iq + eq) + (sq + aq)
    if penyebut == 0:
        return 0
    return round(pembilang / penyebut, 2)

def get_nkhm_level(nkhm):
    if nkhm >= 80:
        return "🌟 Pahlawan Cerdas", "green"
    elif nkhm >= 60:
        return "📚 Cendekia Muda", "blue"
    elif nkhm >= 40:
        return "🌱 Penjelajah Ilmu", "orange"
    else:
        return "🌿 Perintis Jalan", "gray"
