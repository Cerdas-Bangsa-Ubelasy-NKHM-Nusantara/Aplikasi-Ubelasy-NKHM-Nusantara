# nkhm/hadiah/jarimatika_utils.py
"""
Utilitas Jarimatika PMD (Pedang Mata Dua)
Modul ini berisi fungsi-fungsi pendukung untuk perhitungan Jarimatika
tanpa memerlukan OpenCV/MediaPipe.
"""

import random
import logging
from typing import Dict, List, Tuple, Optional

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== KONSTANTASI ==========
# Mapping jari ke angka (6-10)
FINGER_MAP = {
    6: {"nama": "Kelingking", "icon": "🖐️", "posisi": 0, "singkatan": "Kl"},
    7: {"nama": "Manis", "icon": "🖐️", "posisi": 1, "singkatan": "Mn"},
    8: {"nama": "Tengah", "icon": "🖐️", "posisi": 2, "singkatan": "Tg"},
    9: {"nama": "Telunjuk", "icon": "🖐️", "posisi": 3, "singkatan": "Tl"},
    10: {"nama": "Jempol", "icon": "👍", "posisi": 4, "singkatan": "Jp"}
}

FINGER_NAMES = ["Kelingking", "Manis", "Tengah", "Telunjuk", "Jempol"]
FINGER_ICONS = ["🖐️", "🖐️", "🖐️", "🖐️", "👍"]
FINGER_SINGKATAN = ["Kl", "Mn", "Tg", "Tl", "Jp"]

# Level permainan
LEVELS = {
    "Mudah": {"min": 6, "max": 7, "label": "Mudah (6-7)"},
    "Sedang": {"min": 6, "max": 9, "label": "Sedang (6-9)"},
    "Sulit": {"min": 6, "max": 10, "label": "Sulit (6-10)"}
}

# ========== FUNGSI PERHITUNGAN ==========
def hitung_jarimatika(num1: int, num2: int) -> Optional[Dict]:
    """
    Menghitung perkalian menggunakan metode Jarimatika PMD.
    
    Args:
        num1: Angka pertama (6-10)
        num2: Angka kedua (6-10)
    
    Returns:
        dict: Hasil perhitungan dengan detail langkah, atau None jika error
    """
    try:
        # Validasi input
        if not (6 <= num1 <= 10) or not (6 <= num2 <= 10):
            logging.warning(f"Angka di luar rentang 6-10: {num1}, {num2}")
            return None
        
        # Indeks jari (0 = Kelingking, 1 = Manis, 2 = Tengah, 3 = Telunjuk, 4 = Jempol)
        idx1 = num1 - 6
        idx2 = num2 - 6
        
        # Nama jari
        finger1 = FINGER_NAMES[idx1]
        finger2 = FINGER_NAMES[idx2]
        icon1 = FINGER_ICONS[idx1]
        icon2 = FINGER_ICONS[idx2]
        
        # Jari bawah (dari pertemuan ke bawah) - dijumlahkan
        bawah_kiri = idx1 + 1
        bawah_kanan = idx2 + 1
        
        # Jari atas (dari pertemuan ke atas) - dikalikan
        atas_kiri = 5 - bawah_kiri
        atas_kanan = 5 - bawah_kanan
        
        # Total bawah (dijumlahkan) = puluhan
        total_bawah = bawah_kiri + bawah_kanan
        
        # Total atas (dikalikan) = satuan
        total_atas = atas_kiri * atas_kanan
        
        # Hasil akhir
        hasil = total_bawah * 10 + total_atas
        
        return {
            "num1": num1,
            "num2": num2,
            "finger1": finger1,
            "finger2": finger2,
            "icon1": icon1,
            "icon2": icon2,
            "idx1": idx1,
            "idx2": idx2,
            "bawah_kiri": bawah_kiri,
            "bawah_kanan": bawah_kanan,
            "atas_kiri": atas_kiri,
            "atas_kanan": atas_kanan,
            "total_bawah": total_bawah,
            "total_atas": total_atas,
            "hasil": hasil,
            "metode": "PMD"
        }
        
    except Exception as e:
        logging.error(f"Error hitung_jarimatika: {e}")
        return None

def generate_soal(level: str = "Mudah") -> Tuple[int, int]:
    """
    Menghasilkan soal perkalian acak berdasarkan level.
    
    Args:
        level: "Mudah", "Sedang", atau "Sulit"
    
    Returns:
        tuple: (angka1, angka2)
    """
    try:
        config = LEVELS.get(level, LEVELS["Mudah"])
        a = random.randint(config["min"], config["max"])
        b = random.randint(config["min"], config["max"])
        return a, b
    except Exception as e:
        logging.error(f"Error generate_soal: {e}")
        return 6, 6

def get_jari_visualisasi(angka: int, tangan: str = "kiri") -> Dict:
    """
    Mendapatkan visualisasi jari untuk angka tertentu.
    
    Args:
        angka: Angka 6-10
        tangan: "kiri" atau "kanan"
    
    Returns:
        dict: Informasi visualisasi jari
    """
    try:
        if not (6 <= angka <= 10):
            return {
                "jari_bawah": 0,
                "jari_atas": 0,
                "visual": [],
                "tangan": tangan,
                "error": True
            }
        
        idx = angka - 6
        # Jari yang terangkat (bawah)
        jari_bawah = idx + 1
        # Jari yang dilipat (atas)
        jari_atas = 5 - jari_bawah
        
        # Tampilkan jari dari bawah ke atas (kelingking ke jempol)
        visual = []
        for i in range(5):
            if i < jari_bawah:
                # Jari bawah (terangkat) - hijau
                visual.append({
                    "posisi": i,
                    "nama": FINGER_NAMES[i],
                    "icon": FINGER_ICONS[i],
                    "status": "terangkat",
                    "warna": "🟢"
                })
            else:
                # Jari atas (dilipat) - merah
                visual.append({
                    "posisi": i,
                    "nama": FINGER_NAMES[i],
                    "icon": FINGER_ICONS[i],
                    "status": "dilipat",
                    "warna": "🔴"
                })
        
        return {
            "angka": angka,
            "jari_bawah": jari_bawah,
            "jari_atas": jari_atas,
            "visual": visual,
            "tangan": tangan,
            "error": False
        }
    except Exception as e:
        logging.error(f"Error get_jari_visualisasi: {e}")
        return {"error": True, "visual": [], "tangan": tangan}

