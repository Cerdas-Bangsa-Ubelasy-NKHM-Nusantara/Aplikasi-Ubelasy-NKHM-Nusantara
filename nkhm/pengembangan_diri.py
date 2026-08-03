# nkhm/pengembangan_diri.py
import streamlit as st
import markdown
import logging
from pathlib import Path

# ========== LOGGING ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ========== FUNGSI BANTU UNTUK RERUN YANG AMAN ==========
def safe_rerun():
    """Memanggil st.rerun() dengan penanganan error untuk menghindari crash."""
    try:
        st.rerun()
    except Exception as e:
        logging.warning(f"st.rerun gagal di pengembangan_diri: {e}")

def get_document_files(folder_path):
    """Mengembalikan daftar file .md dalam folder"""
    try:
        if not folder_path.exists():
            return []
        files = list(folder_path.glob("*.md"))
        return sorted(files, key=lambda f: f.name)
    except Exception as e:
        logging.error(f"Error get_document_files: {e}")
        return []

def read_text_file(file_path):
    """Membaca file teks (.md)"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error membaca file {file_path}: {e}")
        return f"Error membaca file: {e}"

def render_markdown(content):
    """Mengkonversi dan menampilkan konten markdown dengan styling"""
    try:
        html_content = markdown.markdown(
            content,
            extensions=['extra', 'tables', 'fenced_code', 'codehilite']
        )
        
        st.markdown("""
        <style>
        .markdown-content {
            background-color: #f8f9fa;
            padding: 20px 30px;
            border-radius: 10px;
            border-left: 4px solid #2e7daf;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            margin: 15px 0;
        }
        .markdown-content h1 {
            color: #1a3c6e;
            border-bottom: 2px solid #2e7daf;
            padding-bottom: 10px;
        }
        .markdown-content h2 {
            color: #1a3c6e;
            border-left: 4px solid #2e7daf;
            padding-left: 15px;
            margin-top: 30px;
        }
        .markdown-content h3 {
            color: #2e7daf;
            margin-top: 25px;
        }
        .markdown-content h4 {
            color: #3a5a7a;
            margin-top: 20px;
        }
        .markdown-content blockquote {
            border-left: 4px solid #2e7daf;
            padding: 10px 20px;
            margin: 15px 0;
            background-color: #f0f5fa;
            border-radius: 0 5px 5px 0;
        }
        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        .markdown-content th {
            background-color: #1a3c6e;
            color: white;
            padding: 10px 12px;
            border: 1px solid #ddd;
        }
        .markdown-content td {
            padding: 8px 12px;
            border: 1px solid #ddd;
        }
        .markdown-content tr:nth-child(even) {
            background-color: #f5f8fc;
        }
        .markdown-content ul, .markdown-content ol {
            padding-left: 25px;
        }
        .markdown-content li {
            margin: 5px 0;
        }
        .markdown-content hr {
            border: none;
            border-top: 2px solid #dce4ec;
            margin: 30px 0;
        }
        .markdown-content .highlight-box {
            background-color: #e8f0fe;
            border: 1px solid #2e7daf;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }
        /* Dark mode support */
        .dark-mode .markdown-content {
            background-color: #1a1a2e;
            color: #d0d0e0;
            border-left-color: #4a8abf;
        }
        .dark-mode .markdown-content h1,
        .dark-mode .markdown-content h2 {
            color: #7ab7e0;
        }
        .dark-mode .markdown-content h3 {
            color: #5a9acf;
        }
        .dark-mode .markdown-content blockquote {
            background-color: #1a1a3a;
            border-left-color: #4a8abf;
        }
        .dark-mode .markdown-content th {
            background-color: #2a3a5a;
        }
        .dark-mode .markdown-content tr:nth-child(even) {
            background-color: #22223a;
        }
        .dark-mode .markdown-content .highlight-box {
            background-color: #1a1a4a;
            border-color: #3a6a8a;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<div class="markdown-content">{html_content}</div>', unsafe_allow_html=True)
    except Exception as e:
        logging.error(f"Error render_markdown: {e}")
        st.error(f"❌ Gagal merender konten: {e}")

def show_pengembangan_diri():
    """Fitur Pengembangan Diri dengan dua kategori: Pengembangan Diri & Literasi Keuangan"""
    try:
        st.markdown("## 📚 Pusat Edukasi")
        st.markdown("""
        <div style="background-color: #e8f0fe; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2e7daf;">
            <p style="margin: 0; font-size: 16px;">
                💡 <strong>Selamat datang di Pusat Edukasi!</strong> Temukan berbagai materi untuk 
                mengembangkan diri dan meningkatkan literasi keuangan Anda.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========== PILIH KATEGORI ==========
        category = st.radio(
            "Pilih Kategori",
            ["📚 Pengembangan Diri", "💰 Literasi Keuangan"],
            horizontal=True,
            key="edu_category"
        )
        
        st.markdown("---")
        
        # ========== TENTUKAN FOLDER ==========
        base_folder = Path(__file__).parent.parent / "assets" / "dokumen"
        
        if category == "📚 Pengembangan Diri":
            folder = base_folder / "pengembangan_diri"
            icon = "📖"
            title = "Materi Pengembangan Diri"
            description = "Konten inspiratif untuk pertumbuhan spiritual, mental, dan karakter."
        else:
            folder = base_folder / "literasi_keuangan"
            icon = "💰"
            title = "Materi Literasi Keuangan"
            description = "Panduan praktis untuk mengelola keuangan, investasi, dan mencapai kebebasan finansial."
        
        # Buat folder jika belum ada
        if not folder.exists():
            try:
                folder.mkdir(parents=True, exist_ok=True)
                st.info(f"📁 Folder '{folder.name}' telah dibuat. Silakan tambahkan file .md.")
                return
            except Exception as e:
                logging.error(f"Error membuat folder {folder}: {e}")
                st.error(f"❌ Gagal membuat folder: {e}")
                return
        
        # ========== TAMPILKAN DESKRIPSI KATEGORI ==========
        st.markdown(f"### {icon} {title}")
        st.caption(description)
        
        # ========== DAFTAR FILE ==========
        files = get_document_files(folder)
        
        if not files:
            st.info(f"📂 Belum ada materi di kategori ini. Silakan tambahkan file .md ke folder `assets/dokumen/{folder.name}/`.")
            
            # Tampilkan panduan
            with st.expander("📖 Cara Menambahkan Materi"):
                st.markdown(f"""
                1. Buka folder `assets/dokumen/{folder.name}/` di repositori Anda
                2. Upload file markdown (.md) yang ingin ditampilkan
                3. Refresh halaman ini
                
                **Tips Penamaan File:**
                - Gunakan awalan angka untuk urutan, misal: `01_Pengenalan_Keuangan.md`
                - Gunakan underscore (_) sebagai pengganti spasi
                - Nama file akan menjadi judul materi
                """)
            return
        
        # ========== PILIH MATERI ==========
        st.markdown("### 📄 Pilih Materi")
        
        # Buat pilihan file dengan nama yang lebih rapi
        file_options = {}
        for f in files:
            try:
                # Hapus ekstensi dan ubah underscore menjadi spasi
                display_name = f.stem.replace("_", " ").title()
                file_options[display_name] = f
            except Exception as e:
                logging.error(f"Error memproses file {f}: {e}")
                continue
        
        if not file_options:
            st.warning("Tidak ada file yang valid ditemukan.")
            return
        
        selected_name = st.selectbox(
            "Pilih materi:",
            list(file_options.keys()),
            key="doc_selector"
        )
        
        if selected_name and selected_name in file_options:
            selected_file = file_options[selected_name]
            
            # ========== TAMPILKAN KONTEN ==========
            st.markdown("---")
            st.markdown(f"### 📖 {selected_name}")
            
            try:
                content = read_text_file(selected_file)
                if content.startswith("Error"):
                    st.error(content)
                else:
                    render_markdown(content)
                    
                    # ========== TOMBOL DOWNLOAD ==========
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        try:
                            with open(selected_file, "r", encoding="utf-8") as f:
                                file_content = f.read()
                            st.download_button(
                                label="📥 Download Materi (Markdown)",
                                data=file_content,
                                file_name=selected_file.name,
                                mime="text/markdown",
                                use_container_width=True
                            )
                        except Exception as e:
                            logging.error(f"Error download file {selected_file}: {e}")
                            st.warning("Gagal menyiapkan file untuk download.")
                        
            except Exception as e:
                logging.error(f"Error memuat materi {selected_file}: {e}")
                st.error(f"❌ Gagal memuat materi: {e}")
        elif selected_name:
            st.warning("Materi yang dipilih tidak ditemukan.")
        
        # ========== TOMBOL REFRESH ==========
        st.markdown("---")
        if st.button("🔄 Refresh Daftar Materi", use_container_width=True):
            safe_rerun()
            
    except Exception as e:
        logging.error(f"Error di show_pengembangan_diri: {e}", exc_info=True)
        st.error(f"❌ Terjadi error di Pusat Edukasi: {e}")
        st.exception(e)

if __name__ == "__main__":
    show_pengembangan_diri()