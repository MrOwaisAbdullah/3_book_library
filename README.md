# Personal Library Manager

A simple command-line application to manage your personal book collection, built with Python. Add, remove, search, and track books, with features like statistics and reading recommendations.

## Features
- **Add Books**: Input title, author, year, genre, and read status.
- **Remove Books**: Delete books by title.
- **Search**: Find books by title or author (case-insensitive partial matches).
- **Display All Books**: View your library with numbered entries and read/unread status (✅/🟩).
- **Statistics**: See total books and percentage read.
- **Recommend**: Get a random unread book suggestion.
- **Update Read Status**: Change a book’s read/unread status.
- **Persistent Storage**: Saves to `library.json` after every change.

## Requirements
- Python 3
- No external dependencies beyond standard libraries (`json`, `random`).

## Notes
 - Invalid inputs (e.g., non-numeric year, non-yes/no read status) prompt re-entry.
 - Changes are saved immediately, so no data is lost even if you exit abruptly.
