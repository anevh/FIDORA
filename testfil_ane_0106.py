import pydicom 
import matplotlib.pyplot as plt 
import numpy as np
import cv2 

def get_contours(contour_data):
    roi_seq_names = [roi_seq.ROIName for roi_seq in list(contour_data.StructureSetROISequence)]
    return roi_seq_names #en array med navn på strukturer i den angitte strukturfilen, contour_data

def get_contour_arrays(contour_data):
    roi_array = []
    for con in contour_data:
        for seq in con.ContourSequence:
            roi_array.append(seq.ContourData)
    return roi_array


###############################################################################################################33
def cfile2pixels(file, path, ROIContourSeq=0):
    """
    Given a contour file and path of related images return pixel arrays for contours
    and their corresponding images.
    Inputs
        file: filename of contour
        path: path that has contour and image files
        ROIContourSeq: tells which sequence of contouring to use default 0 (RTV)
    Return
        contour_iamge_arrays: A list which have pairs of img_arr and contour_arr for a given contour file
    """
    # handle `/` missing
    if path[-1] != '/': path += '/'
    f = pydicom.read_file(path + file)
    # index 0 means that we are getting RTV information
    RTV = f.ROIContourSequence[ROIContourSeq]
    # get contour datasets in a list
    contours = [contour for contour in RTV.ContourSequence]
    img_contour_arrays = [coord2pixels(cdata, path) for cdata in contours]  # list of img_arr, contour_arr, im_id

    # debug: there are multiple contours for the same image indepently
    # sum contour arrays and generate new img_contour_arrays
    contour_dict = defaultdict(int)
    for im_arr, cntr_arr, im_id in img_contour_arrays:
        contour_dict[im_id] += cntr_arr
    image_dict = {}
    for im_arr, cntr_arr, im_id in img_contour_arrays:
        image_dict[im_id] = im_arr
    img_contour_arrays = [(image_dict[k], contour_dict[k], k) for k in image_dict]

    return img_contour_arrays

def name_to_index(name, names):
    for i, n in enumerate(names):
        if name == n:
            return i
    return -1

def main():
    ###############################  Doseplan ###############################
    datasetPlan = pydicom.dcmread("V1.dcm")
    dataset_1 = pydicom.dcmread("V1_1.dcm")
    #dataset_2 = pydicom.dcmread("V1_2.dcm")
    #dataset_3 = pydicom.dcmread("V1_3.dcm")
    #dataset_4 = pydicom.dcmread("V1_4.dcm")
    #dataset_5 = pydicom.dcmread("V1_5.dcm")

    print(datasetPlan.pixel_array.shape, "er dimensjonene til doseplan_matrisen")
    #må multiplisere med DoseGridScaling
    #print(datasetPlan.pixel_array[30:40,30:40,50]*datasetPlan.DoseGridScaling)
    #print(dataset_5.pixel_array.shape) #77,83,110
    #print(dataset_1.pixel_array+dataset_2.pixel_array+dataset_3.pixel_array+dataset_4.pixel_array+dataset_5.pixel_array)
    #dose summation type: plan(totalt) vs beam


    #######################  struktur #################################3
    struktur = pydicom.dcmread("V1_struktur.dcm")
    #print(struktur)
    #print("transfersyntax")
    #struktur.file_meta.TransferSyntaxUID
    ctrs = struktur.ROIContourSequence
    #dette funker:
    #print(type(ctrs))
    keys = {}
    for i, name in enumerate(get_contours(struktur)):
        keys[name] = i
    s = ctrs[name_to_index('PTV_v', get_contours(struktur))].ContourSequence[20].ContourData
    #print(s[0:10])



    #print(struktur.Structu<<<reSetROISequence) #skriv akkurat dette!! for å se på de ulkike strukturnavnene

    #######################33 Film ######################################

    filmA = cv2.imread("filmA_corrected.dcm",-1)
    filmA = np.asarray(filmA[:,:,2])
    filmA = np.fliplr(filmA) #speiler bildet
    print(filmA.shape, "er dimensjonene til filmA") #sier hvor mange bits som er i hver fargekanal
    doseMapA = filmA 
    (w,h) = filmA.shape
    for i in range(w):
        for j in range(h):
            doseMapA[i][j] = -403 + 15497108/(filmA[i][j]-2838 ) #D(mGy) = c + b/(PV-a) from calibration curve fitting
    dose_plan =datasetPlan.pixel_array*datasetPlan.DoseGridScaling
    for i in range(0,len(s),3):
        #dose_plan[round(int(s[i])/3):round(int(s[i])/3+20)+10,round(int(s[i+1])/3):round(int(s[i+1])/3)+10,25] = 0
        #doseMapA[round(int(s[i+1])+70)*4:round(int(s[i+1])+71)*4,round(int(s[i])+50)*4:round(int(s[i])+51)*4] = 0
        doseMapA[round(int(s[i+1])*3/0.2)+635:round(int(s[i+1])*3/0.2)+636,round(int(s[i])*3/0.2)+508:round(int(s[i])*3/0.2)+509] = 0

    print(doseMapA[500:505,400:405])

    #cm = m.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
    plt.figure()
    #plt.imshow(dose_plan[:,:,50])
    plt.imshow(doseMapA[220:1050,190:850],vmin=0, vmax=600)
    cbar =plt.colorbar()
    plt.title("Film A")
    cbar.ax.set_ylabel('         cGy', rotation=0)
    plt.show()

    cfile2pixels(struktur,"C:\\Users\\Ane\\Documents\\eksperiment 0106\\V1")

if __name__ == '__main__':
    main()