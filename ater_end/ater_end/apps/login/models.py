from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserModel(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    user_head = models.ImageField(upload_to='user_head', verbose_name='用户头像', blank=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
