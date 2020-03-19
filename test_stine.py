"""

import numpy as np
import pydicom
import matplotlib.pyplot as plt

dataset = pydicom.dcmread("doseplan_ex.dcm")

print((dataset.pixel_array).shape)
print(dataset)

"""

import numpy as np

a = np.ones((3,3))
print(a)

a = a/2

print(a)

print(np.int(a))