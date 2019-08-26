from flask_socketio_lit_html.webcomponent_base import init_webcomponent, IndexModel
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

db = SQLAlchemy(model_class=IndexModel)

class WebcomponentApp(Flask):
    def __init__(self, db, db_file='app.db'):
        """Our example app doesn't keep contents. Drop app.db"""
        super(WebcomponentApp, self).__init__(__name__)
        
        # Database configuration
        self.config['DB_FILE'] = db_file
        open(self.config['DB_FILE'], 'w').close()
        self.db = db
        self.db.init_app(self)
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+self.config['DB_FILE']
        with self.app_context():
            self.db.create_all()
    
        # classic CSS theme 
        Bootstrap(self)
        
        self.appIO = SocketIO(self, engineio_logger=True)
        init_webcomponent(self, self.db, self.appIO)
        # Register <user-item> webcomponent to use /user api endpoint with custom render from user.html
        bluePrint = User.register("/user", "user-item", "user.html")
        self.register_blueprint(bluePrint)

        self.add_url_rule('/', "webComponentApp", lambda : render_template('main.html'))

    def runApp(self):
        self.appIO.run(self)


class User(db.Model):
    """User webcomponent model"""
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)


if __name__ == "__main__":
    WebcomponentApp(db).runApp()
