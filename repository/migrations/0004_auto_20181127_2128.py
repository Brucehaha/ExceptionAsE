# Generated by Django 2.0.1 on 2018-11-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20181127_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created time'),
        ),
    ]
