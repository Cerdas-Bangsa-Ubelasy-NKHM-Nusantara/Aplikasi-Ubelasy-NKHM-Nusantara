# nkhm/pengembangan_diri.py
import streamlit as st
from pathlib import Path

def read_text_file(file_path):
    """Membaca file teks (txt, md)"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error membaca file: {e}"

def read_docx_file(file_path):
    """Membaca file .docx (perlu python-docx)"""
    try:
        from docx import Document
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except ImportError:
        return "⚠️ Library 'python-docx' belum terinstal. Tidak dapat membaca file .docx. Silakan instal dengan `pip install python-docx`."
    except Exception as e:
        return f"Error membaca file .docx: {e}"

def get_document_files(folder_path):
    """Mengembalikan daftar file dalam folder (txt, md, docx)"""
    if not folder_path.exists():
        return []
    files = []
    for ext in ['*.txt', '*.md', '*.docx']:
        files.extend(folder_path.glob(ext))
    return sorted(files, key=lambda f: f.name)

def show_pengembangan_diri():
    # Di dalam fungsi read_markdown_file atau show_pengembangan_diri
    import os
    img_path = Path(__file__).parent.parent / "assets" / "images" / "mencintai_diri" / "image1.png"
    st.write(f"Debug: gambar ditemukan? {img_path.exists()}")
    if img_path.exists():
        st.image(str(img_path))
    
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

    # Tampilkan daftar file sebagai tombol
    selected_file = None
    for file in files:
        if st.button(f"📄 {file.name}", key=f"doc_{file.name}", use_container_width=True):
            selected_file = file

    if selected_file:
        st.markdown("---")
        st.subheader(f"Isi Dokumen: {selected_file.name}")
        ext = selected_file.suffix.lower()
        if ext in ['.txt', '.md']:
            content = read_text_file(selected_file)
            st.markdown(content)
        elif ext == '.docx':
            content = read_docx_file(selected_file)
            st.markdown(content)
        else:
            st.warning(f"Format file {ext} tidak didukung untuk ditampilkan.")

if __name__ == "__main__":
    show_pengembangan_diri()
  
