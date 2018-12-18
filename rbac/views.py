from django.shortcuts import render, HttpResponse
from . import models


class PermissionHandler:
    def init(self, request):
        self.request = request
        self.current_path = request.path_info
        self.session_data()

    def session_data(self):
        user_id = self.request.session.get('user_info')['nid']
        role = models.Role.objects.filter(user2role__u_id=user_id)
        permissions = models.Permission.objects.filter(permission2action__permission2action2role__r__in=role).distinct()
        permited_menu_list = models.Menu.objects.filter(permission__in=permissions).values('id', 'caption', 'parent_id',
                                                                                 'permission__url')
        menu_list = models.Menu.objects.values('id', 'caption', 'parent_id')
        permited_menu_dict = {}
        menu_dict = {}
        parents = {}

        for x in permited_menu_list:
            permited_menu_dict[x['id']] = x['permission__url']

        for x in menu_list:
            x = {
                'id': x['id'],
                'caption': x['caption'],
                'url': permited_menu_dict.get(x['id'], None),
                'child': [],
                'parent_id': x['parent_id'],

            }
            # let id be the key of new dict
            parents[x['id']] = x

            # let parent id be the key of new dict
            # e.g {3:[{'id':1, 'caption':menu, 'parent_id'}, {example}], 4:[{'id':1, 'caption':menu, 'parent_id'}, {example}]}

            if x['parent_id']:
                if x['parent_id'] in menu_dict:
                    menu_dict[x['parent_id']].append(x)
                else:
                    menu_dict[x['parent_id']] = [x, ]

        # loop throgh menu dict(menu_list) add child
        for k, v in menu_dict.items():
            parents[k]['child'].extend(v)

        # loop to filter and get menu with no parent
        menu_stem = []
        for x in parents.values():
            if x['parent_id'] is None:
                menu_stem.append(x)

        menu_final = self.collect_menu(menu_stem)

        permission_info = {
            'menus': menu_final
        }

        self.request.session['menu_list'] = permission_info

    def collect_menu(self, menu_stem, depth=1):
        menu_strings = []
        def menu_string(menu_stem, depth):
            for x in menu_stem:
                menu_strings.append(self.menu_html(x, depth))
                menu_string(x['child'], depth+1)
        menu_string(menu_stem, depth)
        return ''.join(menu_strings)

    @staticmethod
    def menu_html(menu, depth):
        """
        create menu html
        :param menu:
        :param depth:
        :return:
        """

        if depth == 1:
            if menu['url'] is not None:
                html_string = '''
                    <a class="nav-item" href="%s">
                        <i class="fa fa-cogs" aria-hidden="true"></i>
                        <span>%s</span>
                    </a>
                ''' % (menu['url'], menu['caption'])
            else:
                html_string = '''
                    <a class="nav-item">
                        <i class="fa fa-cogs" aria-hidden="true"></i>
                        <span>%s</span>
                    </a>
                ''' % (menu['caption'])
        elif menu['child'] == [] and menu['parent_id'] is not None and menu['url'] == None:
            html_string = ""
        else:
            if menu['url'] is not None:
                html_string = '''<a class="nav-item" style="padding-left:%spx" href="%s"><span>%s</span></a>        
                ''' % (depth*15, menu['url'], menu['caption'])
            else:
                html_string = '''<a class="nav-item" style="padding-left:%spx" ><span>%s</span></a>        
                ''' % (depth*15,  menu['caption'])
        return html_string

