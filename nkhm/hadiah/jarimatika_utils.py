# nkhm/hadiah/jarimatika_utils.py
"""
Utilitas untuk deteksi jari menggunakan MediaPipe dan OpenCV.
"""

import cv2
import numpy as np
import mediapipe as mp
import logging

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== INISIALISASI MEDIAPIPE ==========
try:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    MEDIAPIPE_AVAILABLE = True
    logging.info("✅ MediaPipe tersedia")
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logging.warning("⚠️ MediaPipe tidak terinstall. Install dengan: pip install mediapipe")

# ========== KONFIGURASI ==========
# ID jari di MediaPipe
FINGER_TIPS = [4, 8, 12, 16, 20]  # Ibu jari, Telunjuk, Tengah, Manis, Kelingking
FINGER_PIP = [3, 6, 10, 14, 18]   # Sendi bawah jari

# Nama jari
FINGER_NAMES = ["Ibu Jari", "Telunjuk", "Tengah", "Manis", "Kelingking"]

def count_fingers(hand_landmarks):
    """
    Menghitung jumlah jari yang terangkat dari landmark tangan.
    
    Args:
        hand_landmarks: Landmark tangan dari MediaPipe
    
    Returns:
        int: Jumlah jari yang terangkat
    """
    try:
        if not hand_landmarks:
            return 0
        
        fingers = []
        landmarks = hand_landmarks.landmark
        
        # Ibu jari (deteksi berdasarkan posisi x)
        # Ibu jari terangkat jika tip x < pip x (untuk tangan kanan) atau sebaliknya
        thumb_tip = landmarks[FINGER_TIPS[0]].x
        thumb_pip = landmarks[FINGER_PIP[0]].x
        # Untuk tangan kanan: ibu jari terangkat jika tip < pip
        # Untuk tangan kiri: ibu jari terangkat jika tip > pip
        # Kita deteksi berdasarkan posisi relatif
        if thumb_tip < thumb_pip - 0.02:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # 4 jari lainnya (deteksi berdasarkan posisi y)
        for i in range(1, 5):
            tip = landmarks[FINGER_TIPS[i]].y
            pip = landmarks[FINGER_PIP[i]].y
            if tip < pip - 0.02:  # Jari terangkat jika tip lebih tinggi dari pip
                fingers.append(1)
            else:
                fingers.append(0)
        
        return sum(fingers)
        
    except Exception as e:
        logging.error(f"Error count_fingers: {e}")
        return 0

def detect_fingers_from_frame(frame):
    """
    Mendeteksi jari dari frame video.
    
    Args:
        frame: Gambar dari kamera (numpy array)
    
    Returns:
        tuple: (jumlah_jari, annotated_frame)
    """
    if not MEDIAPIPE_AVAILABLE:
        return 0, frame
    
    try:
        # Konversi BGR ke RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            results = hands.process(rgb_frame)
            
            annotated_frame = frame.copy()
            total_fingers = 0
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Gambar landmark tangan
                    mp_drawing.draw_landmarks(
                        annotated_frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Hitung jari yang terangkat
                    fingers = count_fingers(hand_landmarks)
                    total_fingers += fingers
                    
                    # Tampilkan jumlah jari di frame
                    cv2.putText(
                        annotated_frame,
                        f"Jari: {fingers}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )
            
            # Tampilkan total jari di frame
            if results.multi_hand_landmarks:
                cv2.putText(
                    annotated_frame,
                    f"Total Jari: {total_fingers}",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )
            
            return total_fingers, annotated_frame
            
    except Exception as e:
        logging.error(f"Error detect_fingers_from_frame: {e}")
        return 0, frame

def process_webcam():
    """
    Generator untuk memproses webcam secara real-time.
    
    Yields:
        tuple: (jumlah_jari, annotated_frame)
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logging.error("Tidak dapat membuka webcam")
        yield 0, None
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame secara horizontal untuk mirror effect
            frame = cv2.flip(frame, 1)
            
            fingers, annotated_frame = detect_fingers_from_frame(frame)
            yield fingers, annotated_frame
            
    except Exception as e:
        logging.error(f"Error process_webcam: {e}")
    finally:
        cap.release()