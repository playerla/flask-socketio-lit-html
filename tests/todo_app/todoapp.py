from flask_socketio_lit_html.webcomponent_base import FlaskWelApp, init_webcomponent, db, get_socketio
from flask import render_template


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


if __name__ == "__main__":
    TodoApp().runApp()
