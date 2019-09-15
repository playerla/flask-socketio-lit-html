# https://flask.palletsprojects.com/en/1.1.x/testing/
import os
import tempfile

import pytest

from app import WebcomponentApp, db

@pytest.fixture
def client():
    app = WebcomponentApp(db, "app_test.db")
    with app.test_client() as client:
        yield client
    os.remove(app.config['DB_FILE'])

def test_app_init(client):
    rv = client.get('/')
    assert b'user 2' in rv.data

def test_post_user(client):
    new_user_response = client.post('/user', json=dict(
        username="user1",
        email="user1@example.com"
    ))
    assert b'"index":1' in new_user_response.data

    user1_response = client.get('/user/1')
    assert b'user1@example.com' in user1_response.data

def test_webcomponent(client):
    webcomponent = client.get('/user')
    with open('tests/user.js', 'w') as module:
        module.write(webcomponent.data.decode("utf-8"))
