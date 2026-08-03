# nkhm/ai_assistant.py
"""
Modul AI Assistant untuk NKHM Nusantara.
Mendukung Google Gemini (prioritas) dan OpenAI (fallback).
"""

import os
import random
import logging
from typing import List, Dict, Optional, Tuple
import streamlit as st

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ========== CEK KETERSEDIAAN LIBRARY ==========
try:
    from google import genai
    GENAI_AVAILABLE = True
    logger.info("✅ Google GenAI library tersedia")
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("⚠️ google-genai tidak terinstall. Coba: pip install google-genai")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    logger.info("✅ OpenAI library tersedia")
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("⚠️ openai tidak terinstall.")

# ========== KONFIGURASI ==========
GEMINI_MODEL = "gemini-1.5-flash"  # Atau "gemini-1.5-pro", "gemini-2.0-flash"
OPENAI_MODEL = "gpt-3.5-turbo"     # Atau "gpt-4", "gpt-4-turbo"
MAX_HISTORY_MESSAGES = 5
MAX_TOKENS = 300
TEMPERATURE = 0.7

# ========== RESPON FALLBACK ==========
FALLBACK_RESPONSES = [
    "Halo {name}! Teruslah belajar. NKHM-mu {score} ({level}).",
    "Menarik! Coba cari tahu lebih lanjut tentang sejarah Indonesia.",
    "Apakah kamu sudah mengerjakan soal hari ini? Semangat!",
    "Pertanyaan bagus, {name}! Coba refleksikan dengan nilai-nilai Pancasila.",
    "Jangan lupa istirahat agar otak tetap segar ya!",
    "Belajar adalah perjalanan tanpa akhir. Teruslah melangkah!",
    "Setiap hari adalah kesempatan baru untuk belajar sesuatu yang berharga.",
    "NKHM-mu {score}. Pertahankan dan tingkatkan terus!",
    "Pahlawan tidak dilahirkan, tetapi dibentuk melalui perjuangan dan pembelajaran.",
]

# ========== FUNGSI BANTU ==========
def get_api_key(service: str) -> Optional[str]:
    """
    Mendapatkan API Key dari Streamlit Secrets atau environment variable.
    
    Args:
        service: 'gemini' atau 'openai'
    
    Returns:
        Optional[str]: API Key atau None jika tidak ditemukan
    """
    key_names = {
        'gemini': ['GOOGLE_GEMINI_API_KEY', 'GEMINI_API_KEY'],
        'openai': ['OPENAI_API_KEY']
    }
    
    if service not in key_names:
        logger.error(f"Service '{service}' tidak dikenal")
        return None
    
    try:
        # Coba dari Streamlit Secrets
        for key_name in key_names[service]:
            if key_name in st.secrets:
                key = st.secrets[key_name]
                if key:
                    logger.info(f"✅ API Key {service} ditemukan di Secrets")
                    return key
    except Exception as e:
        logger.debug(f"Error membaca Secrets: {e}")
    
    # Coba dari environment variable
    for key_name in key_names[service]:
        key = os.getenv(key_name)
        if key:
            logger.info(f"✅ API Key {service} ditemukan di environment")
            return key
    
    logger.warning(f"⚠️ API Key {service} tidak ditemukan")
    return None

