import unittest

from sod import (
    DEFAULT_RDCZ_REGISTRY_CONFIG,
    LibId,
    RDczRegistry,
    RelevanceNormalization,
)


class TestRDczRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = RDczRegistry(DEFAULT_RDCZ_REGISTRY_CONFIG)
        self.norm = RelevanceNormalization.Softmax

    def test_parse_barcode(self):
        self.assertEqual(LibId.from_value("2610551205"), LibId.Barcode)

    def test_find_by_one_identifier(self):
        barcode = "2610551205"
        result = self.registry.find_by_identifiers(
            [(LibId.Barcode, barcode)], self.norm
        )
        self.assertIsNotNone(result)
        self.assertEqual(result[0][0], 1.0)
        self.assertEqual(result[0][1].barcode, barcode)

    def test_find_by_multiple_identifiers(self):
        barcode = "2610551205"
        issn = "1801-089X"
        result = self.registry.find_by_identifiers(
            [(LibId.Barcode, barcode), (LibId.Issn, issn)], self.norm
        )
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[0][0], 0.129, 3)
        for relevance, _ in result[1:]:
            self.assertAlmostEqual(relevance, 0.097, 3)
        self.assertEqual(sum(r[0] for r in result), 1.0)
        self.assertEqual(result[0][1].barcode, barcode)
