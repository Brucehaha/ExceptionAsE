from django.shortcuts import render, HttpResponse
from . import models

# Create your views here.


def menu(request):
    menu_list = models.Menu.objects.values('id', 'caption', 'parent_id')
    menu_dict = {}
    parents = []
    for x in menu_list:
        # x = {
        #     'id': x[id],
        #     'caption': x[caption],
        #     'child'
        #
        # }
        if x['parent_id']:
            if x['parent_id'] in menu_dict:
                menu_dict[x['parent_id']].append(x)
            else:
                menu_dict[x['parent_id']] = [x, ]
        else:
            parents.append(x)
    print(menu_dict)
    print(parents)

    return HttpResponse('x')