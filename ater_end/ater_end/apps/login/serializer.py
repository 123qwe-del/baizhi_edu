
from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from requests import request
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from login.models import UserModel
from login.service import get_user_by_account


class registerModelSerializer(ModelSerializer):
    print(7)
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    code = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'phone', 'id', "password", 'token', 'code')
        extra_kwargs = {
            "phone": {
                "write_only": True
            },
            "password": {
                "write_only": True
            },
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')
        print(phone, 31, code)
        redis_connection = get_redis_connection("default")
        phone_code = redis_connection.get('model_%s'%phone)
        if phone_code is not None:
            phone_code1 = phone_code.decode("utf-8")
            print(phone_code1, 45454545454545454545454545)
            if code == phone_code1:
                print("第49行")
                try:
                    user = get_user_by_account(phone)
                    print(user)
                except UserModel.DoesNotExist:
                    user = None
                if user:
                    raise serializers.ValidationError("手机号已注册")
                print(attrs,57)
                return attrs
            else:
                raise serializers.ValidationError("验证码错错误")  # 验证码错错误
        else:
            return Response({"message":"验证码已过期"},status=status.HTTP_400_BAD_REQUEST)

    # 重写create方法
    def create(self, validated_data):
        password = validated_data.get('password')
        hash_pwd = make_password(password)
        phone = validated_data.get('phone')
        # 将用户名默认设置为电话号
        user = UserModel.objects.create(phone=phone, username=phone, password=hash_pwd)

        # 为用户生成token
        from rest_framework_jwt.settings import api_settings
        paylod = api_settings.JWT_PAYLOAD_HANDLER(user)
        user.token = api_settings.JWT_ENCODE_HANDLER(paylod)
        return user

