from django.urls import path

from payments import views

urlpatterns = [
    path("pay/", views.AliPayAPIView.as_view()),
    path("order_end/", views.OrderSuccessAPIView.as_view())
]
