# Python csv 写入比较

结论： `dask.dataframe.read_csv` 的速度是最快的

## pd.read_csv

```python
import pandas as pd
import numpy as np

file_path = "/Users/ed/Git/2020-kdd-debiasing/csv/negative_sampled_data.csv"
```

```python
%%time
result = pd.read_csv(file_path)
```

## dask.dataframe.read_csv

```python
%%time

import dask.dataframe as dd
result = dd.read_csv(file_path).compute() # result 是一个 dataframe
```

```python
%%time

import modin.pandas as modinpd
result = modinpd.read_csv(file_path) # result 是一个 modin.pandas.dataframe.DataFrame 不是 pandas 中的 dataframe
```

```python

```
