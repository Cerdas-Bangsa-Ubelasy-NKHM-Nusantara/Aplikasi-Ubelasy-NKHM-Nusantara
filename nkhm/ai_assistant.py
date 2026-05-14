# nkhm/ai_assistant.py
import random

def get_ai_response(user_input, history, user_name, nkhm_score, nkhm_level):
    responses = [
        f"Halo {user_name}! Teruslah belajar. NKHM-mu {nkhm_score} ({nkhm_level}).",
        f"Menarik! {user_input} ... Coba cari tahu lebih lanjut tentang sejarah Indonesia.",
        "Apakah kamu sudah mengerjakan soal hari ini? Semangat!"
    ]
    return random.choice(responses)
