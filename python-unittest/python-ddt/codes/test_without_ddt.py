import unittest
import ddt
import time

def get_data():
    return zip(range(1000000), range(1000000))

class customTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.start_time = time.time()
        
    @classmethod
    def tearDownClass(cls):
        time_elapsed = int(time.time() - cls.start_time)
        print("Time Used: {}s".format(time_elapsed))

    def test_add(self):
        total = error_count = 0
        for x, y in get_data():
            total += 1
            try:
                self.assertEqual(x + y, x + y)
            except Exception as e:
                print(e)
                error_count += 1
        print("Run: {} Fail: {}".format(total, error_count))


if __name__ == "__main__":
    unittest.main()
