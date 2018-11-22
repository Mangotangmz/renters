import os

# 项目路径

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 模板路径
template_dir = os.path.join(BASE_DIR, 'templates')
# 静态文件
static_dir = os.path.join(BASE_DIR, 'static')

# 模板文件
template_dir = os.path.join(BASE_DIR, 'templates')
# 上传图片路径
UPLOAD_FOLDER = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')
DATABASE = {
    # 用户
    'USER':'root',
    # 密码
    'PASSWORD':'123456',
    # 地址
    'HOST':'127.0.0.1',
    # 端口
    'PORT':'3306',
    # 数据库
    'DB':'mysql',
    # 驱动
    'DRIVER':'pymysql',
    # 数据库名称
    'NAME':'renters'
}