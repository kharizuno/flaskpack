from flask_sqlalchemy import SQLAlchemy

def configDB(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/py_sqlalchemy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    return db