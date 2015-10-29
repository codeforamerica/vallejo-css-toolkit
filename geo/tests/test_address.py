import unittest

from django.test import TestCase

from geo.utils.normalize_address import normalize_descriptor, normalize_name, normalize_address_string

# TODO: deprecate this module


class AddressTestCase(TestCase):

    @unittest.skip("Pending refactor of geocoding processes")
    def test_normalize_desc_basic(self):

        results = normalize_descriptor("St")
        self.assertEqual(results, "st")

    @unittest.skip("Pending refactor of geocoding processes")
    def test_normalize_name_sub(self):

        results = normalize_name("Alemeda")
        self.assertEqual(results, "alameda")

    @unittest.skip("Pending refactor of geocoding processes")
    def test_normalize_address_string_basic(self):

        results = normalize_address_string("555 Santa Clara St.")
        self.assertEqual(results, (555, "santa clara", "st"))

    @unittest.skip("Pending refactor of geocoding processes")
    def test_normalize_address_string_whitespace(self):

        results = normalize_address_string("100  Broadway ")
        self.assertEqual(results, (100, "broadway", None))
