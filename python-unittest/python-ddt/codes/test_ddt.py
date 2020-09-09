import unittest
import ddt
import time

def get_data():
    return zip(range(1000000), range(1000000))

@ddt.ddt
class customTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('ahah')
        cls.start_time = time.time()
        
    @classmethod
    def tearDownClass(cls):
        time_elapsed = int(time.time() - cls.start_time)
        print("Time Used: {}s".format(time_elapsed))

    @ddt.data(*get_data())
    @ddt.unpack
    def test_add(self, x, y):
        self.assertEqual(x + y, x + y)


if __name__ == "__main__":
    unittest.main(verbosity=0)
