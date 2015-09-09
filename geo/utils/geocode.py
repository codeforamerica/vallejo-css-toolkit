from psycopg2.extensions import AsIs

from django.db import connection

from common.utils import dictfetchall

NEARBY_THRESHOLD = 10  # how many street numbers away is 'close enough'


# TODO: need to implement elastic search

def geocode_try_nearby(address_number, street_name):

    if not address_number or not street_name:
        return

    query = """
        SELECT lat, lng
            FROM geo_locationposition
        WHERE
            street_name = %s
            AND abs(address_number - %s) < %s
        ORDER BY
            abs(address_number - %s)
        limit 1
        """
    params = [street_name, address_number, NEARBY_THRESHOLD, address_number]
    cursor = connection.cursor()
    cursor.execute(query, params)
    results = dictfetchall(cursor)

    if results:
        return {'lat': results[0]['lat'], 'lng': results[0]['lng']}

def geocode_try_interpolate(address_number, street_name):

    if not address_number or not street_name:
        return

    modulo = address_number % 2

    query = """
        SELECT lat, lng, address_number
            FROM geo_locationposition
        WHERE
            street_name = %s
            AND address_number %s %s
            AND address_number %% 2 = %s
        ORDER BY
            address_number %s
        LIMIT 1
        """
    params = [street_name]
    cursor = connection.cursor()
    cursor.execute(query, params + [AsIs('>'), address_number, modulo, AsIs('asc')])
    results = dictfetchall(cursor)

    if results:
        first_higher = results[0]
    else:
        first_higher = None

    cursor = connection.cursor()
    cursor.execute(query, params + [AsIs('<'), address_number, modulo, AsIs('desc')])
    results = dictfetchall(cursor)

    if results:
        first_lower = results[0]
    else:
        first_lower = None

    if first_higher and first_lower:
        intersect = float(address_number - first_lower['address_number']) / (first_higher['address_number'] - first_lower['address_number'])

        interp_lat = (first_higher['lat'] - first_lower['lat']) * intersect + first_lower['lat']
        interp_lng = (first_higher['lng'] - first_lower['lng']) * intersect + first_lower['lng']

        return {'lat': interp_lat, 'lng': interp_lng}

def geocode_try_exact(address_number, street_name):

    query = """
        SELECT lat, lng
            FROM geo_locationposition
        WHERE
            street_name = %s
            AND address_number = %s
        """
    params = [street_name, address_number]
    cursor = connection.cursor()
    cursor.execute(query, params)

    results = dictfetchall(cursor)
    if results:
        return {'lat': results[0]['lat'], 'lng': results[0]['lng']}

def geocode(address_number, street_name, try_interpolate=True, try_nearby=True):
    results = geocode_try_exact(address_number, street_name)

    if not results and try_interpolate:
        results = geocode_try_interpolate(address_number, street_name)

        if not results and try_nearby:
            results = geocode_try_nearby(address_number, street_name)

    return results        
