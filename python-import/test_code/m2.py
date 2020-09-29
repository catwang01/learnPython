import sys
from subfolder import m3

for p in sys.path:
    print(p)

def test2():
    print("This is m2")

test2()
m3.test3()
