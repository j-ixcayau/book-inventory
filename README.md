# Book Inventory Management

Welcome to the Book Inventory Management project! This project provides a RESTful API for managing a collection of books, including functionalities such as adding, updating, retrieving, and deleting books, as well as updating book quantities and prices.

## Project Structure

-   **main.py**: Contains the main Flask application and API endpoints.
-   **test_main.py**: Contains the pytest unit and integration tests for the project.

## Database Setup

Ensure that you have a MySQL database running. You will need to create a database and set up the necessary tables.
Execute the atached sql file

## Running the Project

1. Install the required dependencies:

2. Update the `app.py` file with your MySQL database configuration:

    ```python
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<username>:<password>@localhost/book_inventory_management"
    ```

3. Run the Flask application:

    ```sh
    python app.py
    ```

## API Documentation

The API provides the following endpoints:

-   **GET /**: Welcome message.
-   **GET /books**: Retrieve a list of all books.
-   **POST /books**: Add a new book.
-   **PUT /books/{id}**: Update an existing book.
-   **DELETE /books/{id}**: Delete a book by ID.
-   **PUT /books/{id}/quantity**: Update the quantity of a book.
-   **PUT /books/{id}/price**: Update the price of a book.

## Testing

Integration tests are located in the `tests/` directory. These tests ensure that the API endpoints are functioning correctly when integrated with the database.

1. Install pytest and pytest-order:

    ```sh
    pip install pytest pytest-order
    ```

2. Run the tests:

    ```sh
    pytest
    ```

## Postman Collection

To facilitate manual testing, a Postman collection can be created to test the various API endpoints. Import this collection into Postman to easily test the API.
