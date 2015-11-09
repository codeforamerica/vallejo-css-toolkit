from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from workflow.utils import get_properties


@login_required(login_url='/login/')
def property(request):

    return render(request, 'workflow/property.html')


@login_required(login_url='/login/')
def properties(request):

        properties_data, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset = get_properties(request.GET)

        # properties_data = []
        return render(
            request,
            'workflow/properties.html',
            {
                'properties_data': properties_data,
                'pagination_keys': pagination_keys,
                'active_page_number': page_idx and page_idx + 1 or 1,
                'sort_order': sort_order,
                'sort_key': sort_key,
                'limit': limit,
                'offset': offset,
                'page_start': offset + 1,
                'page_end': min(limit + offset, properties_data and properties_data[0][5] or limit + offset),
                'search_get_param': search_get_param
            }
        )
