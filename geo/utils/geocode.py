from psycopg2.extensions import AsIs

from django.db import connection

from common.utils import dictfetchall

NEARBY_THRESHOLD = 10  # how many street numbers away is 'close enough'

VERSION = 0.1


def geocode_try_nearby(street_number, street_name, street_descriptor=None):

    if not street_number or not street_name:
        return

    query = """
        SELECT lat, lng
            FROM geo_locationposition
        WHERE
            street_name = %s
            AND abs(street_number - %s) < %s
        ORDER BY
            abs(street_number - %s)
        limit 1
        """
    params = [street_name, street_number, NEARBY_THRESHOLD, street_number]

    # only supporting this case for now...
    if not street_descriptor:
        pass

    cursor = connection.cursor()
    cursor.execute(query, params)
    results = dictfetchall(cursor)

    if results:
        return {'version': VERSION, 'lat': results[0]['lat'], 'lng': results[0]['lng']}

def geocode_try_interpolate(street_number, street_name, street_descriptor=None):

    if not street_number or not street_name:
        return

    modulo = street_number % 2

    query = """
        SELECT lat, lng, street_number
            FROM geo_locationposition
        WHERE
            street_name = %s
            AND street_number %s %s
            AND street_number %% 2 = %s
        ORDER BY
            street_number %s
        LIMIT 1
        """
    params = [street_name]

    # only supporting this case for now...
    if not street_descriptor:
        pass

    cursor = connection.cursor()
    cursor.execute(query, params + [AsIs('>'), street_number, modulo, AsIs('asc')])
    results = dictfetchall(cursor)

    if results:
        first_higher = results[0]
    else:
        first_higher = None

    cursor = connection.cursor()
    cursor.execute(query, params + [AsIs('<'), street_number, modulo, AsIs('desc')])
    results = dictfetchall(cursor)

    if results:
        first_lower = results[0]
    else:
        first_lower = None

    if first_higher and first_lower:
        intersect = float(street_number - first_lower['street_number']) / (first_higher['street_number'] - first_lower['street_number'])

        interp_lat = (first_higher['lat'] - first_lower['lat']) * intersect + first_lower['lat']
        interp_lng = (first_higher['lng'] - first_lower['lng']) * intersect + first_lower['lng']

        return {'version': VERSION, 'lat': interp_lat, 'lng': interp_lng}

def geocode_try_exact(street_number, street_name, street_descriptor=None):

    query = """
        SELECT lat, lng
            FROM geo_locationposition
        WHERE
            street_name = %s
            AND street_number = %s
        """
    params = [street_name, street_number]

    if street_descriptor:

        query = "%s %s" % (query, """AND lower(street_descriptor) = %s""")
        params += [street_descriptor]

    cursor = connection.cursor()
    cursor.execute(query, params)

    results = dictfetchall(cursor)
    if results:
        return {'version': VERSION, 'lat': results[0]['lat'], 'lng': results[0]['lng']}

def geocode(street_number, street_name, street_descriptor=None, try_interpolate=True, try_nearby=True):
    results =  geocode_try_exact(street_number, street_name, street_descriptor=None)

    if not results and try_interpolate:
        results = geocode_try_interpolate(street_number, street_name, street_descriptor=None) \

        if not results and try_nearby:
            results = geocode_try_nearby(street_number, street_name, street_descriptor=None)

    return results        
