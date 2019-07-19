from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import Model, SQLAlchemy, event
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = 'True'
socketio = SocketIO(app)
db = SQLAlchemy(app, session_options={'autocommit': True})

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

    @classmethod
    def loop(cls):
        for c in cls.__table__.columns:
            print(c, type(c))

    ColumnLookupError = Exception("Error during lookup sqlalchemy.sql.schema.Column")

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

    @app.route('/user', methods=['POST'])
    def post():
        print(request)
        print(request.get_json())
        u = db.session.merge(User(**request.get_json()))
        db.session.commit()
        return jsonify(id=u.id)

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
