# https://flask.palletsprojects.com/en/1.1.x/testing/
import os
import tempfile

import pytest

from app import WebcomponentApp, db
from flask_socketio_lit_html.webcomponent_base import FlaskWelApp
from flask_socketio_lit_html.webcomponent_base import db as default_db

# Default App
class Model(default_db.Model):
    """Todo webcomponent model"""

class App(FlaskWelApp):
    def __init__(self):
        super(App, self).__init__(__name__)
        self.register_blueprint(Model.configure_blueprint())
        self.add_url_rule('/', view_func=lambda : "App loaded")

@pytest.fixture
def client():
    app = WebcomponentApp(db, "app_test.db")
    with app.test_client() as client:
        yield client
    os.remove(app.config['DB_FILE'])

@pytest.fixture
def default_client():
    app = App()
    with app.test_client() as client:
        yield client

def test_app_init_default_client(default_client):
    rv = default_client.get('/')
    assert b'App loaded' in rv.data

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
