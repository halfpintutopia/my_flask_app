from models.todo_list import ToDoList
from .helpers import APIView

"""
class UserAPI(MethodView):

    def get(self, user_id):
        if user_id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass
"""


class ToDoListsListCreateView(APIView): # gets back the info as a json
    methods = ['GET', 'POST']
    post_fields = ['name']

    def get(self): # defines what happens get comes
        todo_lists = ToDoList.query.all()  # return str([l.serialize() for l in todo_lists])
        #  for string to change it to json add json.dumps instead of string
        return self.make_response([l.serialize() for l in todo_lists])

    def post(self):
        data = super().post()
        name = data.get('name')
        todo_lists = ToDoList.query.filter_by(name=name).all()
        if todo_lists:
            return self.abort(f'ToDo list with the name "{name}" already exists!')
        new_todo_list = ToDoList(name=name)
        self.session.add(new_todo_list)
        self.session.commit()
        return self.make_response(new_todo_list.serialize())


class ToDoListGetUpdateDeleteView(APIView):
    methods = ['GET', 'POST', 'DELETE']
    post_fields = ['name']

    def get_todo_list(self, todo_list_id):
        todo_list = ToDoList.query.filter_by(id=todo_list_id).first()
        if not todo_list:
            return self.abort("ToDo List does not exist!")
        return todo_list

    def get(self, **kwargs):
        todo_list = self.get_todo_list(**kwargs)
        return self.make_response(todo_list.serialize())

    def post(self, **kwargs):
        data = super().post()
        name = data.get('name')
        todo_list = self.get_todo_list(**kwargs)
        todo_lists = ToDoList.query.filer_by(name=name).all()
        if todo_lists:
            return self.abort(f'ToDo list with the name "{name}" already exists!')
        todo_list.name = name
        self.session.merge(todo_list)
        self.session.commit()
        return self.make_response(todo_list.serialize())

    def delete(self, **kwargs):
        todo_list = self.get_todo_list(**kwargs)
        self.session.delete(todo_list)
        self.session.commit()
        return f'ToDo List {kwargs.get("todo_list_id")} deleted!'

class ToDoListSearchView(APIView):
    methods = ['GET']

    def get(self, **kwargs):
        search_string = self.request.values.get('q')
        lists = ToDoList.query.filter(ToDoList.name.like(f'%{search_string}%'))
        return self.make_response([l.serialize() for l in lists])


# class ToDoListUpdate(MethodView):
#
#     def get(self):
#         return 'This is to update your list'
#
#     def put(self, todo_list_id):
#         data = request.data
#         data = data.decode()  # changing the byte-string into a string parse into a json will fail
#         # json.loads('') # not passable
#         if not data:
#             data = '{}'
#         else:
#             return 'You have posted into the todo_list'
#         data = json.loads(data)
#         id = data.post('id')
#         if not id:
#             return abort(400, 'You did not update anything!')  # bad request response
#         return json.dumps([l.serialize() for l in data])
#         pass
#
#
# class ToDoListDelete(MethodView):
#
#     def delete(self, todo_list_id):
#         return 'This is to delete an item from your list'
#
#         item_delete = request.item_delete
#         todo_lists = ToDoList.query.filter(ToDoList.name.like('this'))
#         return json.dumps([l.serialize() for l in todo_lists])
#
#
# class ToDoListSearch(MethodView):
#     def get(self, todo_list_id):
#         return 'This is to search your list'
#
#         q = request.values.get('q')
#         todo_lists = ToDoList.query.filter(ToDoList.name.like(f'%{q}%'))
#         return json.dumps([l.serialize() for l in todo_lists])
#
#
# class ToDoListFiler(MethodView):
#     def get(self):
#         filtered_list = []
#         for user in todo_list.query(self.id, self.content, self.created)
#
