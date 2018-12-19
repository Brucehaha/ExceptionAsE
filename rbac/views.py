from . import models
from django.shortcuts import redirect, HttpResponse
import re


class PermissionHandler:
    def __init__(self, request):
        self.request = request
        self.current_path = request.path_info
        self.roles = None
        self.p2a_dict = None
        self.menu_strings = ''
        self.session_data()

    def session_data(self):
        """
        store data in session for display menus and verify the url after login
        :return:
        """
        permission_dict = self.request.session.get('permission_info')
        if permission_dict:
            self.p2a_dict = permission_dict['p2a_dict']
        else:
            user_id = self.request.session['user_info']['nid']
            self.roles = models.Role.objects.filter(user2role__u_id=user_id)
            p2a_list = models.Permission2Action.objects.filter(permission2action2role__r__in=self.roles).\
                values('p__url', 'a__method').distinct()
            p2a_dict ={}
            for x in p2a_list:
                if x['p__url'] in p2a_dict:
                    p2a_dict[x['p__url']].append(x['a__method'])
                else:
                    p2a_dict[x['p__url']] = [x['a__method'],]

            data = {

                'p2a_dict': p2a_dict,
                'menus': self.menus()
            }

            self.request.session['permission_info'] = data

    def menus(self):
        permited_menu_list = models.Permission2Action.objects.filter(permission2action2role__r__in=self.roles). \
            values('p__menu', 'p__url').distinct()
        menu_list = models.Menu.objects.values('id', 'caption', 'parent_id')
        permited_menu_dict = {}
        menu_dict =  {}
        parents = {}
        for x in permited_menu_list:
            permited_menu_dict[x['p__menu']] = x['p__url']
        for x in menu_list:
            x = {
                'id': x['id'],
                'caption': x['caption'],
                'url': permited_menu_dict.get(x['id'], "javaScript:void(0);"),
                'child': [],
                'parent_id': x['parent_id'],

            }
            # let id be the key of new dict
            parents[x['id']] = x
            # let parent id be the key of new dict
            if x['parent_id']:
                if x['parent_id'] in menu_dict:
                    menu_dict[x['parent_id']].append(x)
                else:
                    menu_dict[x['parent_id']] = [x, ]

        # get menu tree
        for k, v in menu_dict.items():
            parents[k]['child'].extend(v)

        # loop to menu tree  and get menu with no parent_id
        menu_stem = []
        for x in parents.values():
            if x['parent_id'] is None:
                menu_stem.append(x)

        return self.menu_tree(menu_stem)


    def verify(self):
        method = []
        print(self.current_path)
        for k, v in self.p2a_dict.items():
            if re.match(k, self.current_path):
                print(k, self.current_path)
                method = v
                break
        return method

    def menu_tree(self, menu_stem, depth=1):
        """
        get the dict menu_stem, loop through get all the menu attached to parent and return html menu
        :param menu_stem:
        :param depth:
        :return:
        """
        self.add_menu(menu_stem, depth)
        print(self.menu_strings)
        return self.menu_strings

    def add_menu(self, menu_stem, depth):
        """
        recursive function, loop through the menu stem
        :param menu_stem:
        :param depth:
        :return:
        """
        for x in menu_stem:
            if not x['child'] and x['parent_id'] is not None and x['url'] == "javaScript:void(0);":
                pass
            else:
                html_start = '<ul><li><a class="nav-item depth-%s" href="%s"><span>%s</span></a>'

                if depth==1:
                    html_start = '<ul><li><a class="nav-item depth-%s" href="%s"><i class="fa fa-cogs" aria-hidden="true"></i><span>%s</span></a>'
                self.menu_strings += html_start % (depth, x['url'], x['caption'])
                print(x)

                if x['child']:
                    self.add_menu(x['child'], depth + 1)
                html_end = '</li></ul>'
                self.menu_strings += html_end



def permission(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/account/login.html')
        perm = PermissionHandler(request)
        method = perm.verify()
        if not method:
            return HttpResponse('Not Authorized to access')
        kwargs['method'] = method
        return func(request, *args, **kwargs)
    return inner

