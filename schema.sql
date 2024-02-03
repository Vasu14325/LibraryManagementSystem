-- Drop the table if it exists
DROP TABLE IF EXISTS books;

-- Create the books table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL,
    available BOOLEAN DEFAULT 1,
    borrower_name TEXT
);
