import re
import sys
import csv

from django.db import connection

from psycopg2.extensions import AsIs


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def geocode_try_nearby(street_number, street_name, street_descriptor=None):

    if not street_number or not street_name:
        return

    modulo = street_number % 2

    query = """
        select lat, lng, street_number
            from geo_address
        where
            lower(street_name) = lower(%s)
            and abs(street_number - %s) < 10
        order by
            abs(street_number - %s)
        limit 1;
        """
    params = [street_name, street_number, street_number]

    # only supporting this case for now...
    if not street_descriptor:
        pass

    cursor = connection.cursor()
    cursor.execute(query, params)
    results = dictfetchall(cursor)

    if results:
        return [{'lat': results[0]['lat'], 'lng': results[0]['lng']}]

def geocode_try_interpolate(street_number, street_name, street_descriptor=None):

    if not street_number or not street_name:
        return

    modulo = street_number % 2

    query = """
        select street_number, lat, lng
            from geo_address
        where
            lower(street_name) = lower(%s)
            and street_number %s %s
            and street_number %% 2 = %s
        order by
            street_number %s
        limit 2
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

        return [{'lat': interp_lat, 'lng': interp_lng}]

def geocode_try_exact(street_number, street_name, street_descriptor=None):

    query = """
        select lat, lng
            from geo_address
        where
            lower(street_name) = lower(%s)
            and street_number = %s
        """
    params = [street_name, street_number]

    if street_descriptor:

        query = "%s %s" % (query, """AND lower(street_descriptor) = %s""")
        params += [street_descriptor]

    cursor = connection.cursor()
    cursor.execute(query, params)

    results = dictfetchall(cursor)
    return results

def geocode(street_number, street_name, street_descriptor=None):

    removals = [
        'Ct',
        ' St',
        'Way',
        'Cir',
        'Place',
        'East',
        'Sr'
    ]

    replacements = [
        ['Pennsylvanis', 'Pennsylvania'],
        ['Sanat Clara', 'Santa Clara'],
        ['Redwod', 'Redwood'],
        ['Illinios', 'Illinois'],
        ['Carsen', 'Carson'],
        ['Alemeda', 'Alameda'],
        ['Lousiana', 'Louisiana'],
        ['Coughlin', 'Coughlan'],
        ['Broadway D', 'Broadway'],
        ['La Montanita', 'Lane Montanita'],
        ['McClane', 'Mc Lane'],
        ['Hazlewood', 'Hazelwood'],
        ['Bergawall', 'Bergwall'],
        ['McDougal', 'Mc Dougal'],
        ['Elliot', 'Elliott']
    ]

    # TODO: need to use regex replace and remove instead

    street_name = street_name.strip()

    for x in removals:
        street_name = street_name.replace(x, '')
        street_name = street_name.replace(x.lower(), '')

    for x, y in replacements:
        street_name = street_name.replace(x, y)

    street_name = street_name.strip()

    return geocode_try_exact(street_number, street_name, street_descriptor=None) \
        or geocode_try_interpolate(street_number, street_name, street_descriptor=None) \
        or geocode_try_nearby(street_number, street_name, street_descriptor=None)
