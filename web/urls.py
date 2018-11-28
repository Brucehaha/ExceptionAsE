from django.conf.urls import re_path
from web.views import home
from web.views import account


urlpatterns = [
    re_path(r'^check_code.html$',account.check_code),
    re_path(r'^login.html', account.login),
    re_path(r'^all/(?P<type_id>\d+).html', home.index, name='index'),
    re_path(r'^', home.index),

]