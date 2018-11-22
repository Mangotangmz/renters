import os

from flask import Blueprint, session, jsonify, request
from flask import render_template

from app.model import User, db, House, Facility, HouseImage, Area, Order
from app.user_view import user_blue
from utils import status_code
from utils.settings import UPLOAD_FOLDER

house_blue = Blueprint('house', __name__)


@house_blue.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


'''
我的房源
'''


@house_blue.route('/myhouse/')
def myhouse():
    return render_template('myhouse.html')


@house_blue.route('/auth_myhouse/', methods=['GET'])
def auth_myhouse():
    # 验证用户是否实名
    user_id = session['user_id']

    user = User.query.get(user_id)
    if user.id_name:
        house = House.query.filter(House.user_id == user_id).order_by(House.id.desc())
        house_list = []
        for item in house:
            house_list.append(item.to_dict())
        return jsonify(code='200', house_list=house_list)
    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


'''
查询区域和设施
'''


@house_blue.route('/area_facility/', methods=['GET'])
def area_facility():
    # 查询地址
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    # 查询设施
    facility_list = Facility.query.all()
    facility_dict_list = [facility.to_dict() for facility in facility_list]
    # 构造结果并返回
    return jsonify(area=area_dict_list, facility=facility_dict_list)


'''
发布新房源
'''


@house_blue.route('/new_house/', methods=['POST', 'GET'])
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')
    if request.method == 'POST':
        #         接收数据
        params = request.form.to_dict()
        facility_ids = request.form.getlist('facility')
        #
        #         创建对象并保存
        house = House()
        house.user_id = session['user_id']
        house.area_id = params.get('area_id')
        house.title = params.get('title')
        house.price = params.get('price')
        house.address = params.get('room_count')
        house.beds = params.get('beds')
        house.unit = params.get('unit')
        house.capacity = params.get('capacity ')
        house.deposit = params.get('deposit')
        house.min_days = params.get('min_days')
        house.max_days = params.get('max_days')
        # 根据设施的编号查询设施对象
        if facility_ids:
            facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
            house.facilities = facility_list
        house.add_update()
        # 返回结果
        return jsonify(code='200', house_id=house.id)


'''
添加新房源图片
'''


@house_blue.route('/image/', methods=["POST"])
def house_image():
    # 房屋编号
    house_id = request.form.get('house_id')
    # 房屋图片
    house_image = request.files.get('house_image')

    # 保存房屋图片
    url = os.path.join(os.path.join(UPLOAD_FOLDER, 'house'), house_image.filename)
    house_image.save(url)

    # 创建一个图片对象
    houseimage = HouseImage()
    houseimage.house_id = house_id
    houseimage.url = url
    houseimage.add_update()

    #     房屋默认图片
    house = House.query.get(house_id)

    if not house.index_image_url:
        house.index_image_url = os.path.join('/static/upload/house', house_image.filename)

    house.add_update()
    # 返回图片信息
    return jsonify(code='200', url=os.path.join('/static/upload/house', house_image.filename))


'''
房屋详细信息
'''


@house_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blue.route('/detail/<int:id>/', methods=["GET"])
def detail_id(id):
    # 获取房源对象
    house = House.query.get(id)
    # 房源设施信息信息
    facility_list = house.facilities
    facility_list_dict = []
    for facility in facility_list:
        facility_dict = facility.to_dict()
        facility_list_dict.append(facility_dict)
    # 判断当前登录用户是否为房屋所有者，从而设置是否显示预定按钮
    booking = 1
    user_id = session['user_id']
    if house.id == user_id:
        booking = 0
    return jsonify(code='200', house=house.to_full_dict(), booking=booking, facility_list=facility_list_dict)


'''首页获取区域,用户，房屋信息,'''
@house_blue.route('/hindex/', methods=["GET"])
def hindex():
    if 'user_id'in session:
        user = User.query.filter(User.id==session['user_id']).first()
        user_name = user.name

    # 返回最新的5个房屋信息
    hlist = House.query.order_by(House.id.desc()).all()[:5]
    hlist2 =[house.to_dict() for house in hlist]

    # 查找地区信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]

    return jsonify(code='200', name=user_name, hlist=hlist2, alist=area_dict_list)


'''
搜索
'''


@house_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@house_blue.route('/searchall/', methods=["GET"])
def searchall():
    # TODO 后期需要优化，过滤掉该用户已经下了单的房间
    dict = request.args

    sort_key = dict.get('sk')  # 排序
    a_id = dict.get('aid')  # 区域
    begin_date = dict.get('sd')  # 入住时间
    end_date = dict.get('ed')  # 离店时间

    houses = House.query.filter_by(area_id=a_id)
    # 不能查询自己发布的房源，排除当前用户发布的房屋
    if 'user_id' in session:
        hlist = houses.filter(House.user_id != (session['user_id']))

    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
    order_list = Order.query.filter(Order.status != 'REJECTED')
    # 情况一：
    order_list1 = order_list.filter(Order.begin_date >= begin_date, Order.end_date <= end_date)
    # 情况二：
    order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
    # 情况三：
    order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
    # 情况四：
    order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
    # 获取订单中的房屋编号
    house_ids = [order.house_id for order in order_list2]
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
    # 查询排除入住时间和离店时间在预约订单内的房屋信息
    hlist = hlist.filter(House.id.notin_(house_ids))

    # 排序规则,默认根据最新排列
    sort = House.id.desc()
    if sort_key == 'booking':
        sort = House.order_count.desc()
    elif sort_key == 'price-inc':
        sort = House.price.asc()
    elif sort_key == 'price-des':
        sort = House.price.desc()
    hlist = hlist.order_by(sort)
    hlist = [house.to_dict() for house in hlist]

    # 获取区域信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]

    return jsonify(code='200', houses=hlist, areas=area_dict_list)




'''
房间预约
'''
@house_blue.route('/booking/')
def booking():

    return render_template('booking.html')


'''
房间预约,房屋详细信息获取
'''
#TODO 获取房屋详情可以复用/house/detail/[id]/接口
@house_blue.route('/getbookingbyid/<int:id>/')
def get_booking_by_id(id):
    house = House.query.get(id)
    return jsonify(house=house.to_dict())
