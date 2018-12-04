from django.utils.safestring import mark_safe


class Pagination(object):

    '''
    :param total_count, total size of data
    :param current_page, current page
    :param item_no, number of each page
    :param max_page, maximum page displayed to user
    :param url relative url of the page
    '''

    def __init__(self, total_count, url="", item_no=20, max_page=7, current_page=1):
        self.total_count = total_count
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.item_no = item_no
        self.totalCount = total_count
        self.max_page = max_page
        self.url= url

    @property
    def start(self):
        return (self.current_page-1)*self.item_no

    @property
    def end(self):
        return self.current_page*self.item_no

    @property
    def total_page(self):
        a, b = divmod(self.total_count, self.item_no)
        if b:
            a+=1
        return a

    def page_list(self):
        start_rng = 1
        end_rng = 1

        # if total page less than max pages, e.g only have 1 page
        if self.total_page < self.max_page:
            end_rng = self.total_page

        else:
            # display all page no. if current page < e.g.7
            if self.current_page < int(self.max_page/2):
                end_rng = self.max_page
            # compare with 7(max page no.), if current page > 3, like 4, display 1-7
            if self.current_page >= int(self.max_page/2):
                start_rng = self.current_page-int(self.max_page/2)
                if start_rng == 0:
                    start_rng = 1
                end_rng = self.current_page+int(self.max_page/2)
                if end_rng > self.total_page:
                    end_rng = self.total_page
        return list(range(start_rng, end_rng+1))

    def pages(self):
        page_list = []
        if self.current_page == 1:
            prev = "<ul class='pagination'><li class='page-item'><a class='page-link' href ='javascript:void(0)'>Previous</a></li>"
        else:
            prev = "<ul class='pagination'><li class='page-item'><a class='page-link' href ='%s?p=%s'>Prev</a></li>"%(self.url, self.current_page-1)
        page_list.append(prev)
        for i in self.page_list():
            if self.current_page == i:
                page = "<li class='page-item  active'><a class='page-link' href='%s?p=%s'>%s</a></li>" % (self.url, i, i)
            else:
                page = "<li class='page-item'><a class='page-link' href ='%s?p=%s'>%s</a></li>" % (self.url, i, i)
            page_list.append(page)

        if self.current_page == self.total_page:
            last = "<li class='page-item'><a class='page-link' href='javascript:void(0)'>Last Page</a></li> </ul>"
        else:
            last = "<li class='page-item'><a class='page-link' href ='%s?p=%s'>Next</a></li></ul>"%(self.url, self.current_page+1)
        page_list.append(last)
        if self.max_page <= 1:
            return ""
        return mark_safe(' '.join(page_list))







