from flask_socketio_lit_html.webcomponent_base import init_webcomponent, db, get_socketio
from flask import Flask, render_template


class Todo(db.Model):
    """Todo webcomponent model"""
    todo = db.Column(db.String(80))


class TodoApp(Flask):
    def __init__(self):
        super(TodoApp, self).__init__(__name__)
        # Default to In-memory database in register
        # Register <todo-item> webcomponent to use /todo endpoint and custom render from todo.html jinja template
        Todo.register("/todo", "todo-item", "todo.html", app=self)
        # TodoApp main page
        self.add_url_rule('/', "TodoApp", lambda : render_template('todoapp.html'))
        self.appIO = get_socketio()

    def runApp(self):
        self.appIO.run(self)


if __name__ == "__main__":
    TodoApp().runApp()
