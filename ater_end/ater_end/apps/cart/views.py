from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection

from ater_end.settings.constants import BRIEF_URL
from course.models import Course, CourseExpire


# 添加购物车接口
class CartAPIView(ViewSet):
    """添加购物车"""
    print("进入添加")
    # 进入购物车前对用户进行登陆校验
    permission_classes = [IsAuthenticated]

    # 自定义添加方法
    def add_cart(self, request):
        print("add")
        """课程id 课程有效期 勾选状态  用户id"""

        # 课程id
        course_id = request.data.get('course_id')
        print(course_id)
        # 用户id
        user_id = request.user.id
        # 勾选状态，默认为勾选
        select = True
        # 有效期
        expire = 0

        # 根据用户id查看数据库有没有这个课程
        try:
            abc = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 存进redis数据库
            redis_connection = get_redis_connection("cart")  # 获取rediss链接
            pipeline = redis_connection.pipeline()  # 开通管道
            pipeline.multi()  # 开启管道
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            pipeline.sadd("selected_%s" % user_id, course_id)  # 被勾选的商品
            pipeline.execute()  # 执行操作
            course_len = redis_connection.hlen("cart_%s" % user_id)  # 获取购物车商品总数量
        except:
            return Response({
                "message": "添加失败",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "message": "添加购物车成功",
            "course_len": course_len,
        }, status=status.HTTP_200_OK)

    # 自定义查询方法
    def find_cart(self, request):
        user_id = request.user.id
        """
        根据用户id查找所有的信息（课程id，有效）
        根据课程id查出课程的对应信息（）
        """

        # 获取链接
        redis_connection = get_redis_connection("cart")
        # 根据用户id查找
        cart_list_bytes = redis_connection.hgetall('cart_%s' % user_id)
        # print(cart_list_bytes, "72查询的72行", type(cart_list_bytes))  # 二进制<class 'dict'>
        # 根据用户id查找已选中的状态
        select_list_bytes = redis_connection.smembers('selected_%s' % user_id)
        # print(select_list_bytes, "75行打印", type(select_list_bytes))  # 二进制<class 'set'>

        data = []
        total_price = 0

        # 遍历查询
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue

            # 如果有效期的id大于0，则需要通过有效期对应的价格来计算活动真实价  id不大于0则使用课程本身的原价
            original_price = course.price
            expire_text = "永久有效"

            try:
                if expire_id > 0:
                    course_expire = CourseExpire.objects.get(id=expire_id)
                    # 对应有效期的价格
                    original_price = course_expire.price
                    expire_text = course_expire.expire_text
            except CourseExpire.DoesNotExist:
                pass
            # 根据已勾选的商品对应的有效期的价格来计算商品的最终价格
            final_price = course.final_price(expire_id)

            data.append({
                "select": True if course_id_byte in select_list_bytes else False,
                "course_img": BRIEF_URL + course.course_img.url,
                "id": course.id,
                "name": course.name,
                "price": course.price,
                "expire_id": expire_id,
                "discount_price": original_price,
                "expire_list": course.useful_life,
                "total_price":total_price
            })
            # 商品叠加后的真实总价
            total_price += float(final_price)

        return Response(data)


