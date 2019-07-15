from flask import Flask, render_template
from flask.views import View
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = 'True'
socketio = SocketIO(app)
db = SQLAlchemy(app)

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/
class IdModel(Model):
    @declared_attr
    def id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.id)
                break
        else:
            type = sa.Integer

        return sa.Column(type, primary_key=True)

db = SQLAlchemy(app, model_class=IdModel)

class User(db.Model):
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    @app.route('/user')
    def user():
        return render_template('user.js'), { 'Content-Type': "text/javascript; charset=utf-8" }

    @app.route('/users')
    def list_users():
        return { 'list': 
            [ {'username': u.username, 'email': u.email } for u in User.query.all() ] 
        }

    @app.route('/user/<int:id>')
    def get(id):
        u = User.query.get(id)
        if u:
            return {'username': u.username, 'email': u.email }
        else:
            return "Not found", 404 

    @socketio.on('add')
    def add(data):
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        socketio.emit('update')

    @app.route('/change/<int:id>/<string:newmail>')
    def change(id, newmail):
        u = User.query.get(id)
        u.email = newmail
        print('before_commit')
        db.session.commit()
        print('after_commit')
        return 'Changed to '+newmail

from sqlalchemy import event
def render_listener(mapper, connection, target):
    socketio.emit('update')

event.listen(User, 'after_insert', render_listener)
event.listen(User, 'after_update', render_listener)

open("app.db", 'w').close()
db.create_all()

@app.errorhandler(Exception)
def all_exception_handler(error):
    return app.send_static_file('404.html'), 404
    
@app.route('/')
def main():
    return render_template('main.html')

socketio.run(app)
