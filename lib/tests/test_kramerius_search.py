import unittest

from sod import (
    DEFAULT_KRAMERIUS_REGISTRY_CONFIG,
    KrameriusRegistry,
    LibId,
    RelevanceNormalization,
    RelevanceNormalizationConfig,
)


class TestKrameriusRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = KrameriusRegistry(
            DEFAULT_KRAMERIUS_REGISTRY_CONFIG,
            RelevanceNormalizationConfig(
                normalization=RelevanceNormalization.Softmax,
                softmax_temperature=1.0,
            ),
        )

    def test_find_by_one_identifier(self):
        barcode = "2610469737"
        result = self.registry.resolve([(LibId.Barcode, barcode)])

        self.assertIsNotNone(result)
        self.assertEqual(result[0][0], 1.0)
        self.assertEqual(result[0][1].barcode[0], barcode)

    def test_find_by_multiple_identifiers(self):
        barcode = "2610469737"
        issn = "1211-3077"
        result = self.registry.resolve(
            [(LibId.Barcode, barcode), (LibId.Issn, issn)]
        )

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[0][0], 0.576, 3)
        for relevance, _ in result[1:]:
            self.assertAlmostEqual(relevance, 0.212, 3)
        self.assertEqual(sum(r[0] for r in result), 1.0)
        self.assertEqual(result[0][1].barcode[0], barcode)
