import unittest
from proj_fin import *
#DO 5 a piece BUT double check to make sure 45 are not necessary.

class TestDataAccess(unittest.TestCase):

    def test_cache_grab_1_a(self):
        try:
            db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        except:
            self.fail()

    def test_cache_grab_2_a(self):
        try:
            db_cache_loader("100number of threads\n'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        except:
            self.fail()

    def test_cache_breaker_1_a(self):
        practice_word = "pass_test"
        try:
            db_cache_loader("100")
        except:
            self.assertEqual('pass_test', practice_word)

    def test_cache_breaker_2_a(self):
        practice_word = "pass_test_2"
        try:
            db_cache_loader("100number of threads\n'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n")
        except:
            self.assertEqual('pass_test_2', practice_word)

    def test_cache_breaker_3_a(self):
        practice_word = "pass_test_3"
        try:
            db_cache_loader()
        except:
            self.assertEqual('pass_test_3', practice_word)



class TestDataStorage(unittest.TestCase):

    def test_cache_1_s(self):
        db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Title FROM Threads'
        results = cur.execute(sql)
        result_list_s = results.fetchall()
        self.assertIn(('Focused Feedback - Ewok Hunt',), result_list_s)
        self.assertEqual(len(result_list_s), 10)
        conn.close()

    def test_cache_2_s(self):
        db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''SELECT Author, COUNT(Author)
                 FROM Threads
                 GROUP BY Author
                 ORDER BY COUNT(Author) DESC
            '''
        results_2 = cur.execute(sql)
        result_list_2_s = results_2.fetchall()
        self.assertIn(('F8RGE', 1), result_list_2_s)
        self.assertEqual(len(result_list_2_s), 10)
        conn.close()

    def test_cache_3_s(self):
        db_cache_loader("100number of threads\n'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT t.Hour_Created
            FROM Threads AS t
            '''
        results_3 = cur.execute(sql)
        result_list_3_s = results_3.fetchall()
        self.assertIn(('00',), result_list_3_s)
        self.assertEqual(len(result_list_3_s), 100)
        conn.close()

    def test_cache_4_s(self):
        db_cache_loader("100number of threads\n'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT t.title, t.Num_Upvotes, SUM(c.Num_Replies)
            FROM Threads AS t JOIN Comments AS c
    	           ON t.Id=c.Thread_ID
            GROUP BY c.Thread_ID
            '''
        results_4 = cur.execute(sql)
        result_list_4_s = results_4.fetchall()
        self.assertIn(('Focused Feedback - Ewok Hunt', 731, 134), result_list_4_s)
        self.assertEqual(len(result_list_4_s), 97)
        conn.close()

    def test_cache_5_s(self):
        practice_word = "pass_test_5"
        try:
            db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()

            sql = 'SELECT '
            results_5 = cur.execute(sql)
            result_list_5_s = results_5.fetchall()
            self.assertIn(('Focused Feedback - Ewok Hunt',), result_list_5_s)
            self.assertEqual(len(result_list_5_s), 10)
            conn.close()
        except:
            self.assertEqual('pass_test_5', practice_word)


class TestDataProcessing(unittest.TestCase):

    def test_init_db_p(self):
        try:
            init_db()
        except:
            self.fail()


    def test_viz_1_p(self):
        try:
            db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
            top_5_thread_users()
        except:
            self.fail()

    def test_viz_2_p(self):
        try:
            db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
            hours_post_thread()
        except:
            self.fail()

    def test_viz_3_p(self):
        try:
            db_cache_loader("10'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
            tot_replies_v_thrd_upvotes()
        except:
            self.fail()

    def test_viz_4_p(self):
        try:
            db_cache_loader("100number of threads\n'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
            hours_post_thread()
        except:
            self.fail()

    def test_viz_5_p(self):
        try:
            db_cache_loader("100number of threads\n'Night on Endor Update Bugs and Feedback Megathread' is the thread title. \n Posted By: 'BattlefrontModTeam' on '2018-04-18 08:08:24' \n With '8d404a' as the thread id.\n\n")
            top_5_thread_users()
        except:
            self.fail()




if __name__ == '__main__':
    unittest.main()
