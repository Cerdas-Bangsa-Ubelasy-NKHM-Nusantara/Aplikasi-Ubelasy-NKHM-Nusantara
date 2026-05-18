# nkhm/questions.py
import os
import json
import streamlit as st

@st.cache_data(ttl=3600)  # cache selama 1 jam untuk mempercepat loading
def load_all_questions():
    """
    Memuat semua soal dari folder 'soal' yang berada di direktori yang sama dengan file ini.
    Struktur: soal/[kategori]/[namafile].json
    """
    questions = []
    
    # Dapatkan path absolut ke direktori tempat file ini berada (nkhm/)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    soal_dir = os.path.join(base_dir, "soal")
    
    # Mapping kategori ke folder
    kategori_folder = ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]
    
    # Debug: cetak path untuk verifikasi (akan muncul di log Streamlit)
    print(f"Base directory: {base_dir}")
    print(f"Soal directory: {soal_dir}")
    
    if not os.path.exists(soal_dir):
        print(f"ERROR: Folder soal tidak ditemukan di {soal_dir}")
        return []
    
    for kategori in kategori_folder:
        folder_path = os.path.join(soal_dir, kategori)
        if not os.path.isdir(folder_path):
            print(f"Folder tidak ditemukan: {folder_path}")
            continue
        
        # Cari semua file .json di folder tersebut
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for item in data:
                                # Pastikan setiap item memiliki field yang diperlukan
                                if "text" not in item or "options" not in item or "correct" not in item:
                                    print(f"Peringatan: Soal di {filepath} tidak lengkap, dilewati")
                                    continue
                                if "type" not in item:
                                    item["type"] = kategori
                                if "national" not in item:
                                    item["national"] = (kategori == "Nasionalisme")
                                questions.append(item)
                        else:
                            # Jika file berisi satu objek soal (tidak dalam list)
                            if "type" not in data:
                                data["type"] = kategori
                            if "national" not in data:
                                data["national"] = (kategori == "Nasionalisme")
                            questions.append(data)
                        print(f"Berhasil memuat {len(data) if isinstance(data, list) else 1} soal dari {filepath}")
                except json.JSONDecodeError as e:
                    print(f"Error JSON di {filepath}: {e}")
                except Exception as e:
                    print(f"Error membaca {filepath}: {e}")
    
    print(f"Total soal dimuat: {len(questions)}")
    return questions
