from django.shortcuts import render, reverse, HttpResponse
from utils.pager import Pagination
from repository import models
import json


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
                          item_no=5,
                          current_page=request.GET.get('p'),
                          url=base_url)
    article_list = models.Article. \
                          objects. \
                          filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]

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
    from django.db import connection, transaction
    cursor = connection.cursor()

    # # Data modifying operation - commit required
    # cursor.execute(
    #     '''
    #     select
    #     count(nid) as num,
    #     strftime("%Y-%m", create_time) as id
    #     from repository_article
    #     group by strftime("%Y-%m",create_time)
    #     ''')
    # row=cursor.fetchall()
    #


    blog_site = kwargs.get('site')
    blog = models.Blog.objects.filter(site=blog_site).select_related('user').first()
    category_list = models.Category.objects.filter(blog=blog)
    article_list = models.Article.objects.filter(blog=blog).order_by('-nid')
    tag_list = models.Tag.objects.filter(blog=blog)
    for x in tag_list:
        print(x.article_set)
    # in django need id, otherwise will get erro
    date_list =models.Article.objects.raw(
        '''
        select
        nid,
        count(nid) as num,
        strftime("%Y-%m", create_time) as id
        from repository_article
        group by strftime("%Y-%m",create_time)
        '''
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
        '''
        select
        nid,
        count(nid) as num, 
        strftime("%Y-%m", create_time) as ctime
        from repository_article 
        group by strftime("%Y-%m",create_time)
        '''
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
    base_url = "%s.html" % nid
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        '''
        select
        nid,
        count(nid) as num,
        strftime("%Y-%m",create_time) as ctime
        from repository_article 
        group by strftime("%Y-%m",create_time)
        '''
    )
    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category', 'articledetail').first()
    category_list = models.Category.objects.filter(blog=blog)
    comments_count =models.Comment.objects.filter(article=article).count()
    page_obj = Pagination(total_count=comments_count,
                          item_no=4,
                          current_page=request.GET.get('p'),
                          url=base_url)

    comment_list = models.Comment.objects.filter(article=article).select_related('reply')[page_obj.start:page_obj.end]

    data = {
        'blog': blog,
        'article': article,
        'comment_list': comment_list,
        'page_obj': page_obj,
        'tag_list': tag_list,
        'category_list': category_list,
        'date_list': date_list,
    }
    return render(request, 'article_detail.html', data)


def reply_comment(request):
    user_id = request.session.get('user_info')['nid']
    print(user_id)
    content= request.POST.get('content')
    print(content)
    article_id = int(request.POST.get('articleID'))
    print(article_id)
    models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
    return HttpResponse(json.dumps("thanks"))
