import pytest
from flask import session
from app.models import User

def test_login_page(client):
    """Test that login page loads correctly."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Sign in to Bloom' in response.data

def test_valid_login(client):
    """Test login with valid credentials."""
    response = client.post('/login', data={
        'username': 'test_user',
        'password': 'test_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back' in response.data

def test_invalid_login(client):
    """Test login with invalid credentials."""
    response = client.post('/login', data={
        'username': 'test_user',
        'password': 'wrong_password'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data

def test_logout(auth_client):
    """Test logout functionality."""
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign in to Bloom' in response.data

def test_protected_routes(client):
    """Test that protected routes require authentication."""
    routes = ['/', '/tasks', '/files', '/sandbox']
    for route in routes:
        response = client.get(route, follow_redirects=True)
        assert b'Sign in to Bloom' in response.data

def test_authenticated_access(auth_client):
    """Test that authenticated users can access protected routes."""
    routes = ['/', '/tasks', '/files', '/sandbox']
    for route in routes:
        response = auth_client.get(route)
        assert response.status_code == 200
