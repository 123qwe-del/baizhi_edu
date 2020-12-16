from rest_framework.generics import CreateAPIView

# 订单试图
from order.models import Order
from order.serializer import OrderModelserializer


class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelserializer
