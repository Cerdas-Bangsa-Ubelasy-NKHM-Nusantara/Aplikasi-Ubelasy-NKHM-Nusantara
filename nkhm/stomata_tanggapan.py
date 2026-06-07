# nkhm/stomata_tanggapan.py
import streamlit as st
import random
import json
from pathlib import Path
from .stomata_utils import SISI_NAMES, LIKERT_SCORE, konversi_ke_skor_0_1, hitung_persentase, tentukan_posisi

def load_soal_dari_path(base_path, kategori):
    folder_path = base_path / kategori
    all_soal = []
    if not folder_path.exists():
        st.warning(f"⚠️ Folder {folder_path} tidak ditemukan")
        return []
    json_files = sorted(folder_path.glob("*.json"))
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if "teks" in item:
                            all_soal.append(item)
        except Exception as e:
            st.warning(f"⚠️ Error baca {json_file.name}: {e}")
    return all_soal

def load_tanggapan_soal():
    base_path = Path(__file__).parent / "soal_stomata_hati" / "tanggapan"
    soal_kasih = load_soal_dari_path(base_path, "kasih")
    soal_iman = load_soal_dari_path(base_path, "iman")
    soal_pengharapan = load_soal_dari_path(base_path, "pengharapan")
    if len(soal_kasih) < 11 or len(soal_iman) < 11 or len(soal_pengharapan) < 11:
        st.error(f"⚠️ Jumlah soal tidak cukup: Kasih={len(soal_kasih)}, Iman={len(soal_iman)}, Pengharapan={len(soal_pengharapan)} (minimal 11 per kategori)")
        return []
    sample_kasih = random.sample(soal_kasih, 11)
    sample_iman = random.sample(soal_iman, 11)
    sample_pengharapan = random.sample(soal_pengharapan, 11)
    all_soal = []
    for s in sample_kasih:
        all_soal.append({
            "kategori": "Kasih",
            "id": s.get("id", 0),
            "teks": s["teks"],
            "pilihan": s.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    for s in sample_iman:
        all_soal.append({
            "kategori": "Iman",
            "id": s.get("id", 0),
            "teks": s["teks"],
            "pilihan": s.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    for s in sample_pengharapan:
        all_soal.append({
            "kategori": "Pengharapan",
            "id": s.get("id", 0),
            "teks": s["teks"],
            "pilihan": s.get("pilihan", ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"])
        })
    random.shuffle(all_soal)
    return all_soal

def init_tanggapan_state():
    prefix = "tanggapan_"
    if f"{prefix}answers" not in st.session_state:
        st.session_state[f"{prefix}answers"] = {}
    if f"{prefix}submitted" not in st.session_state:
        st.session_state[f"{prefix}submitted"] = False
    if f"{prefix}results" not in st.session_state:
        st.session_state[f"{prefix}results"] = None
    if f"{prefix}soal_version" not in st.session_state:
        st.session_state[f"{prefix}soal_version"] = 0
    if f"{prefix}all_soal" not in st.session_state:
        st.session_state[f"{prefix}all_soal"] = None
    if f"{prefix}official_score" not in st.session_state:
        st.session_state[f"{prefix}official_score"] = None
    if f"{prefix}has_official_score" not in st.session_state:
        st.session_state[f"{prefix}has_official_score"] = False

def proses_tanggapan():
    soal_list = st.session_state.tanggapan_all_soal
    if not soal_list:
        return False
    if len(st.session_state.tanggapan_answers) < len(soal_list):
        st.error(f"⚠️ Jawab semua {len(soal_list)} soal")
        return False
    skor_kasih = skor_iman = skor_pengharapan = 0
    for idx, soal in enumerate(soal_list):
        jawaban = st.session_state.tanggapan_answers.get(idx)
        if jawaban:
            nilai = LIKERT_SCORE.get(jawaban, 0)
            skor = konversi_ke_skor_0_1(nilai)
            if soal['kategori'] == "Kasih": skor_kasih += skor
            elif soal['kategori'] == "Iman": skor_iman += skor
            else: skor_pengharapan += skor
    max_kat = 11
    persen_kasih = hitung_persentase(skor_kasih, max_kat)
    persen_iman = hitung_persentase(skor_iman, max_kat)
    persen_pengharapan = hitung_persentase(skor_pengharapan, max_kat)
    sisi = tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan)
    total = skor_kasih + skor_iman + skor_pengharapan
    hasil = {
        "kasih": persen_kasih, "iman": persen_iman, "pengharapan": persen_pengharapan,
        "sisi_list": sisi, "skor_kasih": skor_kasih, "skor_iman": skor_iman,
        "skor_pengharapan": skor_pengharapan, "total_skor": total,
        "max_per_kategori": max_kat, "max_total": 33
    }
    if not st.session_state.tanggapan_has_official_score:
        st.session_state.tanggapan_official_score = hasil
        st.session_state.tanggapan_has_official_score = True
        hasil["is_official"] = True
    else:
        hasil["is_official"] = False
    st.session_state.tanggapan_results = hasil
    st.session_state.tanggapan_submitted = True
    return True

def show_tanggapan():
    init_tanggapan_state()
    if st.session_state.tanggapan_all_soal is None:
        st.session_state.tanggapan_all_soal = load_tanggapan_soal()
    if not st.session_state.tanggapan_all_soal:
        st.error("❌ Gagal memuat soal tanggapan. Periksa folder dan file JSON.")
        return
    if st.session_state.tanggapan_has_official_score and st.session_state.tanggapan_official_score:
        off = st.session_state.tanggapan_official_score
        st.markdown("### 🏆 Skor Resmi Tanggapan Anda")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kasih", f"{off['skor_kasih']}/11")
        col2.metric("Iman", f"{off['skor_iman']}/11")
        col3.metric("Pengharapan", f"{off['skor_pengharapan']}/11")
        st.markdown(f"**Total: {off['total_skor']}/33**")
        st.info(f"Posisi: {', '.join([SISI_NAMES[s] for s in off['sisi_list']])}")
        st.markdown("---")
        st.markdown("### ✨ Mode Latihan Tanggapan ✨")
    else:
        st.info("🎯 Permainan tanggapan pertama. Jawab semua soal dengan jujur.")
    soal_list = st.session_state.tanggapan_all_soal
    ver = st.session_state.tanggapan_soal_version
    jawaban_terjawab = len(st.session_state.tanggapan_answers)
    total_soal = len(soal_list)
    st.markdown(f"**📝 Soal terjawab: {jawaban_terjawab}/{total_soal}**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ganti Soal Tanggapan (Baru)"):
            st.session_state.tanggapan_all_soal = load_tanggapan_soal()
            st.session_state.tanggapan_answers = {}
            st.session_state.tanggapan_submitted = False
            st.session_state.tanggapan_results = None
            st.session_state.tanggapan_soal_version += 1
            st.rerun()
    with col2:
        if st.button("🗑️ Reset Jawaban Tanggapan"):
            st.session_state.tanggapan_answers = {}
            st.session_state.tanggapan_submitted = False
            st.session_state.tanggapan_results = None
            st.rerun()
    with st.container(height=500):
        for idx, soal in enumerate(soal_list):
            key = f"tanggap_{idx}_{soal['id']}_v{ver}"
            current = st.session_state.tanggapan_answers.get(idx)
            selected = st.radio(
                f"**{idx+1}. [{soal['kategori']}]** {soal['teks']}",
                soal['pilihan'],
                index=soal['pilihan'].index(current) if current in soal['pilihan'] else None,
                key=key, label_visibility="collapsed", horizontal=True
            )
            if selected != current:
                st.session_state.tanggapan_answers[idx] = selected
                if st.session_state.tanggapan_submitted:
                    st.session_state.tanggapan_submitted = False
                st.rerun()
    st.progress(jawaban_terjawab/total_soal, text=f"Progress: {jawaban_terjawab}/{total_soal}")
    if st.button("📊 Lihat Hasil Tanggapan", type="primary"):
        if proses_tanggapan():
            st.rerun()
    if st.session_state.tanggapan_submitted and st.session_state.tanggapan_results:
        res = st.session_state.tanggapan_results
        if res.get("is_official"):
            st.success("🎉 Skor resmi tersimpan!")
        else:
            st.info("📝 Hasil latihan (tidak mengubah skor resmi)")
        with st.expander("📈 Detail Skor"):
            st.metric("Kasih", f"{res['skor_kasih']}/{res['max_per_kategori']}")
            st.metric("Iman", f"{res['skor_iman']}/{res['max_per_kategori']}")
            st.metric("Pengharapan", f"{res['skor_pengharapan']}/{res['max_per_kategori']}")
        st.markdown(f"**Total Skor: {res['total_skor']}/{res['max_total']}**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kasih %", f"{res['kasih']:.1f}%")
        col2.metric("Iman %", f"{res['iman']:.1f}%")
        col3.metric("Pengharapan %", f"{res['pengharapan']:.1f}%")
        img_path = Path(__file__).parent.parent / "assets" / "stomata_hati_1.jpg"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.warning("⚠️ Gambar belum tersedia")
        sisi = res['sisi_list']
        st.markdown(f"**Posisi Stomata Hati:** {', '.join([SISI_NAMES[s] for s in sisi])}")
        with st.expander("📖 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"{no}. {nama}")
        if st.button("Mulai Lagi (Soal Sama)"):
            st.session_state.tanggapan_submitted = False
            st.rerun()