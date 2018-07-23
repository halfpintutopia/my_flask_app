from datetime import datetime

from .db import db


# different to-do lists/tables not the same table as todo_list
class ToDoItem(db.Model): # this is what the todos should look like
    __tablename__ = 'todo_item'
    # specify fields (columns)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=True,
                        default=datetime.utcnow)  # click on datetime when underlined red, hold alt key and hit enter to select what to import it / nullable
    #  support a not required due date for each todo_item
    due = db.Column(db.DateTime, nullable=True)
    # support a done flag for each todo_item (not done, done
    # todo_list id with a RELATION in the database with the other table - replace all this with raw sql
    todo_list_id = db.Column( # name of the file . field name
        db.Integer,
        db.ForeignKey('todo_list.id'),
        nullable=False
    )
    # make sure there are no python problems
    todo_list = db.relationship(
        'ToDoList',
        backref=db.backref('todos', lazy=False) # when handling todo_items
    )

    def serialize(self):
        datetime_format = '%Y-%m-%d %H:%M:%S'
        return {
            'id': self.id,
            'content': self.content,
            'created': self.created.strftime(datetime_format)
        }


