from django.test import TestCase

from geo.models import LocationPosition
from geo.utils.geocode import geocode

class GeocodeTestCase(TestCase):
    def setUp(self):
        LocationPosition.objects.create(address_number=555, street_name="SANTA CLARA", lat=38.0, lng=-121.0)
        LocationPosition.objects.create(address_number=100, street_name="B", lat=39.0, lng=-121.0)
        LocationPosition.objects.create(address_number=200, street_name="B", lat=39.0, lng=-122.0)

    def test_geocode_exact(self):
        """Test a simple geocode lookup for an exact match"""

        results = geocode(555, "SANTA CLARA")
        expected_results = {'lat': 38.0, 'lng': -121.0}

        self.assertEqual(results, expected_results)

    def test_geocode_interpolate(self):
        """Test geocode interpolation"""

        results = geocode(160, "B")
        expected_results = {'lat': 39.0, 'lng': -121.6}

        self.assertEqual(results, expected_results)

    def test_geocode_interpolate_wrong_side(self):
        """Test that interpolation fails on wrong side of street"""

        results = geocode(125, "B")

        self.assertEqual(results, None)

    def test_geocode_wrong_side_but_nearby(self):
        """Test that we return nearest known coords when close enough"""

        results = geocode(103, "B")
        expected_results = {'lat': 39.0, 'lng': -121.0}

        self.assertEqual(results, expected_results)
