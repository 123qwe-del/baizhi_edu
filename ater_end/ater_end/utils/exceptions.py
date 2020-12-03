from rest_framework.views import exception_handler
from rest_framework.response import Response

"""
自定义异常处理
"""


def custom_exception_handler(exc, context):  # 继承自drf的exceotions_handle
    response = exception_handler(exc, context)
    if response is None:
        return Response({
            'detail': '%s,%s' % (context['view'], exc)
        })
    return response
