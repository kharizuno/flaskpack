## Author : Kharizuno
## Github : https://github.com/kharizuno

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

from systems.database.mysql import configDB
db = configDB(app)

from api.routes import *
app = configRT(app)
