from classA import A
import dill

b = A()
with open("b.pkl", "wb") as f:
    dill.dump(b, f)
    
