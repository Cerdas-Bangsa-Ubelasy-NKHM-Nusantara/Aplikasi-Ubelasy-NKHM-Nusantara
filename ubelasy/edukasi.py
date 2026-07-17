# ubelasy/edukasi.py
import streamlit as st
import markdown
from pathlib import Path
import base64
import subprocess


def get_document_files(folder_path):
    """Mengembalikan daftar file .md, .txt, .pdf, .docx, .odt dalam folder"""
    if not folder_path.exists():
        return []
    files = []
    for ext in ['*.md', '*.txt', '*.pdf', '*.docx', '*.odt']:
        files.extend(folder_path.glob(ext))
    return sorted(files, key=lambda f: f.name)


def read_text_file(file_path):
    """Membaca file teks (.md, .txt)"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error membaca file: {e}"


def render_markdown(content):
    """Mengkonversi dan menampilkan konten markdown dengan styling"""
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
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="markdown-content">{html_content}</div>', unsafe_allow_html=True)


def display_pdf(file_path):
    """Menampilkan file PDF di Streamlit"""
    try:
        import streamlit.components.v1 as components
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        components.html(
            f'''
            <embed src="data:application/pdf;base64,{base64_pdf}" 
                   type="application/pdf" 
                   width="100%" 
                   height="700" />
            ''',
            height=720,
            scrolling=True
        )
        return True
    except Exception as e:
        st.error(f"Gagal menampilkan PDF: {e}")
        return False


def read_docx_file(file_path):
    """Membaca file .docx"""
    try:
        from docx import Document
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except ImportError:
        return "⚠️ Library 'python-docx' belum terinstal. Silakan instal dengan `pip install python-docx`."
    except Exception as e:
        return f"Error membaca file .docx: {e}"


def read_odt_file(file_path):
    """Membaca file .odt (OpenDocument Text)"""
    try:
        result = subprocess.run(['odt2txt', str(file_path)], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "⚠️ Gagal membaca file .odt. Pastikan odt2txt terinstal.\nAtau konversi file ke PDF/Markdown."
    except FileNotFoundError:
        return "⚠️ Library 'odt2txt' belum terinstal di sistem. Konversi file .odt ke PDF untuk tampilan yang lebih baik."
    except Exception as e:
        return f"Error membaca file .odt: {e}"


def show_edukasi():
    """Fitur Edukasi: Pengembangan Diri & Literasi Keuangan"""
    
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
        key="edu_category_ubelasy"
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
        folder.mkdir(parents=True, exist_ok=True)
        st.info(f"📁 Folder '{folder.name}' telah dibuat. Silakan tambahkan file .md, .txt, .pdf, .docx, atau .odt.")
        return
    
    # ========== TAMPILKAN DESKRIPSI KATEGORI ==========
    st.markdown(f"### {icon} {title}")
    st.caption(description)
    
    # ========== DAFTAR FILE ==========
    files = get_document_files(folder)
    
    if not files:
        st.info(f"📂 Belum ada materi di kategori ini. Silakan tambahkan file ke folder `assets/dokumen/{folder.name}/`.")
        
        # Tampilkan panduan
        with st.expander("📖 Cara Menambahkan Materi"):
            st.markdown(f"""
            1. Buka folder `assets/dokumen/{folder.name}/` di repositori Anda
            2. Upload file yang ingin ditampilkan (format: .md, .txt, .pdf, .docx, .odt)
            3. Refresh halaman ini
            
            **Tips:**
            - Gunakan awalan angka untuk urutan, misal: `01_Pengenalan_Keuangan.md`
            - Gunakan underscore (_) sebagai pengganti spasi
            - Untuk hasil tampilan terbaik, gunakan format .md (Markdown)
            """)
        return
    
    # ========== PILIH MATERI ==========
    st.markdown("### 📄 Pilih Materi")
    
    # Buat pilihan file dengan nama yang lebih rapi
    file_options = {}
    for f in files:
        # Tentukan ikon berdasarkan ekstensi
        ext = f.suffix.lower()
        if ext == '.md':
            icon_file = "📓"
        elif ext == '.txt':
            icon_file = "📝"
        elif ext == '.pdf':
            icon_file = "📕"
        elif ext == '.docx':
            icon_file = "📘"
        elif ext == '.odt':
            icon_file = "📙"
        else:
            icon_file = "📄"
        
        display_name = f"{icon_file} {f.stem.replace('_', ' ').title()}"
        file_options[display_name] = f
    
    selected_name = st.selectbox(
        "Pilih materi:",
        list(file_options.keys()),
        key="doc_selector_ubelasy"
    )
    
    if selected_name:
        selected_file = file_options[selected_name]
        ext = selected_file.suffix.lower()
        
        # ========== TAMPILKAN KONTEN ==========
        st.markdown("---")
        st.markdown(f"### 📖 {selected_file.stem.replace('_', ' ').title()}")
        
        try:
            # ========== TAMPILKAN BERDASARKAN EKSTENSI ==========
            if ext == '.md':
                content = read_text_file(selected_file)
                if content.startswith("Error"):
                    st.error(content)
                else:
                    render_markdown(content)
            
            elif ext == '.txt':
                content = read_text_file(selected_file)
                if content.startswith("Error"):
                    st.error(content)
                else:
                    st.markdown(f'<div class="markdown-content"><pre style="white-space: pre-wrap;">{content}</pre></div>', unsafe_allow_html=True)
            
            elif ext == '.pdf':
                display_pdf(selected_file)
            
            elif ext == '.docx':
                content = read_docx_file(selected_file)
                if content.startswith("⚠️") or content.startswith("Error"):
                    st.error(content)
                    if "python-docx" in content:
                        st.info("💡 Untuk membaca file .docx, instal library python-docx:\n`pip install python-docx`")
                else:
                    st.markdown(f'<div class="markdown-content">{content}</div>', unsafe_allow_html=True)
            
            elif ext == '.odt':
                content = read_odt_file(selected_file)
                if content.startswith("⚠️") or content.startswith("Error"):
                    st.error(content)
                    st.info("💡 Saran: Konversi file .odt ke .pdf atau .md untuk tampilan yang lebih baik.")
                else:
                    st.markdown(f'<div class="markdown-content">{content}</div>', unsafe_allow_html=True)
            
            else:
                st.warning(f"Format file {ext} tidak didukung untuk ditampilkan.")
            
            # ========== TOMBOL DOWNLOAD ==========
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Tentukan MIME type
                mime_types = {
                    '.md': 'text/markdown',
                    '.txt': 'text/plain',
                    '.pdf': 'application/pdf',
                    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    '.odt': 'application/vnd.oasis.opendocument.text'
                }
                mime_type = mime_types.get(ext, 'application/octet-stream')
                
                with open(selected_file, "rb") as f:
                    file_content = f.read()
                
                st.download_button(
                    label=f"📥 Download {selected_file.name}",
                    data=file_content,
                    file_name=selected_file.name,
                    mime=mime_type,
                    use_container_width=True
                )
                    
        except Exception as e:
            st.error(f"❌ Gagal memuat materi: {e}")
    
    # ========== TOMBOL REFRESH ==========
    st.markdown("---")
    if st.button("🔄 Refresh Daftar Materi", use_container_width=True):
        st.rerun()