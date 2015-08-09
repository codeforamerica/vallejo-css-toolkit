from django.test import TestCase

from geo.models import Address
from geo.utils.geocode import geocode

class GeocodeTestCase(TestCase):
    def setUp(self):
        Address.objects.create(street_number=555, street_name="santa clara", street_descriptor="st", lat=38.0, lng=-121.0)
        Address.objects.create(street_number=100, street_name="b", street_descriptor="st", lat=39.0, lng=-121.0)
        Address.objects.create(street_number=200, street_name="b", street_descriptor="st", lat=39.0, lng=-122.0)

    def test_geocode_exact(self):
        """Test a simple geocode lookup for an exact match"""

        results = geocode(555, "Santa Clara", "St")
        expected_results = [{'lat': 38.0, 'lng': -121.0}]

        self.assertEqual(results, expected_results)

    def test_geocode_exact_2(self):
        """Test a simple geocode lookup for an exact match"""

        results = geocode(555, "Santa Clara", "St.")
        expected_results = [{'lat': 38.0, 'lng': -121.0}]

        self.assertEqual(results, expected_results)

    def test_geocode_interpolate(self):
        """Test geocode interpolation"""

        results = geocode(160, "B", "St.")
        expected_results = [{'lat': 39.0, 'lng': -121.6}]

        self.assertEqual(results, expected_results)

    def test_geocode_interpolate_wrong_side(self):
        """Test that interpolation fails on wrong side of street"""

        results = geocode(125, "B", "St.")

        self.assertEqual(results, None)

    def test_geocode_wrong_side_but_nearby(self):
        """Test that we return nearest known coords when close enough"""

        results = geocode(103, "B", "St.")
        expected_results = [{'lat': 39.0, 'lng': -121.0}]

        self.assertEqual(results, expected_results)
