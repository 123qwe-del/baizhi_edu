from django.urls import path

from home import views

urlpatterns = [
    path('banner/',views.BannerApiView.as_view()),  # banner图url
    path('hdr/',views.HeaderNavApiView.as_view()),  # 顶部导航
    path('foot/',views.FootNavApiView.as_view())    # 底部导航
]