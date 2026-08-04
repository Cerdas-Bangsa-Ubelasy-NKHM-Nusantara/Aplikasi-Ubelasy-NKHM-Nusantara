# nkhm/misi.py
"""
Modul Misi & Tantangan untuk fitur Gamifikasi NKHM.
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== DATA MISI ==========
DAFTAR_MISI = [
    {
        "id": "misi_1",
        "nama": "🌱 Perintis Jalan",
        "deskripsi": "Selesaikan 10 soal pertama",
        "target": 10,
        "tipe": "total_soal",
        "reward": 5,
        "level": "pemula"
    },
    {
        "id": "misi_2",
        "nama": "📖 Penjelajah Ilmu",
        "deskripsi": "Selesaikan 50 soal",
        "target": 50,
        "tipe": "total_soal",
        "reward": 10,
        "level": "pemula"
    },
    {
        "id": "misi_3",
        "nama": "📚 Cendekia Muda",
        "deskripsi": "Selesaikan 100 soal",
        "target": 100,
        "tipe": "total_soal",
        "reward": 15,
        "level": "menengah"
    },
    {
        "id": "misi_4",
        "nama": "🌟 Pahlawan Cerdas",
        "deskripsi": "Selesaikan 200 soal",
        "target": 200,
        "tipe": "total_soal",
        "reward": 25,
        "level": "lanjutan"
    },
    {
        "id": "misi_5",
        "nama": "🎯 Akurasi 80%",
        "deskripsi": "Capai akurasi 80% (minimal 20 soal)",
        "target": 80,
        "tipe": "akurasi",
        "reward": 10,
        "level": "menengah"
    },
    {
        "id": "misi_6",
        "nama": "🏆 Akurasi 90%",
        "deskripsi": "Capai akurasi 90% (minimal 30 soal)",
        "target": 90,
        "tipe": "akurasi",
        "reward": 20,
        "level": "lanjutan"
    },
    {
        "id": "misi_7",
        "nama": "🧠 Master IQ",
        "deskripsi": "Skor IQ ≥ 80",
        "target": 80,
        "tipe": "skor_kategori",
        "kategori": "IQ",
        "reward": 15,
        "level": "menengah"
    },
    {
        "id": "misi_8",
        "nama": "❤️ Master EQ",
        "deskripsi": "Skor EQ ≥ 80",
        "target": 80,
        "tipe": "skor_kategori",
        "kategori": "EQ",
        "reward": 15,
        "level": "menengah"
    },
    {
        "id": "misi_9",
        "nama": "🙏 Master SQ",
        "deskripsi": "Skor SQ ≥ 80",
        "target": 80,
        "tipe": "skor_kategori",
        "kategori": "SQ",
        "reward": 15,
        "level": "menengah"
    },
    {
        "id": "misi_10",
        "nama": "💪 Master AQ",
        "deskripsi": "Skor AQ ≥ 80",
        "target": 80,
        "tipe": "skor_kategori",
        "kategori": "AQ",
        "reward": 15,
        "level": "menengah"
    },
    {
        "id": "misi_11",
        "nama": "🇮🇩 Patriot Sejati",
        "deskripsi": "Skor Nasionalisme ≥ 80",
        "target": 80,
        "tipe": "skor_kategori",
        "kategori": "Nasionalisme",
        "reward": 20,
        "level": "lanjutan"
    },
    {
        "id": "misi_12",
        "nama": "💎 NKHM 100",
        "deskripsi": "Capai NKHM Total 100",
        "target": 100,
        "tipe": "nkhm_total",
        "reward": 30,
        "level": "lanjutan"
    },
]

# ========== TANTANGAN HARIAN ==========
def get_tantangan_harian():
    """Menghasilkan tantangan harian berdasarkan hari."""
    try:
        today = datetime.now().date()
        day_of_week = today.weekday()
        
        tantangan_harian = [
            {"nama": "📝 Senin Cerdas", "deskripsi": "Kerjakan 10 soal hari ini!", "target": 10, "reward": 5},
            {"nama": "🧠 Selasa Analisis", "deskripsi": "Kerjakan 10 soal IQ hari ini!", "target": 10, "reward": 5},
            {"nama": "❤️ Rabu Empati", "deskripsi": "Kerjakan 10 soal EQ hari ini!", "target": 10, "reward": 5},
            {"nama": "🙏 Kamis Spiritual", "deskripsi": "Kerjakan 10 soal SQ hari ini!", "target": 10, "reward": 5},
            {"nama": "💪 Jumat Tangguh", "deskripsi": "Kerjakan 10 soal AQ hari ini!", "target": 10, "reward": 5},
            {"nama": "🇮🇩 Sabtu Patriot", "deskripsi": "Kerjakan 10 soal Nasionalisme hari ini!", "target": 10, "reward": 5},
            {"nama": "🏆 Minggu Juara", "deskripsi": "Kerjakan 15 soal hari ini!", "target": 15, "reward": 8},
        ]
        
        return tantangan_harian[day_of_week]
    except Exception as e:
        logging.error(f"Error get_tantangan_harian: {e}")
        return {"nama": "📝 Tantangan Hari Ini", "deskripsi": "Kerjakan 10 soal hari ini!", "target": 10, "reward": 5}

# ========== FUNGSI CEK MISI ==========
def cek_misi(history, scores, total_questions):
    """Mengecek progress misi berdasarkan data pengguna."""
    try:
        misi_status = []
        
        total_soal = len(history)
        benar = sum(1 for h in history if isinstance(h.get('correct'), bool) and h['correct'])
        akurasi = (benar / total_soal * 100) if total_soal > 0 else 0
        
        from nkhm.scoring import calculate_nkhm_q, calculate_nkhm_total
        nkhm_q = calculate_nkhm_q(
            scores.get('IQ', 0),
            scores.get('EQ', 0),
            scores.get('SQ', 0),
            scores.get('AQ', 0)
        )
        nkhm_total = calculate_nkhm_total(nkhm_q, scores.get('Nasionalisme', 0))
        
        for misi in DAFTAR_MISI:
            progress = 0
            selesai = False
            
            if misi["tipe"] == "total_soal":
                progress = min(100, (total_questions / misi["target"]) * 100)
                selesai = total_questions >= misi["target"]
                
            elif misi["tipe"] == "akurasi":
                if total_soal >= 20:
                    progress = min(100, (akurasi / misi["target"]) * 100)
                    selesai = akurasi >= misi["target"]
                else:
                    progress = 0
                    selesai = False
                    
            elif misi["tipe"] == "skor_kategori":
                kategori = misi.get("kategori", "")
                skor = scores.get(kategori, 0)
                progress = min(100, (skor / misi["target"]) * 100)
                selesai = skor >= misi["target"]
                
            elif misi["tipe"] == "nkhm_total":
                progress = min(100, (nkhm_total / misi["target"]) * 100)
                selesai = nkhm_total >= misi["target"]
            
            misi_status.append({
                "id": misi["id"],
                "nama": misi["nama"],
                "deskripsi": misi["deskripsi"],
                "progress": round(progress, 1),
                "selesai": selesai,
                "reward": misi["reward"],
                "level": misi.get("level", "pemula"),
                "tipe": misi["tipe"]
            })
        
        return misi_status
        
    except Exception as e:
        logging.error(f"Error cek_misi: {e}")
        return []

def get_statistik_misi(misi_status):
    """Menghitung statistik misi."""
    try:
        total = len(misi_status)
        selesai = sum(1 for m in misi_status if m["selesai"])
        progress = sum(m["progress"] for m in misi_status) / total if total > 0 else 0
        
        return {
            "total": total,
            "selesai": selesai,
            "progress": round(progress, 1),
            "persentase": round((selesai / total * 100) if total > 0 else 0, 1)
        }
    except Exception as e:
        logging.error(f"Error get_statistik_misi: {e}")
        return {"total": 0, "selesai": 0, "progress": 0, "persentase": 0}

def show_misi_dan_tantangan():
    """Menampilkan halaman Misi & Tantangan."""
    try:
        st.markdown("## 🎯 Misi & Tantangan")
        st.markdown("Selesaikan misi untuk mendapatkan poin reward dan naik level!")
        
        history = st.session_state.get("nkhm_history", [])
        scores = st.session_state.get("nkhm_scores", {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0})
        total_questions = st.session_state.get("nkhm_total_questions", 0)
        user_name = st.session_state.get("nkhm_user", "Pengguna")
        
        if not user_name or user_name == "Pengguna":
            st.info("👤 Login terlebih dahulu untuk melihat misi dan tantangan!")
            return
        
        # ===== TANTANGAN HARIAN =====
        st.markdown("### 📅 Tantangan Hari Ini")
        
        tantangan = get_tantangan_harian()
        
        today = datetime.now().date()
        today_questions = sum(1 for h in history if isinstance(h.get("timestamp"), str) and today.strftime("%Y-%m-%d") in h.get("timestamp", ""))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Target", f"{tantangan['target']} soal")
        with col2:
            st.metric("📊 Progress", f"{today_questions} soal")
        with col3:
            progress_pct = min(100, (today_questions / tantangan["target"]) * 100) if tantangan["target"] > 0 else 0
            st.metric("📈 Persentase", f"{progress_pct:.0f}%")
        
        st.progress(progress_pct / 100, text=f"{tantangan['nama']}: {today_questions}/{tantangan['target']} soal")
        
        if progress_pct >= 100:
            st.success(f"🎉 Selamat! Anda telah menyelesaikan tantangan hari ini! +{tantangan['reward']} poin reward!")
        else:
            st.info(f"💪 Kerjakan {max(0, tantangan['target'] - today_questions)} soal lagi untuk menyelesaikan tantangan hari ini!")
        
        st.markdown("---")
        
        # ===== STATISTIK MISI =====
        misi_status = cek_misi(history, scores, total_questions)
        statistik = get_statistik_misi(misi_status)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total Misi", statistik["total"])
        with col2:
            st.metric("✅ Selesai", statistik["selesai"])
        with col3:
            st.metric("📈 Progress", f"{statistik['persentase']}%")
        with col4:
            total_reward = sum(m["reward"] for m in misi_status if m["selesai"])
            st.metric("🏆 Total Reward", total_reward)
        
        st.markdown("---")
        
        # ===== DAFTAR MISI =====
        st.markdown("### 📋 Daftar Misi")
        
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            filter_level = st.selectbox(
                "Filter Level:",
                ["Semua", "pemula", "menengah", "lanjutan"],
                format_func=lambda x: {
                    "Semua": "✨ Semua Level",
                    "pemula": "🌱 Pemula",
                    "menengah": "📚 Menengah",
                    "lanjutan": "🌟 Lanjutan"
                }.get(x, x)
            )
        
        with col_filter2:
            filter_status = st.selectbox(
                "Filter Status:",
                ["Semua", "Belum Selesai", "Selesai"],
                format_func=lambda x: {
                    "Semua": "📋 Semua Status",
                    "Belum Selesai": "⏳ Belum Selesai",
                    "Selesai": "✅ Selesai"
                }.get(x, x)
            )
        
        # Tampilkan misi
        for misi in misi_status:
            if filter_level != "Semua" and misi["level"] != filter_level:
                continue
            if filter_status == "Belum Selesai" and misi["selesai"]:
                continue
            if filter_status == "Selesai" and not misi["selesai"]:
                continue
            
            status_icon = "✅" if misi["selesai"] else "⏳"
            status_color = "#28a745" if misi["selesai"] else "#fd7e14"
            
            level_icon = {"pemula": "🌱", "menengah": "📚", "lanjutan": "🌟"}.get(misi["level"], "📝")
            
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 12px 15px;
                    border-radius: 8px;
                    margin-bottom: 10px;
                    border-left: 4px solid {status_color};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 20px; font-weight: bold;">
                                {status_icon} {misi['nama']}
                            </span>
                            <span style="font-size: 12px; color: #888; margin-left: 8px;">
                                {level_icon} {misi['level'].capitalize()}
                            </span>
                        </div>
                        <div>
                            <span style="font-size: 14px; font-weight: bold; color: #2e7daf;">
                                🏆 +{misi['reward']}
                            </span>
                        </div>
                    </div>
                    <div style="font-size: 14px; color: #555; margin-top: 4px;">
                        {misi['deskripsi']}
                    </div>
                    <div style="margin-top: 6px;">
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888;">
                            <span>Progress</span>
                            <span>{misi['progress']:.1f}%</span>
                        </div>
                        <div style="width: 100%; background-color: #e9ecef; border-radius: 4px; height: 6px; overflow: hidden;">
                            <div style="
                                width: {min(100, misi['progress'])}%;
                                background-color: {'#28a745' if misi['selesai'] else '#2e7daf'};
                                height: 100%;
                                border-radius: 4px;
                                transition: width 0.5s;
                            "></div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if not misi_status:
            st.info("Belum ada data misi. Mulai kerjakan soal untuk membuka misi!")
            
    except Exception as e:
        logging.error(f"Error show_misi_dan_tantangan: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_misi_dan_tantangan()