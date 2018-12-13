from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^add-eticket.html$', views.add_eticket, name='add_eticket'),
    re_path(r'^admin-eticket-list.html$', views.admin_eticket_list, name='admin_eticket_list'),

    re_path(r'^etickets.html$', views.eticket_list, name='eticket_list'),
    re_path(r'^eticket-(?P<eticket_id>\d+)-detail.html$', views.eticket_detail, name='eticket_detail'),
    re_path(r'^edit-article-(?P<article_id>\d+).html$', views.edit_article, name='edit_article'),

    re_path(r'^add-article.html$', views.add_article, name='add_article'),
    re_path(r'^article-(?P<category_id>\d+)-(?P<type_id>\d+).html$', views.article_list, name="backend_articles"),
    re_path(r'^index.html$', views.article_list, name='backend'),

]
