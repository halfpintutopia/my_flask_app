from datetime import datetime

from .db import db


# different to-do lists/tables not the same table as todo_item
class ToDoList(db.Model): # replace with SQL to replace this table
    __tablename__ = 'todo_list'
    # specify fields (columns) blueprint of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # support a creation date for each todo_item
    created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow) # click on datetime when underlined red, hold alt key and hit enter to select what to import it / nullable


    def serialize(self):
        datetime_format = '%Y-%m-%d %H:%M:%S'
        return {
            'id': self.id,
            'name': self.name,
            'created': self.created.strftime(datetime_format)
        }


