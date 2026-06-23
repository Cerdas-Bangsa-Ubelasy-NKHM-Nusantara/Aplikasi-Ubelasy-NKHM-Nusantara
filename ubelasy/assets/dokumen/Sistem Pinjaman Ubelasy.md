Konversi Dokumen ke Markdown

Saya akan mengkonversi file DOCX ini ke format Markdown dengan struktur yang rapi.

---

SISTEM PINJAMAN/KREDIT MODEL UBELASY UNTUK UMKM SEKTOR PANGAN DAN ENERGI

(Ubelasy Versi 2 Periode, dPSH Maks = 2 untuk tₚ = 25 Tahun, dan Penurunan Suku Bunga 0,5% per Periode)

(Oleh: SR.Pakpahan, SST)

---

I. TEORI, DEFENISI & KONSEP

1.1. Konsep Tahun Yobel dan Keuangan Berkelanjutan

Kitab Imamat 25:8-17 mengajarkan Tahun Yobel (tahun ke-50) sebagai pembebasan sisa hutang dan pengembalian tanah. Prinsip ini diadopsi dalam keuangan berkelanjutan (sustainable finance) yang menekankan pilar ekonomi, sosial, dan lingkungan. Ubelasy menerapkan pembebasan sisa hutang secara proporsional: PSH = SHA × (T / 50) untuk pedesaan (risiko tinggi) dan PSH = SHA × (T / 60) untuk perkotaan (batas keuntungan 16,67% dari usaha bisnis).

1.2. Struktur Permodelan Ubelasy 2 Periode, dPSH Maks = 2

Parameter dasar (untuk T = 6 tahun):

Simbol Keterangan Satuan
T Total masa pinjaman (tenor keseluruhan) tahun
n Jumlah periode pinjaman -
tₚ Tenor per periode (T = n × tₚ) tahun
K Nilai pinjaman per periode Rupiah
rᵢ Suku bunga pada periode ke-i % per tahun
Δr Penurunan suku bunga per periode (0,5%) %

Hubungan: T = n × tₚ

Contoh:

· Pinjaman per periode (K) = Rp 36 juta.
· Jumlah periode (n) = 2
· Tenor per periode (tp) = 3 tahun
· Total tenor T = n × tₚ = 6 tahun
· Suku bunga awal r₁ = 11% per tahun.
· Penurunan bunga per periode, Δr = 0,5% → r₂ = 10,5%
· Biaya dana + overhead = 9% (HPDK 7% + overhead 2%).

Rumus Derajat PSH (dPSH) skala 0--2:

Berdasarkan inspirasi Kitab Imamat 25:8-12, Tahun Yobel penuh terjadi pada tahun ke-50 dengan pembebasan total sisa hutang. Dalam sistem Ubelasy, patokan absolut tetap 50 tahun. Derajat Pembebasan Sisa Hutang (dPSH) didefinisikan dalam skala 0--2. Nilai dPSH = 2 dicapai ketika total tenor pinjaman T = 50 tahun.

dPSH = 2 \times \frac{T}{50} = \frac{T}{25}

dimana T adalah total tenor pinjaman.

Untuk T=6 tahun, dPSH = 6/25 = 0,24.

Rumus Total Sisa Hutang (TSH) per periode (metode flat):

Dalam sistem Ubelasy, skema pembayaran kredit menggunakan asumsi metode cicilan flat (bunga dihitung dari pokok awal dan tetap setiap bulan).

TSH_i = K \times (1 + r_i \times t_p)

dimana K adalah jumlah pinjaman per periode, r_i adalah suku bunga pinjaman di periode ke-i, tₚ adalah tenor pinjaman per periode dalam satuan tahun.

Contoh: K = 36 juta, r₁ = 11%, tₚ = 3 tahun → TSH₁ = 36 × (1 + 0,11×3) = 47,88 juta.

Rumus Sisa Hutang Akhir di Periode Terakhir

Pada periode ke-n, debitur membayar angsuran selama periode tersebut. Jika diasumsikan debitur membayar selama m tahun (dengan 0 < m ≤ tₚ), maka Sisa Hutang Akhir (SHA):

SHA = TSH_n - \left( \frac{TSH_n}{t_p} \right) \times m = TSH_n \left( 1 - \frac{m}{t_p} \right)

dimana m adalah tahun pembayaran dalam periode terakhir (m ≤ tₚ).

Contoh (T=6 tahun, tₚ=3 tahun, m=2 tahun):

Sisa Hutang Akhir (SHA) = 47,34 × (1 -- 2/3) = 47,34 × 1/3 = 15,78 juta

Rumus PSH pedesaan dan perkotaan:

PSH diberikan dua kali pada debitur yaitu setengah bagian PSH diberikan di akhir tahun periode kesatu, dan setengah bagian lagi di akhir tahun periode kedua. Besarnya PSH dihitung dari sisa hutang yang masih tersisa di tahun akhir periode terakhir pinjaman (periode ke-2), bukan dari total TSHₙ.

PSH_{desa} = SHA \times \frac{T}{50}

PSH_{kota} = SHA \times \frac{T}{60}

Contoh (T=6 tahun, SHA = 15,78 juta):

PSH desa = 15,78 × (6/50) = 15,78 × 0,12 = 1,8936 juta, dengan pembagian PSH pertama sebesar 1,8936 juta / 2 = 0,9468 juta atau 946,8 ribu diberikan di tahun akhir periode ke-1. PSH kedua sebesar 1,8936 juta / 2 = 0,9468 juta atau 946,8 ribu diberikan di tahun akhir periode ke-2.

PSH kota = 15,78 × (6/60) = 15,78 × 0,10 = 1,578 juta, dengan pembagian PSH pertama sebesar 1,578 juta / 2 = 0,789 juta atau 789 ribu diberikan di tahun akhir periode ke-1. PSH kedua sebesar 1,578 juta / 2 = 0,789 juta atau 789 ribu diberikan di tahun akhir periode ke-2.

Hal pembagian ini tidak mempengaruhi perhitungan total keuntungan bank karena total PSH tetap sama (1,8936 juta untuk desa). Hanya timing pembayaran yang berbeda, yang dapat berdampak pada arus kas bank tetapi tidak pada keuntungan total selama 6 tahun. Pembagian ini adalah opsional dan dapat disesuaikan dengan kebijakan bank.

Landasan teologis-ekonomi: Pola 6:1 dalam tahun Sabat mengajarkan batas keuntungan maksimal 1/6 (≈16,67%) dalam usaha bisnis/perdagangan. Di perkotaan yang berbasis perdagangan dan jasa, proporsi PSH dikurangi dari T/50 menjadi T/60. Di pedesaan yang berbasis pertanian dengan risiko tinggi, proporsi PSH tetap T/50.

Perhitungan Keuntungan Bank dan Beban Debitur

· Total pinjaman akumulasi = n × K
· Total bayar sebelum PSH = total angsuran yang sudah dibayar (lunas di periode 1 + angsuran sebagian di periode 2) = $TSH_1 + \left( \frac{TSH_n}{t_p} \times m \right)$
· Total bayar setelah PSH = Total bayar sebelum PSH + (Sisa Hutang Akhir -- PSH)
· Keuntungan bank (Rp) = Total bayar setelah PSH -- (n × K)
· Keuntungan bank relatif = (Keuntungan / (n × K)) × 100%
· Return tahunan setara = Keuntungan relatif / T × 100%

Rumus keuntungan bank (total nominal selama T tahun):

Keuntungan = \left( \sum_{i = 1}^{n} TSH_i \right) - PSH - (n \times K)

Rumus margin keuntungan rata-rata per tahun (relatif terhadap total pinjaman yang disalurkan):

Margin\ Tahunan = \frac{Keuntungan}{n \times K \times T} \times 100\%

1.3. Sinergi dengan Kebijakan BI/KSSK

Sistem Ubelasy mendukung suku bunga rendah, pelonggaran likuiditas, RPIM, RIMS, dan penjaminan LPP.

---

II. EKONOMI PERKOTAAN VS PEDESAAN DALAM KONTEKS TAHUN YOBEL

2.1. Landasan Teologis

Kitab Imamat 25:10-17 memandatkan pembebasan sisa hutang di Tahun Yobel secara universal. Dalam Sistem Ubelasy, mandat ini dikontekstualisasikan dengan membedakan besaran PSH antara pedesaan dan perkotaan, berdasarkan realitas ekonomi masing-masing wilayah.

Prinsip Dasar:

"Beban yang lebih ringan (PSH lebih besar) diberikan kepada mereka yang memiliki kapasitas ekonomi lebih rapuh dan akses terbatas terhadap sumber daya pemulihan."

Hal ini selaras dengan semangat Tahun Yobel yang melindungi kaum miskin dan terpinggirkan.

2.2. Perbandingan Karakteristik Wilayah

Karakteristik Perkotaan Pedesaan
Akses & Diversifikasi Akses tinggi ke lembaga keuangan, peluang kerja beragam Akses terbatas, sangat tergantung 1-2 komoditas (misal pertanian)
Profil Risiko Lebih terukur dan beragam; suku bunga cenderung lebih rendah Risiko tinggi (cuaca, hama, fluktuasi harga); NPL pertanian hingga 5%
Kapasitas Pemulihan Pendapatan lebih stabil, jaring pengaman sosial lebih kuat Pendapatan tidak menentu, bergantung musim dan komunitas

2.3. Makna "Pembebasan" di Era Modern

Wilayah Makna Sifat
Desa PSH besar sebagai modal kerja baru (bibit, pupuk) untuk memulai lagi dari awal Restoratif (memulihkan martabat)
Kota PSH kecil sebagai keringanan arus kas untuk ekspansi atau investasi Akseleratif (mendorong pertumbuhan)

2.4. Parameter PSH yang Disesuaikan

Wilayah Prinsip Rentang PSH Rumus
Desa Pembebasan lebih besar (risiko tinggi, kerentanan ekonomi) 20% -- 50% dari SHA PSH_Desa = SHA × (T/50) × θ_Desa (θ_Desa = 2--5)
Kota Pembebasan lebih kecil (ekosistem dinamis) 8% -- 12% dari SHA PSH_Kota = SHA × (T/60) (atau dengan θ_Kota = 0,8--1,2)

