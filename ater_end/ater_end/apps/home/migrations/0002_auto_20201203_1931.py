# Generated by Django 2.0.6 on 2020-12-03 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nav',
            options={'verbose_name': '导航栏', 'verbose_name_plural': '导航栏'},
        ),
        migrations.AlterModelTable(
            name='nav',
            table='nav',
        ),
    ]
