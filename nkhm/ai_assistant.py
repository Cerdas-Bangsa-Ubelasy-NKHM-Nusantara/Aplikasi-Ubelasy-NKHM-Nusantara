# nkhm/ai_assistant.py
import os
import random
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-genai tidak terinstall.")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("openai tidak terinstall.")

def get_ai_response(user_input, history, user_name, nkhm_score, nkhm_level):
    # ===== 1. GEMINI (gunakan key AIzaSy...) =====
    gemini_key = None
    try:
        gemini_key = st.secrets.get("GOOGLE_GEMINI_API_KEY")
    except Exception:
        gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    logger.info(f"Gemini API Key exists: {bool(gemini_key)}")

    if GENAI_AVAILABLE and gemini_key:
        try:
            # Jika key masih AQ, library mungkin gagal, tapi kita coba dulu.
            client = genai.Client(api_key=gemini_key)
            context = (
                f"Anda adalah Ki Hajar, asisten pendidikan di NKHM Nusantara. "
                f"Pengguna bernama {user_name}, skor NKHM {nkhm_score}, level {nkhm_level}. "
                "Jawab pertanyaan dengan bijak, inspiratif, dan berikan motivasi belajar."
            )
            history_text = ""
            for msg in history[-5:]:
                role = "Pengguna" if msg["role"] == "user" else "Ki Hajar"
                history_text += f"{role}: {msg['content']}\n"
            prompt = context + "\n" + history_text + f"Pengguna: {user_input}\nKi Hajar:"
            logger.info("Memanggil Gemini API...")
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            logger.info("Gemini berhasil.")
            return response.text
        except Exception as e:
            logger.error(f"Error Gemini: {e}")

    # ===== 2. OPENAI / OPENROUTER =====
    openai_key = None
    try:
        openai_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        openai_key = os.getenv("OPENAI_API_KEY")
    logger.info(f"OpenAI API Key exists: {bool(openai_key)}")

    if OPENAI_AVAILABLE and openai_key:
        try:
            # Deteksi OpenRouter (key dimulai sk-or-v1)
            base_url = None
            if openai_key.startswith("sk-or-v1"):
                base_url = "https://openrouter.ai/api/v1"
            client = OpenAI(api_key=openai_key, base_url=base_url)

            context = (
                f"Anda adalah Ki Hajar, asisten pendidikan di NKHM Nusantara. "
                f"Pengguna bernama {user_name}, skor NKHM {nkhm_score}, level {nkhm_level}. "
                "Jawab pertanyaan dengan bijak, inspiratif, dan berikan motivasi belajar."
            )
            messages = [{"role": "system", "content": context}]
            for msg in history[-5:]:
                role = "user" if msg["role"] == "user" else "assistant"
                messages.append({"role": role, "content": msg["content"]})
            messages.append({"role": "user", "content": user_input})
            logger.info("Memanggil OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            logger.info("OpenAI berhasil.")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error OpenAI: {e}")

    # ===== 3. FALLBACK =====
    logger.warning("Tidak ada AI yang tersedia. Gunakan fallback random.")
    responses = [
        f"Halo {user_name}! Teruslah belajar. NKHM-mu {nkhm_score} ({nkhm_level}).",
        f"Menarik! {user_input} ... Coba cari tahu lebih lanjut tentang sejarah Indonesia.",
        "Apakah kamu sudah mengerjakan soal hari ini? Semangat!",
        f"Pertanyaan bagus, {user_name}! Coba refleksikan dengan nilai-nilai Pancasila.",
        "Jangan lupa istirahat agar otak tetap segar ya!"
    ]
    return random.choice(responses)
