# nkhm/hadiah/jarimatika.py
"""
Fitur Jarimatika PMD (Pedang Mata Dua) - Perkalian 6-10.
Menggunakan logika perhitungan jari tanpa memerlukan OpenCV/MediaPipe.
"""

import streamlit as st
import random
import logging
from datetime import datetime

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== KONFIGURASI ==========
FINGER_NAMES = ["Kelingking", "Manis", "Tengah", "Telunjuk", "Jempol"]

# ========== FUNGSI PERHITUNGAN JARIMATIKA PMD ==========
def hitung_jarimatika(num1, num2):
    """Menghitung perkalian menggunakan metode Jarimatika PMD."""
    try:
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
            "num1": num1,
            "num2": num2,
            "finger1": finger1,
            "finger2": finger2,
            "idx1": idx1,
            "idx2": idx2,
            "bawah_kiri": bawah_kiri,
            "bawah_kanan": bawah_kanan,
            "atas_kiri": atas_kiri,
            "atas_kanan": atas_kanan,
            "total_bawah": total_bawah,
            "total_atas": total_atas,
            "hasil": hasil
        }
    except Exception as e:
        logging.error(f"Error hitung_jarimatika: {e}")
        return None

def generate_soal():
    """Menghasilkan soal perkalian acak 6-10."""
    try:
        a = random.randint(6, 10)
        b = random.randint(6, 10)
        return a, b
    except Exception as e:
        logging.error(f"Error generate_soal: {e}")
        return 6, 6

def get_jari_visualisasi(angka, tangan="kiri"):
    """Mendapatkan visualisasi jari untuk angka tertentu."""
    try:
        idx = angka - 6
        jari_bawah = idx + 1
        jari_atas = 5 - jari_bawah
        
        jari_nama = ["Kelingking", "Manis", "Tengah", "Telunjuk", "Jempol"]
        
        visual = []
        for i in range(5):
            if i < jari_bawah:
                visual.append(f"🟢 {jari_nama[i]}")
            else:
                visual.append(f"🔴 {jari_nama[i]}")
        
        return {
            "jari_bawah": jari_bawah,
            "jari_atas": jari_atas,
            "visual": visual,
            "tangan": tangan
        }
    except Exception as e:
        logging.error(f"Error get_jari_visualisasi: {e}")
        return {"jari_bawah": 0, "jari_atas": 0, "visual": [], "tangan": tangan}

# ========== INIT STATE ==========
def init_jarimatika_state():
    """Inisialisasi session state untuk Jarimatika."""
    try:
        if "jarimatika_a" not in st.session_state:
            st.session_state.jarimatika_a = None
        if "jarimatika_b" not in st.session_state:
            st.session_state.jarimatika_b = None
        if "jarimatika_hasil" not in st.session_state:
            st.session_state.jarimatika_hasil = None
        if "jarimatika_skor" not in st.session_state:
            st.session_state.jarimatika_skor = 0
        if "jarimatika_total" not in st.session_state:
            st.session_state.jarimatika_total = 0
        if "jarimatika_benar" not in st.session_state:
            st.session_state.jarimatika_benar = 0
        if "jarimatika_feedback" not in st.session_state:
            st.session_state.jarimatika_feedback = None
        if "jarimatika_detail" not in st.session_state:
            st.session_state.jarimatika_detail = None
        if "jarimatika_soal_aktif" not in st.session_state:
            st.session_state.jarimatika_soal_aktif = False
        if "jarimatika_history" not in st.session_state:
            st.session_state.jarimatika_history = []
        if "jarimatika_level" not in st.session_state:
            st.session_state.jarimatika_level = "Mudah"
        if "jarimatika_counter" not in st.session_state:
            st.session_state.jarimatika_counter = 0
    except Exception as e:
        logging.error(f"Error init_jarimatika_state: {e}")

