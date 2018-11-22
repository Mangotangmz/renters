import os
import re

from flask import Flask, jsonify, session
from flask import Blueprint, request, render_template
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from app.model import User, db

from utils import status_code
from utils.functions import is_login
from utils.settings import UPLOAD_FOLDER

user_blue = Blueprint('app', __name__)
login_manager = LoginManager()


@user_blue.route('/createdb/')
def create_db():
    # 创建数据库
    db.create_all()
    return '创建成功'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# 注册
@user_blue.route('/register/', methods=['POST', "GET"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        dict = request.form
        mobile = dict.get('mobile')
        password = dict.get('password')
        password2 = dict.get('password2')
        # 验证参数是否存在
        if not all([mobile, password, password2]):
            return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)
        # 验证手机号是否格式正确
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return jsonify(status_code.USER_LOGIN_PHONE_ERROR)
        # 验证手机号是否存在
        if User.query.filter_by(phone=mobile).count():
            return jsonify(status_code.USER_REGISTER_USER_PHONE_EXSITS)
        # 保存用户对象
        user = User()
        user.phone = mobile
        user.name = mobile
        user.password = password

        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except:
            return jsonify(status_code.USER_REGISTER_USER_ERROR)


# 登录
@user_blue.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == "POST":
        mobile = request.form.get('mobile')
        password = request.form.get('password')

    if not all([mobile, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)
    user = User.query.filter(User.phone == mobile).first()
    if user:
        if check_password_hash(user.pwd_hash, password):

            session['user_id'] = user.id
            return jsonify(status_code.SUCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_ERROR)

    else:
        return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)


# 注销
@user_blue.route('/logout/', methods=['DELETE'])
# @is_login
def user_logout():
    session.clear()
    return jsonify(code='200')


@user_blue.route('/index/', methods=["POST", 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@user_blue.route('/profile/', methods=["PUT", 'GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'PUT':
        dict = request.form
        dict.file = request.files
        if 'avatar' in dict.file:
            try:
                # 获取头像
                f1 = request.files['avatar']
                if not re.match('image/.*', f1.mimetype):
                    # mime-type:国际规范，表示文件的类型，如text/html,text/xml,image/png,image/jpeg..
                    return jsonify(status_code.USER_PROFILE_IMAGE_UPDATE_ERROR)
            except:
                return jsonify(status_code.USER_PROFILE_IMAGE_UPDATE_ERROR)

            #  保存到upload中
            url = os.path.join(UPLOAD_FOLDER, f1.filename)
            f1.save(url)
            #     保存头像信息
            try:
                user = User.query.get(session['user_id'])
                user.avatar = os.path.join('/static/upload', f1.filename)
                user.add_update()
            except:
                return jsonify(status_code.DATABASE_ERROR)
            # 则返回图片信息
            return jsonify(code='200', url=os.path.join('/static/upload', f1.filename))


@user_blue.route('/user_name/', methods=['PUT'])
# @is_login
def get_user_profile():
    name = request.form.get('name')
    # 获取当前登录的用户
    user_id = session['user_id']
    # 查询当前用户的头像、用户名、手机号，并返回
    user = User.query.get(user_id)
    user.name = name
    user.add_update()

    return jsonify(code='200', user=user.to_basic_dict())


@user_blue.route('/my/')
def my():
    if request.method == 'GET':
        return render_template('my.html')


@user_blue.route('/user/', methods=['GET'])
def user():
    user_id = session['user_id']
    # 查询当前用户的头像、用户名、手机号，并返回
    user = User.query.get(user_id)
    return jsonify(code='200', user=user.to_basic_dict())


@user_blue.route('/auth/', methods=['GET'])
# @is_login
def auth():
    return render_template('auth.html')


'''获取实名认证信息'''


@user_blue.route('/auths/', methods=['GET'])
def user_auth():
    # 获取当前登录用户的编号
    user_id = session['user_id']
    # 根据编号查询当前用户
    user = User.query.get(user_id)
    # 返回用户的真实姓名、身份证号
    return jsonify(user.to_auth_dict())


@user_blue.route('/auths/', methods=['PUT'])
def auths_set():
    id_name = request.form.get('id_name')
    id_card = request.form.get('id_card')
    if not all([id_name, id_card]):
        return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)
    # 验证身份证号码是否合法
    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_REGISTER_AUTH_ERROR)
    # 修改数据
    try:
        user = User.query.get(session['user_id'])
    except:
        return jsonify(status_code.DATABASE_ERROR)
    try:
        user.id_card = id_card
        user.id_name = id_name
        user.add_update()
    except Exception as e:
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(status_code.SUCESS)


