from django.test import TestCase

from geo.models import LocationPosition
from geo.utils.geocode import geocode, VERSION
from workflow.models import CaseLocation

class GeocodeTestCase(TestCase):
    def setUp(self):

        LocationPosition.objects.create(street_number=555, street_name="santa clara", street_descriptor="st", lat=38.0, lng=-121.0)
        LocationPosition.objects.create(street_number=100, street_name="b", street_descriptor="st", lat=39.0, lng=-121.0)
        LocationPosition.objects.create(street_number=200, street_name="b", street_descriptor="st", lat=39.0, lng=-122.0)

    def test_geocode_class_method(self):
        """Test a simple geocode lookup for an exact match"""

        case_location = CaseLocation.objects.create(street_number=555, street_name="santa clara", street_descriptor="st")
        results = case_location.geocode()
        expected_results = {'lat': 38.0, 'lng': -121.0, 'version': VERSION}

        self.assertEqual(results, expected_results)

    def test_geocode_exact(self):
        """Test a simple geocode lookup for an exact match"""

        results = geocode(555, "santa clara", "st")
        expected_results = {'lat': 38.0, 'lng': -121.0, 'version': VERSION}

        self.assertEqual(results, expected_results)

    def test_geocode_interpolate(self):
        """Test geocode interpolation"""

        results = geocode(160, "b", "st")
        expected_results = {'lat': 39.0, 'lng': -121.6, 'version': VERSION}

        self.assertEqual(results, expected_results)

    def test_geocode_interpolate_wrong_side(self):
        """Test that interpolation fails on wrong side of street"""

        results = geocode(125, "b", "st")

        self.assertEqual(results, None)

    def test_geocode_wrong_side_but_nearby(self):
        """Test that we return nearest known coords when close enough"""

        results = geocode(103, "b", "st")
        expected_results = {'lat': 39.0, 'lng': -121.0, 'version': VERSION}

        self.assertEqual(results, expected_results)
