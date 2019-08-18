[![ForTheBadge uses-badges](https://img.shields.io/badge/uses-flask-4ab?style=for-the-badge&labelColor=4cd)](https://palletsprojects.com/p/flask/)
[![ForTheBadge uses-badges](https://img.shields.io/badge/uses-lit%20html-4ab?style=for-the-badge&labelColor=4cd)](https://lit-html.polymer-project.org/)
[![ForTheBadge uses-badges](https://img.shields.io/badge/uses-Socket.IO-4ab?style=for-the-badge&labelColor=4cd)](https://socket.io/)

![Version: Alpha](https://img.shields.io/badge/version-alpha-yellow?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Pypi version](https://img.shields.io/pypi/v/flask-socketio-lit-html?style=for-the-badge)](.)
[![ReadTheDocs](https://readthedocs.org/projects/flask-socketio-lit-html/badge/?version=latest&style=for-the-badge)](https://flask-socketio-lit-html.readthedocs.io/)
![Travis (.org)](https://img.shields.io/travis/playerla/flask-socketio-lit-html?style=for-the-badge)

# Flask-Socket.IO-lit-html

Webcomponents with Flask and SocketIO

## Proof of concept project to use Webcomponents in Python Flask

* Generate a restful API (inspired from Flask-Restful)
* Update html on data changes through socketio (Inspired from Angular properties reflection)

## Usage philosophy

Create user webcomponent from sqlalchemy design:
```python
class User(db.Model):
    username = db.Column(db.String(80), nullable=False)

blueprint = User.register("/user", "user-item", "user.html")
app.register_blueprint(blueprint)
```
Display the second user of your database:
```html
<script type="module" src="{{url_for('user-item.webcomponent')}}"></script>
<div> user 2: <user-item index=2 ></user-item></div>
```

This code represent the idea behind the module, it's not real code, look at app.py for a working example.

## Contribute : Pull requests are welcome !

[![Edit with Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/playerla/flask-socketio-lit-html/tree/Dev)

### Updating autodoc

```sh
cd docs && sphinx-apidoc -o source/ ../flask_socketio_lit_html
```

### Build and publish package

```sh
poetry build
```
Just increment the version in [pyproject.toml](./pyproject.toml) to publish after tests are succesfully passed (see [.travis.yml](./.travis.yml))
