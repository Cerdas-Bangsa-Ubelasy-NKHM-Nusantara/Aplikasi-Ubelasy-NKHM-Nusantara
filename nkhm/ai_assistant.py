# nkhm/ai_assistant.py
import os
import random

# === CEK KETERSEDIAAN LIBRARY ===
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

def get_ai_response(user_input, history, user_name, nkhm_score, nkhm_level):
    """
    Menghasilkan respons AI menggunakan Google Gemini (prioritas) atau OpenAI.
    Fallback ke random jika tidak ada API key atau library tidak tersedia.
    """
    # ========== 1. COBA GOOGLE GEMINI ==========
    gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if GEMINI_AVAILABLE and gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            context = (
                f"Anda adalah Ki Hajar, asisten pendidikan di NKHM Nusantara. "
                f"Pengguna bernama {user_name}, skor NKHM {nkhm_score}, level {nkhm_level}. "
                "Jawab pertanyaan dengan bijak, inspiratif, dan berikan motivasi belajar. "
                "Jika ditanya tentang NKHM, jelaskan dengan semangat."
            )

            history_text = ""
            for msg in history[-5:]:
                role = "Pengguna" if msg["role"] == "user" else "Ki Hajar"
                history_text += f"{role}: {msg['content']}\n"

            prompt = context + "\n" + history_text + f"Pengguna: {user_input}\nKi Hajar:"

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(f"⚠️ Error Gemini: {e}")
            # Jika Gemini gagal, lanjut ke OpenAI

    # ========== 2. COBA OPENAI ==========
    openai_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_AVAILABLE and openai_key:
        try:
            client = OpenAI(api_key=openai_key)

            context = (
                f"Anda adalah Ki Hajar, asisten pendidikan di NKHM Nusantara. "
                f"Pengguna bernama {user_name}, skor NKHM {nkhm_score}, level {nkhm_level}. "
                "Jawab pertanyaan dengan bijak, inspiratif, dan berikan motivasi belajar. "
                "Jika ditanya tentang NKHM, jelaskan dengan semangat."
            )

            messages = [{"role": "system", "content": context}]
            for msg in history[-5:]:
                role = "user" if msg["role"] == "user" else "assistant"
                messages.append({"role": role, "content": msg["content"]})
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ Error OpenAI: {e}")

    # ========== 3. FALLBACK ==========
    print("⚠️ Tidak ada AI yang tersedia. Gunakan fallback random.")
    responses = [
        f"Halo {user_name}! Teruslah belajar. NKHM-mu {nkhm_score} ({nkhm_level}).",
        f"Menarik! {user_input} ... Coba cari tahu lebih lanjut tentang sejarah Indonesia.",
        "Apakah kamu sudah mengerjakan soal hari ini? Semangat!",
        f"Pertanyaan bagus, {user_name}! Coba refleksikan dengan nilai-nilai Pancasila.",
        "Jangan lupa istirahat agar otak tetap segar ya!"
    ]
    return random.choice(responses)
