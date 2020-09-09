[toc]


# Python nose

## 使用

### 命令行

新建一个空目录 python-nose，进入目录

```
$ mkdir python-nose
$ cd python-nose/$ 
``` 

在目录下创建一个新的文件

```
$ vim demo.py
``` 

内容如下。

```
def test_hello():
    a, b = 1, 2
    raise a == b
```

然后在 python-nose 目录下运行

```
$ nosetests
```

