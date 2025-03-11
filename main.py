import json
import random

# Load library from library.json file
def load_library():
    """Load the saved book library"""
    try:
        with open('library.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save library to library.json file
def save_library(library):
    """Save the book to library file"""
    try:
        with open('library.json', 'w', encoding='utf-8') as f:
            json.dump(library, f)
    except IOError:
        print("Error saving library to file.")

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

    book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
    library.append(book)
    print("\nBook added successfully!\n")

# Update Book status
def update_read_status(library):
    title = input("\nEnter the title of the book to update: ").lower()
    for book in library:
        if book['title'].lower() == title:
            while True:
                read_input = input("Have you read this book? (yes/no): ").strip().lower()
                if read_input == 'yes':
                    book['read'] = True
                    break
                elif read_input == 'no':
                    book['read'] = False
                    break
                else:
                    print("\nInvalid input. Please enter 'yes' or 'no'.")
            print("\nRead status updated!\n")
            return 
    print("\nBook not found.")

# Remove a book
def remove_book(library):
    """remove the book if found"""
    title = input("\nEnter the title of the book to remove: ").lower()
    for book in library:
        if book['title'].lower() == title:
            library.remove(book)
            print("\nBook removed successfully!\n")
            return
    print("\nBook not found.")

# Search for books
def search_book(library):
    """Search book by title or author."""
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ")
    term = input("Enter the search term: ").lower()
    matches = []
    if choice == '1':
        matches = [book for book in library if term in book['title'].lower()]
    elif choice == '2':
        matches = [book for book in library if term in book['author'].lower()]
    else:
        print("Invalid choice.")
        return
    if matches:
        print("\nMatching Books:")
        for book in matches:
            print(format_book(book))
    else:
        print("No matching books found.\n")

# Display all books
def display_books(library):
    """Print all books in a formatted way."""
    if not library:
        print("\nYour library is empty.\n")
        return
    for index, book in enumerate(library, start=1):
        title = book['title']
        author = book['author']
        year = book['year']
        genre = book['genre']
        read_status = "✅ Read" if book['read'] else "🟩 Unread"
        print(f"{index}. {title} by {author} ({year}) - {genre} - {read_status}")

# Display statistics
def display_statistics(library):
    """Show total books and percentage read."""
    total = len(library)
    if total == 0:
        print("\nTotal books: 0\nPercentage read: 0.0%")
        return
    read_count = sum(1 for book in library if book['read'])
    percentage = (read_count / total) * 100
    print(f"\nTotal books: {total}\nPercentage read: {percentage:.1f}%")

# Recommend an unread book
def recommend_book(library):
    """Suggest a random unread book."""
    unread_books = [book for book in library if not book['read']]
    if unread_books:
        recommended = random.choice(unread_books)
        print(f"\nRecommended book: {format_book(recommended)}")
    else:
        print("\nNo unread books available.")

# Format book details
def format_book(book):
    """Return a book’s details as a string."""
    read_status = "✅ Read" if book['read'] else "🟩 Unread"
    return f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}"

# Main program loop
def main():
    library = load_library()
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
            save_library(library)
        elif choice == '2':
            remove_book(library)
            save_library(library)
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
            save_library(library)
        elif choice == '8':
            save_library(library)
            print("\n\nGoodbye!\n")
            break
        else:
            print("Invalid choice. Please try again.")

main()