Contoh Numerik (T = 6 tahun → T/50 = 12%)

Wilayah Parameter Perhitungan PSH (% dari SHA)
Desa (θ=2) 12% × 2 = 24% SHA × 24% 24%
Desa (θ=5) 12% × 5 = 60% SHA × 60% 60%
Kota (standar) T/60 = 10% TSH × 10% 10%

Catatan: Dalam implementasi standar Ubelasy 2 periode dengan T=6 tahun, digunakan nilai sederhana: Desa = T/50 = 12%, Kota = T/60 = 10% (tanpa faktor pengali tambahan). Parameter θ (2--5 untuk desa, 0,8--1,2 untuk kota) dapat diaktifkan untuk skenario kebijakan khusus.

Kesimpulan

Sistem Ubelasy tidak kaku, tetapi adaptif dan kontekstual. Perbedaan PSH antara desa dan kota memungkinkan sistem tetap setia pada semangat Tahun Yobel (melindungi yang lemah), sekaligus dijalankan sesuai realitas ekonomi modern.

---

III. STRUKTUR RUMUS MODEL UBELASY

3.1. Struktur Rumus Permodelan Ubelasy 2 Periode, dPSH Maks = 2

Berdasarkan prinsip Tahun Yobel dalam Kitab Imamat 25:8-12, patokan waktu absolut adalah 50 tahun. Pada tahun ke-50, seluruh sisa hutang debitur dibebaskan. Dalam Sistem Ubelasy, besarnya PSH bagi seorang debitur ditentukan secara proporsional dari nilai SHA di tahun akhir periode terakhir pinjaman, sesuai total masa pinjaman (T) yang disepakati dibandingkan dengan 50 tahun.

3.2. Parameter Dasar Ubelasy

Simbol Keterangan Satuan
T Total masa pinjaman (tenor keseluruhan) tahun
n Jumlah periode pinjaman -
t_p Tenor per periode $T = n \times t_p$ tahun
K Nilai pinjaman per periode Rupiah
r_i Suku bunga pada periode ke-i % per tahun
∆r Penurunan suku bunga per periode (misalnya 0,5%) %
TSH_i Total Sisa Hutang (total kewajiban debitur) pada periode ke-i (pokok + bunga) jika dilunasi penuh dalam periode tersebut Rupiah
SHA Sisa Hutang Akhir setelah debitur membayar sebagian angsuran di periode terakhir Rupiah
PSH Pembebasan Sisa Hutang di tahun akhir periode terakhir Rupiah

Hubungan: T = n × t_p. Dalam penelitian ini, total tenor ditetapkan T = 6 tahun dengan tiga varian:

Varian (2 Periode) n t_p r_i (i=1..n)
C (utama) 2 3 tahun 11%; 10,5%
A (alternatif desa) 3 2 tahun 11%; 10,5%; 10%
B (alternatif kota) 6 1 tahun 11%; 10,5%; 10%; 9,5%; 9%; 8,5%

Catatan: Model Ubelasy yang diusulkan dalam penelitian ini untuk diadopsi bank adalah Varian C (2 periode × 3 tahun) dengan dPSH Maks = 2. Varian A dan B disajikan sebagai pembanding untuk menunjukkan fleksibilitas sistem.

3.3. Asumsi Dasar Skala Derajat Pembebasan Sisa Hutang (dPSH)

Berdasarkan inspirasi Kitab Imamat 25:8-12, Tahun Yobel penuh terjadi pada tahun ke-50 dengan pembebasan total sisa hutang. Dalam sistem Ubelasy, patokan absolut tetap 50 tahun. Namun untuk memudahkan perhitungan dan adaptasi dengan kebiasaan perbankan, derajat Pembebasan Sisa Hutang (dPSH) didefinisikan dalam skala 0--2. Nilai dPSH Maks = 2 dicapai ketika total tenor pinjaman T = 50 tahun (pembebasan penuh). Dengan demikian, rumus dPSH adalah:

dPSH = \frac{2T}{50} = \frac{T}{25}

di mana T adalah total masa pinjaman dalam satuan tahun (T = n × t_p), dengan $0 < T \leq 50$

Contoh: Untuk T = 6 tahun, $dPSH = \frac{6}{25} = 0,24$.

Meskipun dPSH didefinisikan, dalam praktik perhitungan PSH tidak bergantung pada dPSH secara langsung. PSH dihitung dengan proporsi yang lebih sederhana dan sudah disesuaikan untuk wilayah pedesaan dan perkotaan, sebagai berikut:

PSH_{desa} = TSH_n \times \frac{T}{50}

PSH_{kota} = TSH_n \times \frac{T}{60}

Rumus ini konsisten dengan semangat Tahun Yobel (pembebasan penuh pada T = 50) dan batas keuntungan berkisar 16,67% untuk wilayah perkotaan. Hubungan matematis antara dPSH dan PSH tidak diperlukan dalam implementasi karena PSH sudah dinyatakan secara eksplisit.

3.4. Rumus Sisa Hutang Akhir di Periode Terakhir

Pada periode ke-n, debitur membayar angsuran selama periode tersebut. Jika diasumsikan debitur membayar selama m tahun (dengan 0 < m ≤ tₚ), maka Sisa Hutang Akhir (SHA):

SHA = TSH_n - \left( \frac{TSH_n}{t_p} \right) \times m = TSH_n \left( 1 - \frac{m}{t_p} \right)

dimana m adalah tahun pembayaran dalam periode terakhir (m ≤ tₚ).

3.5. Rumus Total Sisa Hutang (TSH) per Periode

Dalam sistem Ubelasy, skema pembayaran kredit menggunakan asumsi metode cicilan flat (bunga dihitung dari pokok awal dan tetap setiap bulan di suatu periode). Untuk satu periode pinjaman dengan nilai pinjaman K, suku bunga per tahun r_i, dan tenor per periode t_p tahun, maka TSH di akhir periode tersebut (sebelum dikurangi pembayaran angsuran) adalah seluruh kewajiban debitur yang harus dilunasi selama periode tersebut, yaitu pokok ditambah total bunga selama t_p tahun.

Untuk setiap periode ke-i dengan suku bunga r_i, pinjaman K, tenor per periode t_p tahun, total yang harus dibayar debitur selama periode tersebut (asumsi tanpa PSH) adalah:

TSH_i = K \times (1 + r_i \times t_p)

Penjelasan:

· Pokok pinjaman = K
· $Total\ bunga = K \times r_i \times t_p$ (karena bunga flat per tahun dikalikan dengan lama periode)
· Maka Total Sisa Hutang, $TSH_i = K + K \times r_i \times t_p = K \times (1 + r_i \times t_p)$

Rumus tersebut digunakan untuk menghitung Total Sisa Hutang (TSH) pada akhir tahun periode terakhir pinjaman (sebelum dikurangi Pembebasan Sisa Hutang/PSH). Secara lebih rinci, TSH_i adalah total kewajiban debitur yang harus dilunasi selama periode ke-i, yang terdiri dari:

· Pokok pinjaman (K)
· Total bunga selama tenor periode tersebut (K × r_i × t_p), dengan asumsi bunga flat.

Dengan demikian, rumus $K \times (1 + r_i \times t_p)$ menyatakan jumlah total yang harus dibayar debitur pada periode ke-i jika tidak ada PSH.

Contoh: K = 36 juta, r_i = 11%, t_p = 3 tahun, maka TSH_i = 47,88 juta.

Rumus ini berlaku untuk setiap periode pinjaman dengan suku bunga r_i yang mungkin berbeda antar periode. Total Sisa Hutang pada periode ke-i dinotasikan sebagai TSH_i.

3.6. Rumus Pembebasan Sisa Hutang (PSH)

PSH diberikan satu kali di akhir tahun periode terakhir (periode ke-n). Nilainya dibedakan menurut wilayah:

PSH_{desa} = SHA \times \frac{T}{50}

PSH_{kota} = SHA \times \frac{T}{60}

Untuk T = 6 tahun:

· Pedesaan: $PSH_{desa} = SHA \times 12\%$
· Perkotaan: $PSH_{kota} = SHA \times 10\%$

Landasan teologis-ekonomi: Pola 6:1 dalam tahun Sabat (6 tahun kerja, 1 tahun istirahat) mengajarkan batas keuntungan berkisar 1/6 × 100% (≈16,67%) dalam usaha bisnis/perdagangan. Di perkotaan yang berbasis perdagangan dan jasa, proporsi PSH dikurangi dari T/50 menjadi T/60. Sedangkan di pedesaan yang berbasis pertanian dengan risiko tinggi, proporsi PSH tetap T/50.

3.7. Perhitungan Keuntungan Bank dan Beban Debitur

· Total pinjaman akumulasi: $\sum K = n \times K$
· Total bayar sebelum PSH: $\sum_{i = 1}^{n} TSH_i$
· Total bayar setelah PSH: $(\sum_{i = 1}^{n} TSH_i) - PSH$
· Keuntungan bank (Rp): $Total\ bayar\ setelah\ PSH - \sum K$
· Keuntungan bank relatif: $(\frac{Keuntungan}{\sum K}) \times 100\%$

Total bayar debitur sebelum PSH selama seluruh periode adalah jumlah seluruh TSH_i: Total bayar sebelum PSH = $\sum_{i = 1}^{n} TSH_i$

Nilai rupiah PSH dibagi 2 dan hanya diberikan separoh di tahun akhir periode ke-1, dan separoh lagi di tahun akhir periode terakhir (periode ke-2), dan besarnya dihitung berdasarkan wilayah bank (desa/kota) seperti telah dirumuskan pada sub-bab III.6.4. Setelah PSH dikurangkan, diperoleh total bayar akhir debitur.

3.8. Ringkasan Tiga Varian Ubelasy untuk Total Tenor T=6 Tahun

Berdasarkan kesepakatan untuk mencapai win-win solution antara bank dan debitur, dipilih tiga varian dengan jumlah periode dan tenor per periode berbeda, namun total tenor tetap 6 tahun. Parameter suku bunga awal 11% per tahun, penurunan suku bunga 0,5% per periode.

