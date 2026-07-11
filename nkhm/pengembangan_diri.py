# nkhm/pengembangan_diri.py
import streamlit as st
import re
import base64
from pathlib import Path
import markdown


def parse_markdown_with_images(md_content, base_path):
    """
    Mem-parsing konten Markdown, mengganti sintaks gambar dengan st.image()
    dan menampilkan konten markdown dengan format yang benar
    """
    # Cek apakah ada gambar di konten
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    # Jika tidak ada gambar, tampilkan langsung dengan markdown
    if not re.search(image_pattern, md_content):
        # Konversi markdown ke HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['extra', 'tables', 'fenced_code']
        )
        st.markdown(html_content, unsafe_allow_html=True)
        return
    
    # Jika ada gambar, parse per bagian
    parts = re.split(image_pattern, md_content)
    
    for i in range(0, len(parts), 3):
        # Teks sebelum gambar
        if i < len(parts) and parts[i].strip():
            # Konversi teks markdown ke HTML
            html_text = markdown.markdown(parts[i], extensions=['extra', 'tables', 'fenced_code'])
            st.markdown(html_text, unsafe_allow_html=True)
        
        # Gambar
        if i + 2 < len(parts):
            alt_text = parts[i + 1] if parts[i + 1] else ""
            img_path_str = parts[i + 2]
            
            # Cari gambar di berbagai lokasi
            possible_paths = [
                Path(img_path_str),
                base_path / img_path_str,
                Path(__file__).parent.parent / img_path_str,
                Path(__file__).parent.parent / "assets" / "images" / Path(img_path_str).name,
                Path(__file__).parent.parent / "assets" / "dokumen" / Path(img_path_str).name,
            ]
            
            img_path = None
            for p in possible_paths:
                if p.exists():
                    img_path = p
                    break
            
            if img_path and img_path.exists():
                # Gunakan columns untuk gambar agar lebih rapi
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(str(img_path), caption=alt_text if alt_text else None, use_column_width=True)
            else:
                st.warning(f"⚠️ Gambar tidak ditemukan: {img_path_str}")
    
    # Sisa teks setelah gambar terakhir
    if len(parts) % 3 == 1 and parts[-1].strip():
        html_text = markdown.markdown(parts[-1], extensions=['extra', 'tables', 'fenced_code'])
        st.markdown(html_text, unsafe_allow_html=True)


