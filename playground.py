import numpy as np

class MyClass:
    def __init__(self, x):
        self.x = x

a = np.array([MyClass(i) for i in range(10)])
print(a.dtype)