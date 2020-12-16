import xadmin
from xadmin import views
from .models import Comment



class CommentInfo(object):
    list_display = ["name", "content", "time","avatar","count"]

xadmin.site.register(Comment,CommentInfo)