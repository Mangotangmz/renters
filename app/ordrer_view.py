from datetime import datetime

from flask import Flask, jsonify, session
from flask import Blueprint, request, render_template

from app.model import User, db, Order, House
from utils import status_code

order_blue = Blueprint('order', __name__)

'''
下单，创建预约单
'''


@order_blue.route('/', methods=["POST"])
def order():
    # 接收参数
    dict = request.form
    house_id = int(dict.get('house_id'))
    start_date = datetime.strptime(dict.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(dict.get('end_date'), '%Y-%m-%d')

    # 验证有效性
    if not all([house_id, start_date, end_date]):
        return jsonify(status_code.PARAMS_ERROR)

    if start_date > end_date:
        return jsonify(status_code.ORDER_START_END_TIME_ERROR)

    # 查询房屋对象
    try:
        house = House.query.get(house_id)
    except:
        return jsonify(status_code.DATABASE_ERROR)
    # 创建订单对象
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price

    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    # 返回信息
    return jsonify(code='200')


'''
订单
'''


@order_blue.route('/orders/')
def orders():
    return render_template('orders.html')


@order_blue.route('/allorders/')
def allorders():
    user_id = session['user_id']
    orders = Order.query.filter(Order.user_id == user_id).order_by(Order.id.desc())
    order_list = [order.to_dict() for order in orders]

    return jsonify(code='200', olist=order_list)


'''房东操作订单'''
@order_blue.route('/lorders/')
def lorders():
    return  render_template('lorders.html')


'''返回所有订单信息'''
order_blue.route('/fo/')
def fo():
    user_id = session['user_id']
    # 获取用户的所有房源编号
    houses = House.query.filter(House.user_id == user_id)
    hlist_id = [house.id for house in houses]

    # 根据房源编号查找订单
    orders = Order.query.filter(Order.house_id.in_(hlist_id) ).order_by(Order.id.desc())
    olist = [order.to_dict for order in orders]
    return jsonify(olist=olist)