Berdasarkan simulasi numerik (disajikan di Bab IV), diperoleh hasil sebagai berikut:

Varian Wilayah N × t_p Keuntungan Bank (% thd pinjaman) PSH (% thd total pinjaman) Sifat
C Desa & Kota 2 × 3 tahun 29,62% (desa), 30,06% (kota) 2,63% (desa), 2,19% (kota) Win-win solution (fokus utama)
A Desa 3 × 2 tahun 18,60% 2,40% Alternatif pro-debitur
B Kota 6 × 1 tahun 7,94% 1,81% Alternatif pro-bank

Catatan: Varian D (1 × 6 tahun, bunga awal 11% dengan penurunan bunga 0,5% per periode, diperoleh PSH 3,32% di bank desa dan 2,77% di bank kota) tidak digunakan dalam naskah ini karena lebih cocok untuk produk kartu kredit atau kredit konsumtif, bukan untuk sektor produktif pangan dan energi, dengan alasan varian D secara matematis menguntungkan bank, tetapi tidak sesuai dengan semangat Tahun Yobel yang mengajarkan pembebasan berkala (setiap 50 tahun, bukan setelah satu periode panjang), varian D juga tidak memiliki mekanisme penurunan suku bunga, sehingga kurang adaptif terhadap fluktuasi ekonomi.

3.9. Sinergi Ubelasy dengan Kebijakan Bank Indonesia dan KSSK

Sistem Ubelasy dirancang untuk mendukung kebijakan Bank Indonesia dan Komite Stabilitas Sistem Keuangan (KSSK), seperti suku bunga rendah, pelonggaran likuiditas, RPIM, RIMS, serta penjaminan LPP. Dengan menurunkan NPL dan mendorong volume kredit, Ubelasy berkontribusi pada stabilitas sistem keuangan. Khusus untuk Model Ubelasy 2 Periode dengan dPSH Maks = 2. Nilai dPSH = 0,24 pada T=6 tahun menunjukkan bahwa pembebasan sisa hutang bersifat proporsional dan masih dalam koridor kehati-hatian, sehingga mudah diadopsi oleh perbankan.

---

IV. KEUNTUNGAN BANK DARI PINJAMAN DEBITUR PER TAHUN

Margin keuntungan bank konvensional (spread) biasanya 1,3--3,5%, NIM 4,5--5,5%. Ubelasy 2 periode dengan Varian C memberikan spread rata-rata 1,75% per tahun, namun karena volume meningkat dan NPL turun, return tahunan terhadap total pinjaman yang tersalur mencapai sekitar 4,98% {sekitar 4,94% (bank desa) hingga 5,01% (bank kota)}, masih kompetitif dan berkelanjutan.

Berdasarkan data perbankan terkini, keuntungan bank dari pinjaman dapat dilihat dari dua sudut: Margin Keuntungan (Profit Margin) yang ditetapkan bank dalam Suku Bunga Dasar Kredit (SBDK) dan Net Interest Margin (NIM) realisasi bank setelah dikurangi biaya dana.

4.1. Margin Keuntungan (Profit Margin) dalam SBDK

Bank secara transparan mencantumkan margin keuntungan dalam perhitungan Suku Bunga Dasar Kredit. Berikut data dari beberapa bank per Februari--Maret 2026:

Bank & Segmen Margin Keuntungan (% p.a.)
Bank Mandiri-Korporasi 1,99
Bank Mandiri-UMKM Menengah 2,57
Bank Mandiri-UMKM Kecil 3,07
Bank Mandiri-UMKM Mikro 3,37
Bank Mandiri-KPR 3,48
Bankaltimtara Korporasi 1,39
Bankaltimtara-UMKM Mikro 2,38
Bank BTN Korporasi 1,57
Bank BTN-UMKM Mikro 1,32
Bank INA-Seluruh Segmen 1,50

Kesimpulan: Margin keuntungan yang ditetapkan bank bervariasi antara 1,32% hingga 3,48% per tahun, tergantung segmen debitur. Debitur mikro/UMKM kecil dikenakan margin lebih tinggi karena risiko lebih besar.

4.2. Net Interest Margin (NIM) -- Keuntungan Riil Bank

Net Interest Margin (NIM) adalah selisih antara pendapatan bunga dari kredit dan biaya bunga atas dana pihak ketiga (tabungan/deposito), dibagi total aset produktif. Ini mencerminkan keuntungan bersih bank dari kegiatan intermediasi setelah dikurangi biaya dana.

Berdasarkan pernyataan Menteri Keuangan Purbaya Yudhi Sadewa pada Februari 2026:

"Net interest margin kita besar, tertinggi di dunia dan akhirat"

Data OJK menunjukkan:

· Rata-rata NIM industri perbankan Indonesia: 4,56% (Desember 2025)
· Beberapa bank besar masih mencatat NIM di kisaran 5%--6%
· Sebagai perbandingan: AS ~2--3%, Australia ~2%

Kesimpulan: Keuntungan riil bersih bank Indonesia setelah dikurangi biaya dana rata-rata sekitar 4,5%--5% per tahun, tertinggi di dunia.

4.3. Komponen Penentu Keuntungan Bank

Berdasarkan data SBDK bank-bank di atas, keuntungan bank berasal dari tiga komponen utama:

Komponen Kisaran (%) Keterangan
Harga Pokok Dana untuk Kredit (HPDK) 1,97% -- 5,17% Biaya yang bank bayar untuk dana (deposito, tabungan)
Biaya Overhead 2,13% -- 7,53% Biaya operasional, gaji, sewa, IT, dll
Margin Keuntungan 1,32% -- 3,48% Laba kotor bank dari pinjaman

SBDK = HPDK + Overhead + Margin Keuntungan

Total SBDK yang dibebankan ke debitur berkisar antara 7,5% hingga 13,65% tergantung segmen.

Ringkasan: Persentase Keuntungan Bank

Ukuran Keuntungan Kisaran (%) Penjelasan
Margin Keuntungan (Profit Margin) 1,3% -- 3,5% Laba kotor sebelum biaya operasional
Net Interest Margin (NIM) 4,5% -- 5,5% Keuntungan bersih setelah dikurangi biaya dana
SBDK (Suku bunga yang dibayar debitur) 7,5% -- 13,7% Bukan keuntungan, tapi total beban debitur

4.4. Implikasi untuk Sistem Ubelasy 2 Periode, dPSH Maks = 2

Temuan ini sangat relevan untuk memperkuat argumen bahwa Sistem Ubelasy 2 Periode (t_p = 3 tahun, penurunan suku bunga 0,5% per periode, dPSH = T/25 = 0,24 pada T = 6 tahun) tetap menguntungkan bagi bank, dengan rincian sebagai berikut:

1. Rata-rata suku bunga Ubelasy untuk varian C (varian utama: 2 × 3 tahun) adalah 10,75% per tahun (turun dari 11% menjadi 10,5%). Setelah dikurangi biaya dana dan overhead (total 9%), diperoleh spread keuntungan sebesar 1,75% per tahun. Nilai ini masih berada dalam kisaran margin keuntungan bank konvensional (1,3% -- 3,5%).
2. Net Interest Margin (NIM) ekuivalen dari Ubelasy 2 periode, setelah memperhitungkan PSH (pembebasan sisa hutang) dan peningkatan volume kredit, menghasilkan return tahunan setara sekitar 4,94% (bank desa) hingga 5,01% (bank kota) dari total pinjaman yang disalurkan. Angka ini berada di atas rata-rata NIM industri perbankan Indonesia (4,56%) dan masih dalam koridor keuntungan yang sehat.
3. Margin keuntungan Ubelasy dapat dipertahankan di kisaran 1,5% -- 2% per tahun karena:
   · Efisiensi overhead (proses digitalisasi dan skema sederhana dua periode)
   · Insentif regulator (pelonggaran GWM, penurunan bobot risiko kredit Ubelasy dalam KPMM)
   · Peningkatan volume kredit akibat demand booming dari debitur yang tertarik dengan skema ringan, dan adanya PSH
   · Penurunan signifikan biaya CKPN (Cadangan Kerugian Penurunan Nilai) karena NPL diprediksi turun drastis
4. Perbandingan dengan margin konvensional: Bank saat ini memperoleh margin keuntungan 1,32% -- 3,48% untuk berbagai segmen. Ubelasy 2 periode memberikan margin 1,75% (spread) yang berada di atas batas bawah (1,32%) dan mendekati nilai tengah. Untuk segmen UMKM mikro yang biasanya dikenakan margin >3%, Ubelasy menawarkan margin sedikit lebih rendah namun dikompensasi dengan risiko kredit yang lebih kecil dan insentif kebijakan.
5. dPSH Maks = 2 hanya akan dicapai jika total tenor T = 50 tahun. Pada implementasi awal dengan T = 6 tahun, dPSH = 0,24, artinya beban pembebasan sisa hutang bagi bank masih sangat kecil (PSH bank desa 2,63%, PSH bank kota 2,19% dari total pinjaman), sehingga tidak mengganggu profitabilitas bank.

Kesimpulan implikasi:

"Meskipun suku bunga efektif Ubelasy versi 2 periode (rata-rata 10,75%) sedikit lebih rendah dari SBDK konvensional untuk segmen UMKM (yang biasa 11--13%), margin keuntungan bank sebesar 1,75% per tahun masih dalam kisaran sehat (1,3--3,5%). Dengan tambahan insentif regulator, peningkatan volume kredit, dan penurunan NPL, Sistem Ubelasy 2 periode, dPSH Maks = 2 merupakan skema win-win solution yang layak diadopsi untuk mendukung ketahanan pangan dan energi di Sumatera Selatan."

---

V. SIMULASI PENGHITUNGAN VARIAN UBELASY (T = 6 TAHUN)

Asumsi umum:

· Pinjaman per periode K = Rp 36.000.000
· Suku bunga awal r_1 = 11% per tahun
· Penurunan suku bunga ∆r = 0,5% per periode
· Total tenor T = 6 tahun (tetap)
· Metode bunga flat per periode
· Rumus Total Sisa Hutang (PSH) periode ke-i:

