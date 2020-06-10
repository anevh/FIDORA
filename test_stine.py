

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

#print(dataset)

#[507,640]
#slice 94, [93,88]
"""
def pixel_to_dose(P,a,b,c):
    ret = c + b/(P-a)
    return ret

doseplan = dataset2.pixel_array
import Globals
import cv2
cv2Img = cv2.imread("img10x10_001.tif", cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
cv2Img = cv2.medianBlur(cv2Img, 5)
cv2Img = abs(cv2Img-Globals.correctionMatrix127)
cv2Img = np.clip(cv2Img, 0, 65535)

image = cv2Img[365:915,233:783,2]
film_dose = np.zeros((int(image.shape[0]/5), int(image.shape[1]/5)))
for i in range(film_dose.shape[0]):
    for j in range(film_dose.shape[1]):
        film_dose[i,j] = pixel_to_dose(image[i*5,j*5], 1686.5, 16705877.4, -415.541)

film_dose = np.flip(film_dose,1)
isocenter_film = [int((640-365)/5), int((508-233)/5)]

doseplan_slice = doseplan[:,93,:]

profile_film = film_dose[:,isocenter_film[1]]


profile_doseplan = doseplan_slice[33:143,88]

print(len(profile_film))
print(len(profile_doseplan))
x = np.linspace(-5,5,len(profile_doseplan))
profile_doseplan = profile_doseplan*dataset2.DoseGridScaling*100
print(len(x))
plt.figure()
plt.plot(x,profile_film, 'r')
plt.plot(x, profile_doseplan, 'b')
plt.legend(['film', 'doseplan'])
plt.xlabel("lateral displacement")
plt.ylabel("Dose")
plt.title("Profiles, lateral direction across isocenter")
plt.show()

"""

dataset1 = pydicom.dcmread("struct_test.dcm")
structures = dataset1.ROIContourSequence
struct = structures[1]
"""
print(len(structures))
print(struct.ContourSequence[0])
print(struct.ContourSequence[0].ContourData)
"""
struct_cont_coord_px = np.round(struct.ContourSequence[25].ContourData)



print(struct_cont_coord_px)

dataset1 = pydicom.dcmread("testDicom1.dcm")
dataset1_array = dataset1.pixel_array
#slice = dataset1_array[10+120,:,:]

"""
for i in range(0, len(struct_cont_coord_px), 3):
   dataset1_array[120+int(struct_cont_coord_px[i+2]), 315+int(struct_cont_coord_px[i+1]),\
        166+int(struct_cont_coord_px[i])] = 0


plt.figure()
plt.imshow(slice)
plt.show()
"""
"""
x = [1,2,3,4]
y = [1,2,3,4]
m = [[15,14,13,12],[14,12,10,8],[13,10,7,4],[12,8,4,0]]
cs = plt.contour(x,y,m, [9.5])
print(cs.collections[0].get_paths())
"""


dataset = pydicom.dcmread("RD1.2.752.243.1.1.20200303144816605.1110.67773.dcm")
testv2 = pydicom.dcmread("rtplan_v2.dcm")
test_dosemap_v2 = pydicom.dcmread("testv2.dcm")
print(testv2.PatientSetupSequence[0].TableTopLongitudinalSetupDisplacement)
print(testv2.PatientSetupSequence[0].TableTopLateralSetupDisplacement)
print(testv2.PatientSetupSequence[0].TableTopVerticalSetupDisplacement)

a = 0
if(a==0): print("Hei")