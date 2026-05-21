# nkhm/questions.py
import os
import json
import streamlit as st

@st.cache_data(ttl=3600)
def load_all_questions():
    questions = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    soal_dir = os.path.join(base_dir, "soal")
    kategori_folder = ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]
    
    for kategori in kategori_folder:
        folder_path = os.path.join(soal_dir, kategori)
        if not os.path.isdir(folder_path):
            continue
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for item in data:
                                # Jika type belum ada, set berdasarkan kategori dan nama file
                                if "type" not in item:
                                    if kategori == "Nasionalisme":
                                        item["type"] = "Nasionalisme"
                                    elif kategori == "EQ":
                                        if "skor" in filename.lower() or filename in ["ketrampilan_emosi.json", "kecakapan_eq.json", "nilai_eq_dan_keyakinan.json"]:
                                            item["type"] = "EQ_scale"
                                        else:
                                            item["type"] = "EQ"
                                    else:
                                        item["type"] = kategori
                                if "national" not in item:
                                    item["national"] = (kategori == "Nasionalisme")
                                questions.append(item)
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    return questions
