from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from course.models import Course, CourseExpire
from order.models import Order, OrderDetail
from django_redis import get_redis_connection


class OrderModelserializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number", "pay_type")

        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True},
        }

    # 检验支付方式
    def validate(self, attrs):
        print("进入抓鬼那天")
        pay_type = attrs.get("pay_type")  # 获取前端支付方式
        print(pay_type)
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("您选择得支付方式不被支持")

        return attrs

    def create(self, validated_data):
        print("123456789")
        """
       1. 获取user_id  2. 生成唯一的订单号  3. 生成订单  4.生成订单详情， 5.加入事务  6.计算订单总价
       7. 移除已经支付得课程购物车
        :param validated_data:
        :return:
        """
        redis_connection = get_redis_connection("cart")
        # 1. 通过context与试图列request对象链接
        # 获取链接
        user_id = self.context['request'].user.id  # 获取到request对象   获取到user_id
        print(user_id, 44)
        # 2. 生成唯一得订单号（通过时间戳，用户id，数字累加，随机数字）
        ### 生成累加6位数字
        random_number = redis_connection.incr("number")  # 自增张一位数自
        print(random_number, 46)
        # 生成唯一得订单单号
        order_number = "bzjy" + datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % random_number
        print(order_number)
        # 添加事务
        with transaction.atomic():
            rollback_id = transaction.savepoint()
        # 生成订单
            order = Order.objects.create(
                order_title="百知美女在线发牌",
                total_price=0,
                real_price=0,
                order_number=order_number,
                order_status=0,
                pay_type=validated_data.get("pay_type"),
                credit=0,
                coupon=0,
                order_desc="百知教育，要啥有啥，当面蒙娜丽莎，背后蒙谁谁傻",
                user_id=user_id,
            )
            # 生成订单详情
            ## 获取当前购物车所选中得所有商品
            cart_list = redis_connection.hgetall("cart_%s" % user_id)
            select_list = redis_connection.smembers("selected_%s" % user_id)
            print(cart_list, select_list, 7171)
            for course_id_byte, expire_id_byte in cart_list.items():
                course_id = int(course_id_byte)  # 得到课程id
                expire_id = int(expire_id_byte)  #
                if course_id_byte in select_list:  # 如果在cart_list里，说明是选中得id
                    # 查询课程id相同得课程所有信息
                    try:
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        continue

                    # 如果id大于0，则根据有效期后得价格计算出活动得正是价格，否则位永久有效
                    original_price = course.price  # 原价
                    expire_text = "永久有效"

                    try:
                        if expire_id > 0:
                            course_expire = CourseExpire.objects.get(id=expire_id)
                            original_price = course_expire.price
                            expire_text = course_expire.expire_text
                    except CourseExpire.DoesNotExist:
                        pass
                    final_price = course.final_price(expire_id)  # 获取活动后价格
                    print(course.discount_name,1000000)
                    # 生成订单详情
                    try:
                        OrderDetail.objects.create(
                            order=order,  # order是生成得订单
                            course=course,  # 查询得数据库
                            expire=expire_id,  # 课程有效期
                            price=original_price,  # 原价
                            real_price=final_price,  # 活动会得最终价格
                            discount_name=course.discount_name  # 活动名称
                        )
                    except:
                        transaction.savepoint_rollback(rollback_id)
                        raise serializers.ValidationError("订单生成失败")
                    order.total_price += float(original_price)  # 计算总价格
                    order.real_price += float(final_price)  #  计算后动过后得总价格
                    redis_connection.hdel("cart_%s" % user_id, course_id)  # 删除用户id下的单个数据
                    redis_connection.srem("selected_%s" % user_id, course_id)  # 删除选中状态下得数据
                order.save()

            return order



# TODO  点击vue结算清单不显示，，
# TODO  价格错误