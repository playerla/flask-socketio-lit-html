"""Create simple statefull lit-html webcomponent backed with Sqlalchemy.

    Example:
        >>> # ... Init flask app and webcomponent extension ...
        >>> class User(db.Moel):
        >>>     username = db.Column(db.String(80), nullable=False)
        >>> # ... Flask app and extensions setup ...
        in html template: <user-item index=1></user-item>
"""
from flask import render_template, request, jsonify, Blueprint, Flask, Response
from flask_sqlalchemy import SQLAlchemy, Model
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from flask_socketio import SocketIO
import time


class FlaskWelApp(Flask):
    def __init__(self, __name__):
        super(FlaskWelApp, self).__init__(__name__)
        self.appIO = get_socketio()
        # Default to In-memory database in register
        db.init_app(self)
        with self.app_context():
            db.create_all()
        global socketio
        if socketio is None:
            socketio = SocketIO(self)
        self.appIO = socketio

    def runApp(self, **kwargs):
        self.appIO.run(self, **kwargs)


def init_webcomponent(app, sqlAlchemydb, socket_io=None):
    """Init webcomponent with external dependancies

    db store object state and socketio allows efficient
    communication between browser and flask

    Args:
        sqlAlchemydb (SQLAlchemy): Your database storing webcomponent state has to be
            instanciated with SQLAlchemy(app, model_class=IndexModel).
        socket_io (SocketIO): The streaming object instance.

    """
    global socketio, db, config
    socketio = socket_io or socketio or SocketIO(app)
    db = sqlAlchemydb or db
    app.config.setdefault('WEBCOMPONENT_LIGHT_DOM', 'false')
    app.config.setdefault('WEBCOMPONENT_CACHE_MAX_AGE', '3600')
    app.config.setdefault('WEBCOMPONENT_ETAG', '"'+str(time.time())+'"')
    config = app.config


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/
class IndexModel(Model):
    """Webcomponent base class with an Integer index as primary key"""
    __abstract__ = True

    @classmethod
    def configure_blueprint(cls, base_url=None, component_name=None, template=None):
        """ Configure element

        Configure the element with convenient default values.

        Args:
            base_url (String): API endpoint for the component. Default to /classname
            component_name (String): the registered html tag name. Default to classname (lowercase)
            template (String): Template name for the webcomponents. Default to classname.html

        Returns blueprint for flask

        """
        element_name = cls.__name__
        if base_url is None:
            base_url = '/'+element_name
        if component_name is None:
            component_name = element_name.lower()+'-item'
        if template is None:
            template = element_name+'.html'
        blueprint = Blueprint(component_name, __name__,
                              template_folder='webcomponent_templates',
                              static_folder='webcomponents_static')
        blueprint.add_url_rule(base_url+'.js', view_func=IndexModel.webcomponent,
                               defaults={
                                   # Variable for the webcomponent_base.js
                                   'ioupdate': element_name+'.update',
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
        if request.headers.get('If-None-Match') == config['WEBCOMPONENT_ETAG']:
            return Response(status=304)
        return render_template(env['template'], **env), {
            'Content-Type': "text/javascript; charset=utf-8", 
            'Cache-Control': "public, max-age="+config['WEBCOMPONENT_CACHE_MAX_AGE'], 
            'Etag':config['WEBCOMPONENT_ETAG']
        }

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
        socketio.emit(str(cls.__name__)+'.update', item.index)
        return jsonify(index=item.index)

    def get_all(cls):
        """Return all index as `{'items': [list of indexes]}`"""
        return {'items': [columns[0] for columns in db.session.query(cls.index).all()]}

def get_socketio():
    global socketio
    return socketio

socketio = None
db = SQLAlchemy(model_class=IndexModel)
