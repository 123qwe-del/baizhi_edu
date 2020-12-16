from django.contrib.auth.backends import ModelBackend

# 重写jwt返回值
from django.db.models import Q

from login.models import UserModel


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username
    }


def get_user_by_account(account):
    try:
        user = UserModel.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
        print(user, 19,type(user))
    except UserModel.DoesNotExist:
        return None
    return user


# 自定义多种登陆方式：
# 定义类
class UserAuthentication(ModelBackend):
    print('进入自定义')

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写方法实现多方式登陆
        :param request:    前端请求数据
        :param username:  前端数据的条件
        :param password:
        :param kwargs:
        :return:    返回用户
        """
        user = get_user_by_account(username)
        print(user, 38)
        print(password,"***")
        print(user.check_password(password),41)
        print(user.is_authenticated,52)
        if user and user.check_password(password) and user.is_authenticated:
            print(user.check_password(password),42)
            return user
        print(44)
        return None
