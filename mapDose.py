########################### Map dose ###################
def pixelValueToDose(pixelValue):
    a=1
    b=1
    c=1 #må finne disse konstantene 
    return b/(pixelValue - a) + c

def mapDose(img_path):
    dataset = pydicom.dcmread(img_path)
    if "PixelData" in dataset:
        rows= int(dataset.Rows)
        cols = int(dataset.Columns)
        ds= np.pixel_array(ds.PixelData)
        dose_value = np.zeros((rows,cols))
        for i in range(rows):
            for j in range(cols):
                dose_value[i,j]=pixelValueToDose(ds[i,j])
        return dose_value #er et bilde med dose-nivåer, med samme dimensjoner som PV-bildet
    else:
        print("Error. No image stored in dicom file.")
        return 