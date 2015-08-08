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
        select lat, lng, street_number from geo_address
        where lower(street_name) = lower(%s)
        and abs(street_number - %s) < 10
        order by abs(street_number - %s)
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

    query = """select street_number, lat, lng from geo_address
    where lower(street_name) = lower(%s) and street_number %s %s and street_number %% 2 = %s
    order by street_number %s
    limit 2
    """
    params = [street_name]

    # only supporting this case for now...
    if not street_descriptor:
        pass

    cursor = connection.cursor()
    cursor.execute(query, params + [AsIs('>'), street_number, modulo, AsIs('asc')])
    # print cursor.mogrify(query, params + [AsIs('>'), AsIs('street_number'), AsIs('asc')])
    results = dictfetchall(cursor)

    if results:
        first_higher = results[0]
    else:
        first_higher = None

    cursor = connection.cursor()
    cursor.execute(query, params + [AsIs('<'), street_number, modulo, AsIs('desc')])
    # print cursor.mogrify(query, params + [AsIs('<'), AsIs('street_number'), AsIs('desc')])
    results = dictfetchall(cursor)

    if results:
        first_lower = results[0]
    else:
        first_lower = None

    # print first_higher, first_lower

    if first_higher and first_lower:
        intersect = float(street_number - first_lower['street_number']) / (first_higher['street_number'] - first_lower['street_number'])

        interp_lat = (first_higher['lat'] - first_lower['lat']) * intersect + first_lower['lat']
        interp_lng = (first_higher['lng'] - first_lower['lng']) * intersect + first_lower['lng']

        return [{'lat': interp_lat, 'lng': interp_lng}]

    else:
        return geocode_try_nearby(street_number, street_name, street_descriptor=None)

def geocode_try_exact(street_number, street_name, street_descriptor=None):


    base_query = """select lat, lng from geo_address
    where lower(street_name) = lower(%s) and street_number = %s
    """
    base_params = [street_name, street_number]

    if street_descriptor:

        query = base_query + """ AND lower(street_descriptor) = %s """
        params = base_params + [street_descriptor]

    else:
        query = base_query
        params = base_params

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

    maybe_match = geocode_try_exact(street_number, street_name, street_descriptor=None)

    if maybe_match:
        return maybe_match

    else:
        interpolate_match = geocode_try_interpolate(street_number, street_name, street_descriptor=None)

        if interpolate_match:
            return interpolate_match

        else:
            pass
            # print street_number, street_name, len(street_name)


def test_geocode(filepath=None):

    results = {
        'bad street num': 0,
        'bad row': 0,
        'exact hit': 0,
        'total': 0
    }

    with open(filepath, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
        f.seek(0)
        reader = csv.reader(f, dialect)

        next(reader)

        for i, row in enumerate(reader):
            street_number = row[1]
            street_name = row[2]
            results['total'] += 1

            if not street_number and street_name:
                # print 'bad row: ', row
                results['bad row'] += 1
                continue

            if not street_number.isdigit():
                # print 'bad street_number: ', street_number
                results['bad street num'] += 1
                continue

            street_number = int(street_number)
            x = geocode(street_number, street_name)  
            if x:
                results['exact hit'] += 1

            else:
                print street_number, street_name, len(street_name)

    print results

if __name__ == "__main__":

    func_name = sys.argv[1]

    if func_name == 'import_openaddresses':
        filepath = sys.argv[2]
        import_openaddresses(filepath)

    if func_name == 'test_geocode':
        filepath = sys.argv[2]
        test_geocode(filepath)
