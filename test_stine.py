import pydicom


dataset = pydicom.dcmread("V1.dcm")
rt_plan = pydicom.dcmread("RPV1_ane.dcm")
rt_plan2 = pydicom.dcmread("v2_rtplan.dcm")
dataset2 = pydicom.dcmread("v2.dcm")
print(rt_plan)
#print(dataset)
#iso = [100.5, -268.6, -2.7]
#image_pos = [-162.8, -311.7, -119]
#nuf = 77
#row = 83
#colum = 110
iso_1 = int((100.5+162.8)/3)
iso_2 = int((311.7-268.6)/3)
iso_3 = int((119-2.7)/3)
#print(rt_plan)
