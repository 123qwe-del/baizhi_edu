from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from comment.serializer import CommentSerializer
from .models import Comment


class CommentListCreateApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentCreatApiView(GenericAPIView, CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        print(1888888888888888)
        with transaction.atomic():
            return self.create(request, *args, **kwargs)

        # TODO  添加不成功
