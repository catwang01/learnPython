import dill

with open("b.pkl", "rb") as f:
    b = dill.load(f)

b.sayHello()