def reset_jarimatika():
    """Reset semua state Jarimatika."""
    try:
        st.session_state.jarimatika_a = None
        st.session_state.jarimatika_b = None
        st.session_state.jarimatika_hasil = None
        st.session_state.jarimatika_skor = 0
        st.session_state.jarimatika_total = 0
        st.session_state.jarimatika_benar = 0
        st.session_state.jarimatika_feedback = None
        st.session_state.jarimatika_detail = None
        st.session_state.jarimatika_soal_aktif = False
        st.session_state.jarimatika_history = []
        st.session_state.jarimatika_counter += 1
        logging.info("Jarimatika state direset")
    except Exception as e:
        logging.error(f"Error reset_jarimatika: {e}")

# ========== FUNGSI UTAMA ==========
def show_jarimatika():
    """Menampilkan fitur Jarimatika PMD."""
    try:
        init_jarimatika_state()
        
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
                    <div style="font-size: 18px; font-weight: bold;">JARIMATIKA PMD</div>
                    <div style="font-size: 14px; opacity: 0.9;">
                        Perkalian Angka 6-10 dengan Jari Tangan | Pedang Mata Dua
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ===== TAB =====
        tab1, tab2, tab3 = st.tabs(["🧮 Latihan", "📖 Panduan", "📊 Riwayat"])
        
        with tab1:
            show_jarimatika_latihan()
        
        with tab2:
            show_jarimatika_panduan()
        
        with tab3:
            show_jarimatika_riwayat()
        
    except Exception as e:
        logging.error(f"Error di show_jarimatika: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Jarimatika: {e}")
        st.exception(e)

