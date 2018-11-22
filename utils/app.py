from flask import Flask

from app.house_view import house_blue
from app.ordrer_view import order_blue

from app.user_view import user_blue
from utils.config import Config
from utils.functions import init_ext
from utils.settings import static_dir, template_dir


def create_app():
    app = Flask(__name__,static_folder=static_dir, template_folder=template_dir)

    app.register_blueprint(blueprint=user_blue, url_prefix='/user')
    app.register_blueprint(blueprint=house_blue, url_prefix='/house')
    app.register_blueprint(blueprint=order_blue, url_prefix='/order')

    app.config.from_object(Config)

    # 初始化对象
    init_ext(app)

    return app
