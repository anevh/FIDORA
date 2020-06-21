import pydicom
import numpy as np

R1 = pydicom.dcmread('RP1_1.dcm')
R2 = pydicom.dcmread('RP1_2.dcm')

print(R2)