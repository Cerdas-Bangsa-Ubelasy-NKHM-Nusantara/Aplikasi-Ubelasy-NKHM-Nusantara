import React from 'react';
import { getInitialData } from '../utils';
import NoteInput from './NoteInput';
import NotesList from './NotesList';
import NoteSearch from './NoteSearch'; // Import komponen pencarian

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      notes: getInitialData(),      // [Basic] data awal dari utils
      searchKeyword: '',            // [Skilled] state untuk kata kunci pencarian
    };

    // binding method
    this.onAddNoteHandler = this.onAddNoteHandler.bind(this);
    this.onDeleteHandler = this.onDeleteHandler.bind(this);
    this.onArchiveHandler = this.onArchiveHandler.bind(this);
    this.onSearchHandler = this.onSearchHandler.bind(this);
  }

  // [Basic] Tambah catatan baru
  onAddNoteHandler({ title, body }) {
    const newNote = {
      id: +new Date(),              // id unik dari timestamp
      title,
      body,
      createdAt: new Date().toISOString(),
      archived: false,             // catatan baru selalu aktif
    };
    this.setState((prevState) => ({
      notes: [newNote, ...prevState.notes],
    }));
    // [Advanced] Catatan baru langsung muncul di daftar aktif (karena archived = false)
  }

  // [Basic] Hapus catatan berdasarkan id
  onDeleteHandler(id) {
    this.setState((prevState) => ({
      notes: prevState.notes.filter((note) => note.id !== id),
    }));
  }

  // [Advanced] Arsip / Batal arsip (toggle archived)
  onArchiveHandler(id) {
    this.setState((prevState) => ({
      notes: prevState.notes.map((note) =>
        note.id === id ? { ...note, archived: !note.archived } : note
      ),
    }));
  }

  // [Skilled] Simpan keyword pencarian ke state
  onSearchHandler(keyword) {
    this.setState({ searchKeyword: keyword });
  }

  render() {
    const { notes, searchKeyword } = this.state;

    // [Skilled] Filter catatan berdasarkan keyword (case-insensitive)
    let filteredNotes = notes;
    if (searchKeyword.trim() !== '') {
      const lowerKeyword = searchKeyword.toLowerCase();
      filteredNotes = notes.filter(
        (note) =>
          note.title.toLowerCase().includes(lowerKeyword) ||
          note.body.toLowerCase().includes(lowerKeyword)
      );
    }

    // [Advanced] Pisahkan catatan aktif & arsip, lalu urutkan dari terbaru ke terlama
    const sortByDateDesc = (a, b) => new Date(b.createdAt) - new Date(a.createdAt);
    const activeNotes = filteredNotes
      .filter((note) => !note.archived)
      .sort(sortByDateDesc);
    const archivedNotes = filteredNotes
      .filter((note) => note.archived)
      .sort(sortByDateDesc);

    return (
      <div className="note-app" data-testid="note-app">
        <div className="note-app__header" data-testid="note-app-header">
          <h1>Notes</h1>
          {/* [Skilled] Tambahkan komponen pencarian di header */}
          <NoteSearch onSearch={this.onSearchHandler} />
        </div>

        <div className="note-app__body" data-testid="note-app-body">
          <NoteInput addNote={this.onAddNoteHandler} />

          {/* Section Catatan Aktif */}
          <section
            aria-labelledby="active-notes-title"
            data-testid="active-notes-section"
          >
            <h2 id="active-notes-title">Catatan Aktif</h2>
            <NotesList
              notes={activeNotes}
              onDelete={this.onDeleteHandler}
              onArchive={this.onArchiveHandler}
              dataTestId="active-notes-list"
              searchKeyword={searchKeyword}
              isArchivedSection={false}
            />
          </section>

          {/* Section Catatan Arsip */}
          <section
            aria-labelledby="archived-notes-title"
            data-testid="archived-notes-section"
          >
            <h2 id="archived-notes-title">Arsip</h2>
            <NotesList
              notes={archivedNotes}
              onDelete={this.onDeleteHandler}
              onArchive={this.onArchiveHandler}
              dataTestId="archived-notes-list"
              searchKeyword={searchKeyword}
              isArchivedSection={true}
            />
          </section>
        </div>
      </div>
    );
  }
}

export default App;