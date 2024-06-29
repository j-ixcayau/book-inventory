import pytest
from main import app

book_id = None  # Global variable to store the created book ID

@pytest.fixture(scope='module')
def client():
    with app.test_client() as client:
        yield client

@pytest.mark.order(1)
def test_get_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Book Inventory Management" in response.data

@pytest.mark.order(2)
def test_get_books(client):
    response = client.get('/books')
    assert response.status_code == 200

@pytest.mark.order(3)
def test_create_book(client):
    global book_id

    new_book_data = {
        "isbn": "isbn_example",
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

    # Store the created book ID in the global variable
    book_id = returned_data["id"]

@pytest.mark.order(4)
def test_create_duplicate_book(client):
    duplicate_book_data = {
        "isbn": "isbn_example",  # Already exists in the database
        "title": "Duplicate Book",
        "author": "Author Four",
        "genreId": 1  # Assuming 1 is the ID for FICTION genre
    }

    response = client.post('/books', json=duplicate_book_data)
    assert response.status_code == 500  # Conflict status code for duplicate entry

@pytest.mark.order(5)
def test_update_book(client):
    global book_id
    assert book_id is not None, "book_id should have been set by test_create_book"

    updated_book_data = {
        "isbn": "978-3-16",
        "title": "Updated Book Title",
        "author": "Updated Author Name",
        "genreId": 1
    }

    response = client.put(f'/books/{book_id}', json=updated_book_data)
    assert response.status_code == 200

@pytest.mark.order(6)
def test_update_price(client):
    global book_id
    assert book_id is not None, "book_id should have been set by test_create_book"

    updated_price_data = 25.99

    response = client.put(f'/books/{book_id}/price', json=updated_price_data)
    assert response.status_code == 200

@pytest.mark.order(7)
def test_update_quantity(client):
    global book_id
    assert book_id is not None, "book_id should have been set by test_create_book"

    updated_quantity_data = 50

    response = client.put(f'/books/{book_id}/quantity', json=updated_quantity_data)
    assert response.status_code == 200

@pytest.mark.order(8)
def test_delete_book(client):
    global book_id
    assert book_id is not None, "book_id should have been set by test_create_book"

    response = client.delete(f'/books/{book_id}')
    assert response.status_code == 204
