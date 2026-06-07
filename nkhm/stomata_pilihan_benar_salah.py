# nkhm/stomata_pilihan_benar_salah.py
import streamlit as st
import random
import json
from pathlib import Path

# ========== MEMBACA SOAL DARI FILE JSON ==========
def load_soal_from_json(folder_name):
    """
    Membaca SEMUA file JSON dari folder tertentu.
    Struktur: soal_stomata_hati/pilihan_benar_salah/{folder_name}/
    Setiap soal harus memiliki field 'teks' dan 'jawaban' (Benar/Salah)
    """
    base_path = Path(__file__).parent / "soal_stomata_hati" / "pilihan_benar_salah" / folder_name
    all_soal = []
    
    if not base_path.exists():
        st.warning(f"⚠️ Folder {base_path} tidak ditemukan")
        return []
    
    json_files = sorted(base_path.glob("*.json"))
    if not json_files:
        st.warning(f"⚠️ Tidak ada file JSON di {base_path}")
        return []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if "teks" in item and "jawaban" in item:
                            all_soal.append(item)
                        else:
                            st.warning(f"⚠️ Soal di {json_file.name} tidak valid (missing 'teks' or 'jawaban')")
                else:
                    st.warning(f"⚠️ Format {json_file.name} bukan list")
        except Exception as e:
            st.warning(f"⚠️ Error baca {json_file.name}: {e}")
    
    return all_soal

def get_random_soals():
    """Mengambil 11 soal acak per kategori untuk mode benar/salah"""
    try:
        soal_kasih = load_soal_from_json("kasih")
        soal_iman = load_soal_from_json("iman")
        soal_pengharapan = load_soal_from_json("pengharapan")
        
        with st.expander("📊 Bank Soal (Benar/Salah)", expanded=False):
            st.markdown(f"**Kasih:** {len(soal_kasih)} soal")
            st.markdown(f"**Iman:** {len(soal_iman)} soal")
            st.markdown(f"**Pengharapan:** {len(soal_pengharapan)} soal")
        
        if len(soal_kasih) < 11 or len(soal_iman) < 11 or len(soal_pengharapan) < 11:
            st.error(f"Jumlah soal tidak cukup (min 11 per kategori). Kasih={len(soal_kasih)}, Iman={len(soal_iman)}, Pengharapan={len(soal_pengharapan)}")
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
                "pilihan": ["Benar", "Salah"],
                "jawaban": s["jawaban"]
            })
        for s in sample_iman:
            all_soal.append({
                "kategori": "Iman",
                "id": s.get("id", 0),
                "teks": s["teks"],
                "pilihan": ["Benar", "Salah"],
                "jawaban": s["jawaban"]
            })
        for s in sample_pengharapan:
            all_soal.append({
                "kategori": "Pengharapan",
                "id": s.get("id", 0),
                "teks": s["teks"],
                "pilihan": ["Benar", "Salah"],
                "jawaban": s["jawaban"]
            })
        random.shuffle(all_soal)
        return all_soal
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return []

# ========== SISI NAMES dan FUNGSI PENDUKUNG ==========
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

# ========== STATE MANAGEMENT ==========
def init_pilihan_state():
    prefix = "pilihan_bs_"
    if f"{prefix}answers" not in st.session_state:
        st.session_state[f"{prefix}answers"] = {}
    if f"{prefix}submitted" not in st.session_state:
        st.session_state[f"{prefix}submitted"] = False
    if f"{prefix}results" not in st.session_state:
        st.session_state[f"{prefix}results"] = None
    if f"{prefix}soal_version" not in st.session_state:
        st.session_state[f"{prefix}soal_version"] = 0
    if f"{prefix}all_soal" not in st.session_state:
        st.session_state[f"{prefix}all_soal"] = get_random_soals()
    if f"{prefix}official_score" not in st.session_state:
        st.session_state[f"{prefix}official_score"] = None
    if f"{prefix}has_official_score" not in st.session_state:
        st.session_state[f"{prefix}has_official_score"] = False

def force_refresh_questions():
    prefix = "pilihan_bs_"
    new_soals = get_random_soals()
    if new_soals:
        st.session_state[f"{prefix}all_soal"] = new_soals
    else:
        st.error("Gagal memuat soal baru.")
    st.session_state[f"{prefix}answers"] = {}
    st.session_state[f"{prefix}submitted"] = False
    st.session_state[f"{prefix}results"] = None
    st.session_state[f"{prefix}soal_version"] += 1

def hide_results():
    prefix = "pilihan_bs_"
    st.session_state[f"{prefix}submitted"] = False
    st.session_state[f"{prefix}results"] = None

