import pytest
from app import app, db, User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF token checks during test actions

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_user_registration_success(client):
    """Test creating a new account with valid fields."""
    response = client.post('/register', data={
        'username': 'devops_engineer',
        'password': 'SecurePassword123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registration successful" in response.data


def test_user_registration_duplicate(client):
    """Test that the system prevents registering an existing username."""
    # First user
    client.post('/register', data={'username': 'alex', 'password': 'password125'})
    # Duplicate user attempt
    response = client.post('/register', data={'username': 'alex', 'password': 'differentpassword'},
                           follow_redirects=True)

    assert b"Username already exists" in response.data


def test_user_registration_missing_fields(client):
    """Test that empty inputs are rejected by the registration routing logic."""
    response = client.post('/register', data={'username': '', 'password': 'password123'}, follow_redirects=True)
    assert b"Username and password are required!" in response.data


def test_login_and_logout(client):
    """Test logging in with valid credentials and then terminating the session."""
    # Register first
    client.post('/register', data={'username': 'tester', 'password': 'password123'})

    # Test Login
    login_response = client.post('/login', data={
        'username': 'tester',
        'password': 'password123'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    # Test Logout
    logout_response = client.get('/logout', follow_redirects=True)
    assert logout_response.status_code == 200