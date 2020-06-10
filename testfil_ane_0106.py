import pydicom 
import matplotlib.pyplot as plt 
import numpy as np
import cv2 
from sympy import Point, Polygon, pi, Point2D
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

def find_pixels_in_structure(array): #passed 1d array of coordinates on the form (x,y,z)
    points =array3D_to_points(array) # sorts array into a list of 2d points [(x0,y0), (x1,y1), ...]

    #creating polygon
    polyList = []
    for i in range(len(points)):
        polyList.append(i)
    t = tuple(polyList)
    poly = Polygon(*t) #unpacking list elements to make a sequence of points
  
    DVH_points = []
    #iterating through passed array and checking if points are insie polygon
    for i in range(len(array)):
            if (poly.encloses_point(array[i])):
                DVH_points.append(array[i]) 
    
    return DVH_points #returning list of points that are inside the polygon

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def DVH(array,poly):
    points = array3D_to_points(array)
    DVH_points = []
    for i, (x, y) in enumerate(points):
        if (point_inside_polygon(x, y,poly)):
            DVH_points.append(points[i])
    return DVH_points

def array3D_to_points(array):
    Points = []

    for i in range(0,len(array),3):
        Points.append((array[i],array[i+1]))
    return Points


def struktur_array(filename):
    struktur = pydicom.dcmread(filename) #("V1_struktur.dcm")
    ctrs = struktur.ROIContourSequence
    keys = {}
    for i, name in enumerate(get_contours(struktur)):
        keys[name] = i
    s = ctrs[name_to_index('PTV_v', get_contours(struktur))].ContourSequence[20].ContourData
    s = [float(se) for se in s]
    s = array3D_to_points(s)
    return s

def struktur_array_ikke_points(filename):
    struktur = pydicom.dcmread(filename) #("V1_struktur.dcm")
    ctrs = struktur.ROIContourSequence
    keys = {}
    for i, name in enumerate(get_contours(struktur)):
        keys[name] = i
    s = ctrs[name_to_index('PTV_v', get_contours(struktur))].ContourSequence[10].ContourData
    print(ctrs[name_to_index('PTV_v', get_contours(struktur))].ContourSequence[10].ContourData)
    return s


def main():
    ############### test polygon #########################################33#
    print(array3D_to_points([1,2,3,2,4,6]), "er punktene omgitt fra array")
    array =[0.0,0.0,0.0,110,-200,100, -100,-100,-100]
    #poly = [(-1,1),(-1,2),(-1,-1),(-1,0), (0,2),(1,2), (2,2), (2,1), (2,0), (2,-1), (1,-1)]
    poly = struktur_array("V1_struktur.dcm")
    #print(poly, "er polygon listen som definerer strukturen")
    print(DVH(array,poly)[0:10], "er punktene i DVH listen")
    
    #print(find_pixels_in_structure(array), "er punktene i DVH")
 


    ###############################  Doseplan ###############################
    datasetPlan = pydicom.dcmread("V1.dcm")
    dataset_1 = pydicom.dcmread("V1_1.dcm")
    #dataset_2 = pydicom.dcmread("V1_2.dcm")
    #dataset_3 = pydicom.dcmread("V1_3.dcm")
    #dataset_4 = pydicom.dcmread("V1_4.dcm")
    #dataset_5 = pydicom.dcmread("V1_5.dcm")
    ds = datasetPlan.pixel_array*datasetPlan.DoseGridScaling #scaled to dose
    print(datasetPlan.pixel_array.shape, "er dimensjonene til doseplan_matrisen")
    #må multiplisere med DoseGridScaling
    #print(datasetPlan.pixel_array[30:40,30:40,50]*datasetPlan.DoseGridScaling)
    #print(dataset_5.pixel_array.shape) #77,83,110
    #print(dataset_1.pixel_array+dataset_2.pixel_array+dataset_3.pixel_array+dataset_4.pixel_array+dataset_5.pixel_array)
    #dose summation type: plan(totalt) vs beam
    s = struktur_array_ikke_points("V1_struktur.dcm")
    for i in range(0, len(s),3):
        ds[round(-15,int(s[i])):round(int(s[i]))+3, round(int(s[i+1])):round(int(s[i+1]))+3] = 100
    #ds[10,:,:] = 0    
    plt.figure()
    plt.imshow(ds[-15,:,:])
    plt.colorbar()
    plt.show()



  

    #######################  struktur #################################3
    #print(struktur_array("V1_struktur.dcm"))


    #print(struktur.Structu<<<reSetROISequence) #skriv akkurat dette!! for å se på de ulkike strukturnavnene

    #######################33 Film ######################################

    filmA = cv2.imread("filmA_V1_001.tif",-1)
    filmA = np.asarray(filmA[:,:,2])
    filmA = np.fliplr(filmA) #speiler bildet
    print(filmA.shape, "er dimensjonene til filmA") #sier hvor mange bits som er i hver fargekanal
    doseMapA = filmA 
    (w,h) = filmA.shape
    for i in range(w):
        for j in range(h):
            doseMapA[i][j] = -403 + 15497108/(filmA[i][j]-2838 ) #D(mGy) = c + b/(PV-a) from calibration curve fitting
    dose_plan =datasetPlan.pixel_array*datasetPlan.DoseGridScaling
    #for i in range(0,len(struktur_array(filename)),3):
    #    doseMapA[round(int(s[i+1])*3/0.2)+635:round(int(s[i+1])*3/0.2)+636,round(int(s[i])*3/0.2)+508:round(int(s[i])*3/0.2)+509] = 0


    #cm = m.colors.LinearSegmentedColormap('my_colormap', cdict, 1024)
    plt.figure()
    #plt.imshow(dose_plan[:,:,50])
    plt.imshow(doseMapA[220:1050,190:850],vmin=0, vmax=600)
    cbar =plt.colorbar()
    plt.title("Film A")
    cbar.ax.set_ylabel('         cGy', rotation=0)
    plt.show()

#file2pixels(struktur,"C:\\Users\\Ane\\Documents\\eksperiment 0106\\V1")

if __name__ == '__main__':
    main()