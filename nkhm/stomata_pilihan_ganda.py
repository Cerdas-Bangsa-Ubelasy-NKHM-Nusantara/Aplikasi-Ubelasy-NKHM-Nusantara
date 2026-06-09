# nkhm/stomata_pilihan_ganda.py
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
    total = persen_kasih + persen_iman + persen_pengharapan
    if total == 0:
        return [10]
    rk = (persen_kasih / total) * 100
    ri = (persen_iman / total) * 100
    rp = (persen_pengharapan / total) * 100
    if max(rk, ri, rp) - min(rk, ri, rp) < 5:
        return [1, 8, 9]
    max_val = max(rk, ri, rp)
    if max_val >= 60:
        if rk == max_val: return [1]
        if ri == max_val: return [2]
        return [3]
    elif (rk >= 40 and ri >= 40) or (ri >= 40 and rp >= 40) or (rp >= 40 and rk >= 40):
        if rk >= 40 and ri >= 40: return [5]
        if ri >= 40 and rp >= 40: return [4]
        if rp >= 40 and rk >= 40: return [6]
        return [10]
    else:
        if rk == max_val: return [9]
        if ri == max_val: return [7]
        return [8]

# ========== MEMBACA SOAL DARI JSON ==========
def load_questions(kategori):
    # Cari folder dengan beberapa kemungkinan path
    base_paths = [
        Path(__file__).parent / "soal_stomata_hati" / "pilihan_ganda" / kategori,
        Path(__file__).parent.parent / "soal_stomata_hati" / "pilihan_ganda" / kategori,
        Path("soal_stomata_hati") / "pilihan_ganda" / kategori,
    ]
    base = None
    for p in base_paths:
        if p.exists():
            base = p
            break
    if base is None:
        st.error(f"Folder tidak ditemukan untuk {kategori}. Coba periksa path.")
        return []
    all_q = []
    for f in base.glob("*.json"):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    for item in data:
                        if "teks" in item and "pilihan" in item and "jawaban" in item:
                            all_q.append(item)
        except Exception as e:
            st.warning(f"Gagal baca {f.name}: {e}")
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
        result.append({
            "kategori": "Kasih",
            "id": q.get("id", 0),
            "teks": q["teks"],
            "pilihan": q["pilihan"],
            "jawaban_benar": q["jawaban"]
        })
    for q in sample_iman:
        result.append({
            "kategori": "Iman",
            "id": q.get("id", 0),
            "teks": q["teks"],
            "pilihan": q["pilihan"],
            "jawaban_benar": q["jawaban"]
        })
    for q in sample_pengharapan:
        result.append({
            "kategori": "Pengharapan",
            "id": q.get("id", 0),
            "teks": q["teks"],
            "pilihan": q["pilihan"],
            "jawaban_benar": q["jawaban"]
        })
    random.shuffle(result)
    return result

# ========== STATE ==========
def init_state():
    if "pg_answers" not in st.session_state:
        st.session_state.pg_answers = {}
    if "pg_submitted" not in st.session_state:
        st.session_state.pg_submitted = False
    if "pg_results" not in st.session_state:
        st.session_state.pg_results = None
    if "pg_questions" not in st.session_state:
        st.session_state.pg_questions = get_random_33()
    if "pg_official" not in st.session_state:
        st.session_state.pg_official = None
    if "pg_has_official" not in st.session_state:
        st.session_state.pg_has_official = False

def reset():
    st.session_state.pg_answers = {}
    st.session_state.pg_submitted = False
    st.session_state.pg_results = None

def refresh_questions():
    st.session_state.pg_questions = get_random_33()
    reset()

def calculate_result():
    qlist = st.session_state.pg_questions
    if not qlist or len(st.session_state.pg_answers) < len(qlist):
        st.error(f"Jawab semua {len(qlist)} soal")
        return False
    skor = {"Kasih":0, "Iman":0, "Pengharapan":0}
    for i, q in enumerate(qlist):
        if st.session_state.pg_answers.get(i) == q["jawaban_benar"]:
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
    if not st.session_state.pg_has_official:
        st.session_state.pg_official = hasil
        st.session_state.pg_has_official = True
        hasil["is_official"] = True
    else:
        hasil["is_official"] = False
    st.session_state.pg_results = hasil
    st.session_state.pg_submitted = True
    return True

# ========== UI ==========
def show_pilihan_ganda():
    init_state()
    st.markdown("## ✅ Mode Pilihan Ganda (a, b, c, d)")
    st.markdown("Jawab 33 soal pilihan ganda. Setiap jawaban benar = 1 poin.")

    if st.session_state.pg_has_official and st.session_state.pg_official:
        off = st.session_state.pg_official
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

    qlist = st.session_state.pg_questions

    # Debug: cek path dan file
    st.write("Debug: Mencari soal...")
    for kat in ["iman", "kasih", "pengharapan"]:
        path = Path(__file__).parent / "soal_stomata_hati" / "pilihan_ganda" / kat
        st.write(f"{kat}: {path.exists()} -> {list(path.glob('*.json'))}")

    if not qlist:
        st.error("❌ Gagal memuat soal. Periksa folder 'soal_stomata_hati/pilihan_ganda/...'")
        return

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

    for i, q in enumerate(qlist):
        st.markdown(f"**{i+1}. [{q['kategori']}]** {q['teks']}")
        current = st.session_state.pg_answers.get(i)
        # Tampilkan radio button dengan opsi a, b, c, d
        selected = st.radio(
            "Pilih jawaban:",
            q['pilihan'],
            index=q['pilihan'].index(current) if current in q['pilihan'] else None,
            key=f"pg_{i}_{q['id']}",
            horizontal=True,
            label_visibility="collapsed"
        )
        if selected != current:
            st.session_state.pg_answers[i] = selected
            if st.session_state.pg_submitted:
                st.session_state.pg_submitted = False
            st.rerun()
        st.markdown("---")

    terjawab = len(st.session_state.pg_answers)
    total = len(qlist)
    st.progress(terjawab / total, text=f"Progress: {terjawab}/{total} soal terjawab")

    if st.button("📊 Lihat Hasil", use_container_width=True, type="primary"):
        if calculate_result():
            st.rerun()

    if st.session_state.pg_submitted and st.session_state.pg_results:
        r = st.session_state.pg_results
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
                st.session_state.pg_submitted = False
                st.rerun()

if __name__ == "__main__":
    show_pilihan_ganda()