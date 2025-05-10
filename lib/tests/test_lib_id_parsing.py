import unittest

from sod import LibId


class TestLibIdParsing(unittest.TestCase):
    def test_parse_barcode(self):
        self.assertEqual(LibId.from_value("2610551205"), LibId.Barcode)
