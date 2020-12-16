from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from login import views

urlpatterns = [
    path('login/', obtain_jwt_token),  # 登陆接口
    path("captcha/", views.CaptchaAPIView.as_view()),  # 获取图片验证码
    path("register/", views.registerApiView.as_view()),  # 注册接口
    path('message/', views.GetMessageAPIView.as_view()),  # 短信接口
    path("check_phone/", views.check_phone.as_view()),  # 电话校验
    path('messageLogin/', views.MessageLogin.as_view())  # 短信登陆接口
]