TSH_i = K \times (1 + r_i \times t_n)

Dengan tn dalam tahun.

· Rumus Sisa Hutang Akhir (SHA) di periode terakhir:

SHA = TSH_n - \left( \frac{TSH_n}{t_p} \right) \times m = TSH_n \left( 1 - \frac{m}{t_p} \right)

dimana m adalah tahun pembayaran dalam periode terakhir (m ≤ tₚ).

· Rumus Pembebasan Sisa Hutang (PSH):

Rumus PSH pedesaan:

PSH_{desa} = SHA_n \times \frac{T}{50}

Rumus PSH perkotaan:

PSH_{kota} = SHA_n \times \frac{T}{60}

· Rumus Total pinjaman akumulasi = n × K
· Rumus Keuntungan Bank:

Keuntungan bank (nominal):

Keuntungan\ bank\ (nominal) = \left( \sum_{i = 1}^{n} TSH_i \right) - PSH - (n \times K)

Keuntungan bank (%)

Keuntungan\ bank\ (\%) = \frac{Keuntungan\ nominal}{n \times K} \times 100\%

· Rumus Persentase PSH (% thd total pinjaman):

PSH\ (\%\ terhadap\ total\ pinjaman) = \frac{PSH}{n \times K} \times 100\%

· Rumus Return tahunan setara:

Return\ tahunan\ setara = \frac{Keuntungan\ (\%)}{T}

Asumsi Dasar (Untuk Semua Varian) Dalam Bentuk Tabel:

Parameter Nilai
Suku bunga awal (r₁) 11% per tahun
Penurunan suku bunga per periode (Δr) 0,5%
Biaya dana (HPDK) 7% per tahun
Biaya overhead 2% per tahun
Total biaya bank 9% per tahun
Total tenor (T) 6 tahun (tetap)
Pinjaman per periode (K) Rp 36.000.000
Metode bunga Asumsi Flat per periode

5.1. Simulasi Parameter dan Asumsi {Varian utama C: 2 periode x 3 tahun (t_p = 3 tahun)}

Berdasarkan simulasi numerik, struktur rumus, parameter, dan penghitungan Varian C: 2 Periode × 3 Tahun (t_p = 3 tahun) disajikan berikut ini:

Total tenor T = 6 tahun, 2 periode × 3 tahun per periode.

Pinjaman K = Rp 36.000.000 per periode.

r₁ = 11%, r₂ = 10,5%.

Perhitungan TSH:

TSH = Kewajiban debitur membayar hutangnya hingga lunas.

· Periode 1:

Angsuran = (36 juta / 36) + (36 juta × 11% / 12) = 1 juta + 330 ribu = 1,33 juta per bulan.

Total kewajiban bayar = 1,33 juta × 36 = 47,88 juta, ini sama dengan TSH₁.

TSH₁ = 36 juta × (1 + 0,11 × 3) = 36 × 1,33 = 47,88 juta

· Periode 2:

Angsuran = (36 juta / 36) + (36 juta × 10,5% / 12) = 1 juta + 315 ribu = 1,315 juta per bulan.

Total kewajiban bayar = 1,315 juta × 36 = 47,34 juta.

TSH₂ = 36 × (1 + 0,105×3) = 36 × 1,315 = 47,34 juta.

Namun, bila bayar selama 2 tahun (24 bulan):

TSH₂ = Total kewajiban bayar 2 tahun = 1,315 juta × 24 = 31,56 juta.

SHA = 47,34 -- 31,56 = 15,78 juta {karena tahun pembebasan sisa hutang ada di tahun akhir periode terakhir (periode ke-2)}.

Atau dengan rumus:

SHA = TSH_n - \left( \frac{TSH_n}{t_p} \right) \times m = TSH_n \left( 1 - \frac{m}{t_p} \right)

SHA = 47,34 × {1- (2/3)} = 15,78 juta.

dPSH = T/25 = 6/25 = 0,24

Perhitungan per periode:

Periode TSH (total kewajiban) Angsuran/bulan Pembayaran Sisa Hutang Akhir (SHA)
1 47,88 juta 1,33 juta 36 bulan (lunas) 0
2 47,34 juta 1,315 juta 24 bulan 15,78 juta

Total bayar sebelum PSH:

· Periode 1: 47,88 juta
· Periode 2: 1,315 juta × 24 = 31,56 juta
· Total = 79,44 juta

PSH berdasarkan bank desa dan kota:

· PSH desa = 15,78 × (6/50) = 15,78 × 0,12 = 1,8936 juta.

PSH pertama sebesar 1,8936 juta / 2 = 0,9468 juta atau 946,8 ribu diberikan di tahun akhir periode ke-1. PSH kedua sebesar 1,8936 juta / 2 = 0,9468 juta atau 946,8 ribu diberikan di tahun akhir periode ke-2.

· PSH kota = 15,78 × (6/60) = 15,78 × 0,10 = 1,578 juta.

PSH pertama sebesar 1,578 juta / 2 = 0,789 juta atau 789 ribu diberikan di tahun akhir periode ke-1. PSH kedua sebesar 1,578 juta / 2 = 0,789 juta atau 789 ribu diberikan di tahun akhir periode ke-2.

Total bayar setelah PSH:

· Bank Desa: 79,44 + (15,78 -- 1,8936) = 79,44 + 13,8864 = 93,3264 juta
· Bank Kota: 79,44 + (15,78 -- 1,578) = 79,44 + 14,202 = 93,642 juta

Keuntungan bank:

· Bank Desa: 93,3264 -- 72 = 21,3264 juta → 29,62% dari total pinjaman
· Bank Kota: 93,642 -- 72 = 21,642 juta → 30,06% dari total pinjaman

Return tahunan setara:

· Bank Desa: 29,62% / 6 = 4,94% per tahun
· Bank Kota: 30,06% / 6 = 5,01% per tahun

Spread suku bunga:

· Rata-rata SBDK = (11%×3 + 10,5%×3)/6 = 10,75%
· Spread = 10,75% -- 9% = 1,75% per tahun

Perhitungan Return tahunan bank (return rata-rata per tahun terhadap total pinjaman):

Return\ tahunan\ bank\ desa = \frac{29,62\%}{6} = 4,94\%\ per\ tahun

Return\ tahunan\ bank\ kota = \frac{30,06\%}{6} = 5,01\%\ per\ tahun

Perhitungan spread suku bunga (selisih rata-rata SBDK dengan biaya dana+overhead):

Rata-rata\ SBDK = \frac{11\% \times 3 + 10,5\% \times 3}{6} = 10,75\%

Spread = 10,75\% - 9\% = 1,75\%\ per\ tahun

Catatan: Spread 1,75% adalah ukuran marjin bunga bersih tahunan terhadap outstanding loan, sedangkan return tahunan desa 4,94% atau kota 5,01% adalah hasil aktual setelah memperhitungkan PSH dan total pokok. Kedua ukuran ini berbeda tetapi saling melengkapi.

Tabel: Margin per Periode (Varian C: n = 2 periode, tₚ = 3 tahun)

Periode SBDK (bunga pinjaman) Biaya dana (HPDK) Overhead Spread keuntungan bank
1 11% 7% 2% 2%
2 10,5% 7% 2% 1,5%
Rata-rata 10,75% 7% 2% 1,75%

5.2. Varian A: 3 Periode × 2 Tahun (t_p = 2 tahun)

Parameter Varian A:

Besaran Nilai
n 3 periode
tₚ 2 tahun
T = n × tₚ 6 tahun
Total pinjaman akumulasi 3 × 36 = 108 juta
r₁ 11%
r₂ 10,5%
r₃ 10%

Langkah 1: Hitung TSH setiap periode

Rumus: $TSH_i = K \times (1 + r_i \times t_p)$

Periode rᵢ Perhitungan TSH (juta)
1 11% 36 × (1 + 0,11×2) = 36 × 1,22 43,92
2 10,5% 36 × (1 + 0,105×2) = 36 × 1,21 43,56
3 10% 36 × (1 + 0,10×2) = 36 × 1,20 43,20

Total TSH (jika dilunasi semua) = 43,92 + 43,56 + 43,20 = 130,68 juta.

Langkah 2: Tentukan skema pembayaran dan Sisa Hutang Akhir (SHA)

Asumsi pembayaran (konsisten dengan Varian C):

· Periode 1: Dibayar lunas (2 tahun / 24 bulan penuh)
· Periode 2: Dibayar lunas (2 tahun / 24 bulan penuh)
· Periode 3: Dibayar 1 tahun saja (12 bulan), sisanya 1 tahun tidak dibayar sebelum PSH

Periode 3 (periode terakhir)

· TSH₃ = 43,20 juta
· Tenor periode = 2 tahun
· Angsuran per bulan = 43,20 / 24 = 1,80 juta/bulan
· Pembayaran selama 1 tahun (12 bulan) = 1,80 × 12 = 21,60 juta

Sisa Hutang Akhir periode 3 (setelah 12 bulan bayar):

Sisa\ Hutang\ Akhir\ (SHA) = TSH_3 - Pembayaran\ 12\ bulan

Sisa Hutang Akhir (SHA) = 43,20 -- 21,60 = 21,60 juta

Atau menggunakan rumus cepat:

Sisa\ Hutang\ Akhir\ (SHA) = TSH_3 \times \left( 1 - \frac{m}{t_p} \right)

Sisa Hutang Akhir (SHA) = 43,20 × (1 - ½) = 43,20 × 0,5 = 21,60 juta

Langkah 3: Hitung total bayar sebelum PSH

Komponen Nilai (juta)
Periode 1 (lunas) 43,92
Periode 2 (lunas) 43,56
Periode 3 (bayar 1 tahun) 21,60
Total bayar sebelum PSH 109,08

Langkah 4: Hitung PSH (berlaku pada sisa hutang akhir periode 3)

Faktor PSH untuk T = 6 tahun:

· T/50 = 6/50 = 0,12 (12%) untuk bank desa
· T/60 = 6/60 = 0,10 (10%) untuk bank kota

