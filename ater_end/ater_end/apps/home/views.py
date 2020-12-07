from django.shortcuts import render
from rest_framework.generics import ListAPIView

# Create your views here.
from home.models import Banner, Nav
from home.serializer import BannerModelSerializer, NavModelSerializer


# banner图接口
class BannerApiView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by('-orders')
    print(queryset,12121221222121211222)
    serializer_class = BannerModelSerializer


# 顶部连接
class HeaderNavApiView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, is_position=1)
    serializer_class = NavModelSerializer


# 底部连接
class FootNavApiView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False, is_position=2)
    serializer_class = NavModelSerializer
