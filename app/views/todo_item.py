from datetime import datetime

from app.models.todo_list import ToDoList
from app.models.todo_item import ToDoItem
from .helpers import APIView


class ToDoItemListCreateView(APIView):
    methods = ['GET', 'POST']
    post_fields = ['content']

    def get_todo_list(self, todo_list_id):
        todo_list = ToDoList.query.filter_by(id=todo_list_id).first()
        if not todo_list:
            return self.abort('Todo List does not exist!')
        return todo_list

    def get(self, todo_list_id):
        todo_items = ToDoItem.query.filter_by(todo_list_id=todo_list_id)
        return self.make_response([l.serialize() for l in todo_items])

    def post(self, **kwargs):
        data = super().post()
        todo_list = self.get_todo_list(**kwargs)
        new_todo_item = ToDoItem(content=data.get('content'), todo_list=todo_list)
        self.session.add(new_todo_item)
        self.session.commit()
        return self.make_response(new_todo_item.serialize())


class ToDoItemGetUpdateDeleteView(APIView): # gets back the info as a json
    methods = ['GET', 'POST', 'DELETE']
    post_fields = ['content']

    def get_todo_item(self, **kwargs): # defines what happens get comes
        todo_items = ToDoItem.query.filter_by(id=kwargs.get(todo_items_id)).first()  # return str([l.serialize() for l in todo_lists])
        #  for string to change it to json add json.dumps instead of string
        if not todo_items:
            return self.abort('Todo Item does not exist!')
        # return json.dumps([i.serialize() for i in todo_items])
        return todo_items

    def get(self, **kwargs):
        todo_item = get_todo_item(**kwargs)
        return self.make_response(todo_item.serialize())

    def post(self, **kwargs):  # how to get a data from api / accept data from the user - fills a form and then clicks sumbit
        data = super().post()
        todo_list = self.get_todo_item(**kwargs)
        todo_list.content = data.get('content')
        due = data.get('due')  # changing the byte-string into a string parse into a json will fail
        # json.loads('') # not passable
        if due:
            try:
                due = datetime.strptime(due, self.datetime_format)
            except ValueError:
                return self.abort('Wrong DateTime format!')
            todo_list.due = due
        done = data.get('done')
        if due:
            todo_list.done = bool(done)
        self.session.merge(todo_list)
        self.session.commit()
        return self.make_response(todo_list.serialize())

    def delete(self, **kwargs):
        todo_item = self.get_todo_item(**kwargs)
        self.session.delete(todo_item)
        self.session.commit()
        return f'ToDo Item {kwargs.get("todo_list_id")} deleted!'


class ToDoItemSearchView(APIView):
    methods = ['GET']

    def get(self, todo_list_id):
        search_string = self.request.values.get('q')
        todos = ToDoItem.query.filter_by(todo_list_id=todo_list_id).filter(ToDoItem.content.like(f'%{search_string}%'))
        return self.make_response([l.serialize() for l in todos])






