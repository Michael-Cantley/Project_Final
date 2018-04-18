import unittest
from proj_fin import *

class TestRegionSearch(unittest.TestCase):

    def test_region_search(self):
        results = process_command('regions sources bars_sold top=5')
        self.assertEqual(results[0][0], 'Americas')
        self.assertEqual(results[3][1], 66)
        self.assertEqual(len(results), 4)

        results = process_command('regions sellers ratings top=10')
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0][0], 'Oceania')
        self.assertGreater(results[3][1], 3.0)

if __name__ == '__main__':
    unittest.main()