def show_jarimatika_latihan():
    """Menampilkan mode latihan Jarimatika."""
    try:
        # ===== PILIH LEVEL =====
        col1, col2, col3 = st.columns(3)
        with col1:
            level = st.selectbox(
                "📊 Level",
                ["Mudah (6-7)", "Sedang (6-9)", "Sulit (6-10)"],
                key="jarimatika_level_select"
            )
            # Update level di session state
            level_key = level.split()[0]  # "Mudah", "Sedang", "Sulit"
            if st.session_state.jarimatika_level != level_key:
                st.session_state.jarimatika_level = level_key
                st.session_state.jarimatika_soal_aktif = False
        
        with col2:
            st.metric("🏆 Skor", st.session_state.jarimatika_skor)
        
        with col3:
            total = st.session_state.jarimatika_total
            benar = st.session_state.jarimatika_benar
            akurasi = (benar / total * 100) if total > 0 else 0
            st.metric("🎯 Akurasi", f"{akurasi:.0f}%")
        
        # ===== GENERATE SOAL =====
        if not st.session_state.jarimatika_soal_aktif:
            # Tentukan rentang berdasarkan level
            level_name = st.session_state.jarimatika_level
            if level_name == "Mudah":
                range_min, range_max = 6, 7
            elif level_name == "Sedang":
                range_min, range_max = 6, 9
            else:
                range_min, range_max = 6, 10
            
            a = random.randint(range_min, range_max)
            b = random.randint(range_min, range_max)
            st.session_state.jarimatika_a = a
            st.session_state.jarimatika_b = b
            st.session_state.jarimatika_soal_aktif = True
            st.session_state.jarimatika_detail = None
        
        # ===== TAMPILKAN SOAL =====
        if st.session_state.jarimatika_a is not None:
            a = st.session_state.jarimatika_a
            b = st.session_state.jarimatika_b
            
            st.markdown("---")
            st.markdown(f"### 📝 {a} × {b} = ?")
            
            # ===== VISUALISASI JARI =====
            col_jari1, col_jari2 = st.columns(2)
            
            with col_jari1:
                st.markdown(f"**👈 Tangan Kiri ({a})**")
                vis_kiri = get_jari_visualisasi(a, "kiri")
                for item in vis_kiri["visual"]:
                    st.markdown(f"- {item}")
                st.caption(f"Jari bawah: {vis_kiri['jari_bawah']} | Jari atas: {vis_kiri['jari_atas']}")
            
            with col_jari2:
                st.markdown(f"**👉 Tangan Kanan ({b})**")
                vis_kanan = get_jari_visualisasi(b, "kanan")
                for item in vis_kanan["visual"]:
                    st.markdown(f"- {item}")
                st.caption(f"Jari bawah: {vis_kanan['jari_bawah']} | Jari atas: {vis_kanan['jari_atas']}")
            
            st.markdown("---")
            
            # ===== INPUT JAWABAN =====
            col_input1, col_input2, col_input3 = st.columns([2, 1, 2])
            with col_input2:
                # Unique key untuk input
                input_key = f"jarimatika_input_{st.session_state.jarimatika_counter}"
                jawaban_user = st.number_input(
                    "Masukkan jawaban:",
                    min_value=0,
                    max_value=100,
                    step=1,
                    key=input_key
                )
                
                # Unique key untuk tombol Jawab
                btn_key = f"jawab_btn_{st.session_state.jarimatika_counter}_{a}_{b}"
                if st.button("✅ Jawab", key=btn_key, use_container_width=True, type="primary"):
                    proses_jawaban_jarimatika(a, b, jawaban_user)
                    st.rerun()
            
            # ===== TAMPILKAN DETAIL PERHITUNGAN =====
            if st.session_state.jarimatika_detail:
                detail = st.session_state.jarimatika_detail
                
                with st.expander("📊 Lihat Langkah Perhitungan", expanded=True):
                    st.markdown("### 🔢 Langkah-langkah Jarimatika PMD")
                    
                    col_step1, col_step2 = st.columns(2)
                    with col_step1:
                        st.markdown(f"""
                        **1. Identifikasi Jari:**
                        - {detail['num1']} = Jari **{detail['finger1']}** (tangan kiri)
                        - {detail['num2']} = Jari **{detail['finger2']}** (tangan kanan)
                        """)
                        
                        st.markdown(f"""
                        **2. Jari Bawah (dijumlahkan):**
                        - Tangan kiri: {detail['bawah_kiri']} jari
                        - Tangan kanan: {detail['bawah_kanan']} jari
                        - Total: {detail['bawah_kiri']} + {detail['bawah_kanan']} = **{detail['total_bawah']}** (puluhan)
                        """)
                    
                    with col_step2:
                        st.markdown(f"""
                        **3. Jari Atas (dikalikan):**
                        - Tangan kiri: {detail['atas_kiri']} jari
                        - Tangan kanan: {detail['atas_kanan']} jari
                        - Total: {detail['atas_kiri']} × {detail['atas_kanan']} = **{detail['total_atas']}** (satuan)
                        """)
                        
                        st.markdown(f"""
                        **4. Hasil Akhir:**
                        - Puluhan: {detail['total_bawah']}
                        - Satuan: {detail['total_atas']}
                        - **{detail['num1']} × {detail['num2']} = {detail['hasil']}** ✅
                        """)
                    
                    st.success(f"🎯 **Hasil: {detail['num1']} × {detail['num2']} = {detail['hasil']}**")
            
            # ===== TOMBOL SOAL BARU =====
            st.markdown("---")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                # Unique key untuk tombol soal baru
                new_btn_key = f"soal_baru_btn_{st.session_state.jarimatika_counter}"
                if st.button("🎲 Soal Baru", key=new_btn_key, use_container_width=True):
                    st.session_state.jarimatika_soal_aktif = False
                    st.session_state.jarimatika_detail = None
                    st.session_state.jarimatika_feedback = None
                    st.session_state.jarimatika_counter += 1
                    st.rerun()
            
            with col_btn2:
                # Unique key untuk tombol reset
                reset_btn_key = f"reset_btn_{st.session_state.jarimatika_counter}"
                if st.button("🔄 Reset Permainan", key=reset_btn_key, use_container_width=True):
                    reset_jarimatika()
                    st.rerun()
        
        # ===== TAMPILKAN FEEDBACK =====
        if st.session_state.jarimatika_feedback:
            if "✅" in st.session_state.jarimatika_feedback:
                st.success(st.session_state.jarimatika_feedback)
            else:
                st.error(st.session_state.jarimatika_feedback)
                
    except Exception as e:
        logging.error(f"Error show_jarimatika_latihan: {e}")
        st.error(f"Error: {e}")

