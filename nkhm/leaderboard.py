# nkhm/leaderboard.py
import json
import os
import streamlit as st
import pandas as pd
import logging
from datetime import datetime

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LEADERBOARD_FILE = "data/leaderboard.json"

def init_leaderboard():
    """Inisialisasi file leaderboard jika belum ada."""
    try:
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
            logging.info("Leaderboard file created")
    except Exception as e:
        logging.error(f"Error init_leaderboard: {e}")

def save_score(name, nkhm_total):
    """Menyimpan skor NKHM_Total ke leaderboard"""
    try:
        init_leaderboard()
        
        # Baca data existing
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error membaca leaderboard: {e}. Membuat baru.")
            scores = []
        
        # Cek apakah nama sudah ada
        found = False
        for item in scores:
            if item.get("name") == name:
                # Update jika skor lebih tinggi
                if nkhm_total > item.get("score", 0):
                    item["score"] = nkhm_total
                    item["timestamp"] = datetime.now().isoformat()
                    logging.info(f"Skor {name} diperbarui: {nkhm_total}")
                found = True
                break
        
        if not found:
            # Tambahkan entri baru
            scores.append({
                "name": name,
                "score": nkhm_total,
                "timestamp": datetime.now().isoformat()
            })
            logging.info(f"Skor baru untuk {name}: {nkhm_total}")
        
        # Urutkan berdasarkan skor tertinggi
        scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        scores = scores[:100]  # Batasi 100 entri
        
        # Simpan kembali
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        logging.error(f"Error save_score: {e}")

def get_leaderboard():
    """Mengambil data leaderboard."""
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
    """Reset semua data leaderboard."""
    try:
        init_leaderboard()
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        logging.info("Leaderboard direset")
        return True
    except Exception as e:
        logging.error(f"Error reset_leaderboard: {e}")
        return False

def show_leaderboard():
    """Menampilkan leaderboard dengan styling yang baik."""
    try:
        st.subheader("🏆 Peringkat NKHM Tertinggi")
        
        scores = get_leaderboard()
        
        if not scores:
            st.info("📊 Belum ada peserta. Mulai kerjakan soal untuk masuk ke peringkat!")
            return
        
        # Tampilkan total peserta
        st.caption(f"📊 Total peserta: {len(scores)}")
        
        # Tampilkan top 10
        top_scores = scores[:10]
        
        # Buat DataFrame untuk tampilan
        df = pd.DataFrame(top_scores)
        
        # Tambahkan kolom peringkat
        df.index = range(1, len(df) + 1)
        df.index.name = "🏅 Peringkat"
        
        # Format timestamp
        if "timestamp" in df.columns:
            try:
                df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%d/%m/%Y %H:%M")
                df.rename(columns={"timestamp": "Waktu"}, inplace=True)
            except Exception as e:
                logging.warning(f"Error formatting timestamp: {e}")
                if "timestamp" in df.columns:
                    df.drop(columns=["timestamp"], inplace=True)
        
        # Rename kolom
        rename_cols = {"name": "👤 Nama", "score": "🏆 Skor NKHM"}
        df.rename(columns=rename_cols, inplace=True)
        
        # Tampilkan dengan styling
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
            (0, "🥇", "Emas", "#FFD700"),
            (1, "🥈", "Perak", "#C0C0C0"),
            (2, "🥉", "Perunggu", "#CD7F32")
        ]
        
        for idx, (medal_icon, medal_name, color) in enumerate(medals):
            if idx < len(scores):
                with [col1, col2, col3][idx]:
                    st.markdown(
                        f"""
                        <div style="
                            text-align: center;
                            padding: 15px;
                            background-color: #f8f9fa;
                            border-radius: 10px;
                            border: 2px solid {color};
                        ">
                            <div style="font-size: 40px;">{medal_icon}</div>
                            <div style="font-size: 20px; font-weight: bold;">{medal_name}</div>
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
                            <div style="font-size: 40px;">{medal_icon}</div>
                            <div style="font-size: 18px;">{medal_name}</div>
                            <div style="font-size: 14px;">Belum ada</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
        # ========== STATISTIK ==========
        st.markdown("---")
        st.markdown("### 📊 Statistik Leaderboard")
        
        try:
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                st.metric("👥 Total Peserta", len(scores))
            with col_stat2:
                if scores:
                    avg_score = sum(s.get("score", 0) for s in scores) / len(scores)
                    st.metric("📈 Rata-rata Skor", f"{avg_score:.1f}")
                else:
                    st.metric("📈 Rata-rata Skor", "0")
            with col_stat3:
                if scores:
                    max_score = max(s.get("score", 0) for s in scores)
                    st.metric("🏆 Skor Tertinggi", f"{max_score:.1f}")
                else:
                    st.metric("🏆 Skor Tertinggi", "0")
            with col_stat4:
                # Cek posisi user saat ini
                user_name = st.session_state.get("nkhm_user", None)
                if user_name:
                    position = next((i + 1 for i, s in enumerate(scores) if s.get("name") == user_name), None)
                    if position:
                        st.metric("📍 Posisi Anda", f"#{position}")
                    else:
                        st.metric("📍 Posisi Anda", "Belum ada")
                else:
                    st.metric("📍 Posisi Anda", "Login dulu")
        except Exception as e:
            logging.error(f"Error menampilkan statistik: {e}")
        
        # ========== TOMBOL RESET (HIDDEN) ==========
        # Hanya tampilkan jika user adalah admin
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

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di leaderboard: {e}")

if __name__ == "__main__":
    show_leaderboard()