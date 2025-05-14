# 03-Personal-Library-Manager

## Objective
Create a command-line Personal Library Manager that allows users to manage their book collection. The program should let users add, remove, and search for books. Each book will be stored as a dictionary with details like title, author, publication year, genre, and read status. The program should also include a menu system, basic statistics, and optional file handling for saving and loading the library.

## Requirements

### Core Features

#### Book Details:
Each book should have the following attributes:
- **Title** (string)
- **Author** (string)
- **Publication Year** (integer)
- **Genre** (string)
- **Read Status** (boolean: `True` if read, `False` if unread)

#### Menu System:
Implement a menu with the following options:
1. **Add a book**
2. **Remove a book**
3. **Search for a book**
4. **Display all books**
5. **Display statistics** (total books, percentage read)
6. **Exit**

#### Features:

1. **Add a Book**: 
   - Prompt the user to enter the book's details (Title, Author, Publication Year, Genre, Read Status) and add it to the library.

2. **Remove a Book**: 
   - Prompt the user to enter the title of the book to remove it from the library.

3. **Search for a Book**: 
   - Allow the user to search for a book by title or author.
   - Display all matching books.

4. **Display All Books**: 
   - Show all books in the library in a formatted way.

5. **Display Statistics**:
   - **Total Books**: Display the total number of books in the library.
   - **Percentage of Books Read**: Calculate and display the percentage of books that have been read.

6. **Exit**: 
   - Exit the program.

---

## Optional Challenge (File Handling)

### Save Library to a File:
- Save the library data to a file (e.g., `library.txt`) when the program exits.

### Load Library from a File:
- Load the library data from the file when the program starts.

---


