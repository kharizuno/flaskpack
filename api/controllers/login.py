from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.security import check_password_hash
import datetime
import jwt

from api import app
from api.models.user import User

class Login(Resource):
    def get(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        user = User.query.filter_by(name=auth.username).first()

        if not user:
            return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return make_response(jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
