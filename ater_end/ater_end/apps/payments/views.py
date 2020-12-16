from datetime import datetime

from alipay import AliPay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ater_end.settings.develop import ALIAPY_CONFIG
from course.models import CourseExpire
from order.models import Order
from payments.models import UserCourse


class AliPayAPIView(APIView):
    """
    生成支付宝连接
    """

    def get(self, request):

        # 获取订单号
        order_number = request.query_params.get("order_number")

        try:
            order = Order.objects.get(order_number=order_number)  # 查询订单是否存在
        except Order.DoesNotExist:
            return Response({"message": "对不起您支付的订单不存在"}, status=status.HTTP_400_BAD_REQUEST)

        # 初始化支付宝参数
        alipay = AliPay(
            appid=ALIAPY_CONFIG["appid"],
            app_notify_url=ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=ALIAPY_CONFIG["debug"],  # 默认False
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,  # 订单号
            total_amount=float(order.real_price),  # 合计价格
            subject=order.order_title,  # 标题
            return_url=ALIAPY_CONFIG["return_url"],  # 回调路径
            notify_url=ALIAPY_CONFIG["notify_url"],  # 可选, 不填则使用默认notify url
        )

        url = ALIAPY_CONFIG["gateway_url"] + order_string

        print(url)
        return Response(url)


class OrderSuccessAPIView(APIView):
    """
    验证支付是否成功：
    修改订单状态：支付类型，支付时间，
    生成用户购买记录：
    展示结算信息：购买课程数量，付款时间，付款总金额，课程信息
    """

    # 1.验证支付是否成功:
    def get(self, request):
        # 初始化支付宝参数
        alipay = AliPay(
            appid=ALIAPY_CONFIG["appid"],
            app_notify_url=ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=ALIAPY_CONFIG["app_private_key_path"],
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=ALIAPY_CONFIG["alipay_public_key_path"],
            sign_type=ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=ALIAPY_CONFIG["debug"],  # 默认False
        )
        data = request.query_params.dict()
        signature = data.pop("sign")
        # 认证
        success = alipay.verify(data, signature)
        print(success,"***+++++++++++++++++++++++++++++++++++++++++++")
        if success:
            return self.update_order(data)
        return Response("OK")

    def update_order(self, data):
        """
        1.修改订单状态：支付类型，支付时间，
        生成用户购买记录：
        展示结算信息：购买课程数量，付款时间，付款总金额，课程信息
        :param request:
        :return:
        """
        # 1.修改订单状态：支付类型，支付时间，
        # 获取订单号
        order_number = data.get("out_trade_no")
        print(order_number,93,"行","-----------------------------------")
        try:
            order = Order.objects.get(order_number=order_number, order_status=0)
        except Order.DoesNotExist:
            return Response({"message": "订单查询不存在"})
        # 修改数据库
        try:
            order.order_status = 1
            order.pay_time = datetime.now()
            order.save()
            # 生成用户购买记录：
            # 根据订单获取用户id
            user = order.user
            print(user, 100)
            # 获取当期那用户所购买的所有课程信息
            order_course_list = order.order_courses.all()
            print(order_course_list,109)
            # 订单详情页信息显示
            end_list = []  # 返回前端数据
            for order_course in order_course_list:
                # 获取课程信息
                course = order_course.course  # 课程信息
                print(1151115115115)
                course.students += 1
                course.save()
                # 判断用户购买的有效期是否是前长期有效，如果长期有效则时间改为永久，否则用当前时间加有效期天数
                pay_time = order.pay_time
                print(120,pay_time,type(pay_time))
                if order_course.expire > 0:  # 说明不是长期有效
                    # 获取有效期对象
                    expire = CourseExpire.objects.get(pk=order_course.expire)
                    expire_time = expire.expire_time * 24 * 60 * 60  # 修改有效期时间
                    end_time = datetime.fromtimestamp(pay_time + expire_time)  # 计算有效期结束时间
                    print(end_time)
                else:
                    end_time = None
                    # 为用户生成购买记录
                print(130,end_time)
                UserCourse.objects.create(
                    user_id=user.id,
                    course_id=course.id,
                    trade_no=data.get("trade_no"),
                    buy_type=1,
                    pay_time=pay_time,
                    out_time=end_time,
                )
                    # 返回前端所需的数据
                print(139)
                end_list.append({
                    "pay_time": order.pay_time,
                    "course_title": course.name,
                    "total_price": order.total_price,
                })
                print(145)
        except:
            return Response({"message":"更新订单信息失败"}, status=status.HTTP_400_BAD_REQUEST)
        print(148)
        return Response({
            "end_list":end_list
        })
