ok = 200
SUCESS = {'code': 200, 'msg': '请求成功'}
PARAMS_ERROR = {'code': 400, 'msg': '参数错误'}
DATABASE_ERROR = {'code': 401, 'msg': '数据库错误'}

# 用户模块

USER_NOT_LOGIN = {'code': 1000, 'msg': '用户没有登录，请重新登录'}
USER_LOGIN_PARAMS_ERROR = {'code': 1001, 'msg': '参数错误'}
USER_LOGIN_PHONE_ERROR = {'code': 1002, 'msg': '电话号码错误'}
USER_LOGIN_PASSWORD_ERROR = {'code': 1003, 'msg': '密码错误'}
USER_LOGIN_USER_NOT_EXSITS = {'code': 1004, 'msg': '用户不存在'}
USER_REGISTER_USER_PHONE_EXSITS = {'code': 1005, 'msg': '手机号存在'}
USER_REGISTER_USER_ERROR = {'code': 1006, 'msg': '用户注册更新数据库失败'}



USER_PROFILE_IMAGE_UPDATE_ERROR = {'code': 1007, 'msg': '用户上传头像不是图片格式'}
USER_REGISTER_USER_IS_EXSITS = {'code': 1008, 'msg': '用户名已经存在'}
USER_REGISTER_AUTH_ERROR = {'code': 1009, 'msg': '身份证信息错误'}

# 房源模块
MYHOUSE_USER_IS_NOT_AUTH = {'code': 1010, 'msg': '用户没有实名认证'}
ORDER_START_END_TIME_ERROR = {'code': 1011, 'msg': '时间选择错误'}
