from flask import request, jsonify
from flask_restful import Resource

from api import db
from api.models.todo import Todo
from api.middlewares.tokenize import tokenize

class TodoAll(Resource):
    method_decorators = [tokenize]
    def get(self, current_user):
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        output = []
        for todo in todos:
            todo_data = {}
            todo_data['id'] = todo.id
            todo_data['text'] = todo.text
            todo_data['complete'] = todo.complete
            output.append(todo_data)

        return jsonify({'todos': output})
    def post(self, current_user):
        data = request.get_json()

        new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()

        return jsonify({'message': 'Todo created!'})

class TodoOne(Resource):
    # method_decorators = [tokenize]
    def get(self, current_user, todo_id):
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

        if not todo:
            return jsonify({'message': 'No todo found!'})

        todo_data = {}
        todo_data['id'] = todo.id
        todo_data['text'] = todo.text
        todo_data['complete'] = todo.complete

        return jsonify({'todo': todo_data})

# class TodoCreate(Resource):
#     # method_decorators = [tokenize]
#     def post(self, current_user):
#         data = request.get_json()

#         new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)
#         db.session.add(new_todo)
#         db.session.commit()

#         return jsonify({'message': 'Todo created!'})

class TodoComplete(Resource):
    # method_decorators = [tokenize]
    def put(self, current_user, todo_id):
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

        if not todo:
            return jsonify({'message': 'No todo found!'})

        todo.complete = True
        db.session.commit()

        return jsonify({'message': 'Todo item has been completed!'})

class TodoDelete(Resource):
    # method_decorators = [tokenize]
    def delete(self, current_user, todo_id):
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

        if not todo:
            return jsonify({'message': 'No todo found!'})

        db.session.delete(todo)
        db.session.commit()

        return jsonify({'message': 'Todo item has been deleted!'})
