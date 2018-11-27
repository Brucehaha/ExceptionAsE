from django.conf.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^all/(?P<type_id>\d+).html', views.index, name='index'),
    re_path(r'^', views.index),

]