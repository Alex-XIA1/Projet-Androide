import numpy as np

a= np.arange(4)

print(np.array_equal(a, a[::-1]), np.array_equal(a, np.arange(4)))