Wilayah Faktor Perhitungan PSH (juta)
Desa 0,12 21,60 × 0,12 = 2,592
Kota 0,10 21,60 × 0,10 = 2,160

Langkah 5: Hitung total bayar setelah PSH

Wilayah Total bayar sebelum PSH Sisa hutang PSH Sisa hutang setelah PSH Total bayar setelah PSH
Desa 109,08 21,60 2,592 19,008 109,08 + 19,008 = 128,088
Kota 109,08 21,60 2,160 19,440 109,08 + 19,440 = 128,520

Langkah 6: Hitung keuntungan bank

Total pinjaman akumulasi = 108 juta

Wilayah Total bayar setelah PSH Keuntungan (juta) Keuntungan (%) Return tahunan (%/tahun)
Desa 128,088 128,088 -- 108 = 20,088 20,088 / 108 × 100% = 18,60% 18,60% / 6 = 3,10%
Kota 128,520 128,520 -- 108 = 20,520 20,520 / 108 × 100% = 19,00% 19,00% / 6 = 3,17%

Langkah 7: Hitung spread suku bunga rata-rata

Periode SBDK Biaya dana+overhead Spread
1 11% 9% 2%
2 10,5% 9% 1,5%
3 10% 9% 1%

Rata-rata SBDK tertimbang:

\frac{(11\% \times 2) + (10,5\% \times 2) + (10\% \times 2)}{6} = \frac{22 + 21 + 20}{6} = \frac{63}{6} = 10,50\%

Rata-rata spread = 10,50% -- 9% = 1,50% per tahun

Rangkuman Varian A

Besaran Desa Kota
Total pinjaman 108 juta 108 juta
TSH₃ 43,20 juta 43,20 juta
Sisa Hutang Akhir (SHA) periode 3 21,60 juta 21,60 juta
PSH 2,592 juta (2,40% dari total pinjaman) 2,160 juta (2,00% dari total pinjaman)
Total bayar setelah PSH 128,088 juta 128,520 juta
Keuntungan bank 20,088 juta (18,60%) 20,520 juta (19,00%)
Return tahunan 3,10% 3,17%
Spread rata-rata 1,50% 1,50%

5.3. Varian B: 6 Periode × 1 Tahun (t_p = 1 tahun)

Dengan asumsi m = 0 (tidak bayar di periode 6)

Parameter Varian B

Besaran Nilai
n 6 periode
tₚ 1 tahun
T = n × tₚ 6 tahun
Total pinjaman akumulasi 6 × 36 = 216 juta
r₁ 11,0%
r₂ 10,5%
r₃ 10,0%
r₄ 9,5%
r₅ 9%
r₆ 8,5%
m (pembayaran di periode 6) 0 tahun

Langkah 1: Hitung TSH setiap periode

Rumus: $TSH_i = K \times (1 + r_i \times 1) = 36 \times (1 + r_i)$

Periode rᵢ Perhitungan TSH (juta)
1 11,0% 36 × 1,11 39,96
2 10,5% 36 × 1,105 39,78
3 10% 36 × 1,10 39,60
4 9,5% 36 × 1,095 39,42
5 9% 36 × 1,09 39,24
6 8,5% 36 × 1,085 39,06

Total TSH (jika dilunasi semua) = 39,96 + 39,78 + 39,60 + 39,42 + 39,24 + 39,06 = 237,06 juta.

Langkah 2: Tentukan skema pembayaran dan sisa hutang akhir

Asumsi pembayaran (m = 0):

· Periode 1 s.d. 5: Dibayar lunas (masing-masing 1 tahun penuh = 12 bulan)
· Periode 6 (periode terakhir): Tidak dibayar sama sekali (m = 0 tahun)

Periode 6 (periode terakhir)

· TSH₆ = 39,06 juta
· Pembayaran selama 0 tahun = 0 juta

Sisa hutang akhir periode 6:

Sisa\ Hutang\ Akhir = TSH_6 - 0 = 39,06\ juta

Atau menggunakan rumus cepat (m = 0, tₚ = 1 tahun):

Sisa\ Hutang\ Akhir = TSH_6 \times \left( 1 - \frac{m}{t_p} \right)

Sisa Hutang Akhir = 39,06 × (1 -- 0/1) = 39,06 × 1 = 39,06 juta

Langkah 3: Hitung total bayar sebelum PSH

Komponen Nilai (juta)
Periode 1 (lunas) 39,96
Periode 2 (lunas) 39,78
Periode 3 (lunas) 39,60
Periode 4 (lunas) 39,42
Periode 5 (lunas) 39,24
Periode 6 (bayar 0 tahun) 0
Total bayar sebelum PSH 198,00

Langkah 4: Hitung PSH (berlaku pada sisa hutang akhir periode 6)

Faktor PSH untuk T = 6 tahun:

· T/50 = 6/50 = 0,12 (12%) untuk desa
· T/60 = 6/60 = 0,10 (10%) untuk kota

Wilayah Faktor Perhitungan PSH (juta)
Desa 0,12 39,06 × 0,12 = 4,6872
Kota 0,10 39,06 × 0,10 = 3,906

Langkah 5: Hitung total bayar setelah PSH

Wilayah Total bayar sebelum PSH Sisa hutang PSH Sisa hutang setelah PSH Total bayar setelah PSH
Desa 198,00 39,06 4,6872 34,3728 198,00 + 34,3728 = 232,3728
Kota 198,00 39,06 3,906 35,154 198,00 + 35,154 = 233,154

Langkah 6: Hitung keuntungan bank

Total pinjaman akumulasi = 216 juta

Wilayah Total bayar setelah PSH Keuntungan (juta) Keuntungan (%) Return tahunan (%/tahun)
Desa 232,3728 232,3728 -- 216 = 16,3728 16,3728 / 216 × 100% = 7,58% 7,58% / 6 = 1,263%
Kota 233,154 233,154 -- 216 = 17,154 17,154 / 216 × 100% = 7,94% 7,94% / 6 = 1,323%

Langkah 7: PSH terhadap total pinjaman

Wilayah PSH (juta) Total pinjaman (juta) PSH (% thd total pinjaman)
Desa 4,6872 216 4,6872 / 216 × 100% = 2,17%
Kota 3,906 216 3,906 / 216 × 100% = 1,81%

Langkah 8: Spread suku bunga rata-rata

Periode SBDK Biaya dana+overhead Spread
1 11,0% 9% 2%
2 10,5% 9% 1,5%
3 10,0% 9% 1%
4 9,5% 9% 0,5%
5 9,0% 9% 0,0%
6 8,5% 9% -0,5%

Rata-rata SBDK sederhana:

\frac{11,0 + 10,5 + 10,0 + 9,5 + 9,0 + 8,5}{6} = \frac{58,5}{6} = 9,75\%

Rata-rata spread = 9,75% -- 9% = 0,75% per tahun (sama, karena spread tidak tergantung m).

Rangkuman Varian B (m = 0)

Besaran Desa Kota
Total pinjaman 216 juta 216 juta
TSH₆ 39,06 juta 39,06 juta
Sisa hutang akhir periode 6 39,06 juta 39,06 juta
PSH 4,6872 juta (2,17% dari total pinjaman) 3,906 juta (1,81% dari total pinjaman)
Total bayar setelah PSH 232,3728 juta 233,154 juta
Keuntungan bank 16,3728 juta (7,58%) 17,154 juta (7,94%)
Return tahunan 1,263% 1,323%
Spread rata-rata 0,75% 0,75%

Kesimpulan:

Semakin kecil m (semakin sedikit pembayaran di periode terakhir), maka:

· Sisa hutang akhir semakin besar
· PSH semakin besar (karena proporsi dari sisa hutang)
· Namun keuntungan bank sedikit lebih kecil (karena total bayar sebelum PSH lebih kecil)
· Return tahunan sedikit lebih rendah

5.4. Perbandingan Varian C dengan Varian A dan B (untuk T = 6 tahun, tₚ berbeda)

Untuk menunjukkan fleksibilitas, berikut hasil simulasi varian lain (perhitungan lengkap tersedia di Lampiran 4):

Varian (n × t_p) Wilayah Total pinjaman (jt) Keuntungan bank (%) PSH (% thd total pinjaman) Return tahunan setara
C (2 × 3 tahun) Desa 72 29,62% 2,63% 4,94%
 Kota 72 30,06% 2,19% 5,01%
A (3 × 2 tahun) Desa 108 18,60% 2,40% 3,10%
B (6 × 1 tahun) Kota 216 7,94% 1,808% 1,323%

Catatan: Varian D (1 × 6 tahun, bunga awal 11% dengan penurunan bunga 0,5% per periode, diperoleh PSH 3,32% di bank desa dan 2,77% di bank kota). Varian D tidak dimasukkan dalam naskah ini karena lebih cocok untuk produk kartu kredit atau kredit konsumtif, bukan untuk sektor produktif pangan dan energi.

Varian A (3 × 2 tahun):

· n=3, tₚ=2 tahun, K=36 juta/ periode (total pinjaman 108 juta)
· r₁=11%, r₂=10,5%, r₃=10%
· Asumsi pembayaran: lunas di periode 1 dan 2, periode 3 bayar 1 tahun (m=1)
· Sisa Hutang Akhir periode 3 = TSH₃ × (1 -- 1/2) = 43,20 × 0,5 = 21,60 juta
· PSH desa = 21,60 × 0,12 = 2,592 juta (2,40% dari total pinjaman)
· Keuntungan bank desa = 20,088 juta (18,60%)
· Return tahunan ≈ 3,10%

Varian B (6 × 1 tahun):

· n=6, tₚ=1 tahun, total pinjaman 216 juta
· r₁=11%, r₂=10,5%, r₃=10%, r₄=9,5%, r₅=9,0%, r₆=8,5%
· Asumsi pembayaran: lunas di periode 1, 2, 3, 4, dan 5, periode 6 bayar 0 tahun (m=0)
· Sisa Hutang Akhir periode 6 = TSH₃ × (1 -- 0/2) = 39,06 × 1 = 39,06 juta
· PSH kota = 39,06 × 0,10 = 3,906 juta (1,81% dari total pinjaman)
· Keuntungan bank kota = 17,154 juta (7,94%)
· Return tahunan ≈ 1,323%

