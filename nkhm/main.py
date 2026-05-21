= q.get("type") == kecerdasan
    
    if fokus_ok:
        filtered_questions.append(q)
        
        # ========== DETEKSI PERUBAHAN FILTER ==========
        filter_berubah = (st.session_state.nkhm_current_kategori != kategori or 
                          st.session_state.nkhm_current_kecerdasan != kecerdasan)
        
        if filter_berubah:
            st.session_state.nkhm_current_kategori = kategori
            st.session_state.nkhm_current_kecerdasan = kecerdasan
            st.session_state.nkhm_current_filtered = filtered_questions
            st.session_state.nkhm_answered = False
            st.session_state.nkhm_feedback = None
            if filtered_questions:
                st.session_state.nkhm_current_q = random.choice(filtered_questions)
            else:
                st.session_state.nkhm_current_q = None
        else:
            if filtered_questions and (st.session_state.nkhm_current_q is None or 
                                        st.session_state.nkhm_current_q not in filtered_questions):
                st.session_state.nkhm_current_q = random.choice(filtered_questions)
                st.session_state.nkhm_answered = False
                st.session_state.nkhm_feedback = None
            elif not filtered_questions:
                st.session_state.nkhm_current_q = None
        
        # ========== TAMPILKAN SOAL ATAU PERINGATAN ==========
        if not filtered_questions:
            st.warning("Tidak ada soal dengan filter ini. Coba pilih filter lain!")
        else:
            if st.session_state.nkhm_current_q is None:
                st.session_state.nkhm_current_q = random.choice(filtered_questions)
            q = st.session_state.nkhm_current_q
            
            st.markdown(f"### 📝 {q['text']}")
            col_tag1, col_tag2 = st.columns(2)
            display_type = "🇮🇩 Nasionalisme" if q.get('type') == "Nasionalisme" else f"🧠 {q['type']}"
            col_tag1.info(display_type)
            if q.get('national'):
                col_tag2.success("🇮🇩 Nasional")
            else:
                col_tag2.info("📚 Umum")
            
            # Tampilkan bagian dan skala untuk soal EQ_scale
            if q.get("type") == "EQ_scale":
                if q.get("section") and q.get("scale"):
                    st.caption(f"📂 **{q['section']}** — *{q['scale']}*")
                st.info(
                    "📌 **Petunjuk Skor Tanggapan:**\n\n"
                    "Berikan skor tanggapan dalam pilihan Anda (angka 0, 1, 2 atau 3) yang menggambarkan pikiran atau perasaan Anda terhadap hal yang diuraikan:\n"
                    "- **3** = Setuju sekali\n"
                    "- **2** = Setuju\n"
                    "- **1** = Kurang setuju\n"
                    "- **0** = Tidak setuju sekali"
                )
            
            # Tentukan label radio
            radio_label = "Pilih jawabanmu:" if q.get("type") != "EQ_scale" else "Pilih skor tanggapan:"
            
            selected = st.radio(radio_label, q['options'], key=f"radio_{q['text']}", index=None, disabled=st.session_state.nkhm_answered)
            
            # Tombol JAWAB
            if st.button("✅ JAWAB", disabled=st.session_state.nkhm_answered or selected is None, use_container_width=True):
                st.session_state.nkhm_answered = True
                st.session_state.nkhm_total_questions += 1
                
                if q.get("type") == "EQ_scale":
                    # Soal skor tanggapan: nilai langsung dari pilihan (0-3)
                    skor_tambahan = int(selected)
                    skor_baru = st.session_state.nkhm_scores["EQ"] + skor_tambahan
                    st.session_state.nkhm_scores["EQ"] = min(100, skor_baru)
                    st.session_state.nkhm_feedback = "scale_answered"
                    st.session_state.last_score_type = "EQ (skala)"
                    st.session_state.nkhm_history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50],
                        "type": "EQ_scale",
                        "correct": f"Skor {skor_tambahan}",
                        "nkhm_total": get_current_nkhm()[1]
                    })
                else:
                    # Soal pilihan ganda (IQ, EQ biasa, SQ, AQ, Nasionalisme)
                    if q['type'] == "Nasionalisme":
                        score_type = "Nasionalisme"
                    elif q['type'] == "EQ":
                        score_type = "EQ"
                    else:
                        score_type = q['type']
                    
                    st.session_state.last_score_type = score_type
                    
                    if selected == q['correct']:
                        new_score = min(100, st.session_state.nkhm_scores[score_type] + 10)
                        st.session_state.nkhm_scores[score_type] = new_score
                        st.session_state.nkhm_feedback = "benar"
                        _, nkhm_total_baru = get_current_nkhm()
                        save_score(st.session_state.nkhm_user, nkhm_total_baru)
                    else:
                        st.session_state.nkhm_feedback = "salah"
                    
                    nkhm_q_now, nkhm_total_now = get_current_nkhm()
                    st.session_state.nkhm_history.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "question": q['text'][:50],
                        "type": score_type,
                        "correct": selected == q['correct'],
                        "nkhm_q": nkhm_q_now,
                        "nkhm_total": nkhm_total_now
                    })
                
                st.rerun()
            
            # Tampilkan feedback (setelah dijawab)
            if st.session_state.nkhm_feedback == "benar":
                fb_type = st.session_state.get("last_score_type", "kecerdasan")
                st.success(f"✅ BENAR! +10 poin untuk {fb_type}")
            elif st.session_state.nkhm_feedback == "salah":
                if q.get('correct'):
                    st.error(f"❌ SALAH! Jawaban benar: **{q['correct']}**")
                else:
                    st.error("❌ Jawaban salah.")
            elif st.session_state.nkhm_feedback == "scale_answered":
                st.success(f"✅ Skor {selected} ditambahkan ke EQ (skala)")
            
            # Tombol navigasi setelah menjawab
            if st.session_state.nkhm_answered:
                col_nav1, col_nav2 = st.columns(2)
                with col_nav1:
                    if st.button("⏩ SOAL SELANJUTNYA", use_container_width=True):
                        if st.session_state.nkhm_current_filtered:
                            st.session_state.nkhm_current_q = random.choice(st.session_state.nkhm_current_filtered)
                        else:
                            st.session_state.nkhm_current_q = None
                        st.session_state.nkhm_answered = False
                        st.session_state.nkhm_feedback = None
                        st.rerun()
                with col_nav2:
                    if st.button("🎮 KUIS BARU", use_container_width=True):
                        if filtered_questions:
                            st.session_state.nkhm_current_q = random.choice(filtered_questions)
                        else:
                            st.session_state.nkhm_current_q = None
                        st.session_state.nkhm_answered = False
                        st.session_state.nkhm_feedback = None
                        st.rerun()
    
    with tab2:
        st.markdown("### Dashboard")
        df_chart = pd.DataFrame({
            "Kecerdasan": ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"],
            "Skor": [st.session_state.nkhm_scores["IQ"], st.session_state.nkhm_scores["EQ"],
                     st.session_state.nkhm_scores["SQ"], st.session_state.nkhm_scores["AQ"],
                     st.session_state.nkhm_scores["Nasionalisme"]]
        })
        st.bar_chart(df_chart.set_index("Kecerdasan"), height=400)
        with st.expander("📖 Tentang Rumus NKHM"):
            st.markdown("""
            **NKHM_Q** = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
            **NKHM_Total** = (NKHM_Q + Nasionalisme) / 2
            Dimana: IQ, EQ, SQ, AQ, Nasionalisme 0-100
            """)
        if st.session_state.nkhm_history:
            st.markdown("### Riwayat Kuis")
            history_df = pd.DataFrame(st.session_state.nkhm_history[-10:])
            history_df = history_df[["timestamp", "type", "question", "correct", "nkhm_total"]]
            history_df["correct"] = history_df["correct"].map({True: "✅", False: "❌"})
            history_df.columns = ["Waktu", "Tipe", "Soal", "Hasil", "NKHM Total"]
            st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Pencapaian")
        cols = st.columns(5)
        badges = {"IQ": "🧠 Cendekia", "EQ": "❤️ Empati", "SQ": "🙏 Bhinneka", "AQ": "💪 Tangguh", "Nasionalisme": "🇮🇩 Patriot"}
        for i, (t, label) in enumerate(badges.items()):
            if st.session_state.nkhm_scores[t] >= 50:
                cols[i].success(f"✅ **{label}**")
            else:
                cols[i].info(f"🔒 {label} (50+)")
        if all(st.session_state.nkhm_scores[t] >= 50 for t in ["IQ", "EQ", "SQ", "AQ", "Nasionalisme"]):
            st.balloons()
            st.success("🎉 **GELAR: PAHLAWAN CERDAS NUSANTARA!** 🎉")
        answered = len(st.session_state.nkhm_history)
        correct = sum(1 for h in st.session_state.nkhm_history if h["correct"])
        accuracy = (correct / answered * 100) if answered > 0 else 0
        col1, col2, col3 = st.columns(3)
        col1.metric("📖 Total Soal", answered)
        col2.metric("✅ Benar", correct)
        col3.metric("📊 Akurasi", f"{accuracy:.1f}%")
        show_leaderboard()

if __name__ == "__main__":
    main()
