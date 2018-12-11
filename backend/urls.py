from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^edit-article-(?P<article_id>\d+).html$', views.edit_article),
    re_path(r'^add-article.html$', views.add_article),
    re_path(r'^article-(?P<category_id>\d+)-(?P<type_id>\d+).html$', views.article, name="backend_articles"),
    re_path(r'^index.html$', views.article),

]
