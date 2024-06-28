from sqlite3 import IntegrityError
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
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
    books = db.relationship('Book', backref='genre', lazy=True)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    inventory = db.relationship('Inventory', backref='book', uselist=False)
    pricing = db.relationship('Pricing', backref='book', uselist=False)

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
def getBooks():
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

@app.route('/books', methods=['POST'])
def createBook():
    data = request.get_json()
    ISBN = data.get('isbn')
    title = data.get('title')
    author = data.get('author')
    genre_id = data.get('genreId')

    if not ISBN or not title or not author or not genre_id:
        return jsonify({"message": "ISBN, title, author, and genre_id are required"}), 400

    try:
        new_book = Book(ISBN=ISBN, title=title, author=author, genre_id=genre_id)
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred"}), 500

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
def updateBook(id):
    data = request.get_json()
    book = Book.query.get(id)

    if not book:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    book.ISBN = data.get('isbn', book.ISBN)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre_id = data.get('genreId', book.genre_id)

    db.session.commit()

    return jsonify({
        "id": book.id,
        "ISBN": book.ISBN,
        "title": book.title,
        "author": book.author,
        "genre_id": book.genre_id
    }), 200

@app.route('/books/<int:id>', methods=['DELETE'])
def deleteBook(id):
    # Check if the book exists
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    # If the book exists, call the stored procedure to delete the book and its dependencies
    db.session.execute(text('CALL deleteBookAndDependencies(:bookId)'), {'bookId': id})
    db.session.commit()

    return '', 204

@app.route('/books/<int:id>/price', methods=['PUT'])
def updatePrice(id):
    price = request.get_json()

    if price is None:
        return jsonify({"message": "Price is required"}), 400

    pricing = Pricing.query.filter_by(book_id=id).first()

    if not pricing:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    pricing.price = price
    db.session.commit()

    return jsonify({
        "book_id": pricing.book_id,
        "price": pricing.price
    }), 200

@app.route('/books/<int:id>/quantity', methods=['PUT'])
def updateQuantity(id):
    quantity = request.get_json()

    if quantity is None:
        return jsonify({"message": "Quantity is required"}), 400

    inventory = Inventory.query.filter_by(book_id=id).first()

    if not inventory:
        return jsonify({"message": "Book not found", "type": "NotFound"}), 404

    inventory.quantity = quantity
    db.session.commit()

    return jsonify({
        "book_id": inventory.book_id,
        "quantity": inventory.quantity
    }), 200


if __name__ == '__main__':
    app.run(port=5000)