def proses_jawaban_jarimatika(a, b, jawaban_user):
    """Memproses jawaban pengguna."""
    try:
        detail = hitung_jarimatika(a, b)
        
        if detail is None:
            st.session_state.jarimatika_feedback = "❌ Error perhitungan. Coba lagi."
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
        
    except Exception as e:
        logging.error(f"Error proses_jawaban_jarimatika: {e}")
        st.session_state.jarimatika_feedback = f"❌ Error: {e}"

def show_jarimatika_panduan():
    """Menampilkan panduan Jarimatika PMD."""
    st.markdown("## 📖 Panduan Jarimatika PMD")
    
    with st.expander("🎯 Apa itu Jarimatika PMD?", expanded=True):
        st.markdown("""
        **JARIMATIKA PMD (Pedang Mata Dua)** adalah metode berhitung perkalian 
        menggunakan jari-jari tangan untuk angka **6-10**.
        
        **Konsep Dasar:**
        - Setiap jari mewakili angka tertentu
        - Jari bawah dijumlahkan → **puluhan**
        - Jari atas dikalikan → **satuan**
        """)
    
    with st.expander("🖐️ Representasi Jari", expanded=True):
        st.markdown("""
        | Jari | Angka | Posisi |
        |------|-------|--------|
        | Kelingking | 6 | Terbawah |
        | Manis | 7 | Kedua |
        | Tengah | 8 | Ketiga |
        | Telunjuk | 9 | Keempat |
        | Jempol | 10 | Teratas |
        """)
        
        st.markdown("**Visualisasi dari bawah ke atas:**")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown("🟢 Kelingking\n6")
        with col2:
            st.markdown("🟢 Manis\n7")
        with col3:
            st.markdown("🟢 Tengah\n8")
        with col4:
            st.markdown("🟢 Telunjuk\n9")
        with col5:
            st.markdown("🟢 Jempol\n10")
    
    with st.expander("📝 Contoh Perhitungan 7 × 8", expanded=True):
        st.markdown("""
        **Langkah 1: Identifikasi Jari**
        - 7 = Jari **Manis** (tangan kiri)
        - 8 = Jari **Tengah** (tangan kanan)
        
        **Langkah 2: Jari Bawah (dijumlahkan)**
        - Tangan kiri (Manis): 2 jari ke bawah
        - Tangan kanan (Tengah): 3 jari ke bawah
        - Total: 2 + 3 = **5** (puluhan)
        
        **Langkah 3: Jari Atas (dikalikan)**
        - Tangan kiri: 3 jari ke atas
        - Tangan kanan: 2 jari ke atas
        - Total: 3 × 2 = **6** (satuan)
        
        **Langkah 4: Hasil Akhir**
        - Puluhan: 5
        - Satuan: 6
        - **7 × 8 = 56** ✅
        """)
    
    with st.expander("💡 Tips Menggunakan Jarimatika"):
        st.markdown("""
        1. **Pahami representasi jari** – Hafalkan angka setiap jari
        2. **Latihan rutin** – Semakin sering berlatih, semakin cepat
        3. **Gunakan kedua tangan** – Kiri untuk angka pertama, kanan untuk angka kedua
        4. **Perhatikan posisi** – Jari bawah dijumlahkan, jari atas dikalikan
        """)

def show_jarimatika_riwayat():
    """Menampilkan riwayat permainan Jarimatika."""
    st.markdown("## 📊 Riwayat Permainan")
    
    if not st.session_state.jarimatika_history:
        st.info("Belum ada riwayat. Mulai latihan Jarimatika!")
        return
    
    total = len(st.session_state.jarimatika_history)
    benar = sum(1 for h in st.session_state.jarimatika_history if h["benar"])
    akurasi = (benar / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Total Soal", total)
    with col2:
        st.metric("✅ Benar", benar)
    with col3:
        st.metric("🎯 Akurasi", f"{akurasi:.0f}%")
    
    st.markdown("---")
    
    import pandas as pd
    df = pd.DataFrame(st.session_state.jarimatika_history[-20:])
    df = df[["timestamp", "soal", "jawaban_user", "jawaban_benar", "benar"]]
    df["benar"] = df["benar"].map({True: "✅", False: "❌"})
    df.columns = ["Waktu", "Soal", "Jawaban Anda", "Jawaban Benar", "Status"]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    show_jarimatika()