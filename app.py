from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('library.db', check_same_thread=False)
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT NOT NULL,
        available BOOLEAN DEFAULT 1,
        borrower_name TEXT
    )
''')
conn.commit()

@app.route('/')
def index():
    # Fetch all books from the database
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']

    # Insert the book into the database
    cursor.execute('INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)', (title, author, isbn))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/borrow_book/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    borrower_name = request.form['borrower_name']

    # Update the availability status and borrower name of the book
    cursor.execute('''
        UPDATE books
        SET available = 0, borrower_name = ?
        WHERE id = ?
    ''', (borrower_name, book_id))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/return_book/<int:book_id>')
def return_book(book_id):
    # Update the availability status and clear borrower name of the book
    cursor.execute('UPDATE books SET available = 1, borrower_name = NULL WHERE id = ?', (book_id,))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/remove_book/<int:book_id>')
def remove_book(book_id):
    # Remove the book from the database
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/search_books', methods=['GET'])
def search_books():
    search_term = request.args.get('search', '')

    # Fetch books matching the search term from the database
    cursor.execute('''
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
    ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    books = cursor.fetchall()

    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
