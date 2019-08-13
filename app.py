from flask_socketio_lit_html.webcomponent_base import init_webcomponent, IndexModel
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
Bootstrap(app)
db = SQLAlchemy(app, model_class=IndexModel)
socketio = SocketIO(app, engineio_logger=True)
init_webcomponent(app, db, socketio)

class User(db.Model):
    """User webcomponent model"""
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)


# Our example app doesn't keep contents
open("app.db", 'w').close()
db.create_all()

# Register <user-item> webcomponent to use /user api endpoint with custom render from user.html
bluePrint = User.register("/user", "user-item", "user.html")
app.register_blueprint(bluePrint)

@app.route('/')
def main():
    """Users list Application"""
    return render_template('main.html')


if __name__ == "__main__":
    socketio.run(app)