# 是否选中API接口
class SelectAPIView(ViewSet):
    # 用户校验
    permission_classes = [IsAuthenticated]

    # 修改是否选中
    def amend_select(self, request, *args, **kwargs):
        course_id = kwargs.get("id")  # 课程id
        user_id = request.user.id  # 用户id
        redis_connection = get_redis_connection("cart")  # 获取redis连接
        select_list_bytes = redis_connection.smembers('selected_%s' % user_id)  # 查询用户id相等的数据
        list = []
        for cour_id in select_list_bytes:
            cour_id = int(cour_id)
            list.append(int(cour_id))
        if course_id in list:
            """判断状态，如果在列表里，就删除它，如果不在添加（达到选不选中的效果）"""
            redis_connection.srem('selected_%s' % user_id, course_id)
        else:
            redis_connection.sadd('selected_%s' % user_id, course_id)
        return Response({"message": "操作成功"}, status=status.HTTP_200_OK)

    # 删除购物车
    def deletecart(self, request, *args, **kwargs):
        course_id = kwargs.get("id")
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        redis_connection.hdel('cart_%s' % user_id, course_id)  # 删除用户id下的单个数据
        redis_connection.srem('selected_%s' % user_id, course_id)  # 删除选中状态表里的单个数据
        return Response({
            "message": "删除成功"
        }, status=status.HTTP_200_OK)

    # 修改有效期
    def updatecart(self, request):
        course_id = request.data.get("id")
        expire = request.data.get("expire")
        expire = int(expire)
        user_id = request.user.id
        # if expire not in [0, 1, 2, 3, 4, 5]:
        #     return Response({'message': '参数错误'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': '该课程不存在或已下架'}, status=status.HTTP_400_BAD_REQUEST)
        conn = get_redis_connection('cart')
        cart_list = conn.hgetall('cart_%s' % user_id)
        select = conn.hexists("cart_%s" % user_id, course_id)
        if select:
            conn.hset("cart_%s" % user_id, course_id, expire)
        else:
            return Response({'message': '该课程不存在或已下架'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    # 全部选中或全不选中
    def select_all(self, request):
        user_id = request.user.id
        status = request.data.get("status")  # 获取前端数据状态
        course_id = request.data.get("id")
        redis_connection = get_redis_connection("cart")  # 会获取连接
        select_list_bytes = redis_connection.smembers('selected_%s' % user_id)  # 获取当前所选择的课程
        if course_id:
            for course in course_id:  # 便利课程id
                if status == False:  # 如果选中状态为Flase
                    redis_connection.srem('selected_%s' % user_id, course)
                else:
                    if course in select_list_bytes:  # 判断课程id在不在已有的id里有过在什么也不做，如果不在添加
                        pass
                    redis_connection.sadd('selected_%s' % user_id, course)
            return Response({"message": "OK"})
        return Response({"message": '参数错误', })

    # 购物车订单查询
    def get_cart_order(self, request):
        """
        1.获取购物车中一勾选得商品，返回前端所需的数据
        :param request:
        :return:
        """
        user_id = request.user.id
        print(user_id)

        # 获取链接
        redis_connection = get_redis_connection("cart")
        # 获取当前用户所有选中得数据
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        # 获取当前用户所选中得课程
        select_list = redis_connection.smembers("selected_%s" % user_id)
        # 总计价格0
        print(cart_list, select_list, 231)
        total_price = 0 # 是付款
        acount_payable = 0 # 应付款
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            print(course_id, expire_id, 238)
            if course_id_byte in select_list:
                try:
                    # 根据得到得课程id产出对应的课程信息
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue
                # 如果有效期的id大于0，则需要通过有效期对应的价格来计算活动真实价  id不大于0则使用课程本身的原价
                original_price = course.price
                expire_text = "永久有效"
                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(pk=expire_id)
                        print(course_expire, 251)
                        original_price = course_expire.price
                        expire_text = course_expire.expire_text
                        print(original_price, expire_text, 254)
                except CourseExpire.DoesNotExist:
                    pass

                final_price = course.final_price(expire_id)
                print(final_price, 258)

                data.append({
                    "select": True if course_id_byte in select_list else False,
                    "course_img": BRIEF_URL + course.course_img.url,
                    "id": course.id,
                    "name": course.name,
                    "price": original_price,
                    "expire_id": expire_id,
                    "discount_price": final_price,  # 根据有限期价格计算出最终价格
                    "expire_text": expire_text,
                })
                if final_price==None:
                    final_price=original_price
                    total_price += float(final_price)
                else:
                    total_price += float(final_price)
                acount_payable += float(original_price)
        return Response({"data":data,"total_price":total_price,"acount_payable":acount_payable})



