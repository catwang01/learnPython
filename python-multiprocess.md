[toc]

## 进程池

### map

进程池不支持手动管理进程

```
import os
import PIL

from multiing import Pool
from PIL import Image

SIZE = (75,75)
SAVE_DIRECTORY = 'thumbs'

def get_image_paths(folder):
    return (os.path.join(folder, f) for f in os.listdir(folder) if 'jpeg' in f)

def create_thumbnail(filename):
    im = Image.open(filename)
    im.thumbnail(SIZE, Image.ANTIALIAS)
    base, fname = os.path.split(filename)
    save_path = os.path.join(base, SAVE_DIRECTORY, fname)
    im.save(save_path)

if __name__ == '__main__':
    folder = os.path.abspath('11_18_2013_R000_IQM_Big_Sur_Mon__e10d1958e7b766c3e840')
    os.mkdir(os.path.join(folder, SAVE_DIRECTORY))

    images = get_image_paths(folder)

    pool = Pool()
    pool.map(creat_thumbnail, images) #关键点，images是一个可迭代对象
    pool.close()
    pool.join()
```

可以创建下面的函数来完成简单的多进程任务。

```
def multi_(func_name, _num, arg_list):
    """
    多线程
    """
    from multiing import Pool
    pool = Pool(_num)
    result_list = pool.map(func_name, arg_list)
    pool.close()
    pool.join()
    return result_list
```


