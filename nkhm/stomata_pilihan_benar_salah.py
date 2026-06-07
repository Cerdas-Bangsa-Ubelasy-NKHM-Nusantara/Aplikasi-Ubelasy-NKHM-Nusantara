# nkhm/stomata_pilihan_benar_salah.py
import streamlit as st
import random
import json
from pathlib import Path

SISI_NAMES = {
    1: "Kasih", 2: "Iman", 3: "Pengharapan",
    4: "Iman-Pengharapan", 5: "Kasih-Iman", 6: "Pengharapan-Kasih",
    7: "Berbuat iman", 8: "Berbuat pengharapan", 9: "Berbuat kasih",
    10: "Kasih-Iman-Pengharapan", 11: "Berbuat kasih-beriman", 12: "Berbuat kasih-berpengharapan",
}

def load_questions(kategori):
    base = Path(__file__).parent / "soal_stomata_hati" / "pilihan_benar_salah" / kategori
    if not base.exists():
        return []
    all_q = []
    for f in base.glob("*.json"):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    for item in data:
                        if "teks" in item and "jawaban" in item:
                            all_q.append(item)
        except Exception:
            pass
    return all_q

def get_random_33():
    kasih = load_questions("kasih")
    iman = load_questions("iman")
    pengharapan = load_questions("pengharapan")
    if len(kasih) < 11 or len(iman) < 11 or len(pengharapan) < 11:
        return []
    sample_kasih = random.sample(kasih, 11)
    sample_iman = random.sample(iman, 11)
    sample_pengharapan = random.sample(pengharapan, 11)
    result = []
    for q in sample_kasih:
        result.append({"kategori": "Kasih", "id": q.get("id",0), "teks": q["teks"], "jawaban_benar": q["jawaban"]})
    for q in sample_iman:
        result.append({"kategori": "Iman", "id": q.get("id",0), "teks": q["teks"], "jawaban_benar": q["jawaban"]})
    for q in sample_pengharapan:
        result.append({"kategori": "Pengharapan", "id": q.get("id",0), "teks": q["teks"], "jawaban_benar": q["jawaban"]})
    random.shuffle(result)
    return result

def init_state():
    if "pbs_questions" not in st.session_state:
        st.session_state.pbs_questions = get_random_33()
    if "pbs_answers" not in st.session_state:
        st.session_state.pbs_answers = {}
    if "pbs_submitted" not in st.session_state:
        st.session_state.pbs_submitted = False
    if "pbs_results" not in st.session_state:
        st.session_state.pbs_results = None
    if "pbs_official" not in st.session_state:
        st.session_state.pbs_official = None
    if "pbs_has_official" not in st.session_state:
        st.session_state.pbs_has_official = False

def reset():
    st.session_state.pbs_answers = {}
    st.session_state.pbs_submitted = False
    st.session_state.pbs_results = None

def refresh_questions():
    st.session_state.pbs_questions = get_random_33()
    reset()

def calculate_result():
    qlist = st.session_state.pbs_questions
    if not qlist or len(st.session_state.pbs_answers) < len(qlist):
        st.error(f"Jawab semua {len(qlist)} soal")
        return False
    skor = {"Kasih":0, "Iman":0, "Pengharapan":0}
    for i, q in enumerate(qlist):
        if st.session_state.pbs_answers.get(i) == q["jawaban_benar"]:
            skor[q["kategori"]] += 1
    max_kat = 11
    persen = {k: (v / max_kat * 100) for k,v in skor.items()}
    total = sum(skor.values())
    sisi = [1]  # placeholder, Anda bisa gunakan fungsi tentukan_posisi nanti
    hasil = {
        "kasih": persen["Kasih"], "iman": persen["Iman"], "pengharapan": persen["Pengharapan"],
        "sisi_list": sisi,
        "skor_kasih": skor["Kasih"], "skor_iman": skor["Iman"], "skor_pengharapan": skor["Pengharapan"],
        "total_skor": total, "max_kat": max_kat, "max_total": 33
    }
    if not st.session_state.pbs_has_official:
        st.session_state.pbs_official = hasil
        st.session_state.pbs_has_official = True
        hasil["is_official"] = True
    else:
        hasil["is_official"] = False
    st.session_state.pbs_results = hasil
    st.session_state.pbs_submitted = True
    return True

