# nkhm/stomata_pilihan_benar_salah.py
import streamlit as st
import random
import json
from pathlib import Path

# ========== KONSTANTA ==========
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

# ========== BACA SOAL DARI JSON ==========
def baca_soal_dari_folder(kategori):
    """
    Membaca semua file JSON dari:
    nkhm/soal_stomata_hati/pilihan_benar_salah/{kategori}/
    """
    # Path: nkhm/stomata_pilihan_benar_salah.py -> parent = nkhm/
    # Maka soal_stomata_hati berada di folder yang sama dengan nkhm? TIDAK.
    # Struktur Anda: nkhm/soal_stomata_hati/... 
    # Jadi path = nkhm/soal_stomata_hati/pilihan_benar_salah/{kategori}
    base_path = Path(__file__).parent / "soal_stomata_hati" / "pilihan_benar_salah" / kategori
    semua_soal = []
    
    if not base_path.exists():
        st.error(f"❌ Folder tidak ditemukan: `{base_path}`")
        st.info(f"Pastikan folder `{base_path}` ada dan berisi file JSON.")
        return []
    
    json_files = list(base_path.glob("*.json"))
    if not json_files:
        st.warning(f"⚠️ Tidak ada file .json di `{base_path}`")
        return []
    
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if "teks" in item and "jawaban" in item:
                            semua_soal.append(item)
                        else:
                            st.warning(f"Soal di `{file.name}` tidak memiliki 'teks' atau 'jawaban'")
                else:
                    st.warning(f"File `{file.name}` bukan list JSON")
        except Exception as e:
            st.error(f"Gagal membaca `{file.name}`: {e}")
    
    return semua_soal

def siapkan_33_soal():
    """Mengambil 11 acak dari setiap kategori, total 33 soal"""
    soal_kasih = baca_soal_dari_folder("kasih")
    soal_iman = baca_soal_dari_folder("iman")
    soal_pengharapan = baca_soal_dari_folder("pengharapan")
    
    # Tampilkan info jumlah soal
    with st.expander("📚 Info Bank Soal (Benar/Salah)", expanded=True):
        st.write(f"**Kasih:** {len(soal_kasih)} soal ditemukan")
        st.write(f"**Iman:** {len(soal_iman)} soal ditemukan")
        st.write(f"**Pengharapan:** {len(soal_pengharapan)} soal ditemukan")
        if len(soal_kasih) < 11 or len(soal_iman) < 11 or len(soal_pengharapan) < 11:
            st.warning("⚠️ Minimal 11 soal per kategori agar game bisa berjalan.")
    
    if len(soal_kasih) < 11 or len(soal_iman) < 11 or len(soal_pengharapan) < 11:
        return []
    
    sampel_kasih = random.sample(soal_kasih, 11)
    sampel_iman = random.sample(soal_iman, 11)
    sampel_pengharapan = random.sample(soal_pengharapan, 11)
    
    semua = []
    for s in sampel_kasih:
        semua.append({
            "kategori": "Kasih",
            "id": s.get("id", 0),
            "teks": s["teks"],
            "jawaban_benar": s["jawaban"]
        })
    for s in sampel_iman:
        semua.append({
            "kategori": "Iman",
            "id": s.get("id", 0),
            "teks": s["teks"],
            "jawaban_benar": s["jawaban"]
        })
    for s in sampel_pengharapan:
        semua.append({
            "kategori": "Pengharapan",
            "id": s.get("id", 0),
            "teks": s["teks"],
            "jawaban_benar": s["jawaban"]
        })
    random.shuffle(semua)
    return semua

# ========== STATE ==========
def init_state():
    if "bs_answers" not in st.session_state:
        st.session_state.bs_answers = {}
    if "bs_submitted" not in st.session_state:
        st.session_state.bs_submitted = False
    if "bs_results" not in st.session_state:
        st.session_state.bs_results = None
    if "bs_soal" not in st.session_state:
        st.session_state.bs_soal = siapkan_33_soal()
    if "bs_official_score" not in st.session_state:
        st.session_state.bs_official_score = None
    if "bs_has_official" not in st.session_state:
        st.session_state.bs_has_official = False

def reset_jawaban():
    st.session_state.bs_answers = {}
    st.session_state.bs_submitted = False
    st.session_state.bs_results = None

def ganti_soal():
    st.session_state.bs_soal = siapkan_33_soal()
    reset_jawaban()

