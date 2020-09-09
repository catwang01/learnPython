[toc]

# Python unittest 和 ddt 从使用到放弃


笔者被要求做单元测试，很自然的使用 unittest 这个库。笔者从事的深度学习模型相关的工作，其中有一个需求就是将一堆数据喂给模型，然后检验结果是否符合预期，这堆数据存在一个 txt 文件中。

先给出结论：unittest 没有很优雅的满足笔者需求的写法。

## 最开始的写法

```
import unittest


file_path = "/tmp/data.txt"
class Test(unittest.TestCase):

    def test_output(self):
        total = error_num = 0
        with open(file_path) as f:
            total += 1
            for line in f:
                total
                # line look like "hahaha, heheh"
                inputs, outpus = line.strip().split(',')
                prediction = model(inputs)
                try:
                    check(prediction, outputs) 
                except Exception as e:
                    error_num += 1
         print("Run:{} tests Failed: {}".format(total, error_num))
``` 

## 改进

上面的写法，实际上并没有用到 unittest 的统计功能。因为笔者希望这一堆数据被当作不同的测试用例来统计成功失败的次数，而不是被当作一个测试用例。

通过查阅资料，笔者发现 ddt 这个 python 库可以解决这个问题。

```
import unittest
import ddt


file_path = "/tmp/data.txt"

def get_data():
    with open(file_path) as f:
        data = [inputs, outpus for line in f]
    return data

@ddt.ddt
class Test(unittest.TestCase):

    @ddt.ddt(*get_data())
    @ddt.unpack
    def test_output(self):
        prediction = model(inputs)
        self.assertEqual(prediction, outputs) 
```

看起来还比较优雅。但是跑了一波，发现一个严重的问题：慢！

### 测试

笔者写了如下的两个脚本来测试：

```
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
```

这个脚本运行时间 16s 左右。其中 verbosity=0 禁止输出，可以加快速度。

另一个脚本 `test_without_ddt.py` 来测试不适用 ddt 的情况。


```
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
```

这个脚本的运行时间不到 1s！和使用 ddt 相比有巨大的提升。

经过实验，发现 ddt 这种用法会严重影响效率。对于测试用例比较少的时候还好说，对于测试用例多的情况不适用。

因此，笔者放弃使用 unittest 来实现多个测试用例的想法。老老实实使用最开始的方法来测试结果。

