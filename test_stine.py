import pydicom
import numpy as np
a = np.zeros((3,4))

b = np.zeros((3,4))

for i in range(3):
    for j in range(4):
        a[i,j] = i+j
        b[i,j] = i*j
print(a)
print(b)

a += b
print(a)