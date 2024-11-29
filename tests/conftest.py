import os
import tempfile
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SANDBOX_ENABLED': True,
        'SANDBOX_TIMEOUT': 5
    })

    # Create the database and load test data
    with app.app_context():
        db.create_all()
        # Create test user
        user = User(username='test_user', email='test@example.com')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()

    yield app

    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with authentication."""
    client.post('/login', data={
        'username': 'test_user',
        'password': 'test_password'
    }, follow_redirects=True)
    return client
