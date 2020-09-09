[toc]

# Python import

太细节的东西也没有怎么看懂。

## 相对导入和绝对导入

### 绝对导入

- `import module_name` 导入和自己同目录下的模块
- `from package_name import module_name`  导入和自己同目录的包的模块

### 相对导入的语法

- `from . import module_name`。导入和自己同目录下的模块。
- `from .package_name import module_name`。导入和自己同目录的包的模块。
- `from .. import module_name`。导入上级目录的模块。
- `from ..package_name import module_name`。导入位于上级目录下的包的模块。