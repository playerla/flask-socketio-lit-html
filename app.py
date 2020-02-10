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

        # Pluggable components using socketIO
        self.appIO = SocketIO(self, engineio_logger=True, cors_allowed_origins="*")
        init_webcomponent(self, self.db, self.appIO)
        # Register <user-item> webcomponent to use /user api endpoint with custom render from user.html
        userBluePrint = User.configure_blueprint("/user", "user-item", "user.html")
        self.register_blueprint(userBluePrint)

        # Register <car-item> webcomponent to use /car api endpoint with custom render from car.html (using default values from classname)
        carBluePrint = Car.configure_blueprint()
        self.register_blueprint(carBluePrint)

        # You could also use any external_url with the same API scheme
        apiBluePrint = Api.configure_blueprint(external_url='/api')
        self.register_blueprint(apiBluePrint)
        self.add_url_rule('/api/<int:index>', 'GET', lambda index: {'index':index,'value':'value2'})
        self.add_url_rule('/api/<int:index>', 'DELETE', lambda index: {'index':index}, methods=['DELETE'])
        self.add_url_rule('/api', 'POST', lambda: {'index':1}, methods=['POST'])
        self.add_url_rule('/api/all', 'ALL', lambda: {'items':[1,2,3]})

        # Your application
        self.add_url_rule('/', "webComponentApp", lambda : render_template('main.html'))


    def runApp(self):
        self.appIO.run(self)


class User(db.Model):
    """User webcomponent model"""
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def delete(cls, index):
        print(index, "have been deleted")
        return super().delete(cls, index)


class Car(db.Model):
    """User webcomponent model"""
    color = db.Column(db.String(80), nullable=False, default='Blue')


class Api(db.Model):
    value = db.Column(db.String(80), nullable=False)
    

if __name__ == "__main__":
    app = WebcomponentApp(db)
    with app.app_context():
        db.session.add(Car())
        db.session.add(Api(value="value1"))
        db.session.commit()
    app.runApp()
