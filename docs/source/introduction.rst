.. _introduction:

Quick Start
===================================================

.. code-block:: shell

    pip install flask-socketio-lit-html

Example: Todo App
===================================================

Define the todo component in jinja html template

.. code-block:: jinja

    {% extends "webcomponent_base.js" %}


    {% block render %}
    <input type="checkbox">${ this.todo }
    {% endblock %}


    {% block form %}
    <form onsubmit="return false;">
        <input type="text" id="todo" value="task">
        <button id="submit-button" @click="${ this.add_event }">Add</button>
    </form>
    {% endblock %}


Create  Flask application, configure your element and run it

.. code-block:: python

    class Todo(db.Model):
        """Todo webcomponent model"""
        todo = db.Column(db.String(80))

    class TodoApp(FlaskWelApp):
        def __init__(self):
            super(TodoApp, self).__init__(__name__)
            # Register <todo-item> webcomponent to use /todo/ endpoint blueprint and custom render from todo.html jinja template
            self.register_blueprint(Todo.configure_blueprint())
            # TodoApp main page
            self.add_url_rule('/', "TodoApp", lambda : render_template('todoapp.html'))

    TodoApp().runApp()

Keep control of your dependencies

.. code-block:: jinja

    <script src="{{url_for('todo-item.static', filename='socketio-2.3.0.js')}}"></script>
    <script src="{{url_for('todo-item.static', filename='element.js')}}"></script>
    <script type="module" src="{{url_for('todo-item.webcomponent')}}"></script>

Full example at https://github.com/playerla/flask-wel-todoapp/ and
project demo at https://github.com/playerla/flask-socketio-lit-html/blob/master/app.py

How it works
===================================================

The model of the component - the Python class - is used to auto generated all the stuff when configure it with :meth:`webcomponent_base.IndexModel.configure_blueprint`.
The next html tags are then available:

- <`componentname`> : The component html tag to use in .html
- <ul-`componentname`> : A dynamic list of all the components
- <form-`componentname`> : A Form to add new component or modify one

Generate a Rest API
----------------------
Register the component blueprint which contains the next JSON endpoints:

- GET  `/componentname` : The component implementation - a static javascript module. You can get it via url_for('componentname.webcomponent')
- GET  `/componentname/all` : The list of all components indexes in database
- GET  `/componentname/<int:index>` : The component with the primary key `index`
- DELETE  `/componentname/<int:index>` : The component with the primary key `index`
- POST `/componentname` : The JSON new user or the user to modify if `index` key is set
- GET `/componentname/dump` : The full dump of the database. Performance warning: use once and only if you planned to go offline. 

You can overwrite IndexModel class methods :meth:`get()`, :meth:`post()`, :meth:`delete()` and :meth:`get_all()` to implement your own API.
An external URL could also be specified to replace `/componentname` for these four API endpoints. See :meth:`webcomponent_base.IndexModel.configure_blueprint()`

Integrate lit-element in Flask jinja
------------------------------------
The webcomponent inherit from lit-element, business methods have to be overwritten in the jinja template extending `webcomponent_base.js`. Following blocks are available :

- `render` : the HTML view of the component
- `style` : CSS for the component - Global CSS is ignored with shadow DOM
- `form` : an html form which can be used to create component or modify one
- `style_form` : CSS for the form - by default ItemForm inerit the first `style` block

Update html on server side data changes
---------------------------------------
A socketio message is sent by the server to the component JS module after a POST request completes. Something like `<class '__main__.User'>update`: name is
cls+'update' where cls is your python component class. The message is the new or updated index, then the component updates itself with a GET call.

Cache and update strategy
---------------------------------------
:meth:`Item._get()` read cache before any network request. If the key `webcomponent-item.index` matches then it is used.
GET `/componentname/<int:index>` and POST `/componentname/<int:index>` update the local sessionStorage cache on fetch success.
You could populate sessionStorage with GET `/componentname/dump` before loading your webcomponent.js, to write an offline application.