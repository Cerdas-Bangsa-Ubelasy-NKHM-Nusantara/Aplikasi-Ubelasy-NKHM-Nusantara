# nkhm/ai_assistant.py
import os
import random

# Coba import Google Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ google-generativeai tidak terinstall. Gunakan fallback random.")

def get_ai_response(user_input, history, user_name, nkhm_score, nkhm_level):
    """
    Menghasilkan respons AI menggunakan Google Gemini.
    Jika API key tidak tersedia atau library tidak ada, gunakan fallback random.
    """
    # Ambil API key dari environment variable
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("AIzaSyALLmT6l7ip3m0YvODND36S7ENrwEKWBCY")

    if GEMINI_AVAILABLE and api_key:
        try:
            # Konfigurasi Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')  # atau 'gemini-pro'

            # Buat konteks yang kaya
            context = (
                f"Anda adalah Ki Hajar, asisten pendidikan di NKHM Nusantara. "
                f"Pengguna bernama {user_name}, skor NKHM {nkhm_score}, level {nkhm_level}. "
                "Jawab pertanyaan dengan bijak, inspiratif, dan berikan motivasi belajar. "
                "Jika ditanya tentang NKHM, jelaskan dengan semangat."
            )

            # Ambil 5 pesan terakhir dari history (agar konteks tetap relevan)
            history_text = ""
            for msg in history[-5:]:
                role = "Pengguna" if msg["role"] == "user" else "Ki Hajar"
                history_text += f"{role}: {msg['content']}\n"

            # Gabungkan prompt lengkap
            prompt = context + "\n" + history_text + f"Pengguna: {user_input}\nKi Hajar:"

            # Panggil Gemini API
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            # Jika terjadi error (misal API key invalid, kuota habis)
            print(f"⚠️ Error Gemini: {e}")
            return "Maaf, saya sedang sibuk. Coba tanya lagi nanti, ya! 😊"

    else:
        # ========== FALLBACK (jika API key tidak ada atau library tidak terinstall) ==========
        if not GEMINI_AVAILABLE:
            print("⚠️ google-generativeai tidak terinstall. Gunakan fallback random.")
        elif not api_key:
            print("⚠️ API Key tidak ditemukan. Gunakan fallback random.")

        responses = [
            f"Halo {user_name}! Teruslah belajar. NKHM-mu {nkhm_score} ({nkhm_level}).",
            f"Menarik! {user_input} ... Coba cari tahu lebih lanjut tentang sejarah Indonesia.",
            "Apakah kamu sudah mengerjakan soal hari ini? Semangat!",
            f"Pertanyaan bagus, {user_name}! Coba refleksikan dengan nilai-nilai Pancasila.",
            "Jangan lupa istirahat agar otak tetap segar ya!"
        ]
        return random.choice(responses)