def get_finger_name(angka: int) -> Optional[str]:
    """Mendapatkan nama jari untuk angka tertentu."""
    try:
        if angka in FINGER_MAP:
            return FINGER_MAP[angka]["nama"]
        return None
    except Exception as e:
        logging.error(f"Error get_finger_name: {e}")
        return None

def get_finger_icon(angka: int) -> Optional[str]:
    """Mendapatkan ikon jari untuk angka tertentu."""
    try:
        if angka in FINGER_MAP:
            return FINGER_MAP[angka]["icon"]
        return None
    except Exception as e:
        logging.error(f"Error get_finger_icon: {e}")
        return None

def get_angka_dari_jari(nama_jari: str) -> Optional[int]:
    """Mendapatkan angka dari nama jari."""
    try:
        for angka, data in FINGER_MAP.items():
            if data["nama"].lower() == nama_jari.lower():
                return angka
        return None
    except Exception as e:
        logging.error(f"Error get_angka_dari_jari: {e}")
        return None

# ========== FUNGSI STATISTIK ==========
def hitung_statistik(history: List[Dict]) -> Dict:
    """
    Menghitung statistik dari riwayat permainan.
    
    Args:
        history: List riwayat permainan
    
    Returns:
        dict: Statistik permainan
    """
    try:
        total = len(history)
        if total == 0:
            return {"total": 0, "benar": 0, "salah": 0, "akurasi": 0, "skor": 0}
        
        benar = sum(1 for h in history if h.get("benar", False))
        salah = total - benar
        akurasi = (benar / total * 100) if total > 0 else 0
        
        # Hitung skor total (jika ada)
        skor = sum(h.get("poin", 0) for h in history)
        
        return {
            "total": total,
            "benar": benar,
            "salah": salah,
            "akurasi": round(akurasi, 1),
            "skor": skor
        }
    except Exception as e:
        logging.error(f"Error hitung_statistik: {e}")
        return {"total": 0, "benar": 0, "salah": 0, "akurasi": 0, "skor": 0}

def get_soal_terakhir(history: List[Dict], n: int = 5) -> List[Dict]:
    """Mendapatkan n soal terakhir dari riwayat."""
    try:
        return history[-n:] if history else []
    except Exception as e:
        logging.error(f"Error get_soal_terakhir: {e}")
        return []

# ========== FUNGSI FORMAT ==========
def format_hasil(detail: Dict) -> str:
    """
    Memformat hasil perhitungan menjadi string yang mudah dibaca.
    
    Args:
        detail: Hasil dari hitung_jarimatika()
    
    Returns:
        str: String hasil yang diformat
    """
    try:
        if not detail:
            return "Error: data tidak valid"
        
        return f"""
        📊 **Langkah Perhitungan Jarimatika PMD**
        
        🎯 Soal: {detail['num1']} × {detail['num2']}
        
        1️⃣ Identifikasi Jari:
           - {detail['num1']} = {detail['icon1']} {detail['finger1']}
           - {detail['num2']} = {detail['icon2']} {detail['finger2']}
        
        2️⃣ Jari Bawah (dijumlahkan → puluhan):
           - {detail['bawah_kiri']} + {detail['bawah_kanan']} = {detail['total_bawah']}
        
        3️⃣ Jari Atas (dikalikan → satuan):
           - {detail['atas_kiri']} × {detail['atas_kanan']} = {detail['total_atas']}
        
        4️⃣ Hasil Akhir:
           - {detail['total_bawah']}{detail['total_atas']} = {detail['hasil']}
        
        ✅ **{detail['num1']} × {detail['num2']} = {detail['hasil']}**
        """
    except Exception as e:
        logging.error(f"Error format_hasil: {e}")
        return "Error memformat hasil"

# ========== TESTING ==========
if __name__ == "__main__":
    print("="*50)
    print("🧪 TESTING JARIMATIKA UTILS")
    print("="*50)
    
    # Test 1: Hitung Jarimatika
    print("\n📝 Test 1: 7 × 8")
    hasil = hitung_jarimatika(7, 8)
    if hasil:
        print(f"  7 × 8 = {hasil['hasil']}")
        print(f"  Jari: {hasil['finger1']} × {hasil['finger2']}")
        print(f"  Bawah: {hasil['bawah_kiri']}+{hasil['bawah_kanan']}={hasil['total_bawah']}")
        print(f"  Atas: {hasil['atas_kiri']}×{hasil['atas_kanan']}={hasil['total_atas']}")
    
    # Test 2: Generate Soal
    print("\n📝 Test 2: Generate Soal")
    for level in ["Mudah", "Sedang", "Sulit"]:
        a, b = generate_soal(level)
        print(f"  {level}: {a} × {b}")
    
    # Test 3: Visualisasi Jari
    print("\n📝 Test 3: Visualisasi Jari (8)")
    vis = get_jari_visualisasi(8, "kanan")
    for item in vis.get("visual", []):
        print(f"  {item['warna']} {item['nama']} ({item['status']})")
    
    # Test 4: Format Hasil
    print("\n📝 Test 4: Format Hasil")
    if hasil:
        print(format_hasil(hasil))