Kesimpulan: Varian C (2×3 tahun) memberikan return tahunan tertinggi (4,94--5,01%) dan paling sesuai dengan rata-rata NIM perbankan Indonesia, dengan pemberian PSH yang signifikan (2,19--2,63% dari total pinjaman). Ini adalah pilihan utama win-win solution untuk UMKM sektor pangan dan energi di Nusantara.

TABEL PERBANDINGAN LENGKAP KETIGA VARIAN (dengan asumsi standar)

Varian Wilayah Total pinjaman (juta) Sisa hutang akhir (juta) PSH (% terhadap total pinjaman) Keuntungan bank (%) Return tahunan Spread rata-rata
C (2×3 tahun), m=2 Desa 72 15,78 2,63% 29,62% 4,94% 1,75%
 Kota 72 15,78 2,19% 30,06% 5,01% 1,75%
A (3×2 tahun), m=1 Desa 108 21,60 2,40% 18,60% 3,10% 1,50%
 Kota 108 21,60 2,00% 19,00% 3,17% 1,50%
B (6×1 tahun), m=0 Desa 216 39,06 2,17% 7,58% 1,263% 0,75%
 Kota 216 39,06 1,81% 7,94% 1,323% 0,75%

Catatan:

· Dalam naskah asli, varian B (6×1 tahun) hanya mencantumkan baris "Kota" dengan keuntungan 7,94% dan PSH 1,81%. Hasil perhitungan di atas konsisten.
· Varian dengan periode lebih panjang (t_p besar) memberikan keuntungan bank yang lebih tinggi dan PSH yang lebih besar, karena efek penurunan suku bunga hanya terjadi sedikit kali dan sisa hutang periode terakhir lebih besar. Varian 2×3 tahun (t_p=3) adalah yang paling seimbang untuk implementasi awal.

5.5. Kesimpulan Simulasi Berbagai Varian (C, A, B) Pada Sistem Ubelasy (Model Utama: Ubelasy 2 Periode, dPSH Maks = 2, dengan T = 6 tahun → dPSH = 0,24)

Berikut adalah tabel simulasi untuk Varian C, A, dan B (kota dan desa) berdasarkan parameter yang telah disepakati: total tenor T = 6 tahun, suku bunga awal 11%, penurunan 0,5% per periode, biaya dana (HPDK) = 7%, biaya overhead = 2% (total = 9%). Margin keuntungan bank = suku bunga pinjaman - (HPDK + overhead). SBDK (Suku Bunga Dasar Kredit) adalah suku bunga pinjaman yang dibebankan (karena model flat). NIM (Net Interest Margin) di sini disederhanakan sebagai margin keuntungan bank (selisih bunga pinjaman dan biaya dana+overhead). PSH diterima debitur dinyatakan dalam persen terhadap total pinjaman akumulasi (untuk memudahkan perbandingan).

Catatan tentang dPSH Maks = 2:

Dalam Sistem Ubelasy 2 periode, derajat Pembebasan Sisa Hutang (dPSH) didefinisikan sebagai $dPSH = \frac{2T}{50} = \frac{T}{25}$ dengan skala 0--2. Nilai dPSH = 2 tercapai jika total tenor T = 50 tahun (pembebasan penuh). Pada simulasi ini dengan T = 6 tahun, diperoleh dPSH = 6 / 25 = 0,24. Meskipun dPSH belum mencapai maksimum, sistem ini tetap dinamakan "Ubelasy 2 periode, dPSH Maks = 2" karena mengacu pada kapasitas maksimal sistem (ketika T = 50 tahun), implementasi awal menggunakan T yang lebih pendek.

Tabel 1: Ringkasan Varian (Bunga, Margin, PSH)

Varian Wilayah Bunga awal Rata-rata bunga Margin keuntungan bank (rata-rata) PSH diterima debitur (% thd total pinjaman)
C (2×3 tahun), Model Utama Desa 11% 10,75% 1,75% 2,63%
 Kota 11% 10,75% 1,75% 2,19%
A (3×2 tahun) Desa 11% 10,50% 1,50% 2,40%
B (6×1 tahun) Kota 11% 9,75% 0,75% 1,81%

Catatan: Rata-rata bunga dihitung dari suku bunga per periode ditimbang dengan lama periode. Margin keuntungan bank adalah selisih rata-rata bunga dengan total biaya dana+overhead (9%). PSH desa = SHAₙ × T/50 = 12% × SHAₙ; dan PSH kota = SHAₙ × T/60 = 10% × SHAₙ; lalu dibagi total pinjaman akumulasi.

Tabel 2: Detail Margin, SBDK, NIM (Per Periode)

Varian C (2 periode × 3 tahun) -- Model utama Ubelasy 2 periode

Periode Bunga pinjaman (SBDK) Biaya dana (HPDK) Biaya Overhead Margin keuntungan bank NIM (≈ margin)
1 11% 7% 2% 2% 2%
2 10,5% 7% 2% 1,5% 1,5%
Rata-rata 10,75% 7% 2% 1,75% 1,75%

Varian A (3 periode × 2 tahun)

Periode Bunga pinjaman (SBDK) Biaya dana (HPDK) Biaya Overhead Margin keuntungan bank NIM
1 11% 7% 2% 2% 2%
2 10,5% 7% 2% 1,5% 1,5%
3 10% 7% 2% 1% 1%
Rata-rata 10,5% 7% 2% 1,5% 1,5%

Varian B (6 periode × 1 tahun)

Periode Bunga pinjaman (SBDK) Biaya dana (HPDK) Biaya Overhead Margin keuntungan bank NIM
1 11% 7% 2% 2% 2%
2 10,5% 7% 2% 1,5% 1,5%
3 10% 7% 2% 1% 1%
4 9,5% 7% 2% 0,5% 0,5%
5 9% 7% 2% 0% 0%
6 8,5% 7% 2% -0,5% -0,5%
Rata-rata 9,75% 7% 2% 0,75% 0,75%

Penjelasan:

· SBDK (Suku Bunga Dasar Kredit) di sini sama dengan bunga pinjaman karena model flat.
· NIM (Net Interest Margin) secara sederhana adalah selisih bunga pinjaman dengan biaya dana (HPDK). Namun dalam tabel ini saya ikuti margin keuntungan setelah dikurangi overhead, agar lebih realistis.
· Varian B pada periode ke-5 margin 0%, periode ke-6 margin negatif -0,5% (artinya bank rugi kecil pada periode tersebut), namun secara keseluruhan rata-rata masih positif 0,75%. Ini masih bisa ditoleransi jika volume kredit besar dan NPL turun drastis.

Kesimpulan Simulasi untuk Sistem Ubelasy 2 Periode, dPSH Maks = 2

· Varian C (2×3 tahun) adalah model utama yang diusulkan dalam penelitian ini. Dengan dPSH = 0,24 (karena T=6 tahun), varian ini memberikan margin keuntungan rata-rata 1,75% per tahun serta PSH yang signifikan (2,63% untuk desa, 2,19% untuk kota). Ini merupakan pilihan win-win solution terbaik untuk implementasi awal di sektor pangan dan energi Sumatera Selatan.
· Varian A (3×2 tahun) menghasilkan margin 1,5% dan PSH 2,40% -- cocok untuk daerah pedesaan yang menginginkan tenor per periode lebih pendek (2 tahun) dengan tetap mengikuti skema penurunan bunga.
· Varian B (6×1 tahun) memberikan margin tipis (0,75%) dengan PSH kecil (1,81%) -- hanya cocok untuk wilayah perkotaan jika bank mengutamakan fleksibilitas penurunan bunga tahunan, namun perlu mendapat kompensasi insentif dari regulator.

Catatan Akhir: Meskipun dPSH maks = 2 (pembebasan penuh) baru tercapai jika total tenor T = 50 tahun, sistem ini dirancang agar dapat diadaptasi secara bertahap. Untuk T = 6 tahun, dPSH = 0,24 sudah cukup memberikan manfaat bagi debitur tanpa membebani bank. Ke depan, jika skema ini berhasil, tenor dapat diperpanjang (misalnya T = 25 tahun) sehingga dPSH mendekati 1 atau bahkan 2, sesuai dengan semangat Tahun Yobel.

Semua perhitungan ini konsisten dengan asumsi biaya dana 7% dan overhead 2%. Bank tetap untung positif (kecuali periode tertentu di varian B yang sangat kecil, tetapi rata-rata tetap positif). Dengan dukungan insentif regulator (pelonggaran GWM, penurunan bobot risiko kredit), Sistem Ubelasy 2 periode, dPSH Maks = 2 layak diujicobakan.

---

VI. SIMULASI PENGHITUNGAN VARIAN D (1 x 6 TAHUN)

Varian D ini hanya memiliki 1 periode dengan tenor 6 tahun. Karena hanya satu periode, maka tidak ada penurunan suku bunga antar periode (suku bunga tetap). Varian ini tidak direkomendasikan karena lebih cocok untuk produk kartu kredit atau kredit konsumtif jangka panjang, namun tetap kami hitung untuk kelengkapan perbandingan.

VARIAN D: 1 Periode × 6 Tahun (t_p = 6 tahun)

Parameter Varian D

Besaran Nilai
n 1 periode
tₚ 6 tahun
T = n × tₚ 6 tahun
Total pinjaman akumulasi 1 × 36 = 36 juta
r₁ 11% (tetap, karena hanya 1 periode)
Penurunan bunga Tidak ada (Δr tidak berlaku)
m (pembayaran di periode 1) 5 tahun (agar proporsional dengan varian lain)

Langkah 1: Hitung TSH periode 1

Rumus: $TSH_1 = K \times (1 + r_1 \times t_p) = 36 \times (1 + r_i)$

TSH_1 = 36 × (1 + 0,11 × 6) = 36 × (1 + 0,66) = 36 × 1,66 = 59,76 juta.

Langkah 2: Tentukan skema pembayaran dan Sisa Hutang Akhir (SHA)

Asumsi pembayaran:

