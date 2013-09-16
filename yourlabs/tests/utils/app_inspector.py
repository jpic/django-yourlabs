import imp
import os.path
import unittest

from yourlabs.utils.app_inspector import AppInspector


class AppInspectorTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.fixtures_dir = os.path.realpath(os.path.join(
                os.path.dirname(__file__), 'app_inspector_tests'))

    def test_appinspector(self):
        fixture_path = os.path.join(self.fixtures_dir, 'your_app')
        expected_path = os.path.join(fixture_path, 'expected.py')
        expected = imp.load_source('expected', expected_path).expected
        result = AppInspector(path=fixture_path)

        self.assertEquals(expected['name'], result.name)
        self.assertDictEqual(expected['dir'], result.dir)
        self.assertDictEqual(expected['views'], result.views)
