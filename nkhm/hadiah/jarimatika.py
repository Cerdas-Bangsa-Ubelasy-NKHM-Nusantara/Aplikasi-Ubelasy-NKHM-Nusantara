# nkhm/hadiah/jarimatika.py
"""
Fitur Jarimatika dengan Computer Vision.
Mendeteksi jari tangan dari kamera untuk menghitung perkalian.
"""

import streamlit as st
import cv2
import numpy as np
import random
import time
import logging
from PIL import Image
from nkhm.hadiah.jarimatika_utils import detect_fingers_from_frame, MEDIAPIPE_AVAILABLE

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== KONFIGURASI ==========
LEVELS = {
    "Mudah": {"min": 1, "max": 5},
    "Sedang": {"min": 2, "max": 7},
    "Sulit": {"min": 3, "max": 9}
}

SOAL_TERJEMAHAN = {
    1: "satu", 2: "dua", 3: "tiga", 4: "empat", 5: "lima",
    6: "enam", 7: "tujuh", 8: "delapan", 9: "sembilan"
}

def generate_soal(level="Mudah"):
    """Menghasilkan soal perkalian acak."""
    try:
        config = LEVELS.get(level, LEVELS["Mudah"])
        a = random.randint(config["min"], config["max"])
        b = random.randint(config["min"], config["max"])
        jawaban = a * b
        return a, b, jawaban
    except Exception as e:
        logging.error(f"Error generate_soal: {e}")
        return 1, 1, 1

def init_jarimatika_state():
    """Inisialisasi session state untuk Jarimatika."""
    try:
        if "jarimatika_a" not in st.session_state:
            st.session_state.jarimatika_a = None
        if "jarimatika_b" not in st.session_state:
            st.session_state.jarimatika_b = None
        if "jarimatika_jawaban" not in st.session_state:
            st.session_state.jarimatika_jawaban = None
        if "jarimatika_skor" not in st.session_state:
            st.session_state.jarimatika_skor = 0
        if "jarimatika_total" not in st.session_state:
            st.session_state.jarimatika_total = 0
        if "jarimatika_benar" not in st.session_state:
            st.session_state.jarimatika_benar = 0
        if "jarimatika_level" not in st.session_state:
            st.session_state.jarimatika_level = "Mudah"
        if "jarimatika_feedback" not in st.session_state:
            st.session_state.jarimatika_feedback = None
        if "jarimatika_soal_aktif" not in st.session_state:
            st.session_state.jarimatika_soal_aktif = False
    except Exception as e:
        logging.error(f"Error init_jarimatika_state: {e}")

def reset_jarimatika():
    """Reset semua state Jarimatika."""
    try:
        st.session_state.jarimatika_a = None
        st.session_state.jarimatika_b = None
        st.session_state.jarimatika_jawaban = None
        st.session_state.jarimatika_skor = 0
        st.session_state.jarimatika_total = 0
        st.session_state.jarimatika_benar = 0
        st.session_state.jarimatika_feedback = None
        st.session_state.jarimatika_soal_aktif = False
        logging.info("Jarimatika state direset")
    except Exception as e:
        logging.error(f"Error reset_jarimatika: {e}")

