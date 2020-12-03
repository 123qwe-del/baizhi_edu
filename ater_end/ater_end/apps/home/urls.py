from django.urls import path

from home import views

urlpatterns = [
    path('banner/',views.BannerApiView.as_view()),
    path('hdr/',views.HeaderNavApiView.as_view()),
    path('foot/',views.FootNavApiView.as_view())
]