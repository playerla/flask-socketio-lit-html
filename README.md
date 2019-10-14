[![ForTheBadge uses-badges](https://img.shields.io/badge/uses-flask-4ab?style=for-the-badge&labelColor=4cd)](https://palletsprojects.com/p/flask/)
[![ForTheBadge uses-badges](https://img.shields.io/badge/uses-lit%20html-4ab?style=for-the-badge&labelColor=4cd)](https://lit-html.polymer-project.org/)
[![ForTheBadge uses-badges](https://img.shields.io/badge/uses-Socket.IO-4ab?style=for-the-badge&labelColor=4cd)](https://socket.io/)

[![Version: Alpha](https://img.shields.io/badge/version-alpha-yellow?style=for-the-badge)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Pypi version](https://img.shields.io/pypi/v/flask-socketio-lit-html?style=for-the-badge)](https://pypi.org/project/flask-socketio-lit-html/)
[![ReadTheDocs](https://readthedocs.org/projects/flask-socketio-lit-html/badge/?version=latest&style=for-the-badge)](https://flask-socketio-lit-html.readthedocs.io/)
[![Travis (.org)](https://img.shields.io/travis/playerla/flask-socketio-lit-html?style=for-the-badge)](https://travis-ci.org/playerla/flask-socketio-lit-html)
[![codecov](https://img.shields.io/codecov/c/github/playerla/flask-socketio-lit-html?style=for-the-badge)](https://codecov.io/gh/playerla/flask-socketio-lit-html)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/playerla/flask-socketio-lit-html?style=for-the-badge)](https://codeclimate.com/github/playerla/flask-socketio-lit-html)

# Flask-Socket.IO-lit-html

Webcomponents with Flask and SocketIO

[Quick Start on documentation](https://flask-socketio-lit-html.readthedocs.io/introduction.html#introduction)

[Todo App example](https://github.com/playerla/flask-wel-todoapp)

## Proof of concept project to use Webcomponents in Python Flask

* Generate a restful API (inspired from Flask-Restful)
* Update html on data changes through [socketio](https://socket.io/) (Inspired from Angular properties reflection)
* Based on the powerful [lit-element library](https://lit-element.polymer-project.org/guide/start)

## Usage philosophy

Create user webcomponent from sqlalchemy design. GET and POST API on `/user`.
```python
class User(db.Model):
    username = db.Column(db.String(80), nullable=False)

blueprint = User.configure_blueprint("/user", "user-item", "user.html")
app.register_blueprint(blueprint)
```
Define the webcomponent view in a jinja template
```jinja
{% block render %}
<strong>${ this.username }</strong>
{% endblock %}
```
Display the second user of your database with live update:
```html
<script type="module" src="{{url_for('user-item.webcomponent')}}"></script>
<div> user 2: <user-item index=2 ></user-item></div>
```

This code represent the idea behind the module, look at app.py for a working example. Project may be modeled on [wtforms-alchemy](https://github.com/kvesteri/wtforms-alchemy)

## Contribute : Pull requests are welcome !

[![Edit with Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/playerla/flask-socketio-lit-html/tree/Dev)


### Updating autodoc

```sh
cd docs && sphinx-apidoc -o source/ ../flask_socketio_lit_html
```

### Build and test package

```sh
poetry build && pip3 install dist/flask_socketio_lit_html* --force-reinstall
```

### Running browser tests
```sh
cd tests ; yarn ; yarn test
```
Webcomponent's shadow root are disabled when running testcafe (for selecting components)

## Build lit-element with rollup.js
```sh
cd flask_socketio_lit_html/dependencies/ && yarn && yarn build && cd ../..
```
### Any questions ?

[![Slack Status](https://img.shields.io/badge/slack-join-darkblue?style=for-the-badge)](https://join.slack.com/t/flasksocketio-vhj9931/shared_invite/enQtNzUwMDgzMDg5ODU3LWRhNDg4MmNmMTg2MDYwM2UxYjQ5ZDhkN2FmODY2MGI0NDU3YWNmNTdlOWZkM2YzZmZlMjdmYjNmY2JiZThhOGI)

[![Join the community on Spectrum](https://img.shields.io/badge/Spectrum-join-purple?style=for-the-badge)](https://spectrum.chat/flask-sio-lit-html/)

#### External resources

[Learn webcomponents and lit-element on dev.to](https://dev.to/thepassle/web-components-from-zero-to-hero-4n4m)