def build_context(
    user_name: str,
    nkhm_score: float,
    nkhm_level: str,
    history: List[Dict[str, str]]
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Membangun konteks dan pesan untuk AI.
    
    Returns:
        Tuple[str, List[Dict]]: (system_prompt, messages)
    """
    system_prompt = (
        f"Anda adalah Ki Hajar, asisten pendidikan di aplikasi NKHM Nusantara. "
        f"Pengguna bernama {user_name}, skor NKHM {nkhm_score:.1f}, level {nkhm_level}. "
        "Karakter Anda: bijaksana, inspiratif, dan penuh semangat belajar. "
        "Anda selalu memberikan jawaban yang membangun motivasi dan wawasan. "
        "Jika ditanya tentang NKHM, jelaskan dengan antusiasme. "
        "Gunakan bahasa Indonesia yang baik dan mudah dimengerti. "
        "Beri tahu pengguna tentang fitur-fitur NKHM: kuis, dasbor, prestasi, dan tanding."
    )
    
    # Ambil beberapa pesan terakhir dari history
    recent_messages = history[-MAX_HISTORY_MESSAGES:] if history else []
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in recent_messages:
        role = "user" if msg.get("role") == "user" else "assistant"
        content = msg.get("content", "")
        if content:
            messages.append({"role": role, "content": content})
    
    return system_prompt, messages

def generate_gemini_response(
    user_input: str,
    context: str,
    messages: List[Dict[str, str]]
) -> Optional[str]:
    """
    Menghasilkan respons menggunakan Google Gemini.
    
    Returns:
        Optional[str]: Respons AI atau None jika gagal
    """
    if not GENAI_AVAILABLE:
        logger.warning("GenAI tidak tersedia")
        return None
    
    api_key = get_api_key('gemini')
    if not api_key:
        return None
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Bangun prompt lengkap
        prompt = context + "\n"
        for msg in messages[-MAX_HISTORY_MESSAGES:]:
            role = "Pengguna" if msg["role"] == "user" else "Ki Hajar"
            prompt += f"{role}: {msg['content']}\n"
        prompt += f"Pengguna: {user_input}\nKi Hajar:"
        
        logger.info("🔄 Memanggil Gemini API...")
        
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        
        if response and response.text:
            logger.info("✅ Gemini berhasil menghasilkan respons")
            return response.text.strip()
        else:
            logger.warning("⚠️ Gemini mengembalikan respons kosong")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error Gemini: {e}")
        return None

def generate_openai_response(
    user_input: str,
    messages: List[Dict[str, str]]
) -> Optional[str]:
    """
    Menghasilkan respons menggunakan OpenAI.
    
    Returns:
        Optional[str]: Respons AI atau None jika gagal
    """
    if not OPENAI_AVAILABLE:
        logger.warning("OpenAI tidak tersedia")
        return None
    
    api_key = get_api_key('openai')
    if not api_key:
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Tambahkan pertanyaan user
        messages.append({"role": "user", "content": user_input})
        
        logger.info("🔄 Memanggil OpenAI API...")
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        if response and response.choices:
            result = response.choices[0].message.content
            logger.info("✅ OpenAI berhasil menghasilkan respons")
            return result.strip()
        else:
            logger.warning("⚠️ OpenAI mengembalikan respons kosong")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error OpenAI: {e}")
        return None

def get_fallback_response(
    user_input: str,
    user_name: str,
    nkhm_score: float,
    nkhm_level: str
) -> str:
    """
    Menghasilkan respons fallback jika AI tidak tersedia.
    """
    # Pilih respons acak
    response_template = random.choice(FALLBACK_RESPONSES)
    
    # Format dengan data pengguna
    try:
        response = response_template.format(
            name=user_name or "Sahabat",
            score=f"{nkhm_score:.1f}" if nkhm_score else "0",
            level=nkhm_level or "Pemula"
        )
    except KeyError:
        # Jika template memiliki placeholder yang tidak dikenal
        response = response_template
        
    # Tambahkan sapaan khusus jika pengguna memiliki nama
    if user_name and random.random() < 0.3:
        response = f"{user_name}, " + response
    
    return response

def get_ai_response(
    user_input: str,
    history: List[Dict[str, str]],
    user_name: str,
    nkhm_score: float,
    nkhm_level: str
) -> str:
    """
    Menghasilkan respons AI menggunakan Google Gemini (prioritas) atau OpenAI.
    Fallback ke respons manual jika API gagal.
    
    Args:
        user_input: Pertanyaan dari pengguna
        history: Riwayat percakapan
        user_name: Nama pengguna
        nkhm_score: Skor NKHM
        nkhm_level: Level NKHM
    
    Returns:
        str: Respons AI atau fallback
    """
    # Validasi input
    if not user_input or not user_input.strip():
        return "Halo! Ada yang bisa saya bantu?"
    
    user_input = user_input.strip()
    
    # Cek apakah pertanyaan tentang NKHM
    nkhm_keywords = ["nkhm", "skor", "level", "kuis", "soal", "prestasi", "tanding", "dasbor"]
    is_nkhm_question = any(kw in user_input.lower() for kw in nkhm_keywords)
    
    try:
        # Bangun konteks
        context, messages = build_context(user_name, nkhm_score, nkhm_level, history)
        
        # ===== 1. COBA GEMINI =====
        gemini_response = generate_gemini_response(user_input, context, messages)
        if gemini_response:
            return gemini_response
        
        # ===== 2. COBA OPENAI =====
        openai_response = generate_openai_response(user_input, messages)
        if openai_response:
            return openai_response
        
        # ===== 3. FALLBACK =====
        logger.info("💡 Menggunakan fallback response")
        return get_fallback_response(user_input, user_name, nkhm_score, nkhm_level)
        
    except Exception as e:
        logger.error(f"❌ Error get_ai_response: {e}")
        return get_fallback_response(user_input, user_name, nkhm_score, nkhm_level)

def check_ai_availability() -> Dict[str, bool]:
    """
    Memeriksa ketersediaan layanan AI.
    
    Returns:
        Dict: Status ketersediaan setiap layanan
    """
    return {
        "gemini": GENAI_AVAILABLE and bool(get_api_key('gemini')),
        "openai": OPENAI_AVAILABLE and bool(get_api_key('openai')),
        "any": False  # Akan diupdate
    }

def get_ai_status_message() -> str:
    """
    Mendapatkan pesan status AI untuk ditampilkan di UI.
    """
    status = check_ai_availability()
    
    if status["gemini"]:
        return "✅ AI aktif (Gemini)"
    elif status["openai"]:
        return "✅ AI aktif (OpenAI)"
    else:
        return "⚠️ AI tidak tersedia (gunakan mode offline)"

if __name__ == "__main__":
    # ========== TESTING ==========
    print("="*50)
    print("🧪 TESTING AI ASSISTANT")
    print("="*50)
    
    # Cek status
    status = check_ai_availability()
    print(f"\n📊 Status AI:")
    print(f"  Gemini: {'✅' if status['gemini'] else '❌'}")
    print(f"  OpenAI: {'✅' if status['openai'] else '❌'}")
    print(f"  Status: {get_ai_status_message()}")
    
    # Test response
    print("\n💬 Test percakapan:")
    test_inputs = [
        "Apa itu NKHM?",
        "Bagaimana cara meningkatkan skor?",
        "Selamat pagi!",
    ]
    
    test_user = "Budi"
    test_score = 65.5
    test_level = "📚 Cendekia Muda"
    test_history = []
    
    for inp in test_inputs:
        print(f"\n🧑 Pengguna: {inp}")
        response = get_ai_response(inp, test_history, test_user, test_score, test_level)
        print(f"🤖 Ki Hajar: {response[:100]}...")
        test_history.append({"role": "user", "content": inp})
        test_history.append({"role": "assistant", "content": response})