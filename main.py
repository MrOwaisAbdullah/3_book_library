import random
import sqlite3

# Add a new books
def add_book(library):
    """Add books to library"""

    while True:
        title = input("Enter the book title: ")
        if not title.strip(): 
            print("Title cannot be empty.\n")
        if title.strip():
            break
    
    while True:
        author = input("Enter the author: ")
        if not author.strip(): 
            print("Author Name cannot be empty.\n")
        if author.strip():
            break
    
    while True:
        try:
            year = int(input("Enter the publication year: "))
            break
        except ValueError:
            print("Invalid year. Please enter a number.\n")

    while True:
        genre = input("Enter the genre: ")
        if not genre.strip(): 
            print("Genre cannot be empty.\n")
        if genre.strip():
            break

    while True:
        read_input = input("Have you read this book? (yes/no): ").strip().lower()
        if read_input == 'yes':
            read = True
            break
        elif read_input == 'no':
            read = False
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.\n")

    cursor = library.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, year, genre, read)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, year, genre, read))
    library.commit()
    print("\nBook added successfully!\n")

# Update Book status
def update_read_status(library):
    title = input("\nEnter the title of the book to update: ").lower()
    cursor = library.cursor()
    
    # Check if the book exists
    cursor.execute("SELECT * FROM books WHERE LOWER(title) = ?", (title,))
    book = cursor.fetchone()
    
    if book:
        while True:
            read_input = input("Have you read this book? (yes/no): ").strip().lower()
            if read_input == 'yes':
                read = 1
                break
            elif read_input == 'no':
                read = 0
                break
            else:
                print("\nInvalid input. Please enter 'yes' or 'no'.")
        
        # Perform the update
        cursor.execute("UPDATE books SET read = ? WHERE LOWER(title) = ?", (read, title))
        library.commit()
        print("\nRead status updated!\n")
    else:
        print("\nBook not found.\n")

# Remove a book
def remove_book(library):
    """remove the book if found"""
    title = input("\nEnter the title of the book to remove: ").lower()
    
    cursor = library.cursor()

    cursor.execute("DELETE FROM books WHERE LOWER(title) = ?", (title,))

    if cursor.rowcount > 0:
        library.commit()
        print("\nBook removed successfully!\n")
    else:
        print("\nBook not found.\n")

# Search for books
def search_book(library):
    """Search book by title or author."""
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ")
    term = input("Enter the search term: ").lower()
    cursor = library.cursor()

    cursor.execute(""" SELECT * FROM books""")

    books = cursor.fetchall()

    if not books:
        print("\nYour library is empty.\n")
        return
    if choice == '1':
        cursor.execute("SELECT * FROM books WHERE LOWER(title) LIKE ?", ('%' + term + '%',))
    elif choice == '2':
        cursor.execute("SELECT * FROM books WHERE LOWER(author) LIKE ?", ('%' + term + '%',))
    else:
        print("Invalid choice.")
        return
    matches = cursor.fetchall()

    if matches:
        print("\nMatching Books:")
        for book in matches:
            print(format_book(book))
        print("\n")
    else:
        print("No matching books found.\n")

# Display all books
def display_books(library):
    """Print all books in a formatted way."""
    cursor = library.cursor()

    cursor.execute(""" SELECT * FROM books""")

    books = cursor.fetchall()

    if not books:
        print("\nYour library is empty.\n")
        return
    print("\nYour Books:")

    for index, book in enumerate(books, start=1):
        title = book['title']
        author = book['author']
        year = book['year']
        genre = book['genre']
        read_status = "✅ Read" if book['read'] else "🟩 Unread"
        print(f"{index}. {title} by {author} ({year}) - {genre} - {read_status}")

    print("\n")

# Display statistics
def display_statistics(library):
    """Show total books and percentage read."""
    cursor = library.cursor()

    cursor.execute("SELECT COUNT(*) FROM books ")

    total_books = cursor.fetchone()[0]
    
    if total_books == 0:
        print("\nTotal books: 0\nPercentage read: 0.0%")
        return
    
    cursor.execute("SELECT COUNT(*) FROM books WHERE read = 1")
    read_books = cursor.fetchone()[0]

    percentage = (read_books / total_books) * 100
    print(f"\nTotal books: {total_books}\nPercentage read: {percentage:.1f}%\n")

# Recommend an unread book
def recommend_book(library):
    """Suggest a random unread book."""

    cursor = library.cursor()

    cursor.execute(""" SELECT * FROM books WHERE read = 0""")

    unread_books = cursor.fetchall()

    if unread_books:
        recommended = random.choice(unread_books)
        print(f"\nRecommended book: {format_book(recommended)}\n")
    else:
        print("\nNo unread books available.")

# Format book details
def format_book(book):
    """Return a book’s details as a string."""
    read_status = "✅ Read" if book['read'] else "🟩 Unread"
    return f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"


# Main program loop
def main():
    try:
        library = sqlite3.connect('library.db')
        library.row_factory = sqlite3.Row

        cursor = library.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                read BOOLEAN
            )
        ''')

        while True:
            print("\nWelcome to My Personal Library Manager\n")
            print("1. Add a book")
            print("2. Remove a book")
            print("3. Search for a book")
            print("4. Display all books")
            print("5. Display statistics")
            print("6. Recommend a book to read next")
            print("7. Update Book Read Status")
            print("8. Exit")
            choice = input("Enter your choice: ")
            
            if choice == '1':
                add_book(library)
            elif choice == '2':
                remove_book(library)
            elif choice == '3':
                search_book(library)
            elif choice == '4':
                display_books(library)
            elif choice == '5':
                display_statistics(library)
            elif choice == '6':
                recommend_book(library)
            elif choice == '7':
                update_read_status(library)
            elif choice == '8':
                print("\nGoodbye!\n\n")
                break
            else:
                print("Invalid choice. Please try again.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        library.close()

main()