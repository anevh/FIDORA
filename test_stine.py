

import numpy as np
import pydicom
import matplotlib.pyplot as plt

dataset = pydicom.dcmread("doseplan040320.dcm")

print((dataset.pixel_array).shape)
print(dataset)
print(dataset.pixel_array[88,0:10,83:95])
#test_dataset = dataset.pixel_array[30,:,:]
#test_dataset[0,0] = 40000
#print(np.amax(test_dataset))

profile = dataset.pixel_array[88,:,93]

plt.figure()
plt.imshow(dataset.pixel_array[88,:,:]*dataset.DoseGridScaling)
#plt.imshow(test_dataset)
#plt.plot(profile)
plt.colorbar()
plt.show()