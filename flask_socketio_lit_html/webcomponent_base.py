from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
socketio = SocketIO(app, engineio_logger=True)

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/
class IndexModel(Model):
    """Generate a Webcoponent class based on sqlalchemy"""
    __abstract__ = True

    @classmethod
    def register(cls, base_url, component_name, template='webcomponent_base.js'):
        blueprint = Blueprint(component_name, __name__, template_folder='webcomponent_templates')
        blueprint.add_url_rule(base_url, view_func=IndexModel.webcomponent, defaults = {
            # Variable for the webcoponent_base.js
            'ioupdate': str(cls)+'update',
            'component_name': component_name,
            'base_url': base_url,
            'properties': [ c.name for c in cls.__table__.columns ],
            'template': template
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
        return render_template(env['template'], **env), { 'Content-Type': "text/javascript; charset=utf-8" }

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
