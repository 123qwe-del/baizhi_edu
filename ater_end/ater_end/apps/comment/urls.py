from django.urls import path

from comment import views

urlpatterns = [
    path("comment/",views.CommentListCreateApiView.as_view()),
    path("createcomment/",views.CommentCreatApiView.as_view())
]