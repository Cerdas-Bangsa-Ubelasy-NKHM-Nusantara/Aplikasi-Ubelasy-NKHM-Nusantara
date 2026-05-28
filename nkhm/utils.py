
def calculate_nkhm_q(iq, eq, sq, aq):
    pembilang = (iq + eq) * (sq + aq)
    penyebut = (iq + eq) + (sq + aq)
    if penyebut == 0:
        return 0
    return round(pembilang / penyebut, 2)

def calculate_nkhm_total(nkhm_q, nasionalisme):
    return round((nkhm_q + nasionalisme) / 2, 2)