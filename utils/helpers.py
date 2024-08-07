import math
import operator
import uuid
import os, string, random, json
from django.db.models import Q
from functools import reduce
from django.utils.timezone import now


TYPE_COLOR = {
    'poison': '#bb88b4',
    'grass': '#a8f084',
    'bug': '#a8f084',
    'flying': '#f5db6a',
    'fire': '#ff994d',
    'water': '#97afff',
    'fighting': '#df7563',
    'fairy': '#e395af',
    'electric': '#e7d31b',
    'steel': '#b4aac3',
    'ice': '#85ddff'
}

def id_generator(size=25, chars=string.ascii_lowercase + string.digits):
    """
    Generate random string
    """
    return ''.join(random.choice(chars) for _ in range(size))


def is_numeric(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def search_result(queryset, search, orm_lookups):
    """ 
    Filters a queryset based on a search string and ORM lookup fields.

    This function takes a Django queryset, a search string, and a list of ORM lookup fields,
    then filters the queryset to include only the objects where at least one of the lookup fields 
    matches any word in the search string. It splits the search string into individual words 
    and creates OR queries for each word against each lookup field.

    Args:
        queryset (QuerySet): The initial queryset to filter.
        search (str): The search string to filter the queryset by. It can contain multiple words.
        orm_lookups (list of str): A list of ORM lookup fields (e.g., 'name__icontains') to search against.

    Returns:
        QuerySet: The filtered queryset with objects that match the search criteria.
    """
    for bit in search.split():
        or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries))

    return queryset


def format_listing_data(serializer, queryset, pagination_result):
    if pagination_result:
        return {
            'count': pagination_result['count'],
            'limit': pagination_result['limit'],
            'current_page': pagination_result['page'],
            'total_page': pagination_result['pages'],
            'data': serializer(queryset, many=True).data
        }
    return {
        'count': queryset.count(),
        'data': serializer(queryset, many=True).data
    }
  

def upload_avatar_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    path = instance._meta.model_name
    new_filename = '{}_{}{}'.format(
        uuid.uuid4(),
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower()
    )
    return '{}/{}'.format(path, new_filename)

 
def get_or_none(classmodel, **kwargs):
    try:
        obj = classmodel.objects.get(**kwargs)
        return obj
    except:
        return None
    

def decode_request_body(body):
    body_unicode = body.decode('utf-8')
    body = json.loads(body_unicode)
    return body


def format_page(page, limit, count, span=2): 
    page = int(page)
    limit = int(limit)
    span = int(span)

    offset = (page - 1) * limit 

    try:
        page_count = math.ceil(count / limit)
    except:
        page_count = 1

    has_next = page < page_count
    has_prev = page > 1

    record_from = offset + 1
    record_to = offset + limit if offset + limit <= count else count
    max_range = page + span if page + span <= page_count else page_count
    min_range = page - span if page - span >= 1 else 1

    pages = range(min_range, max_range + 1)
    return {
            "limit": limit,
            "record_count": count,
            "page_count": page_count,
            "record_from": record_from,
            "record_to": record_to,
            "pages": list(pages),
            "page": page,
            "has_next": has_next,
            "has_prev": has_prev,  
            'prev': (int(record_from) - 1) if has_prev else None,
            'next': record_to if has_next else None 
        }


class Paginator:
    """
    A simple paginator class to handle pagination of querysets.

    This class provides functionality to paginate a given queryset, allowing you to specify the page number,
    the number of items per page, and an optional span for the range of pages to display.

    Attributes:
        queryset (list): The list of items to paginate.
        page_ranged (bool): Flag to indicate whether to display a range of pages around the current page.

    Methods:
        paginate(page=1, limit=10, span=2): Paginates the queryset and returns pagination details.
    """
     
    def __init__(self, queryset, page_ranged=True):
        self.queryset = queryset
        self.page_ranged = page_ranged

    def paginate(self, page=1, limit=10, span=2):
        """
        Paginates the queryset and returns pagination details.

        Args:
            page (int): The current page number. Default is 1.
            limit (int): The number of items per page. Default is 10.
            span (int): The number of pages to display around the current page if page_ranged is True. Default is 2.

        Returns:
            dict: A dictionary containing pagination details, including:
                - limit (int): The number of items per page.
                - record_count (int): The total number of items in the queryset.
                - page_count (int): The total number of pages.
                - record_from (int): The starting index of the records on the current page.
                - record_to (int): The ending index of the records on the current page.
                - pages (list): The list of page numbers to display.
                - page (int): The current page number.
                - has_next (bool): Whether there is a next page.
                - has_prev (bool): Whether there is a previous page.
                - data (list): The list of items on the current page.
                - showing_text (str): A string indicating the range of pages being shown.
        """
        page = int(page)
        limit = int(limit)
        span = int(span)

        offset = (page - 1) * limit

        count = len(self.queryset)

        try:
            page_count = math.ceil(count / limit)
        except:
            page_count = 1

        has_next = page < page_count
        has_prev = page > 1

        record_from = offset + 1
        record_to = offset + limit if offset + limit <= count else count

        if self.page_ranged:
            max_range = page + span if page + span <= page_count else page_count
            min_range = page - span if page - span >= 1 else 1

            pages = range(min_range, max_range + 1)

        else:
            pages = range(1, page_count + 1)

        return {
            "limit": limit,
            "record_count": count,
            "page_count": page_count,
            "record_from": record_from,
            "record_to": record_to,
            "pages": list(pages),
            "page": page,
            "has_next": has_next,
            "has_prev": has_prev,
            "data": self.queryset[offset:offset + limit], 
            "showing_text": f"Page {page} to {list(pages)[-1]}" if count > 0 else f"Page 1 to 1"
        }