def hitung_dan_simpan_hasil():
    soal_list = st.session_state.bs_soal
    if not soal_list:
        return False
    if len(st.session_state.bs_answers) < len(soal_list):
        st.error(f"Jawab semua {len(soal_list)} soal terlebih dahulu!")
        return False
    
    skor_kasih = skor_iman = skor_pengharapan = 0
    for idx, soal in enumerate(soal_list):
        jawab = st.session_state.bs_answers.get(idx)
        if jawab == soal["jawaban_benar"]:
            if soal["kategori"] == "Kasih":
                skor_kasih += 1
            elif soal["kategori"] == "Iman":
                skor_iman += 1
            else:
                skor_pengharapan += 1
    
    max_kat = 11
    persen_kasih = hitung_persentase(skor_kasih, max_kat)
    persen_iman = hitung_persentase(skor_iman, max_kat)
    persen_pengharapan = hitung_persentase(skor_pengharapan, max_kat)
    sisi = tentukan_posisi(persen_kasih, persen_iman, persen_pengharapan)
    total = skor_kasih + skor_iman + skor_pengharapan
    
    hasil = {
        "kasih": persen_kasih, "iman": persen_iman, "pengharapan": persen_pengharapan,
        "sisi_list": sisi,
        "skor_kasih": skor_kasih, "skor_iman": skor_iman, "skor_pengharapan": skor_pengharapan,
        "total_skor": total, "max_kat": max_kat, "max_total": 33,
    }
    if not st.session_state.bs_has_official:
        st.session_state.bs_official_score = hasil
        st.session_state.bs_has_official = True
        hasil["is_official"] = True
    else:
        hasil["is_official"] = False
    st.session_state.bs_results = hasil
    st.session_state.bs_submitted = True
    return True

# ========== UI ==========
def show_pilihan_benar_salah():
    init_state()
    st.markdown("## ✅ Mode Pilihan Benar/Salah")
    st.markdown("Jawab **33 pernyataan** dengan memilih **Benar** atau **Salah**. Setiap jawaban benar = 1 poin.")
    
    # Tampilkan skor resmi jika ada
    if st.session_state.bs_has_official and st.session_state.bs_official_score:
        off = st.session_state.bs_official_score
        st.markdown("---")
        st.markdown("### 🏆 SKOR RESMI ANDA (Benar/Salah)")
        col1, col2, col3 = st.columns(3)
        col1.metric("💖 Kasih", f"{off['skor_kasih']} / 11")
        col2.metric("🙏 Iman", f"{off['skor_iman']} / 11")
        col3.metric("✨ Pengharapan", f"{off['skor_pengharapan']} / 11")
        st.markdown(f"### **Total: {off['total_skor']} / 33**")
        st.info(f"🌿 Posisi: {', '.join([SISI_NAMES[s] for s in off['sisi_list']])}")
        st.markdown("---")
        st.markdown("### ✨ MODE LATIHAN ✨")
        st.caption("Permainan selanjutnya hanya latihan, tidak mengubah skor resmi.")
        st.markdown("---")
    
    soal_list = st.session_state.bs_soal
    if not soal_list:
        st.error("❌ Gagal memuat soal. Periksa folder `soal_stomata_hati/pilihan_benar_salah/...` dan file JSON.")
        return
    
    total_soal = len(soal_list)
    terjawab = len(st.session_state.bs_answers)
    st.markdown(f"### 📝 Soal terjawab: **{terjawab} / {total_soal}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ganti Soal (Baru)", use_container_width=True):
            ganti_soal()
            st.rerun()
    with col2:
        if st.button("🗑️ Reset Jawaban", use_container_width=True):
            reset_jawaban()
            st.rerun()
    
    st.markdown("---")
    
    # Tampilkan semua soal dalam container scroll
    with st.container(height=500):
        for idx, soal in enumerate(soal_list):
            key = f"bs_{idx}_{soal['id']}"
            current = st.session_state.bs_answers.get(idx)
            pilihan = st.radio(
                f"**{idx+1}. [{soal['kategori']}]** {soal['teks']}",
                ["Benar", "Salah"],
                index=0 if current == "Benar" else (1 if current == "Salah" else None),
                key=key,
                horizontal=True,
                label_visibility="collapsed"
            )
            if pilihan != current:
                st.session_state.bs_answers[idx] = pilihan
                if st.session_state.bs_submitted:
                    st.session_state.bs_submitted = False
                st.rerun()
            st.markdown("---")
    
    st.progress(terjawab / total_soal, text=f"Progress: {terjawab}/{total_soal}")
    
    if st.button("📊 Lihat Hasil", use_container_width=True, type="primary"):
        if hitung_dan_simpan_hasil():
            st.rerun()
    
    # Tampilkan hasil jika sudah submit
    if st.session_state.bs_submitted and st.session_state.bs_results:
        res = st.session_state.bs_results
        st.markdown("---")
        if res.get("is_official"):
            st.success("🎉 Skor resmi telah disimpan! 🎉")
        else:
            st.info("📝 Hasil latihan (tidak mengubah skor resmi)")
        
        with st.expander("📈 Detail Skor"):
            st.metric("Kasih", f"{res['skor_kasih']} / {res['max_kat']}")
            st.metric("Iman", f"{res['skor_iman']} / {res['max_kat']}")
            st.metric("Pengharapan", f"{res['skor_pengharapan']} / {res['max_kat']}")
        st.markdown(f"### **Total Skor: {res['total_skor']} / {res['max_total']}**")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Kasih %", f"{res['kasih']:.1f}%")
        col_b.metric("Iman %", f"{res['iman']:.1f}%")
        col_c.metric("Pengharapan %", f"{res['pengharapan']:.1f}%")
        
        img_path = Path(__file__).parent.parent / "assets" / "stomata_hati_1.jpg"
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.warning("Gambar stomata_hati_1.jpg belum tersedia.")
        
        sisi = res['sisi_list']
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
            if st.button("📝 Lanjutkan (Soal Sama)"):
                st.session_state.bs_submitted = False
                st.rerun()

if __name__ == "__main__":
    show_pilihan_benar_salah()