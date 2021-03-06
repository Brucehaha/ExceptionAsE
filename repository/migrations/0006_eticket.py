# Generated by Django 2.1.3 on 2018-12-14 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20181203_1200'),
    ]

    operations = [
        migrations.CreateModel(
            name='ETicket',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=32)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'open'), (1, 'processing'), (2, 'closed')], default=0)),
                ('claimer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claimer', to='repository.UserInfo')),
                ('processor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processor', to='repository.UserInfo')),
            ],
        ),
    ]
