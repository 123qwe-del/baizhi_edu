from django.db import models


# Create your models here.

class BaseModel(models.Model):
    is_show = models.BooleanField(default=False, verbose_name='是否显示')
    orders = models.IntegerField(default=1, verbose_name='图片排序')
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 设置后不会在数据库中生成表结构
        abstract = True


class Banner(BaseModel):
    img = models.ImageField(upload_to='banner', max_length=256, verbose_name='轮播图')
    link = models.CharField(max_length=256, verbose_name='图片链接')
    title = models.CharField(max_length=80, verbose_name='图片标题')

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Nav(BaseModel):
    POSITION_OPTION = (
        (1, '顶部导航'),
        (2, '底部导航')
    )
    title = models.CharField(max_length=80)
    link = models.CharField(max_length=256)
    is_site = models.BooleanField(default=False, verbose_name='是否是外部链接')
    is_position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name='导航栏位置')


    class Meta:
        db_table = 'nav'
        verbose_name = '导航栏'
        verbose_name_plural = verbose_name