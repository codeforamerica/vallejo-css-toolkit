import re

# TODO: deprecate this module

DESC_REPLACEMENT_MAP = {
    'st': ['street', 'st', 'st.', 'str'],
    'ct': ['ct', 'court', 'ct.'],

}

# resolve some typos seen in city data...
NAME_REPLACEMENT_MAP = [
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

STREET_DESCRIPTOR_RE = "(Wy|Ct|Cir|Rd|St|Dr|Av|Bl|Rl|Ln|Cv|Pl|Ter|Pkwy|Drive East|Drive West|Road E|Avenue E|Road W)"


def normalize_descriptor(street_descriptor_raw):
    street_descriptor_raw = street_descriptor_raw.lower()
    for replacement, originals in DESC_REPLACEMENT_MAP.iteritems():
        for original in originals:
            street_descriptor_raw = re.sub(original, replacement, street_descriptor_raw)

    return street_descriptor_raw.strip()


def normalize_name(street_name):
    for original, replacement in NAME_REPLACEMENT_MAP:
        street_name = re.sub(original, replacement, street_name)

    return street_name.lower().strip()


def normalize_address_by_number_and_street(street_number, street_name):
    if type(street_number) == str:
        if not street_number.isdigit():
            return
    elif not type(street_number) == int:
        return

    street_name = street_name.strip()
    r = re.match('(?P<street_name>.*) (?P<street_descriptor>%s)\.?' % STREET_DESCRIPTOR_RE, street_name, re.IGNORECASE)

    if r:
        street_descriptor_raw = r.groupdict()['street_descriptor']
        street_descriptor = normalize_descriptor(street_descriptor_raw)
        street_name = r.groupdict()['street_name']
    else:
        street_descriptor = None

    street_name = normalize_name(street_name)

    return street_number, street_name, street_descriptor


def normalize_address_string(address):
    address = address.strip()
    r = re.match('(?P<street_number>\d*) (?P<street_name>.*)', address)

    if r:
        street_number = int(r.groupdict()['street_number'])
        street_name = r.groupdict()['street_name']

        return normalize_address_by_number_and_street(street_number, street_name)


def combine_address_parts(street_number, street_name, street_descriptor=None):
    if street_descriptor:
        return '{} {} {}'.format(street_number, street_name, street_descriptor)

    return '{} {}'.format(street_number, street_name)