def show_pilihan_benar_salah():
    init_state()
    st.markdown("## ✅ Mode Pilihan Benar/Salah")
    st.markdown("Jawab 33 pernyataan dengan **Benar** atau **Salah**.")
    
    if st.session_state.pbs_has_official and st.session_state.pbs_official:
        off = st.session_state.pbs_official
        st.markdown("---")
        st.markdown("### 🏆 SKOR RESMI ANDA")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kasih", f"{off['skor_kasih']}/11")
        col2.metric("Iman", f"{off['skor_iman']}/11")
        col3.metric("Pengharapan", f"{off['skor_pengharapan']}/11")
        st.markdown(f"**Total: {off['total_skor']}/33**")
        st.markdown("---")
        st.markdown("### ✨ MODE LATIHAN ✨")
    else:
        st.info("🎯 Permainan pertama. Jawab semua dengan jujur.")
    
    qlist = st.session_state.pbs_questions
    if not qlist:
        st.error("❌ Gagal memuat soal. Periksa folder 'soal_stomata_hati/pilihan_benar_salah/...'")
        return
    
    # Tombol kontrol
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ganti Soal (Baru)", use_container_width=True):
            refresh_questions()
            st.rerun()
    with col2:
        if st.button("🗑️ Reset Jawaban", use_container_width=True):
            reset()
            st.rerun()
    
    st.markdown("---")
    
    # Gunakan form untuk menghindari rerun setiap kali memilih radio
    with st.form(key="pilihan_form"):
        # Tampilkan semua soal dalam form
        for i, q in enumerate(qlist):
            st.markdown(f"**{i+1}. [{q['kategori']}]** {q['teks']}")
            current = st.session_state.pbs_answers.get(i)
            selected = st.radio(
                "Pilih jawaban:",
                ["Benar", "Salah"],
                index=0 if current == "Benar" else (1 if current == "Salah" else None),
                key=f"pbs_{i}_{q['id']}",
                horizontal=True,
                label_visibility="collapsed"
            )
            # Simpan jawaban sementara ke session state (tanpa rerun)
            if selected != current:
                st.session_state.pbs_answers[i] = selected
            st.markdown("---")
        
        # Tombol submit di dalam form
        submitted = st.form_submit_button("📊 Lihat Hasil", use_container_width=True, type="primary")
        if submitted:
            if calculate_result():
                st.rerun()
    
    # Tampilkan progress (di luar form, update setiap kali ada perubahan)
    terjawab = len(st.session_state.pbs_answers)
    total = len(qlist)
    st.progress(terjawab / total, text=f"Progress: {terjawab}/{total}")
    
    # Tampilkan hasil jika sudah submit
    if st.session_state.pbs_submitted and st.session_state.pbs_results:
        r = st.session_state.pbs_results
        if r.get("is_official"):
            st.success("🎉 Skor resmi tersimpan!")
        else:
            st.info("📝 Hasil latihan (tidak mengubah skor resmi)")
        with st.expander("📈 Detail Skor"):
            st.metric("Kasih", f"{r['skor_kasih']}/{r['max_kat']}")
            st.metric("Iman", f"{r['skor_iman']}/{r['max_kat']}")
            st.metric("Pengharapan", f"{r['skor_pengharapan']}/{r['max_kat']}")
        st.markdown(f"### **Total Skor: {r['total_skor']}/{r['max_total']}**")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Kasih %", f"{r['kasih']:.1f}%")
        col_b.metric("Iman %", f"{r['iman']:.1f}%")
        col_c.metric("Pengharapan %", f"{r['pengharapan']:.1f}%")
        img_path = Path(__file__).parent.parent / "assets" / "stomata_hati_1.jpg"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        sisi = r['sisi_list']
        nama_sisi = [SISI_NAMES.get(s, f"Sisi {s}") for s in sisi]
        st.markdown(f"### 🌿 Posisi Stomata Hati: **{', '.join(nama_sisi)}**")
        with st.expander("📖 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"{no}. {nama}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Latihan Lagi (Soal Baru)"):
                refresh_questions()
                st.rerun()
        with col2:
            if st.button("📝 Lanjut (Soal Sama)"):
                st.session_state.pbs_submitted = False
                st.rerun()

if __name__ == "__main__":
    show_pilihan_benar_salah()