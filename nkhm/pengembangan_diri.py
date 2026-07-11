# nkhm/pengembangan_diri.py
import streamlit as st
import re
import base64
from pathlib import Path

def parse_markdown_with_images(md_content, base_path):
    """Mem-parsing konten Markdown, mengganti sintaks gambar dengan st.image()"""
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    parts = re.split(image_pattern, md_content)
    
    for i in range(0, len(parts), 3):
        if i < len(parts) and parts[i].strip():
            st.markdown(parts[i])
        
        if i + 2 < len(parts):
            alt_text = parts[i + 1]
            img_path_str = parts[i + 2]
            
            possible_paths = [
                Path(img_path_str),
                base_path / img_path_str,
                Path(__file__).parent.parent / img_path_str,
                Path(__file__).parent.parent / "assets" / "images" / "mencintai_diri" / Path(img_path_str).name,
            ]
            
            img_path = None
            for p in possible_paths:
                if p.exists():
                    img_path = p
                    break
            
            if img_path and img_path.exists():
                st.image(str(img_path), caption=alt_text if alt_text else None, use_container_width=True)
            else:
                st.warning(f"⚠️ Gambar tidak ditemukan: {img_path_str}")
    
    if len(parts) % 3 == 1 and parts[-1].strip():
        st.markdown(parts[-1])

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
    st.markdown("## 📚 Pengembangan Diri")
    st.markdown("Klik pada salah satu judul dokumen untuk membaca isinya.")

    folder_dokumen = Path(__file__).parent.parent / "assets" / "dokumen"
    if not folder_dokumen.exists():
        st.warning(f"Folder dokumen tidak ditemukan: {folder_dokumen}")
        st.info("Silakan buat folder 'dokumen' di dalam folder 'assets' dan letakkan file di sana.")
        return

    files = get_document_files(folder_dokumen)
    if not files:
        st.info("Belum ada dokumen. Silakan upload file ke folder `assets/dokumen/`.")
        return

    # Gunakan session state untuk menyimpan file yang dipilih
    if "selected_doc" not in st.session_state:
        st.session_state.selected_doc = None

    # Tampilkan daftar file sebagai tombol
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        for file in files:
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
            
            if st.button(f"{icon} {file.name}", key=f"doc_{file.name}", use_container_width=True):
                st.session_state.selected_doc = file
                st.rerun()

    # Tampilkan isi dokumen yang dipilih
    if st.session_state.selected_doc is not None:
        selected_file = st.session_state.selected_doc
        st.markdown("---")
        st.subheader(f"Isi Dokumen: {selected_file.name}")
        ext = selected_file.suffix.lower()
        
        if ext == '.md':
            with st.spinner("Memuat dokumen..."):
                content = read_text_file(selected_file)
                base_path = Path(__file__).parent.parent
                parse_markdown_with_images(content, base_path)
        
        elif ext == '.txt':
            with st.spinner("Memuat dokumen..."):
                content = read_text_file(selected_file)
                st.markdown(content)
        
        elif ext == '.docx':
            with st.spinner("Memuat dokumen..."):
                content = read_docx_file(selected_file)
                if content.startswith("⚠️") or content.startswith("Error"):
                    st.error(content)
                else:
                    st.markdown(content)
        
        elif ext == '.odt':
            with st.spinner("Memuat dokumen..."):
                content = read_odt_file(selected_file)
                if content.startswith("⚠️") or content.startswith("Error"):
                    st.error(content)
                    st.info("💡 Saran: Konversi file .odt ke .pdf atau .md untuk tampilan yang lebih baik.")
                else:
                    st.markdown(content)
        
        elif ext == '.pdf':
            with st.spinner("Memuat PDF..."):
                display_pdf(selected_file)
        
        else:
            st.warning(f"Format file {ext} tidak didukung untuk ditampilkan.")

if __name__ == "__main__":
    show_pengembangan_diri()