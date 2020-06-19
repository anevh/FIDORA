import pydicom


dataset = pydicom.dcmread("V1.dcm")
rt_plan = pydicom.dcmread("RPV1_ane.dcm")
print(dataset)
#print(dataset)
#iso = [100.5, -268.6, -2.7]
#image_pos = [-162.8, -311.7, -119]
#nuf = 77
#row = 83
#colum = 110
iso_1 = int((100.5+162.8)/3)
iso_2 = int((311.7-268.6)/3)
iso_3 = int((119-2.7)/3)
print(rt_plan)
doseplan_array = dataset.pixel_array
#nf - z
#row - y
#col - x
slice = doseplan_array[iso_3,:,:]

slice[iso_2, iso_1] = 0

import matplotlib.pyplot as plt

plt.figure()
plt.imshow(slice)
plt.show()