def tampilkan_hasil():
    prefix = "pilihan_bs_"
    soal_list = st.session_state[f"{prefix}all_soal"]
    if not soal_list:
        return False
    total_soal = len(soal_list)
    if len(st.session_state[f"{prefix}answers"]) < total_soal:
        st.error(f"⚠️ Anda baru menjawab {len(st.session_state[f'{prefix}answers'])} dari {total_soal} soal.")
        return False
    
    skor_kasih = skor_iman = skor_pengharapan = 0
    for idx, soal in enumerate(soal_list):
        jawaban = st.session_state[f"{prefix}answers"].get(idx)
        if jawaban and jawaban == soal["jawaban"]:
            if soal['kategori'] == "Kasih": skor_kasih += 1
            elif soal['kategori'] == "Iman": skor_iman += 1
            else: skor_pengharapan += 1
    
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
    if not st.session_state[f"{prefix}has_official_score"]:
        st.session_state[f"{prefix}official_score"] = hasil
        st.session_state[f"{prefix}has_official_score"] = True
        hasil["is_official"] = True
    else:
        hasil["is_official"] = False
    st.session_state[f"{prefix}results"] = hasil
    st.session_state[f"{prefix}submitted"] = True
    return True

# ========== UI UTAMA ==========
def show_pilihan_benar_salah():
    init_pilihan_state()
    prefix = "pilihan_bs_"

    st.markdown("## ✅ Sto-mata Hati - Mode Pilihan Benar/Salah")
    st.markdown("""
    **Alat Uji Tingkat Iman, Kasih, dan Pengharapan (IKP)**  
    Anda akan menjawab **33 pernyataan** (11 per kategori) dengan memilih **Benar** atau **Salah**.  
    Setiap jawaban benar bernilai **1 poin**. Maksimal skor per kategori 11, total 33.
    """)

    # Tampilkan skor resmi jika sudah ada
    if st.session_state[f"{prefix}has_official_score"] and st.session_state[f"{prefix}official_score"]:
        off = st.session_state[f"{prefix}official_score"]
        st.markdown("---")
        st.markdown("### 🏆 SKOR RESMI ANDA (Benar/Salah) 🏆")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kasih", f"{off['skor_kasih']}/11")
        col2.metric("Iman", f"{off['skor_iman']}/11")
        col3.metric("Pengharapan", f"{off['skor_pengharapan']}/11")
        st.markdown(f"**Total: {off['total_skor']}/33**")
        st.info(f"Posisi: {', '.join([SISI_NAMES[s] for s in off['sisi_list']])}")
        st.markdown("---")
        st.markdown("### ✨ MODE LATIHAN ✨")
        st.caption("Permainan selanjutnya hanya latihan, tidak mengubah skor resmi.")
        st.markdown("---")
    else:
        st.info("🎯 Permainan pertama (Benar/Salah). Jawab semua soal dengan jujur.")

    soal_list = st.session_state[f"{prefix}all_soal"]
    if not soal_list:
        st.error("❌ Gagal memuat soal. Pastikan folder 'soal_stomata_hati/pilihan_benar_salah/...' berisi file JSON.")
        return

    total_soal = len(soal_list)
    jawaban_terjawab = len(st.session_state[f"{prefix}answers"])
    st.markdown(f"**📝 Soal terjawab: {jawaban_terjawab}/{total_soal}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Ganti Soal (Baru)", use_container_width=True):
            force_refresh_questions()
            st.rerun()
    with col2:
        if st.button("🗑️ Reset Jawaban", use_container_width=True):
            hide_results()
            st.rerun()

    with st.container(height=500):
        for idx, soal in enumerate(soal_list):
            key = f"pilihan_bs_{idx}_{soal['id']}_v{st.session_state[f'{prefix}soal_version']}"
            current = st.session_state[f"{prefix}answers"].get(idx)
            selected = st.radio(
                f"**{idx+1}. [{soal['kategori']}]** {soal['teks']}",
                soal['pilihan'],
                index=soal['pilihan'].index(current) if current in soal['pilihan'] else None,
                key=key, label_visibility="collapsed", horizontal=True
            )
            if selected != current:
                st.session_state[f"{prefix}answers"][idx] = selected
                if st.session_state[f"{prefix}submitted"]:
                    hide_results()
                st.rerun()

    st.progress(jawaban_terjawab / total_soal, text=f"Progress: {jawaban_terjawab}/{total_soal}")

    if st.button("📊 Lihat Hasil", type="primary"):
        if tampilkan_hasil():
            st.rerun()

    # Tampilkan hasil jika sudah submit
    if st.session_state[f"{prefix}submitted"] and st.session_state[f"{prefix}results"]:
        res = st.session_state[f"{prefix}results"]
        if res.get("is_official"):
            st.success("🎉 Skor resmi tersimpan!")
        else:
            st.info("📝 Hasil latihan (tidak mengubah skor resmi)")

        with st.expander("📈 Detail Skor"):
            st.metric("Kasih", f"{res['skor_kasih']}/{res['max_per_kategori']}")
            st.metric("Iman", f"{res['skor_iman']}/{res['max_per_kategori']}")
            st.metric("Pengharapan", f"{res['skor_pengharapan']}/{res['max_per_kategori']}")
        st.markdown(f"**Total Skor: {res['total_skor']}/{res['max_total']}**")

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Kasih %", f"{res['kasih']:.1f}%")
        col_b.metric("Iman %", f"{res['iman']:.1f}%")
        col_c.metric("Pengharapan %", f"{res['pengharapan']:.1f}%")

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
            st.session_state[f"{prefix}submitted"] = False
            st.rerun()

if __name__ == "__main__":
    show_pilihan_benar_salah()