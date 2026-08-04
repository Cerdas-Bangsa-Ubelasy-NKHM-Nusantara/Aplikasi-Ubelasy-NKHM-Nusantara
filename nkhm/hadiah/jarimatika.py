# nkhm/hadiah/jarimatika.py
"""
JARIMATIKA PMD – Perkalian 6-10 dengan Jari Tangan
Mode: Manual (input angka) dan Kamera (deteksi jari via CV)
"""

import streamlit as st
import random
import logging
import numpy as np
from PIL import Image
from datetime import datetime

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== KONSTANTA ==========
FINGER_NAMES = ["Kelingking", "Manis", "Tengah", "Telunjuk", "Jempol"]
FINGER_TIPS = [4, 8, 12, 16, 20]
FINGER_PIP = [3, 6, 10, 14, 18]

# ========== CEK KETERSEDIAAN CV ==========
try:
    import cv2
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    CV_AVAILABLE = True
    logger.info("✅ OpenCV + MediaPipe tersedia")
except ImportError:
    CV_AVAILABLE = False
    logger.warning("⚠️ OpenCV/MediaPipe tidak terinstall.")

# ========== DETEKSI JARI ==========
def count_fingers_from_image(image):
    if not CV_AVAILABLE:
        return None, image
    try:
        if isinstance(image, Image.Image):
            image = np.array(image)
        if len(image.shape) == 3 and image.shape[2] == 3:
            rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            rgb = image
        with mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5
        ) as hands:
            results = hands.process(rgb)
            annotated = image.copy()
            total_fingers = 0
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    landmarks = hand_landmarks.landmark
                    fingers = 0
                    thumb_tip = landmarks[FINGER_TIPS[0]].x
                    thumb_ip = landmarks[FINGER_PIP[0]].x
                    if thumb_tip < thumb_ip - 0.02:
                        fingers += 1
                    for i in range(1, 5):
                        tip = landmarks[FINGER_TIPS[i]].y
                        pip = landmarks[FINGER_PIP[i]].y
                        if tip < pip - 0.02:
                            fingers += 1
                    total_fingers += fingers
            return total_fingers, annotated
    except Exception as e:
        logger.error(f"Error count_fingers: {e}")
        return None, image

# ========== PERHITUNGAN JARIMATIKA ==========
def hitung_jarimatika(num1, num2):
    idx1 = num1 - 6
    idx2 = num2 - 6
    finger1 = FINGER_NAMES[idx1]
    finger2 = FINGER_NAMES[idx2]
    bawah_kiri = idx1 + 1
    bawah_kanan = idx2 + 1
    atas_kiri = 5 - bawah_kiri
    atas_kanan = 5 - bawah_kanan
    total_bawah = bawah_kiri + bawah_kanan
    total_atas = atas_kiri * atas_kanan
    hasil = total_bawah * 10 + total_atas
    return {
        "num1": num1, "num2": num2,
        "finger1": finger1, "finger2": finger2,
        "bawah_kiri": bawah_kiri, "bawah_kanan": bawah_kanan,
        "atas_kiri": atas_kiri, "atas_kanan": atas_kanan,
        "total_bawah": total_bawah, "total_atas": total_atas,
        "hasil": hasil
    }

def get_jari_visualisasi(angka):
    idx = angka - 6
    jari_bawah = idx + 1
    visual = []
    for i in range(5):
        if i < jari_bawah:
            visual.append(f"🟢 {FINGER_NAMES[i]}")
        else:
            visual.append(f"🔴 {FINGER_NAMES[i]}")
    return visual

def generate_soal(level="Mudah"):
    levels = {"Mudah": (6,7), "Sedang": (6,9), "Sulit": (6,10)}
    min_v, max_v = levels.get(level, (6,7))
    return random.randint(min_v, max_v), random.randint(min_v, max_v)

