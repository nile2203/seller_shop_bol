from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class BolooPaginator:
    def __init__(self, data, page_size):
        self.paginator = Paginator(object_list=data, per_page=page_size)

    def get_total_number_of_pages(self):
        return self.paginator.num_pages

    def get_page(self, page_number):
        try:
            records = self.paginator.page(page_number)
        except PageNotAnInteger:
            records = self.paginator.page(1)
        except EmptyPage:
            return 0, 'No records found', None

        return 1, '', records.object_list
