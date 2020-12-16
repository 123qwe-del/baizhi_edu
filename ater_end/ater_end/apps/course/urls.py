from django.urls import path

from course import views

urlpatterns = [
    path('big-title/',views.CourseCategoryAPIView.as_view()),
    path('intermediate-title/',views.CourseAPIView.as_view()),
    path('detail/<int:pk>',views.CourseDetialAPIView.as_view()),
]