# ========== STATE ==========
def init_state():
    defaults = {
        "jarimatika_a": None,
        "jarimatika_b": None,
        "jarimatika_skor": 0,
        "jarimatika_total": 0,
        "jarimatika_benar": 0,
        "jarimatika_feedback": None,
        "jarimatika_detail": None,
        "jarimatika_soal_aktif": False,
        "jarimatika_history": [],
        "jarimatika_level": "Mudah",
        "jarimatika_counter": 0,
        "jarimatika_mode": "Manual",
        "jarimatika_detected_fingers": None,
        "jarimatika_annotated_image": None,
        "jarimatika_initialized": True,   # <-- flag inisialisasi
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_state():
    for key in ["jarimatika_a", "jarimatika_b", "jarimatika_feedback", "jarimatika_detail"]:
        st.session_state[key] = None
    st.session_state.jarimatika_skor = 0
    st.session_state.jarimatika_total = 0
    st.session_state.jarimatika_benar = 0
    st.session_state.jarimatika_soal_aktif = False
    st.session_state.jarimatika_history = []
    st.session_state.jarimatika_counter += 1
    st.session_state.jarimatika_detected_fingers = None
    st.session_state.jarimatika_annotated_image = None

# ========== UI UTAMA ==========
def show_jarimatika():
    init_state()  # Pastikan state diinisialisasi

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a3c6e 0%, #2e7daf 100%);
                padding: 15px 20px; border-radius: 12px; color: white; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 40px;">🖐️</div>
            <div>
                <div style="font-size: 18px; font-weight: bold;">JARIMATIKA PMD</div>
                <div style="font-size: 14px; opacity: 0.9;">
                    Perkalian 6-10 dengan Jari Tangan – Manual / Kamera
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🧮 Latihan", "📖 Panduan", "📊 Riwayat"])
    with tab1:
        show_latihan()
    with tab2:
        show_panduan()
    with tab3:
        show_riwayat()

# ========== LATIHAN ==========
def show_latihan():
    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            mode = st.radio("Pilih Mode", ["✍️ Manual", "📷 Kamera"], horizontal=True, key="jarimatika_mode_select")
            st.session_state.jarimatika_mode = mode
        with col2:
            level = st.selectbox("Level", ["Mudah (6-7)", "Sedang (6-9)", "Sulit (6-10)"], key="jarimatika_level_select")
            level_key = level.split()[0]
            if st.session_state.jarimatika_level != level_key:
                st.session_state.jarimatika_level = level_key
                st.session_state.jarimatika_soal_aktif = False
        with col3:
            st.metric("🏆 Skor", st.session_state.jarimatika_skor)
            total = st.session_state.jarimatika_total
            benar = st.session_state.jarimatika_benar
            akurasi = (benar / total * 100) if total > 0 else 0
            st.caption(f"📊 Akurasi: {akurasi:.0f}%")

        # ===== GENERATE SOAL =====
        if not st.session_state.jarimatika_soal_aktif:
            a, b = generate_soal(st.session_state.jarimatika_level)
            st.session_state.jarimatika_a = a
            st.session_state.jarimatika_b = b
            st.session_state.jarimatika_soal_aktif = True
            st.session_state.jarimatika_detail = None
            st.session_state.jarimatika_detected_fingers = None
            st.session_state.jarimatika_annotated_image = None

        a = st.session_state.jarimatika_a
        b = st.session_state.jarimatika_b

        st.markdown("---")
        st.markdown(f"### 📝 {a} × {b} = ?")

        # ===== VISUALISASI JARI =====
        col_ref1, col_ref2 = st.columns(2)
        with col_ref1:
            st.markdown(f"**👈 Tangan Kiri ({a})**")
            for item in get_jari_visualisasi(a):
                st.markdown(f"- {item}")
        with col_ref2:
            st.markdown(f"**👉 Tangan Kanan ({b})**")
            for item in get_jari_visualisasi(b):
                st.markdown(f"- {item}")

        st.markdown("---")

        # ===== MODE MANUAL (dengan form) =====
        if st.session_state.jarimatika_mode == "✍️ Manual":
            with st.form(key="manual_form"):
                jawaban_user = st.number_input("Masukkan jawaban:", min_value=0, max_value=100, step=1, key=f"manual_input_{st.session_state.jarimatika_counter}")
                submitted = st.form_submit_button("✅ Jawab", use_container_width=True, type="primary")
                if submitted:
                    proses_jawaban(a, b, jawaban_user)
                    # Tidak perlu st.rerun() karena form submit otomatis melakukan rerun

        # ===== MODE KAMERA =====
        else:
            if not CV_AVAILABLE:
                st.error("❌ OpenCV/MediaPipe tidak terinstall. Mode kamera tidak tersedia. Gunakan mode Manual.")
            else:
                st.markdown("#### 📷 Ambil Foto Jari Anda")
                cam_image = st.camera_input("Klik untuk mengambil foto", key=f"camera_{st.session_state.jarimatika_counter}")

                if cam_image is not None:
                    try:
                        img = Image.open(cam_image)
                        st.image(img, caption="Foto yang diambil", use_container_width=True)

                        with st.spinner("🔍 Mendeteksi jari..."):
                            fingers, annotated = count_fingers_from_image(img)
                            st.session_state.jarimatika_detected_fingers = fingers

                            if annotated is not None and isinstance(annotated, np.ndarray):
                                annotated_pil = Image.fromarray(annotated)
                                st.image(annotated_pil, caption="Hasil Deteksi Jari", use_container_width=True)

                        if fingers is not None:
                            st.info(f"🖐️ Jumlah jari terdeteksi: **{fingers}**")
                            # Gunakan form untuk tombol jawab CV
                            with st.form(key="cv_form"):
                                submitted_cv = st.form_submit_button("✅ Jawab dengan deteksi ini", use_container_width=True)
                                if submitted_cv:
                                    proses_jawaban(a, b, fingers)
                        else:
                            st.warning("Tidak ada tangan terdeteksi. Coba ambil foto lagi dengan tangan yang jelas.")
                    except Exception as e:
                        st.error(f"Error memproses gambar: {e}")
                        logger.error(f"CV error: {e}")

        # ===== TOMBOL SOAL BARU =====
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🎲 Soal Baru", key=f"new_soal_{st.session_state.jarimatika_counter}", use_container_width=True):
                st.session_state.jarimatika_soal_aktif = False
                st.session_state.jarimatika_feedback = None
                st.session_state.jarimatika_detail = None
                st.session_state.jarimatika_counter += 1
                st.rerun()   # Di sini kita tetap perlu rerun untuk mereset tampilan
        with col_btn2:
            if st.button("🔄 Reset Permainan", use_container_width=True):
                reset_state()
                st.rerun()

        # ===== FEEDBACK & DETAIL =====
        if st.session_state.jarimatika_feedback:
            if "✅" in st.session_state.jarimatika_feedback:
                st.success(st.session_state.jarimatika_feedback)
            else:
                st.error(st.session_state.jarimatika_feedback)

        if st.session_state.jarimatika_detail:
            with st.expander("📊 Lihat Langkah Perhitungan", expanded=True):
                d = st.session_state.jarimatika_detail
                st.markdown(f"""
                **1. Identifikasi Jari:**
                - {d['num1']} = Jari **{d['finger1']}** (tangan kiri)
                - {d['num2']} = Jari **{d['finger2']}** (tangan kanan)

                **2. Jari Bawah (dijumlahkan):**
                - {d['bawah_kiri']} + {d['bawah_kanan']} = **{d['total_bawah']}** (puluhan)

                **3. Jari Atas (dikalikan):**
                - {d['atas_kiri']} × {d['atas_kanan']} = **{d['total_atas']}** (satuan)

                **4. Hasil: {d['num1']} × {d['num2']} = {d['hasil']}** ✅
                """)

    except Exception as e:
        st.error(f"Error: {e}")
        logger.error(f"show_latihan: {e}")

# ========== PROSES JAWABAN ==========
def proses_jawaban(a, b, jawaban_user):
    try:
        detail = hitung_jarimatika(a, b)
        if detail is None:
            st.session_state.jarimatika_feedback = "❌ Error perhitungan"
            return
        st.session_state.jarimatika_detail = detail
        jawaban_benar = detail["hasil"]

        if jawaban_user == jawaban_benar:
            st.session_state.jarimatika_skor += 10
            st.session_state.jarimatika_benar += 1
            st.session_state.jarimatika_feedback = f"✅ BENAR! {a} × {b} = {jawaban_benar}. +10 poin! 🎉"
            st.balloons()
        else:
            st.session_state.jarimatika_feedback = f"❌ SALAH! Jawaban yang benar adalah {jawaban_benar}."

        st.session_state.jarimatika_total += 1
        st.session_state.jarimatika_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "soal": f"{a} × {b}",
            "jawaban_user": jawaban_user,
            "jawaban_benar": jawaban_benar,
            "benar": jawaban_user == jawaban_benar
        })
        st.session_state.jarimatika_counter += 1
        st.session_state.jarimatika_soal_aktif = False   # soal akan diganti di rerun
    except Exception as e:
        st.session_state.jarimatika_feedback = f"❌ Error: {e}"
        logger.error(f"proses_jawaban: {e}")

# ========== PANDUAN ==========
def show_panduan():
    st.markdown("## 📖 Panduan Jarimatika PMD")
    with st.expander("🎯 Apa itu Jarimatika PMD?", expanded=True):
        st.markdown("""
        **JARIMATIKA PMD (Pedang Mata Dua)** adalah metode perkalian angka 6-10 dengan jari tangan.

        **Konsep Dasar:**
        - Setiap jari mewakili angka tertentu
        - Jari bawah dijumlahkan → **puluhan**
        - Jari atas dikalikan → **satuan**
        """)
    with st.expander("🖐️ Representasi Jari", expanded=True):
        st.markdown("""
        | Jari | Angka |
        |------|-------|
        | Kelingking | 6 |
        | Manis | 7 |
        | Tengah | 8 |
        | Telunjuk | 9 |
        | Jempol | 10 |
        """)
    with st.expander("📷 Cara Pakai Kamera", expanded=True):
        st.markdown("""
        1. Pilih mode **Kamera**
        2. Tunjukkan jari tangan sesuai angka yang ingin ditampilkan
        3. Klik tombol kamera untuk mengambil foto
        4. Aplikasi akan mendeteksi jumlah jari
        5. Klik **"Jawab dengan deteksi ini"** untuk mengirim jawaban
        """)
    with st.expander("📝 Contoh 7 × 8", expanded=True):
        st.markdown("""
        - 7 = Manis (kiri) → 2 jari bawah, 3 jari atas
        - 8 = Tengah (kanan) → 3 jari bawah, 2 jari atas
        - Bawah: 2+3=5 (puluhan)
        - Atas: 3×2=6 (satuan)
        - Hasil = 56
        """)

# ========== RIWAYAT ==========
def show_riwayat():
    st.markdown("## 📊 Riwayat Permainan")
    if not st.session_state.jarimatika_history:
        st.info("Belum ada riwayat.")
        return
    total = len(st.session_state.jarimatika_history)
    benar = sum(1 for h in st.session_state.jarimatika_history if h["benar"])
    akurasi = (benar / total * 100) if total > 0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("📝 Total", total)
    col2.metric("✅ Benar", benar)
    col3.metric("🎯 Akurasi", f"{akurasi:.0f}%")
    st.markdown("---")
    import pandas as pd
    df = pd.DataFrame(st.session_state.jarimatika_history[-20:])
    df = df[["timestamp", "soal", "jawaban_user", "jawaban_benar", "benar"]]
    df["benar"] = df["benar"].map({True: "✅", False: "❌"})
    df.columns = ["Waktu", "Soal", "Jawaban", "Benar", "Status"]
    st.dataframe(df, use_container_width=True, hide_index=True)

# ========== ENTRY ==========
if __name__ == "__main__":
    show_jarimatika()