· Periode 1 (satu-satunya periode): Dibayar 5 tahun (60 bulan), sisanya 1 tahun tidak dibayar sebelum PSH

Perhitungan:

· TSH₁ = 59,76 juta
· Tenor periode = 6 tahun = 72 bulan
· Angsuran per bulan = 59,76 / 72 = 0,83 juta/bulan (Rp 830.000)
· Pembayaran selama 5 tahun (60 bulan) = 0,83 × 60 = 49,80 juta

Sisa hutang akhir periode 1:

Sisa\ Hutang\ Akhir = TSH_1 - Pembayaran\ 60\ bulan

Sisa Hutang Akhir = 59,76 -- 49,8 = 9,96 juta

Atau menggunakan rumus cepat (m = 5, tₚ = 6 tahun):

Sisa\ Hutang\ Akhir = TSH_1 \times \left( 1 - \frac{m}{t_p} \right)

Sisa Hutang Akhir = 59,76 × (1 -- 5/6) = 59,76 × 1/6 = 9,96 juta

Langkah 3: Hitung total bayar sebelum PSH

Komponen Nilai (juta)
Periode 1 (bayar 5 tahun) 49,80 juta
Total bayar sebelum PSH 49,80 juta

Langkah 4: Hitung PSH (berlaku pada Sisa Hutang Akhir (SHA) periode 1)

Faktor PSH untuk T = 6 tahun:

· T/50 = 6/50 = 0,12 (12%) untuk desa
· T/60 = 6/60 = 0,10 (10%) untuk kota

Wilayah Faktor Perhitungan PSH (juta)
Desa 0,12 9,96 × 0,12 = 1,1952
Kota 0,10 9,96 × 0,10 = 0,996

Langkah 5: Hitung total bayar setelah PSH

Wilayah Total bayar sebelum PSH Sisa hutang PSH Sisa hutang setelah PSH Total bayar setelah PSH
Desa 49,80 9,96 1,1952 8,7648 49,80 + 8,7648 = 58,5648
Kota 49,80 9,96 0,996 8,964 49,80 + 8,964 = 58,764

Langkah 6: Hitung keuntungan bank

Total pinjaman akumulasi = 36 juta

Wilayah Total bayar setelah PSH Keuntungan (juta) Keuntungan (%) Return tahunan (%/tahun)
Desa 58,5648 58,5648 -- 36 = 22,5648 22,5646 / 36 × 100% = 62,68% 62,68% / 6 = 10,45
Kota 58,764 58,764 -- 36 = 22,764 22,764 / 36 × 100% = 63,23 63,23% / 6 = 10,54

Langkah 7: PSH terhadap total pinjaman

Wilayah PSH (juta) Total pinjaman (juta) PSH (% thd total pinjaman)
Desa 1,1952 36 1,1952 / 36 × 100% = 3,32%
Kota 0,996 36 0,996 / 36 × 100% = 2,77%

Langkah 8: Spread suku bunga

Karena hanya 1 periode dengan bunga tetap

SBDK Biaya dana+overhead Spread
11% 9% 2,00% per tahun

Rangkuman Varian D (1 × 6 tahun, m = 5 tahun)

Besaran Desa Kota
Total pinjaman 36 juta 36 juta
TSH₁ 59,76 juta 59,76 juta
Sisa hutang akhir periode 1 9,96 juta 9,96 juta
PSH 1,1952 juta (3,32% dari total pinjaman) 0,996 juta (2,77% dari total pinjaman)
Total bayar setelah PSH 58,5648 juta 58,764 juta
Keuntungan bank 22,5648 juta (62,68%) 22,764 juta (63,23%)
Return tahunan 10,45% 10,54%
Spread rata-rata 2,00% 2,00%

Kesimpulan VARIAN D (1 Periode × 6 tahun, m=5 tahun)

Aspek Penilaian
Return tahunan bank 10,45--10,54% (tertinggi di antara semua varian)
Spread 2,00% (tertinggi)
PSH bagi debitur 2,77--3,32% (cukup signifikan)
Kesesuaian dengan NIM perbankan Terlalu tinggi (di atas rata-rata 4,5--5,5%)
Penurunan suku bunga ❌ Tidak ada (hanya 1 periode)
Kesesuaian dengan Tahun Yobel ❌ Tidak ada pembebasan berkala
Rekomendasi untuk naskah ❌ Tidak direkomendasikan untuk sektor pangan dan energi

Alasan Varian D Tidak Dimasukkan ke Dalam Naskah Utama:

1. Tidak memiliki penurunan suku bunga periodik (hanya 1 periode, ∆r tidak berlaku).
2. Tidak sesuai dengan prinsip Tahun Yobel yang mengajarkan pembebasan berkala.
3. Kurang adaptif terhadap fluktuasi ekonomi selama 6 tahun.
4. Varian ini lebih cocok untuk produk kredit konsumtif atau kartu kredit, bukan untuk sektor produktif pangan dan energi yang membutuhkan fleksibilitas dan keadilan berkala. Oleh karena itu, Varian D tidak direkomendasikan untuk tujuan ketahanan pangan dan energi di Sumatera Selatan.
5. Return tahunan terlalu tinggi (10,45--10,54%) sehingga berpotensi membebani debitur karena tidak mencerminkan keadilan bagi debitur sektor pangan dan energi.

---

VII. KESIMPULAN FINAL VARIAN UBELASY DALAM NASKAH UTAMA

7.1. Tabel Perbandingan Lengkap Semua Varian (dengan asumsi standar)

Varian Wilayah Total pinjaman (jt) Sisa Hutang Akhir PSH (% thd total pinjaman) Keuntungan bank (%) Return tahunan Spread Status dalam naskah
C (2×3 thn) m=2 Desa 72 15,78 2,63% 29,62% 4,94% 1,75% ✅ Varian utama (dipilih untuk implementasi)
 Kota 72 15,78 2,19% 30,06% 5,01% 1,75% 
A (3×2 thn) m=1 Desa 108 21,60 2,40% 18,60% 3,10% 1,50% Sebagai pembanding (alternatif pro-debitur)
 Kota 108 21,60 2,00% 19,00% 3,17% 1,50% 
B (6×1 thn) m=0 Desa 216 39,06 juta 2,17% 7,58% 1,263% 0,75% Sebagai pembanding (alternatif pro-bank, dengan catatan)
 Kota 216 39,06 juta 1,81% 7,94% 1,323% 0,75% 
D (1×6 thn) m=5 Desa 36 9,96 3,32% 62,68% 10,45% 2,00% ❌ Tidak dimasukkan
 Kota 36 9,96 2,77% 63,23% 10,54% 2,00% 

7.2. Catatan Akhir

✅ Varian C (2×3 tahun) tetap menjadi pilihan utama karena:

· Return tahunan (4,94--5,01%) paling sesuai dengan rata-rata NIM perbankan Indonesia
· Memiliki penurunan suku bunga (11% → 10,5%)
· PSH cukup signifikan bagi debitur (2,19--2,63%)
· Merupakan win-win solution terbaik

✅ Varian A dan B hanya sebagai pembanding untuk menunjukkan fleksibilitas sistem.

✅ Varian D dengan m=5 tetap tidak direkomendasikan untuk dimasukkan ke dalam naskah utama karena:

1. Tidak memiliki penurunan suku bunga periodik
2. Return tahunan terlalu tinggi (10,45--10,54%)
3. Tidak sesuai dengan semangat Tahun Yobel yang mengajarkan pembebasan berkala
4. Lebih cocok untuk produk kredit komersial jangka panjang

7.3. Rekomendasi Final

Varian Status Alasan
C (2×3 tahun) ✅ PILIHAN UTAMA Return tahunan 4,94--5,01% (sesuai NIM perbankan), penurunan bunga, PSH signifikan.
A (3×2 tahun) ✅ PEMBANDING Return 3,10--3,17%, tenor per periode lebih pendek.
B (6×1 tahun) ✅ PEMBANDING Return 1,26--1,32%, fleksibilitas penurunan bunga tahunan.
D (1×6 tahun) ❌ TIDAK DIREKOMENDASIKAN Return terlalu tinggi (10,45--10,54%), tidak ada penurunan bunga, tidak sesuai Tahun Yobel

---

VIII. STATUS DEBITUR BERDASARKAN dPSH (DERAJAT PEMBEBASAN SISA HUTANG) PADA SISTEM UBELASY 2 PERIODE, dPSH MAKS = 2

8.1. KONSEP DASAR

dPSH (Derajat Pembebasan Sisa Hutang) adalah skala yang mengukur tingkat keringanan / pembebasan sisa hutang yang diterima oleh debitur dalam Sistem Ubelasy.

Nilai dPSH dihitung berdasarkan rumus yang telah ditetapkan:

dPSH = \frac{2T}{50} = \frac{T}{25}

dengan:

· T = total tenor pinjaman (dalam tahun), $0 < T \leq 50$
· Skala dPSH = 0 -- 2
· dPSH = 2 dicapai pada T = 50 tahun (setara dengan Tahun Yobel)

Dari Rumus PSH:

PSH_{desa} = SHA \times \frac{T}{50}

PSH_{kota} = SHA \times \frac{T}{60}

didapat hubungan PSH desa/kota dengan dPSH:

PSH_{desa} = SHA \times \frac{dPSH}{2}

PSH_{kota} = SHA \times \frac{dPSH}{2,4}

Kenaikan PSH per tahun (linier):

· Desa: setiap kenaikan T = 1 tahun → PSH naik 2% dari SHA
· Kota: setiap kenaikan T = 1 tahun → PSH naik 1,67% dari SHA

8.2. SKALA STATUS DEBITUR (dPSH 0 -- 2)

Berdasarkan nilai dPSH, debitur diklasifikasikan ke dalam 5 (lima) status utama:

