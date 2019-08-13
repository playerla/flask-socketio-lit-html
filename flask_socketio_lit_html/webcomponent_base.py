"""Create simple statefull lit-html webcomponent backed with Sqlalchemy.

    Example:
        >>> # ... Init flask app and webcomponent extension ...
        >>> class User(db.Moel):
        >>>     username = db.Column(db.String(80), nullable=False)
        >>> # ... Flask app and extensions setup ...
        in html template: <user-item index=1></user-item>
"""
from flask import render_template, request, jsonify, Blueprint
from flask_sqlalchemy import Model
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr

socketio = None
db = None


def init_webcomponent(app, sqlAlchemydb, socket_io):
    """Init webcomponent with external dependancies

    db store object state and socketio allows efficient
    communication between browser and flask

    Args:
        sqlAlchemydb (SQLAlchemy): Your database storing webcomponent state has to be
            instanciated with SQLAlchemy(app, model_class=IndexModel).
        socket_io (SocketIO): The streaming object instance. engineio_logger
            is set to True.

    """
    global socketio, db
    socketio = socket_io
    db = sqlAlchemydb
    socketio.engineio_logger = True


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/
class IndexModel(Model):
    """Webcomponent base class with an Integer index as primary key"""
    __abstract__ = True

    @classmethod
    def register(cls, base_url, component_name, template='webcomponent_base.js'):
        """ Register webcomponent to api endpoint"""
        blueprint = Blueprint(component_name, __name__,
                              template_folder='webcomponent_templates')
        blueprint.add_url_rule(base_url, view_func=IndexModel.webcomponent,
                               defaults={
                                   # Variable for the webcomponent_base.js
                                   'ioupdate': str(cls)+'update',
                                   'component_name': component_name,
                                   'base_url': base_url,
                                   'properties': [c.name for c in cls.__table__.columns],
                                   'template': template
                               })
        blueprint.add_url_rule(base_url+'/<int:index>', view_func=IndexModel.get,
                               defaults={'cls': cls})
        blueprint.add_url_rule(base_url, view_func=IndexModel.post,
                               defaults={'cls': cls}, methods=['POST'])
        blueprint.add_url_rule(base_url+'/all', view_func=IndexModel.get_all,
                               defaults={'cls': cls})
        return blueprint

    @declared_attr
    def index(cls):
        """Define the index primary key"""
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.index)
                break
        else:
            type = sa.Integer
        return sa.Column(type, primary_key=True)

    def webcomponent(**env):
        """Send the webcomponent.js dependancies"""
        return render_template(env['template'], **env), {'Content-Type': "text/javascript; charset=utf-8"}

    # https://stackoverflow.com/a/11884806
    def _asdict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get(cls, index):
        """Return webcomponent instance value as json. HTTP GET."""
        item = db.session.query(cls).filter(cls.index == index).first()
        return item._asdict() if item else ("Not found", 404)

    def post(cls):
        """Save webcomponent instance value from json. HTTP POST."""
        item = db.session.merge(cls(**request.get_json()))
        db.session.commit()
        socketio.emit(str(cls)+'update', item.index)
        return jsonify(index=item.index)

    def get_all(cls):
        """Return all index as `{'items': [list of indexes]}`"""
        return {'items': db.session.query(cls.index).all()}
