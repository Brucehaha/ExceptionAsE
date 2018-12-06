from django.shortcuts import render, HttpResponse, reverse
from repository import models
from utils.pager import Pagination


def manage(request):
    return render(request, 'backend/backend_layout.html', {})


def article(request):
    return render(request, 'backend/backend_article.html', {})


def article(request, *args, **kwargs):
    """
    list the articles by conditions
    :param request: user_info
    :param args:
    :param kwargs: type_id, category_id
    :return: articles
    """
    conditions = {}
    blog_id = request.session.get('user_info')['blog__nid']

    for k, v in kwargs.items():
        if v == '0':
            pass
        else:
            conditions[k] = int(v)
    conditions['blog_id'] = blog_id

    articles = models.Article.objects.filter(**conditions).order_by('-nid')
    category_list = models.Category.objects.filter(blog_id=blog_id).only('nid', 'title')
    type_list = models.Article.type_choices
    print(type_list)
    print(articles.count())
    data = {
        'articles': articles,
        'conditions': conditions,
        'category_list': category_list,
        'type_list': type_list,
    }
    return render(request, 'backend/backend_article.html', data)
