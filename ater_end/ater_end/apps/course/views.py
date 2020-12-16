from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from course.models import CourseCategory, Course
from course.serializer import CourseCategoryModelserializer, CourseModelSerializer, CourseDetailModelSerializer
from django_filters.rest_framework import DjangoFilterBackend

from course.service import CoursePageNumberPagination


class CourseCategoryAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseCategoryModelserializer


class CourseAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('orders')
    serializer_class = CourseModelSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)
    ordering_fields = ("id", "students", "price")
    pagination_class = CoursePageNumberPagination

class CourseDetialAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseDetailModelSerializer
