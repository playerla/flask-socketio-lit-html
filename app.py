from flask import Flask, render_template
from flask.views import View
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = 'True'
socketio = SocketIO(app)
db = SQLAlchemy(app)

class User(db.Model, View):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    def list_users():
        return [{'username': u.username, 'email': u.email } for u in User.query.all()]

    @socketio.on('add')
    def add(data):
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        socketio.emit('message', User.list_users())
    
open("app.db", 'w').close()
db.create_all()

@app.route('/')
def main():
    return render_template('main.html')

socketio.run(app)
