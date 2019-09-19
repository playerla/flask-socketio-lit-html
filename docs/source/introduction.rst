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

See https://github.com/playerla/flask-socketio-lit-html/tree/Dev/tests/todo_app/

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
- GET  `/componentname/<int:index>` : The component with the primary key `index`
- GET  `/componentname/all` : The list of all components indexes in database
- POST `/componentname` : The JSON new user or the user to modify if `index` key is set

Integrate lit-element in Flask jinja
------------------------------------
The webcomponent inherit from lit-element, business methods have to be overwritten in the jinja template extending `webcomponent_base.js`. Following blocks are available :

- `render` : the HTML view of the component
- `style` : CSS for the component - Global CSS is ignored with shadow DOM
- `form` : an html form which can be used to create component or modify one

Update html on server side data changes
---------------------------------------
A socketio message is sent by the server to the component JS module after a POST request completes. Something like `<class '__main__.User'>update`: name is
cls+'update' where cls is your python component class. The message is the new or updated index, then the component updates itself with a GET call.
