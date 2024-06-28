from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import text

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Abcd123$@localhost/book_inventory_management"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = relationship('Book', backref='genre', lazy=True)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    genre = relationship('Genre')
    inventory = relationship('Inventory', uselist=False, backref='book')
    pricing = relationship('Pricing', uselist=False, backref='book')

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Pricing(db.Model):
    __tablename__ = 'pricing'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

@app.route('/', methods=['GET'])
def main():
    return "Welcome to Book Inventory Management", 200

@app.route('/books', methods=['GET'])
def get_books():
    books_info = db.session.execute(text('CALL getBooksInfo()')).fetchall()
    books_list = []
    for book_info in books_info:
        book_data = {
            "id": book_info[0],
            "ISBN": book_info[1],
            "title": book_info[2],
            "author": book_info[3],
            "genre_id": book_info[4],
            "genre": book_info[5],
            "quantity": book_info[6],
            "price": book_info[7]
        }
        books_list.append(book_data)
    return jsonify(books_list), 200

@app.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    book_data = {
        "id": book.id,
        "ISBN": book.ISBN,
        "title": book.title,
        "author": book.author,
        "genre": book.genre.name,
        "quantity": book.inventory.quantity if book.inventory else 0,
        "price": float(book.pricing.price) if book.pricing else 0.0
    }
    return jsonify(book_data), 200

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    isbn = data.get('isbn')
    title = data.get('title')
    author = data.get('author')
    genre_id = data.get('genreId')

    if not isbn or not title or not author or not genre_id:
        return jsonify({"message": "ISBN, title, author, and genre_id are required"}), 400

    new_book = Book(ISBN=isbn, title=title, author=author, genre_id=genre_id)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "id": new_book.id,
        "ISBN": new_book.ISBN,
        "title": new_book.title,
        "author": new_book.author,
        "genre_id": new_book.genre_id,
        "quantity": 0,
        "price": 0.0,
    }), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    data = request.get_json()
    book.ISBN = data.get('ISBN', book.ISBN)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre_id = data.get('genre_id', book.genre_id)
    db.session.commit()

    return jsonify({
        "id": book.id,
        "ISBN": book.ISBN,
        "title": book.title,
        "author": book.author,
        "genre_id": book.genre_id
    }), 200

@app.route('/books/<int:id>/quantity', methods=['PUT'])
def update_quantity(id):
    inventory = Inventory.query.filter_by(book_id=id).first()
    if inventory is None:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    data = request.get_json()
    inventory.quantity = data.get('quantity', inventory.quantity)
    db.session.commit()

    return jsonify({"message": "Quantity updated successfully"}), 200

@app.route('/books/<int:id>/price', methods=['PUT'])
def update_price(id):
    pricing = Pricing.query.filter_by(book_id=id).first()
    if pricing is None:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    data = request.get_json()
    pricing.price = data.get('price', pricing.price)
    db.session.commit()

    return jsonify({"message": "Price updated successfully"}), 200

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    Inventory.query.filter_by(book_id=id).delete()
    Pricing.query.filter_by(book_id=id).delete()
    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"}), 204


app.run()