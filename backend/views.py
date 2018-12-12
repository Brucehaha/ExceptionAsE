from django.shortcuts import render, HttpResponse, redirect
from repository import models
from utils.pager import Pagination
from .forms import form
from django.db import transaction


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
    print(blog_id)
    for k, v in kwargs.items():
        if v == '0':
            pass
        else:
            conditions[k] = int(v)
    conditions['blog_id'] = blog_id

    articles_counts = models.Article.objects.filter(**conditions).count()

    category_list = models.Category.objects.filter(blog_id=blog_id).only('nid', 'title')
    type_list = models.Article.type_choices
    pager = Pagination(total_count=articles_counts,
                       current_page=request.GET.get('p'),
                       item_no=5,
                       url='/backend/article-%s-%s.html' %
                           (kwargs.get('category_id', 0), kwargs.get('type_id', 0))
                       )
    articles = models.Article.objects.filter(**conditions).order_by('-nid')[pager.start:pager.end]

    data = {
        'articles': articles,
        'conditions': conditions,
        'category_list': category_list,
        'type_list': type_list,
        'pager':pager,
    }
    return render(request, 'backend/backend_article.html', data)


def add_article(request):
    """
    create new article
    :param request:
    :param args: reqquest data, session
    :param kwargs:
    :return:
    """
    if request.method == "GET":
        form_obj = form.ArticleForm(request=request)
        return render(request, 'backend/add-article.html', {'form': form_obj})
    elif request.method == "POST":
        user_info = request.session.get('user_info')
        if user_info:
            blog_id = user_info['blog__nid']
            form_obj = form.ArticleForm(request=request, data=request.POST)
            if form_obj.is_valid():
                try:
                    with transaction.atomic():
                        tags_id = form_obj.cleaned_data.pop('tags')
                        content = form_obj.cleaned_data.pop('content')
                        form_obj.cleaned_data['blog_id'] = blog_id
                        article_obj = models.Article.objects.create(**form_obj.cleaned_data)
                        models.ArticleDetail.objects.create(content=content, article=article_obj)
                        tag_list = list(map(lambda x: models.Article2Tag(tag_id=int(x), article=article_obj), tags_id))
                        models.Article2Tag.objects.bulk_create(tag_list)
                except Exception as e:
                    # return render(request, 'backend/add-article.html', {'form': form_obj})
                    print(e)
                    return HttpResponse("Created Failed")
            else:
                return render(request, 'backend/add-article.html', {'form': form_obj})
            return redirect("/backend/index.html")
        else:
            return redirect("/account/login.html")


def edit_article(request, article_id):
    """
    eidit arthcle
    :param request:
    :return:
    """
    blog_id = request.session.get('user_info')['blog__nid']
    if blog_id:
        if request.method == 'GET':
                obj = models.Article.objects.filter(nid=article_id, blog_id=blog_id).first()
                tag_list = models.Article2Tag.objects.filter(article=obj).values_list('tag_id')
                if tag_list:
                    tags = list(zip(*tag_list))[0]
                else:
                    tags = ()
                data = {
                    'title': obj.title ,
                    'summary': obj.summary,
                    'content': obj.articledetail.content,
                    'category_id': obj.category_id,
                    'type_id': obj.type_id,
                    'tags': tags,

                }
                instance = form.ArticleForm(request=request, data=data)

                return render(request, 'backend/edit_article.html', {'form': instance})
        elif request.method == 'POST':
                # stop modify other one's article like edit-article-1.hml change to edit-article-2.hml
                obj = models.Article.objects.filter(nid=article_id, blog_id=blog_id)
                if not obj:
                    return redirect('/login.html')
                instance = form.ArticleForm(request=request, data=request.POST)
                if instance.is_valid():
                    content = instance.cleaned_data.pop('content')
                    tags = instance.cleaned_data.pop('tags')
                    try:
                        with transaction.atomic():
                            article_obj = models.Article.objects.filter(nid=obj.nid).update(**instance)
                            models.ArticleDetail.objects.filter(article=article_obj).update(content=content)
                            models.Article2Tag.objects.filter(article=article_obj).delete()
                            tag_list = (lambda x: models.Article2Tag(article=article_obj, tag_id=int(x)), tags)
                            models.Article2Tag.objects.bulk_create(list(tag_list))
                    except Exception as e:
                        return HttpResponse('e')
                    return redirect('/backend.html')
    else:
        return redirect('/login.html')


def add_eticket(request):
    if request.method == 'GET':
        pass