def show_jarimatika():
    """Menampilkan fitur Jarimatika."""
    try:
        init_jarimatika_state()
        
        st.markdown("## 🧮 Jarimatika dengan Computer Vision")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
            padding: 15px 20px;
            border-radius: 12px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 40px;">🖐️</div>
                <div>
                    <div style="font-size: 18px; font-weight: bold;">Belajar Perkalian dengan Jari!</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Gunakan kamera untuk mendeteksi jari tangan Anda dan jawab soal perkalian.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== CEK KETERSEDIAAN CAMERA =====
        if not MEDIAPIPE_AVAILABLE:
            st.error("""
            ❌ **MediaPipe tidak terinstall!**
            
            Untuk menggunakan fitur ini, install dependensi yang diperlukan:
            ```
            pip install opencv-python mediapipe numpy
            ```
            
            Atau gunakan mode manual (tanpa kamera).
            """)
            
            # Mode manual sebagai fallback
            show_jarimatika_manual()
            return
        
        # ===== PILIH LEVEL =====
        col1, col2, col3 = st.columns(3)
        with col1:
            level = st.selectbox(
                "📊 Level Kesulitan",
                ["Mudah", "Sedang", "Sulit"],
                index=["Mudah", "Sedang", "Sulit"].index(st.session_state.jarimatika_level)
            )
            if level != st.session_state.jarimatika_level:
                st.session_state.jarimatika_level = level
                st.session_state.jarimatika_soal_aktif = False
                st.rerun()
        
        with col2:
            st.metric("🏆 Skor", st.session_state.jarimatika_skor)
        
        with col3:
            config = LEVELS.get(level, LEVELS["Mudah"])
            st.caption(f"📊 Rentang angka: {config['min']} - {config['max']}")
        
        # ===== TAMPILKAN SOAL =====
        if not st.session_state.jarimatika_soal_aktif:
            a, b, jawaban = generate_soal(level)
            st.session_state.jarimatika_a = a
            st.session_state.jarimatika_b = b
            st.session_state.jarimatika_jawaban = jawaban
            st.session_state.jarimatika_soal_aktif = True
        
        st.markdown("---")
        st.markdown(f"### 📝 {st.session_state.jarimatika_a} × {st.session_state.jarimatika_b} = ?")
        
        # ===== KAMERA =====
        st.markdown("### 📷 Kamera")
        st.markdown("Tunjukkan jari tangan Anda di depan kamera untuk menjawab!")
        
        # Placeholder untuk video
        video_placeholder = st.empty()
        
        # ===== KONTROL KAMERA =====
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            start_camera = st.button("📷 Mulai Kamera", use_container_width=True)
        with col2:
            stop_camera = st.button("⏹️ Stop Kamera", use_container_width=True)
        with col3:
            detect_btn = st.button("🔍 Deteksi Jari", use_container_width=True, type="primary")
        with col4:
            if st.button("🔄 Soal Baru", use_container_width=True):
                a, b, jawaban = generate_soal(level)
                st.session_state.jarimatika_a = a
                st.session_state.jarimatika_b = b
                st.session_state.jarimatika_jawaban = jawaban
                st.session_state.jarimatika_feedback = None
                st.rerun()
        
        # ===== PROSES KAMERA =====
        if start_camera:
            st.session_state.jarimatika_camera_active = True
        
        if stop_camera:
            st.session_state.jarimatika_camera_active = False
        
        if st.session_state.get("jarimatika_camera_active", False):
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    st.error("❌ Tidak dapat membuka kamera. Pastikan kamera terhubung.")
                    st.session_state.jarimatika_camera_active = False
                else:
                    ret, frame = cap.read()
                    cap.release()
                    
                    if ret:
                        frame = cv2.flip(frame, 1)
                        fingers, annotated_frame = detect_fingers_from_frame(frame)
                        
                        # Konversi ke RGB untuk Streamlit
                        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(annotated_frame_rgb)
                        video_placeholder.image(image, caption="Deteksi Jari", use_container_width=True)
                        
                        # Tampilkan jumlah jari yang terdeteksi
                        st.info(f"🖐️ Jari terdeteksi: {fingers}")
                        
                        # Auto-detect jika tombol ditekan atau setiap detik
                        if detect_btn:
                            process_jarimatika_answer(fingers)
                    else:
                        st.warning("⚠️ Gagal mengambil gambar dari kamera.")
                        st.session_state.jarimatika_camera_active = False
            except Exception as e:
                logging.error(f"Error camera: {e}")
                st.error(f"Error kamera: {e}")
                st.session_state.jarimatika_camera_active = False
        else:
            # Tampilkan placeholder jika kamera tidak aktif
            video_placeholder.info("🖐️ Klik 'Mulai Kamera' untuk mengaktifkan kamera")
        
        # ===== FEEDBACK =====
        if st.session_state.jarimatika_feedback:
            if "✅" in st.session_state.jarimatika_feedback:
                st.success(st.session_state.jarimatika_feedback)
            else:
                st.error(st.session_state.jarimatika_feedback)
        
        # ===== STATISTIK =====
        st.markdown("---")
        st.markdown("### 📊 Statistik")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Total Soal", st.session_state.jarimatika_total)
        with col2:
            st.metric("✅ Benar", st.session_state.jarimatika_benar)
        with col3:
            akurasi = (st.session_state.jarimatika_benar / st.session_state.jarimatika_total * 100) if st.session_state.jarimatika_total > 0 else 0
            st.metric("🎯 Akurasi", f"{akurasi:.1f}%")
        
        # ===== TOMBOL RESET =====
        if st.button("🔄 Reset Permainan", use_container_width=True):
            reset_jarimatika()
            st.rerun()
        
        # ===== PANDUAN =====
        with st.expander("📖 Panduan Jarimatika"):
            st.markdown("""
            ### 🖐️ Cara Menggunakan Jarimatika dengan Kamera
            
            1. **Siapkan Kamera** – Klik tombol "Mulai Kamera"
            2. **Tunjukkan Jari** – Angkat jari sesuai angka yang ingin ditunjukkan
            3. **Deteksi** – Klik "Deteksi Jari" atau tunggu auto-detect
            4. **Jawab Soal** – Jumlah jari yang terdeteksi akan menjadi jawaban
            
            ### 💡 Tips
            
            - Pastikan kamera menghadap tangan Anda dengan jelas
            - Gunakan latar belakang yang terang
            - Angkat jari dengan jelas agar terdeteksi dengan baik
            - Untuk angka 0, tutup semua jari (tinju)
            
            ### 🔢 Contoh
            
            - Soal: 3 × 4 = ?
            - Tunjukkan 12 jari (atau 1 jari + 2 jari)
            - Deteksi jari akan membaca 12
            - Jawaban: 12 ✅
            """)
        
    except Exception as e:
        logging.error(f"Error di show_jarimatika: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Jarimatika: {e}")
        st.exception(e)

