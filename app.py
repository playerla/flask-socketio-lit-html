from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = 'True'
socketio = SocketIO(app, engineio_logger=True)
db = SQLAlchemy(app, session_options={'autocommit': True})


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/
class IndexModel(Model):
    __abstract__ = True
    
    @classmethod
    def register(cls, base_url, component_name):
        blueprint = Blueprint(component_name, __name__, template_folder='webcomponent_templates')
        blueprint.add_url_rule(base_url, view_func=IndexModel.webcomponent, defaults = {
            # Variable for the webcoponent_base.js
            'ioupdate': str(cls)+'update',
            'component_name': component_name,
            'base_url': base_url,
        })
        blueprint.add_url_rule(base_url+'/<int:index>', view_func=IndexModel.get, defaults = { 'cls': cls })
        blueprint.add_url_rule(base_url, view_func=IndexModel.post, defaults={ 'cls': cls }, methods=['POST'])
        blueprint.add_url_rule(base_url+'/all', view_func=IndexModel.get_all, defaults={ 'cls': cls })
        return blueprint
        
    @declared_attr
    def index(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.index)
                break
        else:
            type = sa.Integer

        return sa.Column(type, primary_key=True)
    
    def webcomponent(**env):
        return render_template('webcomponent_base.js', **env), { 'Content-Type': "text/javascript; charset=utf-8" }

    # https://stackoverflow.com/a/11884806
    def _asdict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get(cls, index):
        item = db.session.query(cls).filter(cls.index==index).first()
        return item._asdict() if item else ("Not found", 404)

    def post(cls):
        item = db.session.merge(cls(**request.get_json()))
        db.session.commit()
        socketio.emit(str(cls)+'update', item.index)
        return jsonify(index=item.index)

    def get_all(cls):
        return { 'items': db.session.query(cls.index).all() }

db = SQLAlchemy(app, model_class=IndexModel)

class User(db.Model):
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

open("app.db", 'w').close()
db.create_all()

@app.errorhandler(Exception)
def all_exception_handler(error):
    return app.send_static_file('404.html'), 404
    
blueprint = User.register("/user", "user-item")
app.register_blueprint(blueprint)

@app.route('/')
def main():
    return render_template('main.html')

socketio.run(app)
