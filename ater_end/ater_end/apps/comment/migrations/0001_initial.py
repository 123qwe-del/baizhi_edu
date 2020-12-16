# Generated by Django 2.0.6 on 2020-12-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='当前登陆的用户名')),
                ('content', models.CharField(max_length=1024, verbose_name='评论内容')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('avatar', models.ImageField(null=True, upload_to='', verbose_name='头像')),
                ('count', models.IntegerField(default=0, verbose_name='点赞数量')),
            ],
            options={
                'verbose_name': '评论表',
                'verbose_name_plural': '评论表',
                'db_table': 'bz_comment',
            },
        ),
    ]
