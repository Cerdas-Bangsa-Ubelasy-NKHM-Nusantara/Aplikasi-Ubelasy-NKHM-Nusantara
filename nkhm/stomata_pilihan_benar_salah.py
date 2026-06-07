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
        return [1] if rk == max_val else [2] if ri == max_val else [3]
    elif (rk >= 40 and ri >= 40) or (ri >= 40 and rp >= 40) or (rp >= 40 and rk >= 40):
        if rk >= 40 and ri >= 40: return [5]
        if ri >= 40 and rp >= 40: return [4]
        if rp >= 40 and rk >= 40: return [6]
        return [10]
    else:
        return [9] if rk == max_val else [7] if ri == max_val else [8]

def baca_semua_soal(kategori):
    # Path ke file ini: nkhm/stomata_pilihan_benar_salah.py
    current_dir = Path(__file__).resolve().parent  # nkhm/
    base_path = current_dir / "soal_stomata_hati" / "pilihan_benar_salah" / kategori
    st.write(f"🔍 DEBUG: Mencari folder `{base_path}`")
    if not base_path.exists():
        st.error(f"❌ Folder tidak ditemukan: {base_path}")
        st.info("Pastikan struktur folder: `nkhm/soal_stomata_hati/pilihan_benar_salah/iman/`, `kasih/`, `pengharapan/`")
        return []
    files = list(base_path.glob("*.json"))
    if not files:
        st.warning(f"⚠️ Tidak ada file .json di {base_path}")
        return []
    semua = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    for item in data:
                        if "teks" in item and "jawaban" in item:
                            semua.append(item)
                        else:
                            st.warning(f"⚠️ Item di {f.name} tidak punya 'teks' atau 'jawaban'")
                else:
                    st.warning(f"⚠️ {f.name} bukan list JSON")
        except Exception as e:
            st.error(f"❌ Gagal baca {f.name}: {e}")
    return semua

def siapkan_33_soal():
    st.write("🔍 DEBUG: Memuat soal...")
    soal_kasih = baca_semua_soal("kasih")
    soal_iman = baca_semua_soal("iman")
    soal_pengharapan = baca_semua_soal("pengharapan")
    
    st.write(f"Jumlah soal: Kasih={len(soal_kasih)}, Iman={len(soal_iman)}, Pengharapan={len(soal_pengharapan)}")
    
    if len(soal_kasih) < 11 or len(soal_iman) < 11 or len(soal_pengharapan) < 11:
        st.error(f"❌ Jumlah soal tidak mencukupi (minimal 11 per kategori)")
        return []
    
    sampel_kasih = random.sample(soal_kasih, 11)
    sampel_iman = random.sample(soal_iman, 11)
    sampel_pengharapan = random.sample(soal_pengharapan, 11)
    
    semua = []
    for s in sampel_kasih:
        semua.append({"kategori": "Kasih", "id": s.get("id",0), "teks": s["teks"], "jawaban_benar": s["jawaban"]})
    for s in sampel_iman:
        semua.append({"kategori": "Iman", "id": s.get("id",0), "teks": s["teks"], "jawaban_benar": s["jawaban"]})
    for s in sampel_pengharapan:
        semua.append({"kategori": "Pengharapan", "id": s.get("id",0), "teks": s["teks"], "jawaban_benar": s["jawaban"]})
    random.shuffle(semua)
    st.success(f"✅ Berhasil memuat {len(semua)} soal (11 per kategori)")
    return semua

def init():
    if "pbs_answers" not in st.session_state:
        st.session_state.pbs_answers = {}
    if "pbs_submitted" not in st.session_state:
        st.session_state.pbs_submitted = False
    if "pbs_results" not in st.session_state:
        st.session_state.pbs_results = None
    if "pbs_soal" not in st.session_state:
        st.session_state.pbs_soal = siapkan_33_soal()
    if "pbs_official" not in st.session_state:
        st.session_state.pbs_official = None
    if "pbs_has_official" not in st.session_state:
        st.session_state.pbs_has_official = False

def reset_jawaban():
    st.session_state.pbs_answers = {}
    st.session_state.pbs_submitted = False
    st.session_state.pbs_results = None

def ganti_soal():
    st.session_state.pbs_soal = siapkan_33_soal()
    reset_jawaban()

def hitung_hasil():
    soal = st.session_state.pbs_soal
    if not soal:
        return False
    if len(st.session_state.pbs_answers) < len(soal):
        st.error(f"Jawab dulu {len(soal)} soal")
        return False
    skor = {"Kasih":0, "Iman":0, "Pengharapan":0}
    for i, s in enumerate(soal):
        if st.session_state.pbs_answers.get(i) == s["jawaban_benar"]:
            skor[s["kategori"]] += 1
    max_kat = 11
    persen = {k: hitung_persentase(v, max_kat) for k,v in skor.items()}
    sisi = tentukan_posisi(persen["Kasih"], persen["Iman"], persen["Pengharapan"])
    total = sum(skor.values())
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
    init()
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
        st.info(f"Posisi: {', '.join([SISI_NAMES[s] for s in off['sisi_list']])}")
        st.markdown("---")
        st.markdown("### ✨ MODE LATIHAN ✨")
    else:
        st.info("🎯 Permainan pertama. Jawab semua dengan jujur.")
    
    soal_list = st.session_state.pbs_soal
    if not soal_list:
        st.error("❌ Gagal memuat soal. Periksa debug di atas.")
        return
    
    terjawab = len(st.session_state.pbs_answers)
    total = len(soal_list)
    st.markdown(f"📝 **Soal terjawab: {terjawab}/{total}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ganti Soal (Baru)"):
            ganti_soal()
            st.rerun()
    with col2:
        if st.button("🗑️ Reset Jawaban"):
            reset_jawaban()
            st.rerun()
    
    with st.container(height=500):
        for i, soal in enumerate(soal_list):
            key = f"pbs_{i}_{soal['id']}"
            curr = st.session_state.pbs_answers.get(i)
            pilih = st.radio(
                f"**{i+1}. [{soal['kategori']}]** {soal['teks']}",
                ["Benar", "Salah"],
                index=0 if curr=="Benar" else (1 if curr=="Salah" else None),
                key=key, horizontal=True, label_visibility="collapsed"
            )
            if pilih != curr:
                st.session_state.pbs_answers[i] = pilih
                st.session_state.pbs_submitted = False
                st.rerun()
    
    st.progress(terjawab/total, text=f"Progress: {terjawab}/{total}")
    if st.button("📊 Lihat Hasil", use_container_width=True, type="primary"):
        if hitung_hasil():
            st.rerun()
    
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
        else:
            st.warning("Gambar stomata_hati_1.jpg belum tersedia.")
        
        sisi = r['sisi_list']
        nama_sisi = [SISI_NAMES[s] for s in sisi]
        st.markdown(f"### 🌿 Posisi Stomata Hati: **{', '.join(nama_sisi)}**")
        with st.expander("📖 12 Sisi Stomata Hati"):
            for no, nama in SISI_NAMES.items():
                st.markdown(f"{no}. {nama}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Latihan Lagi (Soal Baru)"):
                ganti_soal()
                st.rerun()
        with col2:
            if st.button("📝 Lanjut (Soal Sama)"):
                st.session_state.pbs_submitted = False
                st.rerun()

if __name__ == "__main__":
    show_pilihan_benar_salah()