from flask import Flask,render_template, jsonify
from flask.views import View
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send

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
    
    @socketio.on('add')
    def add(data):
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        User.get()
    
    @app.route("/get")
    def get():
        users = [{'username': u.username, 'email': u.email } for u in User.query.all()]
        socketio.emit('message', users)
        return render_template('users.html', users=users)

open("app.db", 'w').close()
db.create_all()

@app.route('/')
def main():
    return """
<script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" integrity="sha256-yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I=" crossorigin="anonymous"></script>
<script type="module" charset="utf-8">
    import 'https://unpkg.com/@material/mwc-button@0.6.0/mwc-button.js?module';
    import {html, render} from 'https://unpkg.com/lit-html?module';
    function add() {
        socket.emit('add', {
                            username: document.getElementById('username').value, 
                            email:    document.getElementById('email').value
                           })
    }
    const Users = (users) => html`
        <ul>
            ${users.map((u) => html`<li><strong>${ u.username }</strong> ${ u.email }</li>`)}
        </ul>
        <input id='username' value='username'>
        <input id='email' value='email'>
        <mwc-button unelevated label="Add" @click="${add}"></mwc-button>`;
    render(Users([]), document.body);
    var socket = io();
    socket.on('message', function(json){
        render(Users(json), document.body);
    });
</script>
    """

socketio.run(app)
