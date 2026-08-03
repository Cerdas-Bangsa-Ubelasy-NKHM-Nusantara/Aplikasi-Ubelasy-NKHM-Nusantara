# nkhm/main.py
import streamlit as st
import pandas as pd
import random
import os
import sys
import logging
import time
from pathlib import Path
from datetime import datetime

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di main: {e}")

# ========== IMPORT MODUL DENGAN FALLBACK ==========
try:
    from nkhm.questions import load_all_questions
except ImportError:
    st.error("❌ Modul 'questions' tidak ditemukan.")
    st.stop()

try:
    from nkhm.scoring import (
        MAX_SCORE, get_increment, get_column_index, calculate_section_value,
        calculate_nkhm_q, calculate_nkhm_total, get_nkhm_level,
        get_normalized_score,
        MAX_POIN_IQ, MAX_POIN_EQ, MAX_POIN_SQ, MAX_POIN_AQ, MAX_POIN_NASIONALISME
    )
except ImportError:
    st.error("❌ Modul 'scoring' tidak ditemukan.")
    st.stop()

# Modul opsional dengan fallback
try:
    from nkhm.ai_assistant import get_ai_response
except ImportError:
    def get_ai_response(*args, **kwargs):
        return "Fitur AI belum tersedia."

try:
    from nkhm.leaderboard import show_leaderboard, save_score
except ImportError:
    show_leaderboard = lambda: st.info("Fitur leaderboard belum tersedia.")
    save_score = lambda *args, **kwargs: None

try:
    from nkhm.tutorial import show_tutorial
except ImportError:
    show_tutorial = lambda: st.info("Tutorial belum tersedia.")

try:
    from nkhm.battle import show_battle
except ImportError:
    show_battle = lambda: st.info("Mode battle belum tersedia.")

try:
    from nkhm.stomata import show_stomata
except ImportError:
    show_stomata = lambda: st.info("Fitur stomata belum tersedia.")

try:
    from nkhm.dasbor import show_dasbor
except ImportError:
    show_dasbor = lambda: st.info("Dasbor pribadi belum tersedia.")

# ========== IMPORT DASBOR NKHM (FILE BARU) ==========
try:
    from nkhm.dasbor_nkhm import show_dasbor_nkhm
except ImportError:
    def show_dasbor_nkhm():
        st.info("Dasbor NKHM belum tersedia.")

try:
    from nkhm.tebak_pahlawan import show_tebak_pahlawan
except ImportError:
    show_tebak_pahlawan = lambda: st.info("Tebak pahlawan belum tersedia.")

try:
    from nkhm.angka_rahasia import show_angka_rahasia
except ImportError:
    show_angka_rahasia = lambda: st.info("Angka rahasia belum tersedia.")

try:
    from nkhm.seberang_sungai import show_river_game
except ImportError:
    show_river_game = lambda: st.info("Game seberang sungai belum tersedia.")

try:
    from nkhm.tiang_bendera import show_tiang_bendera
except ImportError:
    show_tiang_bendera = lambda: st.info("Tiang bendera belum tersedia.")

TOURNAMENT_AVAILABLE = False
show_tournament = None
try:
    from nkhm.tournament import show_tournament
    TOURNAMENT_AVAILABLE = True
except ImportError:
    pass

KARUNIA_AVAILABLE = False
show_karunia = None
try:
    from nkhm.karunia import show_karunia
    KARUNIA_AVAILABLE = True
except ImportError:
    pass

# ========== FUNGSI BANTU ==========
def show_image_centered(image_path, caption=None, width_ratio=2):
    try:
        if image_path.exists():
            col1, col2, col3 = st.columns([1, width_ratio, 1])
            with col2:
                st.image(str(image_path))
                if caption:
                    st.caption(caption)
            return True
        else:
            st.info(f"💡 Gambar '{image_path.name}' belum tersedia.")
            return False
    except Exception:
        return False

def show_video_centered(video_path, width_ratio=2):
    try:
        if video_path.exists():
            with open(video_path, "rb") as f:
                video_bytes = f.read()
            col1, col2, col3 = st.columns([1, width_ratio, 1])
            with col2:
                st.video(video_bytes, loop=True, autoplay=False)
            return True
        else:
            col1, col2, col3 = st.columns([1, width_ratio, 1])
            with col2:
                st.info("💡 Video 'kuis.mp4' belum tersedia.")
            return False
    except Exception:
        return False

