from django.conf.urls import re_path
from web.views import home
from web.views import account


urlpatterns = [
    re_path(r'^json/reply-comment$', home.reply_comment),
    re_path(r'^account/login.html$', account.login),
    re_path(r'^account/check_code.html$', account.check_code),
    re_path(r'^all/(?P<type_id>\d+).html', home.index, name='index'),
    re_path(r'^(?P<site>\w+)/(?P<nid>\d+).html$', home.ArticleDetail, name='article'),
    re_path(r'^(?P<site>\w+)/(?P<condition>(tag)|(category)|(date))/(?P<val>\w+-*\w*).html$', home.filter),
    re_path(r'^(?P<site>\w+).html$', home.site),
    re_path(r'^', home.index),

]