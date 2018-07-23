from flask import Blueprint

from .views.todo_item import ToDoItemListCreateView, ToDoItemGetUpdateDeleteView, ToDoItemSearchView
from .views.todo_list import ToDoListsListCreateView, ToDoListGetUpdateDeleteView, ToDoListSearchView

#make sure we can accept variable stuff into our urls
todo_list_api = Blueprint('todo-list-api', 'todo-list-api')
todo_list_api.add_url_rule(rule='/', view_func=ToDoListsListCreateView.as_view('todo-lists-list-create'))
todo_list_api.add_url_rule(rule='/<int:todo_list_id>/', view_func=ToDoListGetUpdateDeleteView.as_view('todo-lists-get-update-delete'))
todo_list_api.add_url_rule(rule='/search/', view_func=ToDoListSearchView.as_view('todo-lists-search'))

todo_items_api = Blueprint('todo-item-api', 'todo-items-api')
todo_items_api.add_url_rule(rule='/<int:todo_list_id>/', view_func=ToDoItemListCreateView.as_view('todo-items-list-create'))
todo_items_api.add_url_rule(rule='/<int:todo_list_id>/<int:todo_item_id>/', view_func=ToDoItemGetUpdateDeleteView.as_view('todo-items-get-update-delete'))
todo_items_api.add_url_rule(rule='/<int:todo_list_id>/search/', view_func=ToDoItemSearchView.as_view('todo-items-search'))

