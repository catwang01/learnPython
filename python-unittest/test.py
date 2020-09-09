import unittest

class MyTest(unittest.TestCase):  # 继承unittest.TestCase
    def setUp(self):
        print('Call setUp')

    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('Call tearDown')

    @classmethod
    def setUpClass(self):
    # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('Call setUpClass')

    @classmethod
    def tearDownClass(self):
    # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
         print('Call tearDownClass')

    def test_a_run(self):
        self.assertEqual(1, 1)  # 测试用例
        
    def test_b_run(self):
        self.assertEqual(2, 2)  # 测试用例
        
    def test_c_run(self):
        self.assertEqual(2, 2)  # 测试用例

if __name__ == '__main__':
    unittest.main()#运行所有的测试用例
