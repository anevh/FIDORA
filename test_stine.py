

import numpy as np
import pydicom
import matplotlib.pyplot as plt
"""
dataset = pydicom.dcmread("RD1.2.752.243.1.1.20200303144816605.1110.67773.dcm")

print((dataset.pixel_array).shape)
print(dataset.pixel_array[88,70:120,70:120])
#print(dataset.pixel_array[88,0:10,83:95])
#test_dataset = dataset.pixel_array[30,:,:]
#test_dataset[0,0] = 40000
print((np.amax(dataset.pixel_array[88, :,:])*dataset.DoseGridScaling))

print(dataset.PixelSpacing)
if(dataset.SliceThickness == 1 and dataset.PixelSpacing==['1', '1']):
    print(type(dataset.SliceThickness))
    print("ehi")

if(dataset.PixelSpacing==[1,1]):
    print("Hei")

if(dataset.ImageOrientationPatient == [1,0,0,0,1,0]):
    print("greit")
profile = dataset.pixel_array[88,:,93]

plt.figure()
plt.imshow(dataset.pixel_array[88,:,:]*dataset.DoseGridScaling)
#plt.imshow(test_dataset)
#plt.plot(profile)
plt.colorbar()
plt.show()
"""
"""

a = np.zeros((30,40))
b = np.zeros((30,40))
c = np.zeros((30,40))
for i in range(30):
    for j in range(40):
        a[i,j] = 2*i+j/3
        b[i,j] = 1/(j+1)
        c[i,j] = 2+i+j


print(a)
print(b)
print(c)

a = np.reshape(a,-1)
b = np.reshape(b, -1)
c = np.reshape(c, -1)

d = np.corrcoef(a,b)
e = np.corrcoef(a,c)

print(d)
print(e)
print(abs(d[0,1]))

"""
"""

l = [5, 2,52, 54, 2323, 4,2,5,65,2,434]
s = [2,45,1]

l.sort()
s.sort()

print(l)
print()
print(s)

indices = np.searchsorted(l,s)

print(indices)

"""
dataset = pydicom.dcmread("RP1.2.752.243.1.1.20200416093706693.6400.13463.dcm")
dataset2 = pydicom.dcmread("RD1.2.752.243.1.1.20200416093706694.6800.60855.dcm")
dataset3 = pydicom.dcmread("RD1.2.752.243.1.1.20200416093706694.6700.43272.dcm")
dataset4 = pydicom.dcmread("RS1.2.752.243.1.1.20200416093706681.1200.85072.dcm")
iso = dataset.BeamSequence[0].ControlPointSequence[0].IsocenterPosition
"""
print(iso)
iso = np.round(iso)
print(type(iso[0]))


try:
    print(dataset.PatientSetupSequence[0].TableTopVerticalSetupDisplacement)
    print(dataset.PatientSetupSequence[0].TableTopLongitudinalSetupDisplacement)
    print(dataset.PatientSetupSequence[0].TableTopLateralSetupDisplacemen)
    print("hei")
except:
    print("nei")

"""
#print(dataset)

print(dataset2)