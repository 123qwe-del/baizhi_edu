from django.urls import path

from cart import views

urlpatterns = [
    path("cart/", views.CartAPIView.as_view({"post": "add_cart",
                                             "get": "find_cart"})),  # 查询购物车数据
    path("select/<int:id>/", views.SelectAPIView.as_view({"get": "amend_select",
                                                          "delete": "deletecart",
                                                          "put": "updatecart",
                                                          "patch": "select_all"})),  # 购物车单个功能实现
    path("select/", views.SelectAPIView.as_view({"get": "amend_select",
                                                 "delete": "deletecart",
                                                 "put": "updatecart",
                                                 "patch": "select_all"})),  # 购物车单个功能实现
    path("order/",views.SelectAPIView.as_view({"get":"get_cart_order"}))
]
