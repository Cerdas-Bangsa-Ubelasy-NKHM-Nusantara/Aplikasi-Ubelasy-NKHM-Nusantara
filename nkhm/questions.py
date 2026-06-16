# nkhm/questions.py
import json
from pathlib import Path
import streamlit as st

@st.cache_data(ttl=3600)
def load_all_questions():
    """
    Memuat semua soal dari folder nkhm/soal/ dan subfoldernya.
    Menentukan type dan national berdasarkan folder.
    """
    base_dir = Path(__file__).parent / "soal"
    questions = []
    
    if not base_dir.exists():
        return questions
    
    # Cari semua file .json di base_dir dan subfolder (rekursif)
    for json_file in base_dir.glob("**/*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    continue
                
                # Tentukan kategori berdasarkan folder parent (misal: .../soal/EQ/)
                folder_name = json_file.parent.name  # EQ, IQ, SQ, AQ, Nasionalisme, dll.
                # Jika folder_name tidak dikenali, gunakan 'Lainnya'
                if folder_name not in ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]:
                    folder_name = "Lainnya"
                
                for item in data:
                    # Pastikan field minimal ada
                    if "text" not in item or "options" not in item or "correct" not in item:
                        continue
                    
                    # Set type berdasarkan folder, jika belum ada
                    if "type" not in item:
                        if folder_name == "Nasionalisme":
                            item["type"] = "Nasionalisme"
                        elif folder_name == "EQ":
                            # Deteksi jika ini soal skala (EQ_scale) berdasarkan nama file
                            if "skor" in json_file.name.lower() or json_file.name in ["ketrampilan_emosi.json", "kecakapan_eq.json", "nilai_eq_dan_keyakinan.json"]:
                                item["type"] = "EQ_scale"
                            else:
                                item["type"] = "EQ"
                        else:
                            item["type"] = folder_name if folder_name in ["IQ", "SQ", "AQ"] else "Lainnya"
                    
                    # Set national berdasarkan folder
                    if "national" not in item:
                        item["national"] = (folder_name == "Nasionalisme")
                    
                    questions.append(item)
        except Exception as e:
            print(f"⚠️ Gagal membaca {json_file}: {e}")
    
    return questions