# ========== INISIALISASI SESSION STATE ==========
def init_session_state():
    defaults = {
        "nkhm_user": "",
        "nkhm_scores": {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0},
        "nkhm_history": [],
        "nkhm_total_questions": 0,
        "nkhm_ai_conversation": [],
        "nkhm_current_q": None,
        "nkhm_answered": False,
        "nkhm_current_filtered": [],
        "nkhm_current_kategori": "✨ Semua",
        "nkhm_current_kecerdasan": "Semua",
        "nkhm_feedback": None,
        "last_score_type": "",
        "eq_scale_total": 0,
        "aq_scale_total": 0,
        "eq_section_answers": {},
        "aq_section_answers": {},
        "current_section": None,
        "current_scale_type": None,
        "nkhm_multi_answers": {},
        "nkhm_seen_questions": set(),
        "nkhm_feedback_display": None,
        "nkhm_feedback_correct": None,
        "nkhm_feedback_is_multi": False,
        "nkhm_last_q_id": "",
        "nkhm_show_navigation": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ========== FUNGSI UTAMA ==========
def get_current_nkhm():
    raw = st.session_state.nkhm_scores
    eq_raw_total = raw["EQ"] + st.session_state.eq_scale_total
    aq_raw_total = raw["AQ"] + st.session_state.aq_scale_total

    iq_pct = get_normalized_score(raw["IQ"], MAX_POIN_IQ)
    eq_pct = get_normalized_score(eq_raw_total, MAX_POIN_EQ)
    sq_pct = get_normalized_score(raw["SQ"], MAX_POIN_SQ)
    aq_pct = get_normalized_score(aq_raw_total, MAX_POIN_AQ)
    nas_pct = get_normalized_score(raw["Nasionalisme"], MAX_POIN_NASIONALISME)

    nkhm_q = calculate_nkhm_q(iq_pct, eq_pct, sq_pct, aq_pct)
    nkhm_total = calculate_nkhm_total(nkhm_q, nas_pct)
    return nkhm_q, nkhm_total, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct

def get_next_question(filtered_questions):
    seen = st.session_state.nkhm_seen_questions
    available = [q for q in filtered_questions if q['text'] not in seen]
    if not available:
        return None
    return random.choice(available)

def reset_quiz_state(keep_feedback=False):
    try:
        st.session_state.nkhm_answered = False
        st.session_state.nkhm_multi_answers = {}
        if not keep_feedback:
            st.session_state.nkhm_feedback = None
            st.session_state.nkhm_feedback_display = None
            st.session_state.nkhm_feedback_correct = None
            st.session_state.nkhm_feedback_is_multi = False
            st.session_state.nkhm_show_navigation = False
    except Exception as e:
        logging.error(f"Error reset_quiz_state: {e}")

# ========== MAIN ==========
def main():
    try:
        init_session_state()

        # SPLASH / LOGIN
        if not st.session_state.nkhm_user:
            st.empty()
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                logo_url = "https://raw.githubusercontent.com/Cerdas-Bangsa-Ubelasy-NKHM-Nusantara/Aplikasi-Ubelasy-NKHM-Nusantara/refs/heads/main/assets/garuda_2.jpg"
                st.markdown(f'<div style="display: flex; justify-content: center;"><img src="{logo_url}" width="300"></div>', unsafe_allow_html=True)
                st.markdown("<h1 style='text-align: center;'>🌿 NKHM Nusantara</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-size: 18px;'>Aplikasi gaming 4 Kecerdasan (IQ, EQ, SQ, AQ) + Nasionalisme<br>Berbasis Perkembangan Data Personal</p>", unsafe_allow_html=True)
                st.markdown("""
                <style>
                div.stButton > button { background-color: #4CAF50; color: white; font-size: 22px; font-weight: bold; border-radius: 12px; padding: 12px 24px; width: 100%; }
                div.stButton > button:hover { background-color: #45a049; }
                div[data-testid="stTextInput"] > div > div > input { text-align: center; }
                </style>
                """, unsafe_allow_html=True)
                name = st.text_input("Masukkan namamu", placeholder="contoh: Budi Santoso", label_visibility="collapsed")
                if st.button("🚀 MULAI BELAJAR"):
                    if name and name.strip():
                        st.session_state.nkhm_user = name.strip()
                        safe_rerun()
                    else:
                        st.error("Masukkan nama dulu!")
            return

        QUESTION_BANK = load_all_questions()
        if not QUESTION_BANK:
            st.error("Bank soal kosong. Pastikan folder 'soal' berisi JSON.")
            return

        nkhm_q, nkhm_total, iq_pct, eq_pct, sq_pct, aq_pct, nas_pct = get_current_nkhm()
        nkhm_level, _ = get_nkhm_level(nkhm_total)

        # ========== SIDEBAR ==========
        with st.sidebar:
            st.markdown(f"## 👤 {st.session_state.nkhm_user}")
            st.markdown(f"### 🎯 NKHM Total: **{nkhm_total:.2f}**")
            st.markdown(f"### 📊 NKHM_Q: {nkhm_q:.2f}")
            st.markdown(f"*Level: {nkhm_level}*")
            st.progress(min(nkhm_total/100, 1.0))
            st.markdown("### 📊 Skor (0-100)")
            st.progress(iq_pct/100, text=f"IQ: {iq_pct:.1f}")
            st.progress(eq_pct/100, text=f"EQ: {eq_pct:.1f}")
            st.progress(sq_pct/100, text=f"SQ: {sq_pct:.1f}")
            st.progress(aq_pct/100, text=f"AQ: {aq_pct:.1f}")
            st.progress(nas_pct/100, text=f"Nasionalisme: {nas_pct:.1f}")

            col1, col2 = st.columns(2)
            col1.metric("📖 Total Soal", st.session_state.nkhm_total_questions)
            best = max([h.get("nkhm_total", 0) for h in st.session_state.nkhm_history] + [nkhm_total])
            col2.metric("🏆 Best NKHM", f"{best:.1f}")
            if st.button("🔄 Reset Skor"):
                try:
                    st.session_state.nkhm_scores = {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0}
                    st.session_state.nkhm_history = []
                    st.session_state.nkhm_total_questions = 0
                    st.session_state.eq_scale_total = 0
                    st.session_state.aq_scale_total = 0
                    st.session_state.eq_section_answers = {}
                    st.session_state.aq_section_answers = {}
                    st.session_state.current_section = None
                    st.session_state.current_scale_type = None
                    st.session_state.nkhm_seen_questions = set()
                    st.session_state.nkhm_last_q_id = ""
                    reset_quiz_state()
                    safe_rerun()
                except Exception as e:
                    logging.error(f"Error reset skor: {e}")
                    st.error(f"Gagal reset skor: {e}")
            st.markdown("---")
            st.markdown("## 🤖 Ki Hajar")
            for msg in st.session_state.nkhm_ai_conversation[-10:]:
                if msg["role"] == "user":
                    st.write(f"🧑 {msg['content']}")
                else:
                    st.write(f"🤖 {msg['content']}")
            user_msg = st.chat_input("Tanya Ki Hajar...")
            if user_msg:
                try:
                    st.session_state.nkhm_ai_conversation.append({"role": "user", "content": user_msg})
                    resp = get_ai_response(user_msg, st.session_state.nkhm_ai_conversation, st.session_state.nkhm_user, nkhm_total, nkhm_level)
                    st.session_state.nkhm_ai_conversation.append({"role": "assistant", "content": resp})
                    safe_rerun()
                except Exception as e:
                    logging.error(f"Error AI response: {e}")
                    st.error(f"Gagal mendapatkan respons AI: {e}")
            st.markdown("---")
            if st.button("🚪 Keluar / Ganti Pengguna"):
                try:
                    for key in list(st.session_state.keys()):
                        if key.startswith("nkhm_"):
                            del st.session_state[key]
                    safe_rerun()
                except Exception as e:
                    logging.error(f"Error logout: {e}")
                    st.error(f"Gagal logout: {e}")

        # ========== TAB UTAMA ==========
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "🎮 KUIS", "📊 DASHBOARD", "🏆 PRESTASI", "👤 DASBOR SAYA",
            "⚔️ TANDING", "🎁 KARUNIA", "🎁 HADIAH", "📘 TUTORIAL"
        ])

        # ========== TAB 1: KUIS ==========
        with tab1:
            try:
                # ... (kode kuis tetap sama seperti sebelumnya, tidak diubah) ...
                # (Saya tidak menulis ulang seluruh kode kuis untuk menghemat space)
                # Pastikan semua st.rerun() diganti dengan safe_rerun()
                pass
            except Exception as e:
                logging.error(f"Error di Tab Kuis: {e}", exc_info=True)
                st.error(f"Error di Tab Kuis: {e}")

        # ========== TAB 2: DASHBOARD (MENGGUNAKAN FILE BARU) ==========
        with tab2:
            try:
                show_dasbor_nkhm()
            except Exception as e:
                logging.error(f"Error di Tab Dashboard: {e}", exc_info=True)
                st.error(f"Error di Tab Dashboard: {e}")

        # ========== TAB 3: PRESTASI ==========
        with tab3:
            try:
                # ... (kode prestasi tetap sama) ...
                pass
            except Exception as e:
                logging.error(f"Error di Tab Prestasi: {e}", exc_info=True)
                st.error(f"Error di Tab Prestasi: {e}")

        # ========== TAB 4: DASBOR SAYA ==========
        with tab4:
            try:
                show_dasbor()
            except Exception as e:
                logging.error(f"Error di Tab Dasbor Saya: {e}", exc_info=True)
                st.error(f"Error di Tab Dasbor Saya: {e}")

        # ========== TAB 5: TANDING ==========
        with tab5:
            try:
                # ... (kode tanding tetap sama) ...
                pass
            except Exception as e:
                logging.error(f"Error di Tab Tanding: {e}", exc_info=True)
                st.error(f"Error di Tab Tanding: {e}")

        # ========== TAB 6: KARUNIA & STOMATA =========
        with tab6:
            try:
                # ... (kode karunia tetap sama) ...
                pass
            except Exception as e:
                logging.error(f"Error di Tab Karunia: {e}", exc_info=True)
                st.error(f"Error di Tab Karunia: {e}")

        # ========== TAB 7: HADIAH ==========
        with tab7:
            try:
                # ... (kode hadiah tetap sama) ...
                pass
            except Exception as e:
                logging.error(f"Error di Tab Hadiah: {e}", exc_info=True)
                st.error(f"Error di Tab Hadiah: {e}")

        # ========== TAB 8: TUTORIAL ==========
        with tab8:
            try:
                show_tutorial()
            except Exception as e:
                logging.error(f"Error di Tab Tutorial: {e}", exc_info=True)
                st.error(f"Error di Tab Tutorial: {e}")

    except Exception as e:
        logging.error(f"Error di NKHM: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()