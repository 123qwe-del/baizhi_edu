import random
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
# 滑块验证码
from ater_end.libs.geetest import GeetestLib
from ater_end.settings import constants
from ater_end.utils.send_message import Message
from login.models import UserModel
from login.serializer import registerModelSerializer
from login.service import get_user_by_account

pc_geetest_id = "759d5436a6bfe1e0a94d222e9452097b"
pc_geetest_key = "2061a99f3c25e50989a0c04536132953"


# 图片验证码接口
class CaptchaAPIView(APIView):
    user_id = 1
    status = False

    def get(self, request):
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        print(user)
        if user is None:
            return Response({'message': '该用户不存在'}, status.HTTP_400_BAD_REQUEST)
        self.user_id = user.id
        print(self.user_id, "*****************", user.id, "*************", 19, user)

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge")
        validate = request.data.get("geetest_validate")
        seccode = request.data.get("geetest_seccode")

        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print(result)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


# 电话输入框认证
class check_phone(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get("phone")
        print(phone)
        user = get_user_by_account(phone)
        if user:
            return Response({"message": 'ERROR'}, status=status.HTTP_200_OK)
        return Response({"message": "OK"}, status=status.HTTP_200_OK)


# 用户注册接口
class registerApiView(CreateAPIView):
    print(50)
    queryset = UserModel.objects.all()
    serializer_class = registerModelSerializer


# 短信验证接口
class GetMessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 获取电话号
        phone = request.query_params.get("phone")
        print(phone, 616161616161616116616666)
        # 获取redis链接
        redis_connection = get_redis_connection("default")
        # 查询是存在验证码
        phone_code = redis_connection.get("sms_%s" % phone)
        if phone_code is not None:
            return Response({"message": '60秒内只能发送一条数据'}, status=status.HTTP_400_BAD_REQUEST)
        # 生成随机验证码
        code = random.randint(100000, 999999)
        print(code, "**********************************************")
        redis_connection.setex("sms_%s" % phone, 60, code)  # 存储验证时间为60秒
        redis_connection.setex('model_%s' % phone, 600, code)  # 有效期为10分钟
        # 调用短信发送方法
        try:
            msg = Message(constants.MESSAGE_API_KEY)
            msg.send_message(phone=phone, code=code)
        except:
            return Response({"message":'ERROR'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # 短信发送失败
        return Response({"message": 'OK'}, status=status.HTTP_200_OK)  # 短信发送成功


# 短息登陆
class MessageLogin(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        code = request.data.get('code')
        redis_connection = get_redis_connection("default")
        phone_code = redis_connection.get('model_%s' % phone)
        print(105,phone_code,105)
        try:
            phone_code = phone_code.decode("utf-8")
            print(107,phone, code, phone_code,107)
            if code == phone_code:
                user = UserModel.objects.filter(phone=phone).first()
                if user:
                    from rest_framework_jwt.settings import api_settings
                    paylod = api_settings.JWT_PAYLOAD_HANDLER(user)
                    token = api_settings.JWT_ENCODE_HANDLER(paylod)
                    # return user
                    print(token)
                    return Response(token)
                return None
        except:
            return Response({"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)  # 验证码错误
