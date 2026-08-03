# nkhm/dasbor_nkhm.py
import streamlit as st
import pandas as pd
import logging
from nkhm.scoring import calculate_nkhm_q, calculate_nkhm_total

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def show_dasbor_nkhm():
    """Menampilkan Dasbor NKHM (Tab Dashboard)."""
    try:
        st.markdown("### 📊 Dasbor NKHM")
        
        # Ambil data dari session state
        scores = st.session_state.get("nkhm_scores", {"IQ": 0, "EQ": 0, "SQ": 0, "AQ": 0, "Nasionalisme": 0})
        history = st.session_state.get("nkhm_history", [])
        
        # Hitung NKHM
        nkhm_q = calculate_nkhm_q(scores["IQ"], scores["EQ"], scores["SQ"], scores["AQ"])
        nkhm_total = calculate_nkhm_total(nkhm_q, scores["Nasionalisme"])
        
        # ===== METRIK UTAMA =====
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🧠 NKHM_Q", f"{nkhm_q:.2f}")
        with col2:
            st.metric("🏆 NKHM Total", f"{nkhm_total:.2f}")
        with col3:
            total_soal = st.session_state.get("nkhm_total_questions", 0)
            st.metric("📖 Total Soal", total_soal)
        
        st.markdown("---")
        
        # ===== GRAFIK BAR =====
        st.markdown("### 📊 Skor Kecerdasan (0-100%)")
        
        # Hitung persentase skor
        from nkhm.scoring import get_normalized_score, MAX_POIN_IQ, MAX_POIN_EQ, MAX_POIN_SQ, MAX_POIN_AQ, MAX_POIN_NASIONALISME
        
        eq_raw_total = scores["EQ"] + st.session_state.get("eq_scale_total", 0)
        aq_raw_total = scores["AQ"] + st.session_state.get("aq_scale_total", 0)
        
        iq_pct = get_normalized_score(scores["IQ"], MAX_POIN_IQ)
        eq_pct = get_normalized_score(eq_raw_total, MAX_POIN_EQ)
        sq_pct = get_normalized_score(scores["SQ"], MAX_POIN_SQ)
        aq_pct = get_normalized_score(aq_raw_total, MAX_POIN_AQ)
        nas_pct = get_normalized_score(scores["Nasionalisme"], MAX_POIN_NASIONALISME)
        
        df_chart = pd.DataFrame({
            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"],
            "Skor": [iq_pct, eq_pct, sq_pct, aq_pct, nas_pct]
        })
        st.bar_chart(df_chart.set_index("Kecerdasan"), height=400, use_container_width=True)
        
        # ===== INFORMASI RUMUS =====
        with st.expander("📖 Tentang Rumus NKHM"):
            st.markdown("""
            **NKHM_Q** = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
            
            **NKHM_Total** = (NKHM_Q + Nasionalisme) / 2
            
            **Keterangan:**
            - IQ, EQ, SQ, AQ, Nasionalisme dalam skala 0-100
            - NKHM_Q mengukur kombinasi kecerdasan intelektual, emosional, spiritual, dan adversitas
            - NKHM_Total menggabungkan NKHM_Q dengan nilai Nasionalisme
            """)
        
        # ===== RIWAYAT KUIS =====
        if history:
            st.markdown("---")
            st.markdown("### 📋 Riwayat Kuis Terakhir")
            try:
                history_df = pd.DataFrame(history[-10:])
                required_cols = ["timestamp", "type", "question", "correct", "nkhm_total"]
                existing_cols = [col for col in required_cols if col in history_df.columns]
                history_df = history_df[existing_cols]
                
                # Konversi nilai boolean ke emoji
                if "correct" in history_df.columns:
                    history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
                
                # Rename kolom
                column_mapping = {
                    "timestamp": "Waktu",
                    "type": "Tipe",
                    "question": "Soal",
                    "correct": "Hasil",
                    "nkhm_total": "NKHM Total"
                }
                history_df.rename(columns=column_mapping, inplace=True)
                
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            except Exception as e:
                logging.error(f"Error menampilkan riwayat: {e}")
                st.warning("Gagal menampilkan riwayat kuis.")
        else:
            st.info("Belum ada riwayat kuis. Mulai kerjakan soal untuk melihat perkembangan.")
        
        # ===== STATISTIK =====
        if history:
            st.markdown("---")
            st.markdown("### 📈 Statistik")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                answered = len(history)
                st.metric("📝 Total Jawaban", answered)
            with col2:
                correct = sum(1 for h in history if isinstance(h.get("correct"), bool) and h["correct"])
                st.metric("✅ Jawaban Benar", correct)
            with col3:
                accuracy = (correct / answered * 100) if answered > 0 else 0
                st.metric("🎯 Akurasi", f"{accuracy:.1f}%")
        
    except Exception as e:
        logging.error(f"Error di show_dasbor_nkhm: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Dasbor NKHM: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_dasbor_nkhm()