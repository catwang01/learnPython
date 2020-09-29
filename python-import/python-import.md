[toc]

# Python import

如果报错 `xx is not a package`，考虑两种可能

1. xx 目录下是否存在 `__init__.py` 
2. 是否存在与 xx 同名的文件

## 相对导入和绝对导入

其实我们一般使用的都是绝对导入。个人认为相对导入容易出错，所以统一使用绝对导入，不使用相对导入。

### 绝对导入

- `import module_name` 导入和自己同目录下的模块
- `from package_name import module_name`  导入和自己同目录的包的模块

### 相对导入的语法

- `from . import module_name`。导入和自己同目录下的模块。
- `from .package_name import module_name`。导入和自己同目录的包的模块。
- `from .. import module_name`。导入上级目录的模块。
- `from ..package_name import module_name`。导入位于上级目录下的包的模块。

## python import 机制

对于 python 的import 机制，个人认为需要记住三点

1. python 是通过查找 sys.path 中的目录下有没有 import 的模块，如果有，就 import 进来，如果没有就报错。因此，如果报错找不到 xx 模块，99% 是因为 xx 模块所在的目录没有在 sys.path 中。

2. 对于入口文件，python 会自动将入口文件所在的目录添加到 sys.path 中。比如，我们在 `test_code` 目录下有一个 `m1.py` 文件，`m1.py` 中的内容如下：


```
# m1.py
import sys
for p in sys.path:
    print(p)
```

运行 `m1.py` ，输出如下

```
$ python m1.py
/Users/ed/Git/learnPython/python-import/test_code
/anaconda3/lib/python37.zip
/anaconda3/lib/python3.7
/anaconda3/lib/python3.7/lib-dynload
/anaconda3/lib/python3.7/site-packages
/anaconda3/lib/python3.7/site-packages/aeosa` 
```

其中第一个就是 `m1.py` 所在的目录，即 `test_code` 目录。

3. 对于非入口文件，其所在的目录不会被添加到 sys.path。

我们在 test_code 目录下添加 subfolder 目录，其下添加 m3.py 文件，内容如下：

```
def test3():
    print("This is m3")
```

而我们在 `test_code` 目录下添加一个 `m2.py` ，其中内容如下


添加完这些文件后，我们的目录看起来是下面这个样子的

```
$ tree test_code/
test_code/
├── m1.py
├── m2.py
└── subfolder
    └── m3.py
```


我们运行 `m2.py` 

```
$ python m2.py
/Users/ed/Git/learnPython/python-import/test_code
/anaconda3/lib/python37.zip
/anaconda3/lib/python3.7
/anaconda3/lib/python3.7/lib-dynload
/anaconda3/lib/python3.7/site-packages
/anaconda3/lib/python3.7/site-packages/aeosa
This is m2
This is m3
```

可以看到上面到结果中，只有虽然使用了 `m3.py` ，但是 `sys.path` 中并没有 `m3.py` 所在的目录，即 subfolder

### 导致的问题

这种特性会导致一个问题。在上面的情况中，在 subfolder 下创建一个新的文件 `m4.py`，并在其中引用同级的 `m3.py` 中的内容。`m4.py` 中的内容如下：


```
import m3

def test4():
    print("This is m4")

m3.test3()
test4()
```

我们进入 subfolder，然后直接运行  `m4.py` ，可以正常运行。

```
$ cd subfolder/
$ python m4.py
This is m3
This is m4
```

然后在 test_code 目录下添加文件 `m5.py` ，其中引用 `m4.py` 中，`m5.py` 的内容如下

```
from subfolder import m4

def test5():
    print("This is m5")

m4.test4()
test5()
```

此时我们的目录结构如下：

```
$ tree test_code/
test_code/
├── m1.py
├── m2.py
├── m5.py
└── subfolder
    ├── m3.py
    └── m4.py
```

运行 `m5.py`，发现报错了。

```
$ python m5.py
Traceback (most recent call last):
  File "m5.py", line 1, in <module>
    from subfolder import m4
  File "/Users/ed/Git/learnPython/python-import/test_code/subfolder/m4.py", line 1, in <module>
    import m3
ModuleNotFoundError: No module named 'm3'
```

其原因就是在于，`m4.py` 中引用了 `m3.py`，要找到 `m3.py` 需要 sys.path 中有 subfolder。在我们直接运行 `m4.py` 时，由于 `m4.py` 是入口文件，其所在的目录即 subfolder 会被自动添加到 `sys.path` 中，因此 `import m3` 时可以正确找到 `m3.py` 。

但是，当我们运行 `m5.py` 时，`m4.py` 不是入口文件，因此 `subfolder` 这个目录不会被自动导入 sys.path 中，因此 `import m3` 会报错。

解决方法是在 `m4.py` 中手动导入其所在的路径，`m4.py` 修改后的内容如下

```
import sys
import os
sys.path.append(os.path.dirname(__file__))
import m3

def test4():
    print("This is m4")

m3.test3()
test4()
```

此时再运行 `m5.py` 就不会出错了


```
$ python m5.py
This is m3
This is m4
This is m4
This is m5    
```

### 建议

为了防止上面这种情况的出现，个人认为

1. 统一使用绝对导入，不使用相对导入
2. 对于每个 python 文件最开头都写上下面的内容以导入自己所在的目录。至少可以保障同目录的文件 import 不会出错。如果还引用了其他本地文件，也将其路径 append 到 `sys.path`  中。

```
import sys
import os
sys.path.append(os.path.dirname(__file__))
```

遵从这两个建议，99% 的情况下都不会出错了。