dPSH Status Debitur Total Tenor (T) PSH (% dari SHA) Makna / Keterangan
0,00 -- 0,20 🟢 Pemula (Beginner) 0 -- 5 tahun 0 -- 10% 0 -- 8,33%
0,21 -- 0,50 🔵 Berkembang (Developing) 5,25 -- 12,5 tahun 10,5 -- 25% 8,75 -- 20,8%
0,51 -- 1,00 🟡 Madya (Intermediate) 12,75 -- 25 tahun 25,5 -- 50% 21,25 -- 41,7%
1,01 -- 1,80 🟠 Lanjut (Advanced) 26,25 -- 45 tahun 50,5 -- 90% 42,1 -- 75%
1,81 -- 2,00 🔴 Yobel (Jubilee) 45,25 -- 50 tahun 90,5 -- 100% 75,4 -- 83,3%

8.3. TABEL LENGKAP STATUS DEBITUR BERDASARKAN MODEL UBELASY VARIAN C

Dalam naskah utama, simulasi dilakukan dengan Varian C: 2 × 3 tahun (T = 6 tahun, dPSH = 0,24). Berdasarkan hasil perhitungan:

Parameter Nilai Keterangan
Total tenor (T) 6 tahun 2 periode × 3 tahun
dPSH 6 / 25 = 0,24 Termasuk dalam status Berkembang
SHA (Sisa Hutang Akhir) 15,78 juta Setelah pembayaran lunas di periode 1 (3 tahun), dan pembayaran 2 tahun di periode 2 (dari total 3 tahun periode 2)
PSH Desa 15,78 × (6/50) = 1,8936 juta (12% dari SHA) PSH = 12% × SHA
PSH Kota 15,78 × (6/60) = 1,578 juta (10% dari SHA) PSH = 10% × SHA
Keuntungan bank desa 29,62% dari total pinjaman Return tahunan = 4,94%
Keuntungan bank kota 30,06% dari total pinjaman Return tahunan = 5,01%

Kesimpulan: Debitur pada Varian C termasuk dalam status BERKEMBANG (Developing) dengan dPSH = 0,24. Debitur menerima PSH sebesar 12% (desa) atau 10% (kota) dari Sisa Hutang Akhir (SHA).

8.4. MAKNA SETIAP STATUS DEBITUR

🟢 Debitur Pemula (Beginner) -- dPSH 0,00 -- 0,20

Aspek Keterangan
Karakteristik Baru pertama kali mengakses kredit Ubelas, atau mengambil tenor pendek (<5 tahun)
PSH yang diterima Kecil (0--10% dari SHA untuk desa)
Tujuan Pembiasaan dengan sistem, edukasi keuangan, kredit musiman
Rekomendasi Didampingi pendamping lapangan untuk memahami mekanisme PSH

🔵 Debitur Berkembang (Developing) -- dPSH 0,21 -- 0,50

Aspek Keterangan
Karakteristik Telah menyelesaikan minimal 1 periode dengan baik; tenor sedang (5--12,5 tahun)
PSH yang diterima Mulai terasa (10,5--25% dari SHA untuk desa)
Tujuan Target utama implementasi awal Ubelas. Debitur mulai merasakan manfaat pembebasan
Contoh dalam Naskah (Varian C, 2×3 tahun) Varian C (T=6 tahun, dPSH=0,24) → PSH desa = 12% × SHA

🟡 Debitur Madya (Intermediate) -- dPSH 0,51 -- 1,00

Aspek Keterangan
Karakteristik Debitur loyal dengan riwayat pembayaran baik; tenor panjang (12,5--25 tahun)
PSH yang diterima Signifikan 21,25-41,7% (kota) atau 25,5-50% (desa) dari SHA
Tujuan Apresiasi atas loyalitas; mendorong usaha skala menengah ke atas
Contoh T=25 tahun (dPSH=1,00) → PSH desa = 50% × SHA

🟠 Debitur Lanjut (Advanced) -- dPSH 1,01 -- 1,80

Aspek Keterangan
Karakteristik Debitur dengan kontribusi ekonomi tinggi (penyerapan tenaga kerja, inovasi); tenor sangat panjang (25--45 tahun)
PSH yang diterima Sangat besar (50,5--90% dari SHA untuk desa)
Tujuan Insentif luar biasa bagi debitur yang mendukung ketahanan pangan & energi nasional
Catatan Memerlukan persetujuan khusus dari bank dan regulator

🔴 Debitur Yobel (Jubilee) -- dPSH 1,81 -- 2,00

Aspek Keterangan
Karakteristik Debitur dengan masa pinjaman mendekati 50 tahun; loyalitas ekstrem; atau dampak sosial luar biasa
PSH yang diterima Hampir penuh hingga penuh (90,5--100% dari SHA untuk desa)
Tujuan Pembebasan total setara Tahun Yobel (Imamat 25:8-12). Apresiasi tertinggi sistem
Contoh T=50 tahun (dPSH=2,00) → PSH desa = 100% × SHA (seluruh sisa hutang dibebaskan)

8.5. TABEL LENGKAP STATUS DEBITUR (DENGAN CONTOH NUMERIK)

Asumsi: Pinjaman K = Rp 36 juta per periode, SHA = 15,78 juta (seperti Varian C)

Status dPSH T (tahun) PSH Desa  PSH Kota 
   % dari SHA Nilai Rp % dari SHA Nilai Rp
Pemula 0,08 2 4% 0,6312 jt 3,33% 0,526 jt
 0,16 4 8% 1,2624 jt 6,67% 1,052 jt
Berkembang 0,24 6 12% 1,8936 jt 10,00% 1,578 jt
 0,40 10 20% 3,156 jt 16,67% 2,630 jt
Madya 0,60 15 30% 4,734 jt 25,00% 3,945 jt
 0,80 20 40% 6,312 jt 33,33% 5,260 jt
 1,00 25 50% 7,890 jt 41,67% 6,575 jt
Lanjut 1,20 30 60% 9,468 jt 50,00% 7,890 jt
 1,60 40 80% 12,624 jt 66,67% 10,520 jt
Yobel 1,80 45 90% 14,202 jt 75,00% 11,835 jt
 2,00 50 100% 15,780 jt 83,33% 13,150 jt

8.6. STATUS KHUSUS (FASILITAS TAMBAHAN)

Selain status berdasarkan dPSH, debitur juga dapat memperoleh status khusus berdasarkan faktor lain:

Status Khusus Kriteria Manfaat Tambahan
Debitur Pedesaan (Rural) Lokasi usaha di desa/terpencil PSH menggunakan rumus T/50 (lebih besar dari T/60)
Debitur Perkotaan (Urban) Lokasi usaha di kota PSH menggunakan rumus T/60 (sesuai batas keuntungan 1/6 × 100%)
Debitur Prioritas Pangan Sektor pertanian, perkebunan, perikanan Subsidi bunga / insentif fiskal dari Pemda
Debitur Prioritas Energi Sektor bioenergi, panas bumi, surya Pelonggaran agunan / penjaminan LPP
Debitur Berprestasi 3 periode berturut-turut tidak pernah terlambat Potongan bunga tambahan 0,25% di periode berikutnya
Debitur Terdampak Bencana Bencana alam (banjir, kekeringan, kebakaran) Percepatan PSH / restrukturisasi tanpa denda

8.7. MEKANISME EVALUASI STATUS

Aspek Keterangan
Periode evaluasi Status dievaluasi setiap akhir periode (setiap 3 tahun pada Varian C)
Kenaikan status Debitur dapat naik status jika memperpanjang tenor atau mengambil pinjaman baru dengan T lebih besar
Penurunan status Tidak terjadi kecuali debitur wanprestasi. Sistem Ubelas dirancang untuk melindungi, bukan menghukum
Reset siklus Setelah mencapai T = 50 tahun (dPSH = 2, status Yobel), debitur dapat memulai siklus baru dari awal (T=0, dPSH=0)

8.8. KESIMPULAN STATUS DEBITUR UNTUK UBELASY VERSI 2 PERIODE

Status Debitur dPSH Implementasi dalam Ubelas
🟢 Pemula 0,00 -- 0,20 Untuk kredit mikro jangka pendek, edukasi keuangan
🔵 Berkembang 0,21 -- 0,50 Fokus implementasi awal Ubelas (Varian C: T=6 tahun → dPSH=0,24)
🟡 Madya 0,51 -- 1,00 Untuk debitur loyal dengan tenor panjang (T=12,5--25 tahun)
🟠 Lanjut 1,01 -- 1,80 Insentif luar biasa untuk debitur berdampak tinggi (T=25--45 tahun)
🔴 Yobel 1,81 -- 2,00 Pembebasan total setara Tahun Yobel (T=45--50 tahun)

Debitur pada Varian C (2 periode × 3 Tahun) termasuk dalam status "Berkembang (Developing)" dengan dPSH = 0,24. Debitur menerima PSH sebesar 12% (desa) atau 10% (kota) dari Sisa Hutang Akhir (SHA). Setelah mencapai T = 50 tahun (dPSH = 2, status Yobel), debitur dapat memulai siklus baru dari awal (T=0, dPSH=0).

Catatan Akhir:

· Tabel dan perhitungan di atas sepenuhnya konsisten dengan naskah utama dan lampiran yang sudah ada.
· Rumus yang digunakan: PSH desa = SHA × T/50, PSH kota = SHA × T/60, dPSH = T/25.
· Varian C (2×3 tahun, T=6 tahun) termasuk dalam status BERKEMBANG dengan dPSH = 0,24.
· Status debitur dievaluasi setiap akhir periode (setiap 3 tahun pada Varian C).
· Debitur dapat naik status jika memperpanjang tenor atau mengambil pinjaman baru dengan T lebih besar.
· Penurunan status tidak terjadi kecuali debitur wanprestasi. Sistem Ubelasy dirancang untuk melindungi, bukan menghukum.

---

Jurnal & Karya Ilmiah (Penelitian Terdahulu):

1. Pakpahan, SR. (2025). Sistem Pinjaman Model Tahun Yobel (Tahun Pembebasan Sisa Hutang) Serba Guna Mengatasi Credit Crunch Dan Kredit Macet Pada Lembaga Perbankan Indonesia. (Dokumen pribadi / pre-print).

---

Nama Penulis: SR Pakpahan SST

Email: pakpahan.ministry@gmail.com

No. Telepon/HP: 082170814310

Pangkalan Kerinci, Mei 2026