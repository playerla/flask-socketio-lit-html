from flask_socketio_lit_html.webcomponent_base import IndexModel, app, db, socketio
from flask import render_template

class User(db.Model):
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

open("flask_socketio_lit_html/app.db", 'w').close()
db.create_all()

@app.errorhandler(Exception)
def all_exception_handler(error):
    return app.send_static_file('404.html'), 404

blueprint = User.register("/user", "user-item", "user.html")
app.register_blueprint(blueprint)

@app.route('/')
def main():
    return render_template('main.html')

if __name__ == "__main__":
    socketio.run(app)
