import unittest

from sod import (
    DEFAULT_RDCZ_REGISTRY_CONFIG,
    LibId,
    RDczRegistry,
    RelevanceNormalization,
    RelevanceNormalizationConfig,
)


class TestRDczRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = RDczRegistry(
            DEFAULT_RDCZ_REGISTRY_CONFIG,
            RelevanceNormalizationConfig(
                normalization=RelevanceNormalization.Softmax,
                softmax_temperature=1.0,
            ),
        )

    def test_parse_barcode(self):
        self.assertEqual(LibId.from_value("2610551205"), LibId.Barcode)

    def test_find_by_one_identifier(self):
        barcode = "2610551205"
        result = self.registry.resolve([(LibId.Barcode, barcode)])

        self.assertIsNotNone(result)
        self.assertEqual(result[0][0], 1.0)
        self.assertEqual(result[0][1].barcode, barcode)

    def test_find_by_multiple_identifiers(self):
        barcode = "2610551205"
        issn = "1801-089X"
        result = self.registry.resolve(
            [(LibId.Barcode, barcode), (LibId.Issn, issn)]
        )

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[0][0], 0.232, 3)
        for relevance, _ in result[1:]:
            self.assertAlmostEqual(relevance, 0.085, 3)
        self.assertEqual(sum(r[0] for r in result), 1.0)
        self.assertEqual(result[0][1].barcode, barcode)
