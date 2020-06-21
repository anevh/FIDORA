import pydicom
import numpy as np

R1 = pydicom.dcmread('RP1_1.dcm')
R2 = pydicom.dcmread('RP1_2.dcm')

RD1 = pydicom.dcmread('RD1.dcm')
RD4 = pydicom.dcmread('RD4.dcm')
print(RD4)