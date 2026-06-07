# nkhm/stomata_pilihan_benar_salah.py
import streamlit as st
import random
import json
from pathlib import Path

# ========== 12 SISI STOMATA HATI ==========
SISI_NAMES = {
    1: "Kasih",
    2: "Iman",
    3: "Pengharapan",
    4: "Iman-Pengharapan",
    5: "Kasih-Iman",
    6: "Pengharapan-Kasih",
    7: "Berbuat iman",
    8: "Berbuat pengharapan",
    9: "Berbuat kasih",
    10: "Kasih-Iman-Pengharapan",
    11: "Berbuat kasih-beriman",
    12: "Berbuat kasih-berpengharapan",
}

def hitung_persentase(skor, max_skor=11):
    return (skor / max_skor) * 100 if max_skor else 0

def tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan):
    """
    Menentukan posisi (sisi) Stomata Hati berdasarkan persentase Iman, Kasih, Pengharapan.
    Mengembalikan list nomor sisi (bisa 1, 2, atau 3 sisi).
    """
    total = persen_kasih + persen_iman + persen_pengharapan
    if total == 0:
        return [10]
    # Normalisasi ke 100
    rk = (persen_kasih / total) * 100
    ri = (persen_iman / total) * 100
    rp = (persen_pengharapan / total) * 100

    # Kasus seimbang (selisih maks < 5%) -> sisi 1, 8, 9
    if max(rk, ri, rp) - min(rk, ri, rp) < 5:
        return [1, 8, 9]

    max_val = max(rk, ri, rp)
    if max_val >= 60:
        # Dominasi tunggal -> sisi sudut
        if rk == max_val:
            return [1]
        elif ri == max_val:
            return [2]
        else:
            return [3]
    elif (rk >= 40 and ri >= 40) or (ri >= 40 and rp >= 40) or (rp >= 40 and rk >= 40):
        # Kombinasi dua -> sisi kombinasi
        if rk >= 40 and ri >= 40:
            return [5]
        elif ri >= 40 and rp >= 40:
            return [4]
        elif rp >= 40 and rk >= 40:
            return [6]
        else:
            return [10]
    else:
        # Nilai sedang -> sisi tindakan berdasarkan tertinggi
        if rk == max_val:
            return [9]   # Berbuat kasih
        elif ri == max_val:
            return [7]   # Berbuat iman
        else:
            return [8]   # Berbuat pengharapan

# ========== MEMBACA SOAL DARI JSON ==========
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

# ========== STATE ==========
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
    persen = {k: hitung_persentase(v, max_kat) for k,v in skor.items()}
    sisi = tentukan_posisi(persen["Kasih"], persen["Iman"], persen["Pengharapan"])
    total = sum(skor.values())
    hasil = {
        "kasih": persen["Kasih"],
        "iman": persen["Iman"],
        "pengharapan": persen["Pengharapan"],
        "sisi_list": sisi,
        "skor_kasih": skor["Kasih"],
        "skor_iman": skor["Iman"],
        "skor_pengharapan": skor["Pengharapan"],
        "total_skor": total,
        "max_kat": max_kat,
        "max_total": 33
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

# ========== UI ==========
def show_pilihan_benar_salah():
    init_state()
    st.markdown("## ✅ Mode Pilihan Benar/Salah")
    st.markdown("Jawab 33 pernyataan dengan **Benar** atau **Salah**.")
    
    # Tampilkan skor resmi jika sudah ada
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
    
    # Tampilkan semua soal (tanpa form, agar setiap pilihan langsung trigger rerun)
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
        if selected != current:
            st.session_state.pbs_answers[i] = selected
            # Jika sudah ada hasil sebelumnya, reset status submit
            if st.session_state.pbs_submitted:
                st.session_state.pbs_submitted = False
            st.rerun()
        st.markdown("---")
    
    # Progress bar (update otomatis karena setiap pilihan trigger rerun)
    terjawab = len(st.session_state.pbs_answers)
    total = len(qlist)
    st.progress(terjawab / total, text=f"Progress: {terjawab}/{total} soal terjawab")
    
    # Tombol lihat hasil
    if st.button("📊 Lihat Hasil", use_container_width=True, type="primary"):
        if calculate_result():
            st.rerun()
    
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
        st.markdown(f"### 🌿 Posisi Stomata Hati: **{', '.join(nama_sisi)}** (Sisi {', '.join(map(str, sisi))})")
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