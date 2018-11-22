import functools


from flask_session import Session
from werkzeug.utils import redirect

from app.model import db

session = Session()

def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            if 'user_id' in session['user_id']:
                return view_fun()
            else:
                return redirect('/user/login/')
        except Exception as e:
            return redirect('/user/login/')
    return decorator

def init_ext(app):

    db.init_app(app=app)
    session.init_app(app=app)

def get_db_uri(DATABASE):

    user = DATABASE.get('USER')
    passoword = DATABASE.get('PASSWORD')
    host = DATABASE.get('HOST')
    port = DATABASE.get('PORT')
    name = DATABASE.get('NAME')
    db = DATABASE.get('DB')
    driver = DATABASE.get('DRIVER')

    return '{}+{}://{}:{}@{}:{}/{}'.format(db, driver,
                                           user, passoword,
                                           host, port, name)