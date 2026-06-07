# nkhm/stomata_utils.py
SISI_NAMES = {
    1: "Kasih", 2: "Iman", 3: "Pengharapan",
    4: "Iman-Pengharapan", 5: "Kasih-Iman", 6: "Pengharapan-Kasih",
    7: "Berbuat iman", 8: "Berbuat pengharapan", 9: "Berbuat kasih",
    10: "Kasih-Iman-Pengharapan", 11: "Berbuat kasih-beriman", 12: "Berbuat kasih-berpengharapan",
}

LIKERT_SCORE = {"Sangat Tidak Setuju": 0, "Tidak Setuju": 1, "Netral": 2, "Setuju": 3, "Sangat Setuju": 4}

def konversi_ke_skor_0_1(nilai_likert):
    return 1 if nilai_likert >= 3 else 0

def hitung_persentase(skor, max_skor=11):
    return (skor / max_skor) * 100 if max_skor else 0

def tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan):
    total = persen_kasih + persen_iman + persen_pengharapan
    if total == 0:
        return [10]
    rk = (persen_kasih / total) * 100
    ri = (persen_iman / total) * 100
    rp = (persen_pengharapan / total) * 100
    if max(rk, ri, rp) - min(rk, ri, rp) < 5:
        return [1, 8, 9]
    max_val = max(rk, ri, rp)
    if max_val >= 60:
        return [1] if rk == max_val else [2] if ri == max_val else [3]
    elif (rk >= 40 and ri >= 40) or (ri >= 40 and rp >= 40) or (rp >= 40 and rk >= 40):
        if rk >= 40 and ri >= 40: return [5]
        if ri >= 40 and rp >= 40: return [4]
        if rp >= 40 and rk >= 40: return [6]
        return [10]
    else:
        return [9] if rk == max_val else [7] if ri == max_val else [8]