def read_text_file(file_path):
    """Membaca file teks biasa (txt, md)"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error membaca file: {e}"


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
        import subprocess
        result = subprocess.run(['odt2txt', str(file_path)], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "⚠️ Gagal membaca file .odt. Pastikan odt2txt terinstal.\nAtau konversi file ke PDF/Markdown."
    except FileNotFoundError:
        return "⚠️ Library 'odt2txt' belum terinstal di sistem. Konversi file .odt ke PDF untuk tampilan yang lebih baik."
    except Exception as e:
        return f"Error membaca file .odt: {e}"


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


def get_document_files(folder_path):
    """Mengembalikan daftar file dalam folder (pdf, docx, odt, txt, md)"""
    if not folder_path.exists():
        return []
    files = []
    for ext in ['*.pdf', '*.docx', '*.odt', '*.txt', '*.md']:
        files.extend(folder_path.glob(ext))
    return sorted(files, key=lambda f: f.name)


def show_pengembangan_diri():
    """
    Menampilkan daftar dokumen dan isinya untuk fitur Pengembangan Diri
    """
    st.markdown("## 📚 Pengembangan Diri")
    st.markdown("Klik pada salah satu judul dokumen untuk membaca isinya.")
    st.markdown("---")

    # Tentukan folder dokumen
    folder_dokumen = Path(__file__).parent.parent / "assets" / "dokumen"
    
    # Buat folder jika belum ada
    if not folder_dokumen.exists():
        folder_dokumen.mkdir(parents=True, exist_ok=True)
        st.info(f"📁 Folder 'assets/dokumen' telah dibuat. Silakan upload file markdown (.md) Anda.")
        return

    # Dapatkan daftar file
    files = get_document_files(folder_dokumen)
    if not files:
        st.info("📂 Belum ada dokumen. Silakan upload file ke folder `assets/dokumen/`.")
        return

    # ========== TAMPILKAN DAFTAR FILE ==========
    # Gunakan session state untuk menyimpan file yang dipilih
    if "selected_doc" not in st.session_state:
        st.session_state.selected_doc = None

    # Tampilkan daftar file sebagai tombol dengan grid 2 kolom
    col1, col2 = st.columns(2)
    for idx, file in enumerate(files):
        # Tentukan ikon berdasarkan ekstensi
        icon = "📄"
        if file.suffix.lower() == '.pdf':
            icon = "📕"
        elif file.suffix.lower() == '.docx':
            icon = "📘"
        elif file.suffix.lower() == '.odt':
            icon = "📙"
        elif file.suffix.lower() == '.txt':
            icon = "📝"
        elif file.suffix.lower() == '.md':
            icon = "📓"
        
        # Tampilkan tombol di kolom yang sesuai
        with (col1 if idx % 2 == 0 else col2):
            if st.button(f"{icon} {file.name}", key=f"doc_{file.name}", use_container_width=True):
                st.session_state.selected_doc = file
                st.rerun()

    # ========== TAMPILKAN ISI DOKUMEN YANG DIPILIH ==========
    if st.session_state.selected_doc is not None:
        selected_file = st.session_state.selected_doc
        st.markdown("---")
        st.markdown(f"### 📖 {selected_file.name}")
        
        ext = selected_file.suffix.lower()
        
        # CSS untuk tampilan yang rapi
        st.markdown("""
        <style>
        .document-content {
            background-color: #f8f9fa;
            padding: 20px 30px;
            border-radius: 10px;
            border-left: 4px solid #2e7daf;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
        }
        .document-content h1 {
            color: #1a3c6e;
            border-bottom: 2px solid #2e7daf;
            padding-bottom: 10px;
        }
        .document-content h2 {
            color: #1a3c6e;
            border-left: 4px solid #2e7daf;
            padding-left: 15px;
            margin-top: 30px;
        }
        .document-content h3 {
            color: #2e7daf;
            margin-top: 25px;
        }
        .document-content h4 {
            color: #3a5a7a;
            margin-top: 20px;
        }
        .document-content blockquote {
            border-left: 4px solid #2e7daf;
            padding: 10px 20px;
            margin: 15px 0;
            background-color: #f0f5fa;
            border-radius: 0 5px 5px 0;
        }
        .document-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        .document-content th {
            background-color: #1a3c6e;
            color: white;
            padding: 10px 12px;
            border: 1px solid #ddd;
        }
        .document-content td {
            padding: 8px 12px;
            border: 1px solid #ddd;
        }
        .document-content tr:nth-child(even) {
            background-color: #f5f8fc;
        }
        .document-content ul, .document-content ol {
            padding-left: 25px;
        }
        .document-content li {
            margin: 5px 0;
        }
        .document-content hr {
            border: none;
            border-top: 2px solid #dce4ec;
            margin: 30px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        try:
            if ext == '.md':
                with st.spinner("Memuat dokumen..."):
                    content = read_text_file(selected_file)
                    if content.startswith("Error"):
                        st.error(content)
                    else:
                        # Gunakan markdown library untuk konversi
                        html_content = markdown.markdown(
                            content,
                            extensions=['extra', 'tables', 'fenced_code', 'codehilite']
                        )
                        st.markdown(f'<div class="document-content">{html_content}</div>', unsafe_allow_html=True)
                        
                        # Tombol download
                        st.markdown("---")
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            with open(selected_file, "r", encoding="utf-8") as f:
                                file_content = f.read()
                            st.download_button(
                                label="📥 Download Materi (Markdown)",
                                data=file_content,
                                file_name=selected_file.name,
                                mime="text/markdown",
                                use_container_width=True
                            )
            
            elif ext == '.txt':
                with st.spinner("Memuat dokumen..."):
                    content = read_text_file(selected_file)
                    if content.startswith("Error"):
                        st.error(content)
                    else:
                        st.markdown(f'<div class="document-content"><pre>{content}</pre></div>', unsafe_allow_html=True)
            
            elif ext == '.docx':
                with st.spinner("Memuat dokumen..."):
                    content = read_docx_file(selected_file)
                    if content.startswith("⚠️") or content.startswith("Error"):
                        st.error(content)
                    else:
                        st.markdown(f'<div class="document-content">{content}</div>', unsafe_allow_html=True)
            
            elif ext == '.odt':
                with st.spinner("Memuat dokumen..."):
                    content = read_odt_file(selected_file)
                    if content.startswith("⚠️") or content.startswith("Error"):
                        st.error(content)
                        st.info("💡 Saran: Konversi file .odt ke .pdf atau .md untuk tampilan yang lebih baik.")
                    else:
                        st.markdown(f'<div class="document-content">{content}</div>', unsafe_allow_html=True)
            
            elif ext == '.pdf':
                with st.spinner("Memuat PDF..."):
                    display_pdf(selected_file)
            
            else:
                st.warning(f"Format file {ext} tidak didukung untuk ditampilkan.")
                
        except Exception as e:
            st.error(f"Terjadi error saat memuat dokumen: {e}")
    
    # ========== TOMBOL REFRESH ==========
    st.markdown("---")
    if st.button("🔄 Refresh Daftar Materi", use_container_width=True):
        st.rerun()


if __name__ == "__main__":
    show_pengembangan_diri()