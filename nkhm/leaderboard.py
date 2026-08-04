# nkhm/leaderboard.py
import json
import os
import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di leaderboard: {e}")

LEADERBOARD_FILE = "data/leaderboard.json"

def init_leaderboard():
    try:
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
            logging.info("Leaderboard file created")
    except Exception as e:
        logging.error(f"Error init_leaderboard: {e}")

def save_score(name, nkhm_total):
    try:
        init_leaderboard()
        
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error membaca leaderboard: {e}. Membuat baru.")
            scores = []
        
        found = False
        for item in scores:
            if item.get("name") == name:
                if nkhm_total > item.get("score", 0):
                    item["score"] = nkhm_total
                    item["timestamp"] = datetime.now().isoformat()
                    logging.info(f"Skor {name} diperbarui: {nkhm_total}")
                found = True
                break
        
        if not found:
            scores.append({
                "name": name,
                "score": nkhm_total,
                "timestamp": datetime.now().isoformat()
            })
            logging.info(f"Skor baru untuk {name}: {nkhm_total}")
        
        scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        scores = scores[:100]
        
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        logging.error(f"Error save_score: {e}")

def get_leaderboard():
    try:
        init_leaderboard()
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
            return scores
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error membaca leaderboard: {e}")
            return []
    except Exception as e:
        logging.error(f"Error get_leaderboard: {e}")
        return []

def reset_leaderboard():
    try:
        init_leaderboard()
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        logging.info("Leaderboard direset")
        return True
    except Exception as e:
        logging.error(f"Error reset_leaderboard: {e}")
        return False

# ========== FITUR TAMBAHAN ==========

def get_user_position(scores, user_name):
    """Mendapatkan posisi user di leaderboard."""
    if not user_name:
        return None
    for idx, s in enumerate(scores):
        if s.get("name") == user_name:
            return idx + 1
    return None

def get_level_from_score(score):
    """Menentukan level berdasarkan skor."""
    if score >= 90:
        return "🌟 Grand Master", "gold"
    elif score >= 75:
        return "🏆 Master", "blue"
    elif score >= 60:
        return "📚 Expert", "green"
    elif score >= 40:
        return "🌱 Learner", "orange"
    elif score >= 20:
        return "📖 Beginner", "gray"
    else:
        return "🌿 Novice", "red"

def get_next_level(score):
    """Mendapatkan level berikutnya dan target skor."""
    levels = [
        {"name": "🌿 Novice", "min": 0, "max": 19},
        {"name": "📖 Beginner", "min": 20, "max": 39},
        {"name": "🌱 Learner", "min": 40, "max": 59},
        {"name": "📚 Expert", "min": 60, "max": 74},
        {"name": "🏆 Master", "min": 75, "max": 89},
        {"name": "🌟 Grand Master", "min": 90, "max": 100}
    ]
    
    for i, level in enumerate(levels):
        if score <= level["max"]:
            if i < len(levels) - 1:
                next_level = levels[i + 1]
                return {
                    "current": level["name"],
                    "next": next_level["name"],
                    "progress": (score - level["min"]) / (level["max"] - level["min"]) * 100,
                    "target": next_level["min"]
                }
            else:
                return {
                    "current": level["name"],
                    "next": "🏆 Maksimum!",
                    "progress": 100,
                    "target": 100
                }
    return None

def show_statistik_kompetitif(scores):
    """Menampilkan statistik kompetitif."""
    try:
        st.markdown("### 📊 Statistik Kompetitif")
        
        if not scores:
            st.info("Belum ada data peserta.")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Peserta", len(scores))
        with col2:
            avg_score = sum(s.get("score", 0) for s in scores) / len(scores) if scores else 0
            st.metric("📈 Rata-rata Skor", f"{avg_score:.1f}")
        with col3:
            max_score = max(s.get("score", 0) for s in scores) if scores else 0
            st.metric("🏆 Skor Tertinggi", f"{max_score:.1f}")
        with col4:
            # Posisi user
            user_name = st.session_state.get("nkhm_user", None)
            position = get_user_position(scores, user_name) if user_name else None
            if position:
                st.metric("📍 Posisi Anda", f"#{position} dari {len(scores)}")
            else:
                st.metric("📍 Posisi Anda", "Belum terdaftar")
                
    except Exception as e:
        logging.error(f"Error show_statistik_kompetitif: {e}")

