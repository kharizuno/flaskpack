from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash
import uuid

from api import db
from api.models.user import User
from api.middlewares.tokenize import tokenize

class UserAll(Resource):
    method_decorators = [tokenize]
    def get(self, current_user):
        if not current_user.admin:
            return jsonify({'message': 'Cannot perform that function!'})

        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'users': output})
    def post(self, current_user):
        if not current_user.admin:
            return jsonify({'message': 'Cannot perform that function!'})

        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})

class UserOne(Resource):
    method_decorators = [tokenize]
    def get(self, current_user, public_id):
        if not current_user.admin:
            return jsonify({'message': 'Cannot perform that function!'})

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message': 'No user found!'})
        
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        return jsonify({'user': user_data})

# class UserCreate(Resource):
#     method_decorators = [tokenize]
#     def post(self, current_user):
#         if not current_user.admin:
#         return jsonify({'message': 'Cannot perform that function!'})

#         data = request.get_json()
#         hashed_password = generate_password_hash(data['password'], method='sha256')

#         new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({'message': 'New user created!'})

class UserPromote(Resource):
    method_decorators = [tokenize]
    def put(self, current_user, public_id):
        if not current_user.admin:
            return jsonify({'message': 'Cannot perform that function!'})

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message': 'No user found!'})

        user.admin = True
        db.session.commit()

        return jsonify({'message': 'The user has been promote!'})

class UserDelete(Resource):
    method_decorators = [tokenize]
    def delete(self, current_user, public_id):
        if not current_user.admin:
            return jsonify({'message': 'Cannot perform that function!'})

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message': 'No user found!'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'The user has been deleted!'})
