import numpy as np


x = np.array([[1,2],[3,4]])


d = {}


xs = np.array_str(x)


s = set([xs])

print(xs in s)