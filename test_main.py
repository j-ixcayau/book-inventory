
import pytest
from main import app, db
from main import Book, Genre, Inventory, Pricing

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Book Inventory Management" in response.data

def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200
    # assert len(response.get_json()) == 2  # Assuming two sample books were inserted in init_database

def test_create_book(client):
    new_book_data = {
        "isbn": "978-3-13",
        "title": "Sample Book 3",
        "author": "Author Three",
        "genreId": 2  # Assuming 2 is the ID for NON_FICTION genre
    }

    response = client.post('/books', json=new_book_data)
    assert response.status_code == 201

    # Check if the returned data matches the expected structure
    returned_data = response.get_json()
    assert "id" in returned_data
    assert returned_data["ISBN"] == new_book_data["isbn"]
    assert returned_data["title"] == new_book_data["title"]
    assert returned_data["author"] == new_book_data["author"]
    assert returned_data["genre_id"] == new_book_data["genreId"]

def test_create_duplicate_book(client):
    # Attempt to create a book with duplicate ISBN
    duplicate_book_data = {
        "isbn": "978-3-16",  # Already exists in the database
        "title": "Duplicate Book",
        "author": "Author Four",
        "genreId": 1  # Assuming 1 is the ID for FICTION genre
    }

    response = client.post('/books', json=duplicate_book_data)
    assert response.status_code == 409  # Conflict status code for duplicate entry

def test_update_book(client):
    book_id = 1  # Assuming the ID of the first book

    updated_book_data = {
        "isbn": "978-3-16",
        "title": "Updated Book Title",
        "author": "Updated Author Name",
        "genreId": 1
    }

    response = client.put(f'/books/{book_id}', json=updated_book_data)
    assert response.status_code == 200

    # Check if the book was updated correctly
    updated_book = Book.query.get(book_id)
    assert updated_book.ISBN == updated_book_data["isbn"]
    assert updated_book.title == updated_book_data["title"]
    assert updated_book.author == updated_book_data["author"]
    assert updated_book.genre_id == updated_book_data["genreId"]

def test_delete_book(client):
    book_id = 1  # Assuming the ID of the first book

    response = client.delete(f'/books/{book_id}')
    assert response.status_code == 204

    # Check if the book was deleted
    deleted_book = Book.query.get(book_id)
    assert deleted_book is None

def test_update_price(client):
    book_id = 1  # Assuming the ID of the first book

    updated_price_data = {
        "price": 25.99
    }

    response = client.put(f'/books/{book_id}/price', json=updated_price_data)
    assert response.status_code == 200

    # Check if the price was updated correctly
    updated_pricing = Pricing.query.filter_by(book_id=book_id).first()
    assert updated_pricing.price == updated_price_data["price"]

def test_update_quantity(client):
    book_id = 1  # Assuming the ID of the first book

    updated_quantity_data = {
        "quantity": 50
    }

    response = client.put(f'/books/{book_id}/quantity', json=updated_quantity_data)
    assert response.status_code == 200

    # Check if the quantity was updated correctly
    updated_inventory = Inventory.query.filter_by(book_id=book_id).first()
    assert updated_inventory.quantity == updated_quantity_data["quantity"]
