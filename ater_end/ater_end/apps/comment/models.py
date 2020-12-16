from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name="当前登陆的用户名")
    content = models.CharField(max_length=1024,verbose_name="评论内容")
    time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    avatar = models.ImageField(null=True,verbose_name="头像")
    count = models.IntegerField(default=0,verbose_name="点赞数量")

    class Meta:
        db_table = "bz_comment"
        verbose_name = "评论表"
        verbose_name_plural = verbose_name