def show_jarimatika_manual():
    """Mode manual Jarimatika tanpa kamera (fallback)."""
    st.markdown("### 🧮 Mode Manual (Tanpa Kamera)")
    
    # ===== PILIH LEVEL =====
    level = st.selectbox(
        "📊 Level Kesulitan",
        ["Mudah", "Sedang", "Sulit"],
        key="jarimatika_manual_level"
    )
    
    # ===== GENERATE SOAL =====
    if st.button("🎲 Soal Baru", key="jarimatika_manual_new"):
        a, b, jawaban = generate_soal(level)
        st.session_state.jarimatika_a = a
        st.session_state.jarimatika_b = b
        st.session_state.jarimatika_jawaban = jawaban
        st.session_state.jarimatika_feedback = None
        st.rerun()
    
    if st.session_state.jarimatika_a is not None and st.session_state.jarimatika_b is not None:
        st.markdown(f"### 📝 {st.session_state.jarimatika_a} × {st.session_state.jarimatika_b} = ?")
        
        # Input jawaban manual
        jawaban_user = st.number_input(
            "Masukkan jawaban Anda:",
            min_value=0,
            max_value=100,
            step=1,
            key="jarimatika_manual_input"
        )
        
        if st.button("✅ Jawab", key="jarimatika_manual_submit"):
            process_jarimatika_answer(jawaban_user)
            st.rerun()
        
        if st.session_state.jarimatika_feedback:
            if "✅" in st.session_state.jarimatika_feedback:
                st.success(st.session_state.jarimatika_feedback)
            else:
                st.error(st.session_state.jarimatika_feedback)
    else:
        st.info("Klik 'Soal Baru' untuk memulai!")

def process_jarimatika_answer(jawaban_user):
    """Memproses jawaban pengguna."""
    try:
        jawaban_benar = st.session_state.jarimatika_jawaban
        
        if jawaban_user == jawaban_benar:
            st.session_state.jarimatika_skor += 10
            st.session_state.jarimatika_benar += 1
            st.session_state.jarimatika_feedback = f"✅ BENAR! Jawabannya adalah {jawaban_benar}. +10 poin!"
            st.balloons()
        else:
            st.session_state.jarimatika_feedback = f"❌ SALAH! Jawaban yang benar adalah {jawaban_benar}."
        
        st.session_state.jarimatika_total += 1
        
        # Generate soal baru
        level = st.session_state.jarimatika_level
        a, b, jawaban = generate_soal(level)
        st.session_state.jarimatika_a = a
        st.session_state.jarimatika_b = b
        st.session_state.jarimatika_jawaban = jawaban
        
        logging.info(f"Jarimatika: {st.session_state.jarimatika_total} soal, {st.session_state.jarimatika_benar} benar")
        
    except Exception as e:
        logging.error(f"Error process_jarimatika_answer: {e}")
        st.session_state.jarimatika_feedback = f"❌ Error: {e}"

if __name__ == "__main__":
    show_jarimatika()