-- Create database
CREATE DATABASE book_inventory_management;
USE book_inventory_management;

-- Create genre table
CREATE TABLE genre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Create book table
CREATE TABLE book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ISBN VARCHAR(13) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

-- Create inventory table
CREATE TABLE inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (book_id) REFERENCES book(id)
);

-- Create pricing table
CREATE TABLE pricing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (book_id) REFERENCES book(id)
);

-- Create trigger to insert into inventory and pricing tables
DELIMITER //

CREATE TRIGGER after_book_insert
AFTER INSERT ON book
FOR EACH ROW
BEGIN
    -- Insert into inventory table
    INSERT INTO inventory (book_id, quantity) VALUES (NEW.id, 0);

    -- Insert into pricing table
    INSERT INTO pricing (book_id, price) VALUES (NEW.id, 0.00);
END;
//

DELIMITER ;

-- Procedure to delete

DELIMITER //

CREATE PROCEDURE deleteBookAndDependencies(IN bookId INT)
BEGIN
    DELETE FROM inventory WHERE book_id = bookId;
    DELETE FROM pricing WHERE book_id = bookId;
    DELETE FROM book WHERE id = bookId;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE getBooksInfo()
BEGIN
    SELECT
        book.id,
        book.ISBN,
        book.title,
        book.author,
        genre.id as genre_id,
        genre.name AS genre,
        inventory.quantity,
        pricing.price
    FROM
        book
    JOIN
        genre ON book.genre_id = genre.id
    JOIN
        inventory ON book.id = inventory.book_id
    JOIN
        pricing ON book.id = pricing.book_id;
END //

DELIMITER ;


-- Insert sample genres
INSERT INTO genre (name) VALUES ('FICTION');
INSERT INTO genre (name) VALUES ('NON_FICTION');

-- Insert sample books
INSERT INTO book (ISBN, title, author, genre_id)
VALUES
('978-3-16', 'Sample Book 1', 'Author One', (SELECT id FROM genre WHERE name = 'FICTION')),
('978-1-23', 'Sample Book 2', 'Author Two', (SELECT id FROM genre WHERE name = 'NON_FICTION'));

-- Select books with genre names
CALL getBooksInfo();
