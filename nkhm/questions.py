# nkhm/questions.py
import os
import json

def load_all_questions():
    questions = []
    base_dir = os.path.join(os.path.dirname(__file__), "soal")
    kategori_folder = ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]
    
    for kategori in kategori_folder:
        folder_path = os.path.join(base_dir, kategori)
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
                                if "type" not in item:
                                    item["type"] = kategori
                                if "national" not in item:
                                    item["national"] = (kategori == "Nasionalisme")
                                questions.append(item)
                        else:
                            if "type" not in data:
                                data["type"] = kategori
                            if "national" not in data:
                                data["national"] = (kategori == "Nasionalisme")
                            questions.append(data)
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
    return questions