def show_user_level_progress(scores):
    """Menampilkan level dan progress user."""
    try:
        user_name = st.session_state.get("nkhm_user", None)
        if not user_name:
            return
        
        # Cari skor user
        user_score = None
        for s in scores:
            if s.get("name") == user_name:
                user_score = s.get("score", 0)
                break
        
        if user_score is None:
            st.info("Anda belum memiliki skor. Mulai kerjakan soal!")
            return
        
        st.markdown("### 🎯 Level & Progress")
        
        level_info = get_next_level(user_score)
        if level_info:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Level Saat Ini:** {level_info['current']}")
                st.progress(level_info['progress'] / 100, text=f"{level_info['progress']:.1f}%")
            with col2:
                st.markdown(f"**Level Berikutnya:** {level_info['next']}")
                st.caption(f"Target: {level_info['target']} poin")
        
        # Tampilkan badge level
        level, color = get_level_from_score(user_score)
        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: 15px;
                background-color: #f0f5fa;
                border-radius: 10px;
                border: 2px solid {'#FFD700' if color == 'gold' else '#2e7daf'};
            ">
                <div style="font-size: 40px;">{level.split()[0]}</div>
                <div style="font-size: 20px; font-weight: bold; color: {'#FFD700' if color == 'gold' else '#2e7daf'};">
                    {level}
                </div>
                <div style="font-size: 14px; color: #666;">Skor: {user_score:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    except Exception as e:
        logging.error(f"Error show_user_level_progress: {e}")

def show_tren_skor(scores):
    """Menampilkan tren skor (simulasi berdasarkan data)."""
    try:
        st.markdown("### 📈 Tren Perkembangan")
        
        if not scores:
            st.info("Belum ada data untuk tren.")
            return
        
        # Ambil data dari leaderboard (simulasi distribusi skor)
        df = pd.DataFrame(scores)
        if "score" in df.columns:
            # Kelompokkan skor ke dalam rentang
            bins = [0, 20, 40, 60, 80, 100]
            labels = ["0-20", "21-40", "41-60", "61-80", "81-100"]
            df["range"] = pd.cut(df["score"], bins=bins, labels=labels, right=False)
            
            # Hitung distribusi
            distribution = df["range"].value_counts().sort_index()
            
            st.markdown("**Distribusi Skor Peserta:**")
            st.bar_chart(distribution, height=250, use_container_width=True)
            
            # Tambahan: posisi user
            user_name = st.session_state.get("nkhm_user", None)
            if user_name:
                user_score = next((s.get("score", 0) for s in scores if s.get("name") == user_name), None)
                if user_score is not None:
                    st.caption(f"📌 Skor Anda: {user_score:.1f} - {get_level_from_score(user_score)[0]}")
        
    except Exception as e:
        logging.error(f"Error show_tren_skor: {e}")

def show_tantangan(scores):
    """Menampilkan tantangan dan misi."""
    try:
        st.markdown("### 🎯 Tantangan & Misi")
        
        user_name = st.session_state.get("nkhm_user", None)
        if not user_name:
            st.info("Login untuk melihat tantangan pribadi!")
            return
        
        # Cari skor user
        user_score = None
        for s in scores:
            if s.get("name") == user_name:
                user_score = s.get("score", 0)
                break
        
        if user_score is None:
            st.info("Mulai kerjakan soal untuk membuka tantangan!")
            return
        
        # Tantangan berdasarkan skor
        challenges = []
        
        if user_score < 20:
            challenges.append(("🌱", "Capai 20 poin", "Level Beginner", 20 - user_score))
        elif user_score < 40:
            challenges.append(("📖", "Capai 40 poin", "Level Learner", 40 - user_score))
        elif user_score < 60:
            challenges.append(("🌱", "Capai 60 poin", "Level Expert", 60 - user_score))
        elif user_score < 75:
            challenges.append(("📚", "Capai 75 poin", "Level Master", 75 - user_score))
        elif user_score < 90:
            challenges.append(("🏆", "Capai 90 poin", "Level Grand Master", 90 - user_score))
        else:
            challenges.append(("🌟", "Pertahankan posisi", "Grand Master", 0))
        
        # Tampilkan tantangan
        for icon, title, desc, remaining in challenges:
            col1, col2, col3 = st.columns([1, 6, 1])
            with col1:
                st.markdown(f"<div style='font-size: 30px;'>{icon}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{title}**")
                st.caption(desc)
            with col3:
                if remaining > 0:
                    st.markdown(f"<div style='text-align: center;'><span style='font-size: 20px;'>🎯</span><br><span style='font-size: 12px;'>+{remaining:.1f}</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center;'>✅</div>", unsafe_allow_html=True)
        
    except Exception as e:
        logging.error(f"Error show_tantangan: {e}")

# ========== MAIN ==========
def show_leaderboard():
    try:
        # ===== TAB SELECTOR =====
        tab1, tab2, tab3 = st.tabs(["🏆 Peringkat", "📊 Statistik", "🎯 Tantangan"])
        
        scores = get_leaderboard()
        
        # ===== TAB 1: PERINGKAT =====
        with tab1:
            st.subheader("🏆 Peringkat NKHM Tertinggi")
            
            if not scores:
                st.info("📊 Belum ada peserta. Mulai kerjakan soal untuk masuk ke peringkat!")
                return
            
            st.caption(f"📊 Total peserta: {len(scores)}")
            
            top_scores = scores[:10]
            
            df = pd.DataFrame(top_scores)
            df.index = range(1, len(df) + 1)
            df.index.name = "🏅 Peringkat"
            
            if "timestamp" in df.columns:
                try:
                    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%d/%m/%Y %H:%M")
                    df.rename(columns={"timestamp": "Waktu"}, inplace=True)
                except Exception as e:
                    logging.warning(f"Error formatting timestamp: {e}")
                    if "timestamp" in df.columns:
                        df.drop(columns=["timestamp"], inplace=True)
            
            rename_cols = {"name": "👤 Nama", "score": "🏆 Skor NKHM"}
            df.rename(columns=rename_cols, inplace=True)
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "🏅 Peringkat": st.column_config.NumberColumn("🏅 Peringkat"),
                    "👤 Nama": st.column_config.TextColumn("👤 Nama"),
                    "🏆 Skor NKHM": st.column_config.NumberColumn("🏆 Skor NKHM", format="%.1f"),
                    "Waktu": st.column_config.TextColumn("📅 Waktu"),
                }
            )
            
            # ========== MEDALI UNTUK 3 TERATAS ==========
            st.markdown("---")
            st.markdown("### 🎖️ Peraih Medali")
            
            col1, col2, col3 = st.columns(3)
            
            medals = [
                {"icon": "🥇", "name": "Emas", "color": "#FFD700"},
                {"icon": "🥈", "name": "Perak", "color": "#C0C0C0"},
                {"icon": "🥉", "name": "Perunggu", "color": "#CD7F32"}
            ]
            
            for idx, medal in enumerate(medals):
                if idx < len(scores):
                    with [col1, col2, col3][idx]:
                        st.markdown(
                            f"""
                            <div style="
                                text-align: center;
                                padding: 15px;
                                background-color: #f8f9fa;
                                border-radius: 10px;
                                border: 2px solid {medal['color']};
                            ">
                                <div style="font-size: 40px;">{medal['icon']}</div>
                                <div style="font-size: 20px; font-weight: bold;">{medal['name']}</div>
                                <div style="font-size: 18px;">{scores[idx].get('name', 'Unknown')}</div>
                                <div style="font-size: 16px; color: #666;">Skor: {scores[idx].get('score', 0):.1f}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    with [col1, col2, col3][idx]:
                        st.markdown(
                            f"""
                            <div style="
                                text-align: center;
                                padding: 15px;
                                background-color: #f8f9fa;
                                border-radius: 10px;
                                border: 2px dashed #ccc;
                                color: #999;
                            ">
                                <div style="font-size: 40px;">{medal['icon']}</div>
                                <div style="font-size: 18px;">{medal['name']}</div>
                                <div style="font-size: 14px;">Belum ada</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        
        # ===== TAB 2: STATISTIK =====
        with tab2:
            show_statistik_kompetitif(scores)
            st.markdown("---")
            show_user_level_progress(scores)
            st.markdown("---")
            show_tren_skor(scores)
        
        # ===== TAB 3: TANTANGAN =====
        with tab3:
            show_tantangan(scores)
        
        # ===== TOMBOL RESET (HIDDEN) =====
        if st.session_state.get("nkhm_user") == "Admin":
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Reset Leaderboard", use_container_width=True, type="secondary"):
                    if reset_leaderboard():
                        st.success("✅ Leaderboard berhasil direset!")
                        safe_rerun()
                    else:
                        st.error("❌ Gagal mereset leaderboard.")
        
    except Exception as e:
        logging.error(f"Error di show_leaderboard: {e}", exc_info=True)
        st.error(f"❌ Terjadi error: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_leaderboard()