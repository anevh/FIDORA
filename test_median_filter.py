from scipy import ndimage, misc
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data
from skimage.filters import median
from skimage.morphology import disk


filmA = cv2.imread("filmA_V1_001.tif",-1)
filmA = np.asarray(filmA[:,:,:])
filmA = np.fliplr(filmA) #speiler bildet

img_median = median(filmA[:,:,2], disk(5))


cv2.imshow('img', img_median[220:1050,190:850]) # Display img with median filter
cv2.waitKey(0)        # Wait for a key press to
cv2.destroyAllWindows # close the img window.
