import json
import operator

from functools import reduce

from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from kodo_app.mock_data import mock_data
from kodo_app.models import MockData


PAGE_SIZE = 10

# Create your views here.
@require_http_methods(['POST'])
def load_data(request: HttpRequest) -> JsonResponse:
    mock_data_to_insert = []

    for data in mock_data:
        new_data = MockData(
            name=data['name'],
            image=data['image'],
            description=data['description'],
            date_last_edited=data['date_last_edited']
        )
        mock_data_to_insert.append(new_data)
    
    MockData.objects.bulk_create(mock_data_to_insert)

    return JsonResponse({'message': 'data successfully inserted'})


# Note: Not a clean and ideal code but it fulfils the requirements mentioned in the task
@require_http_methods(['GET'])
def search_data(request: HttpRequest) -> JsonResponse:
    query_params = dict(request.GET.items())
    if 'order' in query_params:
        order = query_params.pop('order')
        order = order.split(',')
        mock_data_response = MockData.objects.all().order_by(*order)
    elif 'name' in query_params:
        query_value = query_params['name']
        if query_value.startswith('\"') and query_value.endswith('\"'):
            query_value = query_value[1:-1]
            mock_data_response = MockData.objects.filter(
                name__icontains=query_value
            )
        else:
            query_string_list = query_value.split()
            mock_data_response = MockData.objects.filter(
                reduce(
                    operator.or_,
                    (Q(name__icontains=query) for query in query_string_list)
                )
            )
    elif 'description' in query_params:
        query_value = query_params['description']
        if query_value.startswith('\"') and query_value.endswith('\"'):
            query_value = query_value[1:-1]
            mock_data_response = MockData.objects.filter(
                description__icontains=query_value
            )
        else:
            query_string_list = query_value.split()
            mock_data_response = MockData.objects.filter(
                reduce(
                    operator.or_,
                    (Q(description__icontains=query) for query in query_string_list)
                )
            )
    else:
        mock_data_response = MockData.objects.all()

    page_number = query_params.get('page_number', 1)
    paginated_response = Paginator(mock_data_response, PAGE_SIZE).get_page(page_number)

    serialized_data = json.loads(serializers.serialize('json', paginated_response))
    mock_datas = [data['fields'] for data in serialized_data]
    response = {
        'count': mock_data_response.count(),
        'page_size': PAGE_SIZE,
        'current_page': page_number,
        'data': mock_datas
    }

    if paginated_response.has_next():
        response['next_page'] = paginated_response.next_page_number()

    return JsonResponse(response, safe=False)
