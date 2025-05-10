import unittest

from sod import DEFAULT_SOD_REGISTRY_CONFIG, LibId, SodRegistry
from sod.custom_types.registry_type import SodSource


class TestKrameriusRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = SodRegistry(DEFAULT_SOD_REGISTRY_CONFIG)

    def test_find_by_one_identifier(self):
        barcode = "2610469737"
        result = self.registry.resolve([(LibId.Barcode, barcode)])

        self.assertIsNotNone(result)
        self.assertEqual(result[0][0], 0.5)
        self.assertEqual(result[0][1].document.barcode, barcode)

    def test_find_by_multiple_identifiers(self):
        barcode = "2610469737"
        issn = "1211-3077"
        result = self.registry.resolve(
            [(LibId.Barcode, barcode), (LibId.Issn, issn)]
        )
        for relevance, document in result:
            print(f"Relevance: {relevance}\nDocument: {document}")

        self.assertIsNotNone(result)
        for relevance, _ in result[:10]:
            self.assertAlmostEqual(relevance, 0.052, 3)
        self.assertEqual(sum(r[0] for r in result), 1.0)
        self.assertEqual(result[0][1].source, SodSource.Kramerius)
        self.assertEqual(result[0][1].document.barcode[0], barcode)
