import unittest
from proj_fin import *

class TestMapping(unittest.TestCase):

    # we can't test to see if the maps are correct, but we can test that
    # the functions don't return an error!
    def test_show_state_map(self):
        try:
            plot_sites_for_state('mi')
            plot_sites_for_state('az')
        except:
            self.fail()

if __name__ == '__main__':
    unittest.main()
