# This file contains mock tests for the API routes to verify logic without a real database.

import pytest
from unittest.mock import patch, MagicMock
from app import create_app

@pytest.fixture
def client():
    """Sets up a test client for the application."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_healthz_returns_ok(client):
    """Tests if the /healthz endpoint returns a 200 OK status."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

@patch('app.routes.films.ReadSession')
def test_get_films_returns_200(mock_read_session, client):
    """Tests if listing films returns a 200 status code."""
    mock_session = MagicMock()
    mock_read_session.return_value = mock_session
    mock_session.query.return_value.limit.return_value.all.return_value = []
    
    response = client.get("/api/films/")
    assert response.status_code == 200

@patch('app.routes.films.WriteSession')
def test_create_film_returns_201(mock_write_session, client):
    """Tests if creating a new film returns a 201 Created status."""
    mock_session = MagicMock()
    mock_write_session.return_value = mock_session
    
    response = client.post("/api/films/", json={
        "title": "Test Movie",
        "description": "A test movie",
        "release_year": 2024
    })
    
    assert response.status_code == 201
    assert "film_id" in response.json

@patch('app.routes.films.ReadSession')
def test_get_film_not_found_returns_404(mock_read_session, client):
    """Tests if requesting a non-existent film returns a 404 Not Found."""
    mock_session = MagicMock()
    mock_read_session.return_value = mock_session
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    response = client.get("/api/films/9999")
    assert response.status_code == 404

@patch('app.routes.customers.ReadSession')
def test_get_customers_returns_200(mock_read_session, client):
    """Tests if listing active customers returns a 200 status code."""
    mock_session = MagicMock()
    mock_read_session.return_value = mock_session
    mock_session.query.return_value.filter_by.return_value.limit.return_value.all.return_value = []
    
    response = client.get("/api/customers/")
    assert response.status_code == 200

@patch('app.routes.customers.WriteSession')
def test_create_customer_returns_201(mock_write_session, client):
    """Tests if registering a new customer returns a 201 Created status."""
    mock_session = MagicMock()
    mock_write_session.return_value = mock_session
    
    response = client.post("/api/customers/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    })
    
    assert response.status_code == 201
    assert "customer_id" in response.json

@patch('app.routes.rentals.WriteSession')
def test_create_rental_returns_201(mock_write_session, client):
    """Tests if creating a rental returns a 201 Created status."""
    mock_session = MagicMock()
    mock_write_session.return_value = mock_session
    
    response = client.post("/api/rentals/", json={
        "inventory_id": 1,
        "customer_id": 1,
        "staff_id": 1
    })
    
    assert response.status_code == 201
    assert "rental_id" in response.json

@patch('app.routes.rentals.WriteSession')
def test_return_rental_updates_return_date(mock_write_session, client):
    """Tests if returning a rental correctly commits the update and returns 200."""
    mock_session = MagicMock()
    mock_write_session.return_value = mock_session
    
    # Mocking the rental object returned by the database query
    mock_rental = MagicMock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_rental
    
    response = client.put("/api/rentals/1/return")
    
    assert response.status_code == 200
    assert response.json["message"] == "Rental returned"
    # Ensure the transaction was committed
    mock_session.commit.assert_called_once()
