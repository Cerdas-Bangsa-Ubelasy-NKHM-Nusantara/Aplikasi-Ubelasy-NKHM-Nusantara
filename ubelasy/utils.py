# ubelasy/utils.py
def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")
