## Author : Kharizuno
## Github : https://github.com/kharizuno

from flask_restful import Api

from api.controllers.login import *
from api.controllers.user import *
from api.controllers.todo import *

def configRT(app):

    api = Api(app)

    # import types
    # def ApiRoute(self, *args, **kwargs):
    #     def wrapper(cls):
    #         self.add_resource(cls, *args, **kwargs)
    #         return cls
    #     return wrapper
    # api.route = types.MethodType(ApiRoute, api)
    
    # Login Route
    api.add_resource(Login, '/login')

    # User Route
    api.add_resource(UserAll, '/user')
    api.add_resource(UserOne, '/user/<public_id>')
    api.add_resource(UserPromote, '/user/<public_id>')
    api.add_resource(UserDelete, '/user/<public_id>')

    # Todo Route
    api.add_resource(TodoAll, '/todo') 
    api.add_resource(TodoOne, '/todo/<todo_id>')
    api.add_resource(TodoComplete, '/todo/<todo_id>')
    api.add_resource(TodoDelete, '/todo/<todo_id>')
    
    return app