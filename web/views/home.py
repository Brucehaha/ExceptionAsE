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


def site(request, *args, **kwargs):
    """
    template for personal blog page
    :param request:
    :param args:
    :param kwargs: blog
    :return:
    """
    blog_site = kwargs.get('site')
    blog = models.Blog.objects.filter(site=blog_site).select_related('user').first()
    category_list = models.Category.objects.filter(blog=blog)
    article_list = models.Article.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    for x in tag_list:
        print(x.article_set)
    date_list =models.Article.objects.raw(
        'select nid, count(nid) as num, strftime("%Y-%m", create_time) as ctime from repository_article'
    )

    data = {
        'blog':blog,
        'category_list': category_list,
        'article_list': article_list,
        'date_list': date_list,
        'tag_list': tag_list,
    }
    return render(request, 'site.html', data)


def filter(request, site, condition, val):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    date_list =models.Article.objects.raw(
        'select nid, count(nid) as num, strftime("%Y-%m", create_time) as ctime from repository_article'
    )

    if condition == "category":
        article_list= models.Article.objects.filter(blog=blog, category=val)
    if condition == "tag":
        article_list= models.Article.objects.filter(blog=blog, tags=val)
    if condition == "date":
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
        # select * from tb where blog_id=1 and strftime("%Y-%m",create_time)=2017-01

    data = {
        'blog': blog,
        'category_list': category_list,
        'article_list': article_list,
        'date_list': date_list,
        'tag_list': tag_list,
    }
    return render(request, 'site.html', data)

def ArticleDetail(request, site, nid):
    """

    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category', 'articledetail').first()
    comment_list = models.Comment.objects.filter(article=article).select_related('reply')
    category_list = models.Category.objects.filter(blog=blog)
    data = {
        'blog': blog,
        'article': article,
        'comment_list': comment_list,
        'tag_list': tag_list,
        'category_list': category_list,
        'date_list': date_list,
    }
    return render(request, 'article_detail.html', data)
