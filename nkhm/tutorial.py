# nkhm/tutorial.py
"""
Modul Tutorial untuk NKHM Nusantara.
Berisi panduan lengkap semua fitur aplikasi.
"""

import streamlit as st
import logging

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== CSS KUSTOM UNTUK TUTORIAL ==========
def inject_tutorial_css():
    """Menambahkan CSS kustom untuk tampilan tutorial."""
    st.markdown("""
    <style>
    .tutorial-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    .tutorial-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 4px solid #2e7daf;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .tutorial-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .tutorial-card h3 {
        color: #1a3c6e;
        margin-top: 0;
        margin-bottom: 10px;
    }
    .tutorial-card ul {
        padding-left: 20px;
        margin-bottom: 0;
    }
    .tutorial-card li {
        margin: 6px 0;
        line-height: 1.6;
    }
    .tutorial-step {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        padding: 10px 0;
        border-bottom: 1px solid #e9ecef;
    }
    .tutorial-step:last-child {
        border-bottom: none;
    }
    .tutorial-number {
        background-color: #2e7daf;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
        font-size: 14px;
    }
    .tutorial-icon {
        font-size: 28px;
        margin-right: 10px;
    }
    .tutorial-tip {
        background-color: #e8f0fe;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
        border-left: 4px solid #2e7daf;
    }
    .tutorial-warning {
        background-color: #fff3cd;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    .tutorial-success {
        background-color: #d4edda;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    .dark-mode .tutorial-card {
        background-color: #1a1a2e;
        border-left-color: #4a8abf;
    }
    .dark-mode .tutorial-card h3 {
        color: #7ab7e0;
    }
    .dark-mode .tutorial-step {
        border-bottom-color: #333;
    }
    .dark-mode .tutorial-tip {
        background-color: #1a1a3a;
        border-left-color: #4a8abf;
    }
    .dark-mode .tutorial-warning {
        background-color: #2a2a0a;
        border-left-color: #ffc107;
    }
    .dark-mode .tutorial-success {
        background-color: #0a2a1a;
        border-left-color: #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

# ========== FUNGSI BANTU ==========
def create_step(number, icon, title, description):
    """Membuat elemen step tutorial."""
    return f"""
    <div class="tutorial-step">
        <div class="tutorial-number">{number}</div>
        <div>
            <div style="font-weight: bold; font-size: 16px;">
                <span class="tutorial-icon">{icon}</span> {title}
            </div>
            <div style="color: #555; margin-top: 4px; line-height: 1.6;">{description}</div>
        </div>
    </div>
    """

# ========== KONTEN TUTORIAL ==========
def show_tutorial_umum():
    """Tutorial umum tentang aplikasi NKHM."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            🌿 Selamat Datang di NKHM Nusantara
        </h2>
        
        <div style="text-align: center; margin-bottom: 30px; font-size: 16px; color: #555;">
            Aplikasi pembelajaran berbasis kecerdasan untuk mengembangkan 
            <strong>IQ, EQ, SQ, AQ</strong> dan <strong>Nasionalisme</strong>.
        </div>
        
        <div class="tutorial-card">
            <h3>🎯 Apa itu NKHM?</h3>
            <p>
                <strong>NKHM</strong> adalah singkatan dari <strong>Nusantara Kecerdasan Hati dan Minda</strong>.
                Aplikasi ini dirancang untuk mengembangkan 4 kecerdasan utama:
            </p>
            <ul>
                <li><strong>🧠 IQ (Intelligence Quotient)</strong> – Kecerdasan intelektual, logika, dan analisis</li>
                <li><strong>❤️ EQ (Emotional Quotient)</strong> – Kecerdasan emosional, empati, dan sosial</li>
                <li><strong>🙏 SQ (Spiritual Quotient)</strong> – Kecerdasan spiritual, nilai, dan makna hidup</li>
                <li><strong>💪 AQ (Adversity Quotient)</strong> – Kecerdasan menghadapi tantangan dan kesulitan</li>
                <li><strong>🇮🇩 Nasionalisme</strong> – Cinta tanah air dan kebangsaan</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>📊 Rumus NKHM</h3>
            <div style="background-color: #e8f0fe; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 16px;">
                <strong>NKHM_Q</strong> = ((IQ + EQ) × (SQ + AQ)) / ((IQ + EQ) + (SQ + AQ))
                <br><br>
                <strong>NKHM_Total</strong> = (NKHM_Q + Nasionalisme) / 2
            </div>
            <p style="margin-top: 10px; font-size: 14px; color: #666;">
                💡 Semakin tinggi NKHM Total, semakin baik perkembangan kecerdasan Anda!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_kuis():
    """Tutorial fitur Kuis."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            🎮 Fitur Kuis
        </h2>
        
        <div class="tutorial-card">
            <h3>📝 Cara Menggunakan Kuis</h3>
            
            <div class="tutorial-step">
                <div class="tutorial-number">1</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Pilih Filter Soal</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Gunakan filter <strong>Kategori</strong> (Semua, Nasionalisme, Umum) dan 
                        <strong>Fokus</strong> (Semua, IQ, EQ, SQ, AQ, Nasionalisme) untuk memilih jenis soal.
                    </div>
                </div>
            </div>
            
            <div class="tutorial-step">
                <div class="tutorial-number">2</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Baca Soal dengan Seksama</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Setiap soal memiliki teks dan pilihan jawaban. Pilih jawaban yang menurut Anda benar.
                    </div>
                </div>
            </div>
            
            <div class="tutorial-step">
                <div class="tutorial-number">3</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Klik "JAWAB"</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Setelah memilih jawaban, klik tombol <strong>JAWAB</strong> untuk mengirimkan jawaban.
                    </div>
                </div>
            </div>
            
            <div class="tutorial-step">
                <div class="tutorial-number">4</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Lihat Feedback</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Setelah menjawab, Anda akan melihat feedback <strong>✅ BENAR</strong> atau <strong>❌ SALAH</strong>.
                        Jawaban benar akan menambah poin sesuai kategori.
                    </div>
                </div>
            </div>
            
            <div class="tutorial-step">
                <div class="tutorial-number">5</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Navigasi ke Soal Berikutnya</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Gunakan tombol <strong>⏩ SOAL BERIKUTNYA</strong> untuk melanjutkan ke soal berikutnya,
                        atau <strong>🔄 KUIS BARU</strong> untuk memulai ulang dari awal.
                    </div>
                </div>
            </div>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips:</strong> Kerjakan soal sebanyak-banyaknya untuk meningkatkan skor NKHM Anda!
            Setiap jawaban benar akan menambah poin pada kategori yang bersangkutan.
        </div>
        
        <div class="tutorial-warning">
            ⚠️ <strong>Perhatikan:</strong> Soal dengan filter berbeda akan menghasilkan soal yang berbeda pula.
            Ganti filter untuk variasi soal yang lebih banyak.
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_dasbor():
    """Tutorial fitur Dasbor."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            📊 Fitur Dasbor
        </h2>
        
        <div class="tutorial-card">
            <h3>👤 Dasbor Saya</h3>
            <p>Dasbor menampilkan ringkasan perkembangan dan rekomendasi personal Anda.</p>
            
            <h4>📋 Ringkasan & Progres</h4>
            <ul>
                <li><strong>👤 Nama Pengguna</strong> – Nama yang Anda gunakan saat login</li>
                <li><strong>📖 Total Soal Dikerjakan</strong> – Jumlah soal yang sudah Anda jawab</li>
                <li><strong>🏆 NKHM Total</strong> – Skor NKHM keseluruhan Anda</li>
                <li><strong>📈 Perkembangan NKHM</strong> – Grafik perkembangan skor Anda</li>
                <li><strong>🧠 Analisis Kecerdasan</strong> – Skor per kategori (IQ, EQ, SQ, AQ, Nasionalisme)</li>
                <li><strong>💡 Rekomendasi Personal</strong> – Saran untuk meningkatkan setiap kategori</li>
                <li><strong>📋 Riwayat Terbaru</strong> – 5 soal terakhir yang Anda kerjakan</li>
                <li><strong>🎯 Target Berikutnya</strong> – Target skor berikutnya untuk dicapai</li>
            </ul>
            
            <h4>📝 Catatan</h4>
            <ul>
                <li><strong>✏️ Catatan Cepat</strong> – Tulis catatan harian atau ide belajar</li>
                <li><strong>📱 Catatan Pribadi (React)</strong> – Aplikasi catatan interaktif dengan fitur lengkap</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>📊 Dasbor NKHM</h3>
            <ul>
                <li><strong>🧠 NKHM_Q</strong> – Skor kombinasi IQ, EQ, SQ, dan AQ</li>
                <li><strong>🏆 NKHM Total</strong> – Gabungan NKHM_Q dan Nasionalisme</li>
                <li><strong>📊 Grafik Skor</strong> – Visualisasi skor per kategori</li>
                <li><strong>📖 Tentang Rumus</strong> – Penjelasan rumus perhitungan NKHM</li>
            </ul>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips:</strong> Gunakan fitur <strong>Catatan</strong> untuk mencatat hal-hal penting yang Anda pelajari.
            Catatan disimpan di server dan bisa diakses kembali kapan saja.
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_prestasi():
    """Tutorial fitur Prestasi."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            🏆 Fitur Prestasi
        </h2>
        
        <div class="tutorial-card">
            <h3>🏅 Pencapaian</h3>
            <p>Fitur ini menampilkan badge yang Anda peroleh berdasarkan pencapaian:</p>
            <ul>
                <li><strong>🧠 Cendekia</strong> – IQ ≥ 50</li>
                <li><strong>❤️ Empati</strong> – EQ ≥ 50</li>
                <li><strong>🙏 Bhinneka</strong> – SQ ≥ 50</li>
                <li><strong>💪 Tangguh</strong> – AQ ≥ 50</li>
                <li><strong>🇮🇩 Patriot</strong> – Nasionalisme ≥ 50</li>
                <li><strong>🌟 Pahlawan Cerdas Nusantara</strong> – Semua kategori ≥ 50</li>
            </ul>
            <p>Jika semua kategori ≥ 50, Anda akan mendapatkan gelar <strong>PAHLAWAN CERDAS NUSANTARA</strong>! 🎉</p>
        </div>
        
        <div class="tutorial-card">
            <h3>📊 Statistik</h3>
            <ul>
                <li><strong>📖 Total Soal</strong> – Jumlah soal yang sudah dikerjakan</li>
                <li><strong>✅ Benar</strong> – Jumlah jawaban benar</li>
                <li><strong>📊 Akurasi</strong> – Persentase jawaban benar</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🏆 Leaderboard</h3>
            <ul>
                <li><strong>🏅 Peringkat</strong> – 10 pemain teratas berdasarkan skor NKHM</li>
                <li><strong>🎖️ Peraih Medali</strong> – 3 pemain teratas mendapat medali emas, perak, perunggu</li>
                <li><strong>📊 Statistik Kompetitif</strong> – Total peserta, rata-rata skor, skor tertinggi</li>
                <li><strong>🎯 Level & Progress</strong> – Level Anda dan progress menuju level berikutnya</li>
                <li><strong>📈 Tren Skor</strong> – Distribusi skor semua peserta</li>
            </ul>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips:</strong> Semakin tinggi skor Anda, semakin tinggi posisi Anda di leaderboard.
            Kejar posisi teratas dan raih medali emas! 🥇
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_tanding():
    """Tutorial fitur Tanding."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            ⚔️ Fitur Tanding
        </h2>
        
        <div class="tutorial-card">
            <h3>⚔️ Mode 1v1 (Hot Seat)</h3>
            <p>Dua pemain bergantian menjawab soal menggunakan <strong>perangkat yang sama</strong>.</p>
            
            <h4>📋 Cara Bermain:</h4>
            <div class="tutorial-step">
                <div class="tutorial-number">1</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Atur Pertandingan</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Masukkan nama kedua pemain, pilih jumlah soal (3, 5, 7, atau 10), 
                        dan tentukan waktu per giliran (15, 30, 45, atau 60 detik).
                    </div>
                </div>
            </div>
            
            <div class="tutorial-step">
                <div class="tutorial-number">2</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Bergantian Menjawab</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Pemain bergiliran menjawab soal. Pemain yang gilirannya sedang aktif 
                        harus menjawab sebelum waktu habis.
                    </div>
                </div>
            </div>
            
            <div class="tutorial-step">
                <div class="tutorial-number">3</div>
                <div>
                    <div style="font-weight: bold; font-size: 16px;">Lihat Hasil</div>
                    <div style="color: #555; margin-top: 4px; line-height: 1.6;">
                        Setelah semua soal selesai, aplikasi akan menampilkan pemenang 
                        berdasarkan poin tertinggi.
                    </div>
                </div>
            </div>
        </div>
        
        <div class="tutorial-card">
            <h3>🏆 Mode Turnamen Kelas</h3>
            <p>Sistem gugur untuk kompetisi antar peserta.</p>
            <ul>
                <li><strong>Peserta</strong> – Masukkan nama peserta (pisahkan dengan koma)</li>
                <li><strong>Bracket</strong> – Sistem pertandingan gugur</li>
                <li><strong>Pemenang</strong> – Peserta yang memenangkan semua pertandingan</li>
            </ul>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips:</strong> Mode Tanding sangat cocok untuk kompetisi di kelas atau antar teman.
            Semakin banyak soal, semakin seru pertandingannya!
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_karunia():
    """Tutorial fitur Karunia."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            🎁 Fitur Karunia Motivasi
        </h2>
        
        <div class="tutorial-card">
            <h3>📜 Karunia Umum</h3>
            <p>Tes untuk mengetahui 7 karunia motivasi Anda:</p>
            <ol>
                <li><strong>Bernubuat (Perceiver)</strong> – Melihat kebenaran, membedakan baik dan jahat</li>
                <li><strong>Melayani (Doer)</strong> – Menolong dan memenuhi kebutuhan praktis</li>
                <li><strong>Mengajar (Teacher)</strong> – Menyampaikan kebenaran secara logis</li>
                <li><strong>Menasihati (Encourager)</strong> – Mendorong dan memotivasi orang lain</li>
                <li><strong>Memberi (Giver)</strong> – Memberi dengan sukacita</li>
                <li><strong>Memimpin (Leader)</strong> – Memimpin dan mengarahkan orang lain</li>
                <li><strong>Berbelas Kasihan (Compassion)</strong> – Mengasihi dan menolong yang menderita</li>
            </ol>
            <p>
                <strong>Cara:</strong> Jawab 70 pernyataan dengan nilai 0-5. 
                Hasil akan menunjukkan 3 karunia tertinggi Anda.
            </p>
        </div>
        
        <div class="tutorial-card">
            <h3>✨ Karunia 140 Karakter</h3>
            <p>Versi lebih detail dengan 140 pernyataan untuk mengidentifikasi karunia motivasi.</p>
            <ul>
                <li>140 pernyataan dengan skala 0-5</li>
                <li>Hasil menunjukkan 3 karunia tertinggi</li>
                <li>Cocok untuk analisis yang lebih mendalam</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>📋 Karakter & Masalah</h3>
            <p>Menggabungkan 140 pernyataan karakteristik dengan 35 pernyataan masalah.</p>
            <ul>
                <li>Total 175 pernyataan</li>
                <li>Membantu mengidentifikasi potensi dan area pengembangan</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>💖 Sto-mata Hati</h3>
            <p>Alat uji tingkat Iman, Kasih, dan Pengharapan (IKP) dengan 3 mode:</p>
            <ul>
                <li><strong>📝 Tanggapan (Skala Likert)</strong> – 33 pernyataan dengan skala 0-4</li>
                <li><strong>✅ Pilihan Benar/Salah</strong> – 33 pernyataan benar/salah</li>
                <li><strong>🔢 Pilihan Ganda</strong> – 33 soal pilihan ganda (a, b, c, d)</li>
            </ul>
            <p>Hasil menunjukkan posisi Stomata Hati berdasarkan 12 sisi.</p>
        </div>
        
        <div class="tutorial-card">
            <h3>📚 Pengembangan Diri</h3>
            <p>Materi edukasi dalam format markdown untuk pengembangan diri dan literasi keuangan.</p>
            <ul>
                <li><strong>📚 Pengembangan Diri</strong> – Materi spiritual, mental, dan karakter</li>
                <li><strong>💰 Literasi Keuangan</strong> – Panduan mengelola keuangan dan investasi</li>
            </ul>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips:</strong> Tes karunia membantu Anda memahami potensi diri 
            dan area pengembangan dalam pelayanan.
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_hadiah():
    """Tutorial fitur Hadiah."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            🎁 Fitur Hadiah & Permainan
        </h2>
        
        <div class="tutorial-card">
            <h3>🦅 Tebak Pahlawan</h3>
            <p>Tebak pahlawan nasional dari 12 pahlawan yang tersedia.</p>
            <ul>
                <li><strong>Aturan:</strong> 5 kesempatan untuk mengumpulkan skor</li>
                <li><strong>Benar:</strong> +10 poin</li>
                <li><strong>Target:</strong> Pahlawan berganti setelah setiap tebakan</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🔢 Angka Rahasia</h3>
            <p>Permainan angka untuk melatih logika dan perhitungan.</p>
            <ul>
                <li>Tuliskan deretan angka di Baris 1</li>
                <li>Aplikasi menyiapkan jawaban rahasia</li>
                <li>Lengkapi Baris 2-5 sesuai petunjuk</li>
                <li>Cocokkan hasil penjumlahan dengan jawaban rahasia</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🚣 Pahlawan Menyeberang Sungai</h3>
            <p>Permainan strategi menyeberangkan 4 entitas dengan aturan tertentu.</p>
            <ul>
                <li><strong>Entitas:</strong> Pahlawan, Tawanan, Perbekalan, Anak Buah</li>
                <li><strong>Aturan 1:</strong> Tawanan + Perbekalan tanpa pahlawan = GAGAL</li>
                <li><strong>Aturan 2:</strong> Tawanan + Anak Buah tanpa pahlawan = TIDAK GAGAL, tapi tidak dapat poin</li>
                <li><strong>Poin:</strong> 10 poin jika berhasil tanpa melanggar aturan</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🇮🇩 Tiang Bendera</h3>
            <p>Permainan menara Hanoi versi Indonesia dengan bendera.</p>
            <ul>
                <li><strong>Susunan Awal:</strong> 🚩 Merah Putih → 🟢 Hijau → 🟡 Kuning → 🔵 Biru</li>
                <li><strong>Target:</strong> Pindahkan semua ke Tiang C</li>
                <li><strong>Aturan:</strong> Cakram besar tidak boleh di atas cakram kecil</li>
            </ul>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips:</strong> Permainan hadiah melatih berbagai keterampilan: 
            pengetahuan sejarah, logika, strategi, dan pemecahan masalah.
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_gamifikasi():
    """Tutorial fitur Gamifikasi."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            🎮 Fitur Gamifikasi
        </h2>
        
        <div class="tutorial-card">
            <h3>🎯 Misi & Tantangan</h3>
            <p>Selesaikan misi untuk mendapatkan poin reward dan naik level!</p>
            
            <h4>📅 Tantangan Harian</h4>
            <p>Setiap hari Anda mendapatkan tantangan berbeda:</p>
            <ul>
                <li><strong>Senin:</strong> 📝 Senin Cerdas – 10 soal</li>
                <li><strong>Selasa:</strong> 🧠 Selasa Analisis – 10 soal IQ</li>
                <li><strong>Rabu:</strong> ❤️ Rabu Empati – 10 soal EQ</li>
                <li><strong>Kamis:</strong> 🙏 Kamis Spiritual – 10 soal SQ</li>
                <li><strong>Jumat:</strong> 💪 Jumat Tangguh – 10 soal AQ</li>
                <li><strong>Sabtu:</strong> 🇮🇩 Sabtu Patriot – 10 soal Nasionalisme</li>
                <li><strong>Minggu:</strong> 🏆 Minggu Juara – 15 soal</li>
            </ul>
            <p>✅ Selesaikan tantangan harian untuk mendapatkan <strong>5-8 poin reward</strong>!</p>
            
            <h4>📋 Daftar Misi (12 Misi)</h4>
            
            <p><strong>🌱 Level Pemula:</strong></p>
            <ul>
                <li>🌱 Perintis Jalan – 10 soal → 5 poin</li>
                <li>📖 Penjelajah Ilmu – 50 soal → 10 poin</li>
            </ul>
            
            <p><strong>📚 Level Menengah:</strong></p>
            <ul>
                <li>📚 Cendekia Muda – 100 soal → 15 poin</li>
                <li>🎯 Akurasi 80% – 80% akurasi → 10 poin</li>
                <li>🧠 Master IQ – IQ ≥ 80 → 15 poin</li>
                <li>❤️ Master EQ – EQ ≥ 80 → 15 poin</li>
                <li>🙏 Master SQ – SQ ≥ 80 → 15 poin</li>
                <li>💪 Master AQ – AQ ≥ 80 → 15 poin</li>
            </ul>
            
            <p><strong>🌟 Level Lanjutan:</strong></p>
            <ul>
                <li>🌟 Pahlawan Cerdas – 200 soal → 25 poin</li>
                <li>🏆 Akurasi 90% – 90% akurasi → 20 poin</li>
                <li>🇮🇩 Patriot Sejati – Nasionalisme ≥ 80 → 20 poin</li>
                <li>💎 NKHM 100 – NKHM Total 100 → 30 poin</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🏆 Leaderboard</h3>
            <p>Kompetisi sehat untuk meraih posisi teratas!</p>
            
            <h4>📊 Sistem Level</h4>
            <ul>
                <li><strong>🌿 Novice</strong> – Skor 0-19 (Merah)</li>
                <li><strong>📖 Beginner</strong> – Skor 20-39 (Abu-abu)</li>
                <li><strong>🌱 Learner</strong> – Skor 40-59 (Oranye)</li>
                <li><strong>📚 Expert</strong> – Skor 60-74 (Hijau)</li>
                <li><strong>🏆 Master</strong> – Skor 75-89 (Biru)</li>
                <li><strong>🌟 Grand Master</strong> – Skor 90-100 (Emas)</li>
            </ul>
            
            <h4>🎖️ Medali</h4>
            <ul>
                <li>🥇 Emas – Peringkat 1</li>
                <li>🥈 Perak – Peringkat 2</li>
                <li>🥉 Perunggu – Peringkat 3</li>
            </ul>
        </div>
        
        <div class="tutorial-tip">
            💡 <strong>Tips Gamifikasi:</strong>
            <ul>
                <li>Kerjakan tantangan harian setiap hari untuk mengumpulkan poin</li>
                <li>Fokus selesaikan misi level pemula terlebih dahulu</li>
                <li>Kejar posisi teratas di leaderboard</li>
                <li>Semakin tinggi level, semakin besar reward yang didapat</li>
            </ul>
        </div>
        
        <div class="tutorial-success">
            🎉 <strong>Target Akhir:</strong> Capai <strong>🌟 Grand Master</strong> dan raih posisi 
            <strong>🥇 Juara 1</strong> di leaderboard!
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_tips():
    """Tips dan trik menggunakan aplikasi."""
    st.markdown("""
    <div class="tutorial-container">
        <h2 style="text-align: center; color: #1a3c6e; margin-bottom: 30px;">
            💡 Tips & Trik
        </h2>
        
        <div class="tutorial-card">
            <h3>🎯 Tips Umum</h3>
            <ul>
                <li><strong>Konsistensi:</strong> Kerjakan soal setiap hari untuk meningkatkan skor</li>
                <li><strong>Variasi:</strong> Gunakan filter berbeda untuk variasi soal</li>
                <li><strong>Catatan:</strong> Gunakan fitur catatan untuk mencatat hal penting</li>
                <li><strong>Kompetisi:</strong> Tantang teman di mode Tanding</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🚀 Tips Meningkatkan Skor</h3>
            <ul>
                <li><strong>IQ:</strong> Banyak membaca dan latihan logika</li>
                <li><strong>EQ:</strong> Latih empati dan kesadaran diri</li>
                <li><strong>SQ:</strong> Refleksi dan meditasi nilai-nilai kehidupan</li>
                <li><strong>AQ:</strong> Hadapi tantangan dengan sikap positif</li>
                <li><strong>Nasionalisme:</strong> Pelajari sejarah dan budaya Indonesia</li>
            </ul>
        </div>
        
        <div class="tutorial-card">
            <h3>🎮 Tips Gamifikasi</h3>
            <ul>
                <li><strong>Tantangan Harian:</strong> Jangan lewatkan reward harian</li>
                <li><strong>Misi:</strong> Selesaikan misi level pemula terlebih dahulu</li>
                <li><strong>Leaderboard:</strong> Pantau posisi Anda dan kejar ranking</li>
                <li><strong>Level:</strong> Semakin tinggi level, semakin besar prestise</li>
            </ul>
        </div>
        
        <div class="tutorial-warning">
            ⚠️ <strong>Ingat!</strong> Aplikasi ini adalah alat bantu belajar. 
            Kunci utama adalah <strong>konsistensi</strong> dan <strong>niat belajar</strong> yang tulus.
        </div>
        
        <div class="tutorial-success">
            🌟 <strong>Selamat belajar!</strong> Semoga Anda menjadi <strong>Pahlawan Cerdas Nusantara</strong>! 🇮🇩
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== FUNGSI UTAMA ==========
def show_tutorial():
    """Menampilkan halaman Tutorial lengkap."""
    try:
        inject_tutorial_css()
        
        st.markdown("## 📘 Tutorial NKHM Nusantara")
        st.markdown("Panduan lengkap untuk menggunakan semua fitur di aplikasi NKHM.")
        st.markdown("---")
        
        # ===== TAB SELECTOR =====
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "🏠 Umum",
            "🎮 Kuis",
            "📊 Dasbor",
            "🏆 Prestasi",
            "⚔️ Tanding",
            "🎁 Karunia",
            "🎁 Hadiah",
            "🎮 Gamifikasi",
            "💡 Tips"
        ])
        
        with tab1:
            show_tutorial_umum()
        
        with tab2:
            show_tutorial_kuis()
        
        with tab3:
            show_tutorial_dasbor()
        
        with tab4:
            show_tutorial_prestasi()
        
        with tab5:
            show_tutorial_tanding()
        
        with tab6:
            show_tutorial_karunia()
        
        with tab7:
            show_tutorial_hadiah()
        
        with tab8:
            show_tutorial_gamifikasi()
        
        with tab9:
            show_tutorial_tips()
        
        # ===== FOOTER =====
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 20px 0; color: #888; font-size: 14px;">
            <p>🌿 NKHM Nusantara – Aplikasi Gaming 4 Kecerdasan + Nasionalisme</p>
            <p style="font-size: 12px;">Berbasis Perkembangan Data Personal | © 2026</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logging.error(f"Error di show_tutorial: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Tutorial: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_tutorial()