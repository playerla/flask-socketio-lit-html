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

        self.config['DB_FILE'] = db_file
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+self.config['DB_FILE']
        # Database configuration
        self.db = db
        self.db.init_app(self)
        with self.app_context():
            self.db.drop_all()
            self.db.create_all()

        # classic CSS theme
        Bootstrap(self)

        self.appIO = SocketIO(self, engineio_logger=True)
        init_webcomponent(self, self.db, self.appIO)
        # Register <user-item> webcomponent to use /user api endpoint with custom render from user.html
        bluePrint = User.configure_blueprint("/user", "user-item", "User.html")
        # You could also use any external_url with the same API scheme
        # bluePrint = User.configure_blueprint(external_url='/fake')
        self.register_blueprint(bluePrint)

        self.add_url_rule('/', "webComponentApp", lambda : render_template('main.html'))
        self.add_url_rule('/fake/<int:index>', 'GET', lambda index: {'index':index,'username':'name','email':'@'})
        self.add_url_rule('/fake/<int:index>', 'DELETE', lambda index: {'index':index}, methods=['DELETE'])
        self.add_url_rule('/fake', 'POST', lambda: {'index':1}, methods=['POST'])
        self.add_url_rule('/fake/all', 'ALL', lambda: {'items':[1,2,3]})

    def runApp(self):
        self.appIO.run(self)


class User(db.Model):
    """User webcomponent model"""
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def delete(cls, index):
        print(index, "have been deleted")
        return super().delete(cls, index)

if __name__ == "__main__":
    WebcomponentApp(db).runApp()
