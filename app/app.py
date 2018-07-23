import random
import string

from flask import Flask
from flask_migrate import Migrate

from .models import ToDoItem
from .models import db
from .models import ToDoList
from .urls import todo_list_api, todo_items_api

app = Flask(__name__)  # create an instance of the Flask and giving it a name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/todo_app.sqlite'  # tells SQLALCHEMY where the database is
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False  # tells the command line to "shut up" stop springing errors

migrate = Migrate(app, db)  # current_app > is the short-cut for the app k via flask which knows the models and db from the sql
db.init_app(app)  # the db knows about the app


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@app.cli.command()  # flask decorator cli - command line interface - call functions from the command line
def create_dummy_data():
    for i in range(10):
        new_list = ToDoList(name=randomword(10))
        for i2 in range(10):
            new_item=ToDoItem(
                content=randomword(10),
                todo_list=new_list,
            )
        # db.Model can arguments i.e. id, created - a way to generate a random string
            db.session.add(new_item)
    db.session.commit()
    print("Printed 10 Todo lists")


@app.cli.command()  # flask decorator cli - command line interface - call functions from the command line
def give_word():
    print(randomword(10))


# Flask - decorator to access '/' tells Flask on '/' it will execute this definition - like a router think Colt Steele - return json or html etc.
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# move the class ToDoListView(MethodView): to views/todo_list
app.register_blueprint(todo_list_api, url_prefix='/todo-lists')
app.register_blueprint(todo_items_api, url_prefix='/todo-items')


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
    # db.create_all() # execute app - we no longer use as we will use flask-Migrate
