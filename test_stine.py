

import numpy as np
import pydicom
import matplotlib.pyplot as plt

dataset = pydicom.dcmread("doseplan040320_2.dcm")

print((dataset.pixel_array).shape)
print(dataset)

#test_dataset = dataset.pixel_array[30,:,:]
#test_dataset[0,0] = 40000
#print(np.amax(test_dataset))


plt.figure()
plt.imshow(dataset.pixel_array[88,:,:]*dataset.DoseGridScaling)
#plt.imshow(test_dataset)
plt.colorbar()
plt.show()