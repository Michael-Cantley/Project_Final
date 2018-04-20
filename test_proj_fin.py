import unittest
from proj_fin import *


class TestDataAccess(unittest.TestCase):

    def test_cache_grab(self):
        try:
            db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        except:
            self.fail()


# class TestDataStorage(unittest.TestCase):
#
#     def test_show_state_map(self):
#         try:
#             plot_sites_for_state('mi')
#             plot_sites_for_state('az')
#         except:
#             self.fail()
#
#
# class TestDataProcessing(unittest.TestCase):
#
#     def test_show_state_map(self):
#         try:
#             plot_sites_for_state('mi')
#             plot_sites_for_state('az')
#         except:
#             self.fail()

if __name__ == '__main__':
    unittest.main()
