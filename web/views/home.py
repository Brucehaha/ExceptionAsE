from django.shortcuts import render, reverse
from utils.pager import Pagination
from repository import models


def index(request, *args, **kwargs):
    type_choices = models.Article.type_choices
    if kwargs:
        article_type_id = kwargs['type_id']
        base_url = reverse('index', kwargs=kwargs)
    else:
        article_type_id = None
        base_url = ""
    article_count = models.Article.objects.filter(**kwargs).count()
    page_obj = Pagination(total_count=article_count,
                          item_no=7,
                          current_page=request.GET.get('p'),
                          url=base_url)
    article_list = models.Article. \
                          objects. \
                          filter(**kwargs)[page_obj.start:page_obj.end]

    data = {
        'article_list': article_list,
        'article_type_id': article_type_id,
        'type_choices': type_choices,
        'page_obj': page_obj,
    }

    return render(request, 'index.html', data)
