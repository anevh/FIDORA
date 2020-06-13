def processDoseplan_usingIsocenter(only_one):
    
    ################  RT Plan ######################

    #Find each coordinate in mm to isocenter relative to first element in doseplan
    iso_1 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[0] - Globals.profiles_isocenter_mm[0])
    iso_2 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[1] - Globals.profiles_isocenter_mm[1])
    iso_3 = abs(Globals.profiles_dataset_doseplan.ImagePositionPatient[2] - Globals.profiles_isocenter_mm[2])
    #Given as [x,y,z] in patient coordinates
    Globals.profiles_isocenter_mm = [iso_1, iso_2, iso_3]


    #Isocenter in pixel relative to the first element in the doseplan
    isocenter_px = np.zeros(3)
    distance_in_doseplan_ROI_reference_point_px = []
    if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
        isocenter_px[0] = np.round(iso_1)#np.round(Globals.profiles_isocenter_mm[0])
        isocenter_px[1] = np.round(iso_2)#np.round(Globals.profiles_isocenter_mm[1])
        isocenter_px[2] = np.round(iso_3)#np.round(Globals.profiles_isocenter_mm[2])
        
        #Change distance in film to pixel in doseplan
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[0][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[0][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[1][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[1][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[2][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[2][1])])
        distance_in_doseplan_ROI_reference_point_px.append([np.round(Globals.profiles_distance_isocenter_ROI[3][0]),\
            np.round(Globals.profiles_distance_isocenter_ROI[3][1])])
    
    elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
        isocenter_px[0] = np.round(Globals.profiles_isocenter_mm[0]/2)
        isocenter_px[1] = np.round(Globals.profiles_isocenter_mm[1]/2)
        isocenter_px[2] = np.round(Globals.profiles_isocenter_mm[2]/2)
       
        
        #Change distance in film to pixel in doseplan
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[0][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[0][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[1][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[1][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[2][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[2][1])/2)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[3][0])/2),\
            np.round((Globals.profiles_distance_isocenter_ROI[3][1])/2)])

    else:
        isocenter_px[0] = np.round(Globals.profiles_isocenter_mm[0]/3)
        isocenter_px[1] = np.round(Globals.profiles_isocenter_mm[1]/3)
        isocenter_px[2] = np.round(Globals.profiles_isocenter_mm[2]/3)
        
        #Change distance in film to pixel in doseplan
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[0][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[0][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[1][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[1][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[2][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[2][1])/3)])
        distance_in_doseplan_ROI_reference_point_px.append([np.round((Globals.profiles_distance_isocenter_ROI[3][0])/3),\
            np.round((Globals.profiles_distance_isocenter_ROI[3][1])/3)])

    reference_point = np.zeros(3)
    
    ######################## Doseplan ##################################
    #dataset_swapped is now the dataset entered the same way as expected with film (slice, rows, columns)
    #isocenter_px and reference_point is not turned according to the doseplan and film orientation.
    if(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 1, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[2]
        reference_point[1] = isocenter_px[1]
        reference_point[2] = isocenter_px[0]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #number of frames -> rows
            #rows -> number of frames
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #column -> number of frames
            #number of frames -> rows
            #rows -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            #dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            #temp_ref = reference_point[0]
            #reference_point[0] = reference_point[1]
            #reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        else:
            messagebox.showerror("Error", "Something has gone wrong here.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[1, 0, 0, 0, 0, 1]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[1]
        reference_point[1] = isocenter_px[2]
        reference_point[2] = isocenter_px[0]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #columns -> number of frames
            #number of frames -> columns
            #rows -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> number of frames
            #number of frames -> rows
            #columns -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 1, 0, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[2]
        reference_point[1] = isocenter_px[0]
        reference_point[2] = isocenter_px[1]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> columns
            #columns -> number of frames
            #number of frames -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #number -> rows
            #colums -> colums
            #rows -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #column -> rows
            #rows -> column
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 1, 0, 0, 0, 1]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[0]
        reference_point[1] = isocenter_px[2]
        reference_point[2] = isocenter_px[1]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> rows
            #columns -> number of frames
            #number of frames ->columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #number of frames -> columns
            #columns -> rows
            #rows -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 1, 0, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[1]
        reference_point[1] = isocenter_px[0]
        reference_point[2] = isocenter_px[2]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> columns
            #columns -> rows
            #number of frames -> number of frames
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[1]
            reference_point[1] = reference_point[2]
            reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #rows -> number of frames
            #columns -> rows
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            #dataset_swapped = np.swapaxes(dataset_swapped, 1,2)
            #temp_iso = isocenter_px[1]
            #isocenter_px[1] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            #temp_ref = reference_point[1]
            #reference_point[1] = reference_point[2]
            #reference_point[2] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            #rows -> columns
            #colums -> number of frames
            #number of frames -> rows
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    elif(Globals.profiles_dataset_doseplan.ImageOrientationPatient==[0, 0, 1, 0, 1, 0]):
        #reference_point[1] = isocenter_px[0]
        #reference_point[2] = isocenter_px[1]
        #reference_point[0] = isocenter_px[2]
        reference_point[0] = isocenter_px[0]
        reference_point[1] = isocenter_px[1]
        reference_point[2] = isocenter_px[2]
        if(Globals.profiles_film_orientation.get()=='Coronal'):
            #rows -> number of frames
            #columns ->rows
            #number of frames -> columns
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[2]
            #isocenter_px[2] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
            dataset_swapped = np.swapaxes(dataset_swapped, 0,1)
            #temp_iso = isocenter_px[0]
            #isocenter_px[0] = isocenter_px[1]
            #isocenter_px[1] = temp_iso
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[1]
            reference_point[1] = temp_ref
        elif(Globals.profiles_film_orientation.get()=='Sagittal'):
            #rows -> columns
            #columns -> rows
            #number of frames -> number of frames
            dataset_swapped = Globals.profiles_dataset_doseplan.pixel_array
        elif(Globals.profiles_film_orientation.get()=='Axial'):
            dataset_swapped = np.swapaxes(Globals.profiles_dataset_doseplan.pixel_array, 0,2)
            temp_ref = reference_point[0]
            reference_point[0] = reference_point[2]
            reference_point[2] = temp_ref
        else:
            messagebox.showerror("Error", "Something has gone wrong.")
            clearAll()
            return
    else:
        messagebox.showerror("Error", "Something has gone wrong.")
        clearAll()
        return



    ####################### Match film and doseplan ###############################

    #Pick the slice where the reference point is (this is the slice-position of the film)
    dose_slice = dataset_swapped[int(reference_point[0]), :, :]
    
    #calculate the coordinates of the Region of Interest in doseplan (marked on the film) 
    #and checks if it actualy exists in dosematrix
    
    doseplan_ROI_coords = []
    top_left_test_side = False; top_left_test_down = False
    top_right_test_side = False; top_right_test_down = False
    bottom_left_test_side = False; bottom_left_test_down = False
    bottom_right_test_side = False; bottom_right_test_down = False
    top_left_side_corr = 0; top_left_down_corr = 0
    top_right_side_corr = 0; top_right_down_corr = 0
    bottom_left_side_corr = 0; bottom_left_down_corr = 0
    bottom_right_side_corr = 0; bottom_right_down_corr = 0


    top_left_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[0][0]
    top_left_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[0][1]
    if(top_left_to_side < 0):
        top_left_test_side = True
        top_left_side_corr = abs(top_left_to_side)
        top_left_to_side = 0
    if(top_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_left_down < 0):
        top_left_test_down = True
        top_left_down_corr = abs(top_left_down)
        top_left_down = 0
    if(top_left_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    
    top_right_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[1][0]
    top_right_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[1][1]
    if(top_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(top_right_to_side > dose_slice.shape[1]):
        top_right_test_side = True
        top_right_side_corr = top_right_to_side - dose_slice.shape[1]
        top_right_to_side = dose_slice.shape[1]
    if(top_right_down < 0):
        top_right_test_down = True
        top_right_down_corr = abs(top_right_down)
        top_right_down = 0
    if(top_right_down > dose_slice.shape[0]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return

    bottom_left_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[2][0]
    bottom_left_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[2][1]
    if(bottom_left_to_side < 0):
        bottom_left_test_side = True
        bottom_left_side_corr = abs(bottom_left_to_side)
        bottom_left_to_side = 0
    if(bottom_left_to_side > dose_slice.shape[1]):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_left_down > dose_slice.shape[0]):
        bottom_left_down_corr = bottom_left_down - dose_slice.shape[0]
        bottom_left_down = dose_slice.shape[0]
        bottom_left_test_down = True
    
    bottom_right_to_side = reference_point[2] - distance_in_doseplan_ROI_reference_point_px[3][0]
    bottom_right_down = reference_point[1] - distance_in_doseplan_ROI_reference_point_px[3][1]
    if(bottom_right_to_side < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_to_side > dose_slice.shape[1]):
        bottom_right_side_corr = bottom_right_to_side - dose_slice.shape[1]
        bottom_right_to_side = dose_slice.shape[1]
        bottom_right_test_side = True
    if(bottom_right_down < 0):
        messagebox.showerror("Fatal Error", "Fatal error: marked ROI is out of range in doseplan. Try again")
        clearAll()
        return
    if(bottom_right_down > dose_slice.shape[0]):
        bottom_right_down_corr = bottom_right_down - dose_slice.shape[0]
        bottom_right_down = dose_slice.shape[0]
        bottom_right_test_down = True
    

    if(top_right_test_side or top_right_test_down or top_left_test_side or top_left_test_down \
        or bottom_right_test_side or bottom_right_test_down or bottom_left_test_side or bottom_left_test_down):
        ROI_info = "Left side: " + str(max(top_left_side_corr, bottom_left_side_corr)) + " pixels.\n"\
            + "Right side: " + str(max(top_right_side_corr, bottom_right_side_corr)) + " pixels.\n "\
            + "Top side: " + str(max(top_left_down_corr, top_right_down_corr)) + " pixels.\n"\
            + "Bottom side: " + str(max(bottom_left_down_corr, bottom_right_down_corr)) + " pixels."  
        messagebox.showinfo("ROI info", "The ROI marked on the film did not fit with the size of the doseplan and had to \
            be cut.\n" + ROI_info )

    doseplan_ROI_coords.append([top_left_to_side, top_left_down])
    doseplan_ROI_coords.append([top_right_to_side, top_right_down])
    doseplan_ROI_coords.append([bottom_left_to_side, bottom_left_down])
    doseplan_ROI_coords.append([bottom_right_to_side, bottom_right_down])


    if(only_one):
        Globals.profiles_doseplan_dataset_ROI = \
            dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
    
    
        img=Globals.profiles_doseplan_dataset_ROI
        if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
            img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
        elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
            img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
        else:
            img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        mx=np.max(img)
        max_dose = mx*Globals.profiles_dose_scaling_doseplan
        img = img/mx
        PIL_img_doseplan_ROI = Image.fromarray(np.uint8(cm.viridis(img)*255))

        wid = PIL_img_doseplan_ROI.width;heig = PIL_img_doseplan_ROI.height
        doseplan_canvas = tk.Canvas(Globals.profiles_film_panedwindow)
        doseplan_canvas.grid(row=2, column=0, sticky=N+S+W+E)
        Globals.profiles_film_panedwindow.add(doseplan_canvas, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())
        doseplan_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            height=max(heig, Globals.profiles_doseplan_text_image.height()), \
                width=wid + Globals.profiles_doseplan_text_image.width())


        Globals.doseplan_write_image = tk.Canvas(doseplan_canvas)
        Globals.doseplan_write_image.grid(row=0,column=1,sticky=N+S+W+E)
        Globals.doseplan_write_image.config(bg='#ffffff', relief=FLAT, highlightthickness=0, width=wid, height=heig)

        doseplan_text_image_canvas = tk.Canvas(doseplan_canvas)
        doseplan_text_image_canvas.grid(row=0,column=0,sticky=N+S+W+E)
        doseplan_text_image_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0, \
            width=Globals.profiles_doseplan_text_image.width(), height=Globals.profiles_doseplan_text_image.height())

        scaled_image_visual = PIL_img_doseplan_ROI
        scaled_image_visual = ImageTk.PhotoImage(image=scaled_image_visual)
        Globals.doseplan_write_image_width = scaled_image_visual.width()
        Globals.doseplan_write_image_height = scaled_image_visual.height()
        Globals.doseplan_write_image.create_image(0,0,image=scaled_image_visual, anchor="nw")
        Globals.doseplan_write_image.image = scaled_image_visual
        doseplan_text_image_canvas.create_image(0,0,image=Globals.profiles_doseplan_text_image, anchor="nw")
        doseplan_text_image_canvas.image=Globals.profiles_doseplan_text_image

        drawProfiles()

    else:
        img=dose_slice[int(top_left_down):int(bottom_left_down), int(top_left_to_side):int(top_right_to_side)]
        """
        if(Globals.profiles_number_of_doseplans == 1):
            Globals.profiles_doseplan_dataset_ROI_several = img
            Globals.profiles_number_of_doseplans+=1

            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
            else:
                Globals.profiles_several_img = cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))

        else:
            Globals.profiles_doseplan_dataset_ROI_several += img
            Globals.profiles_number_of_doseplans+=1
            
            if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5))
            elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10))
            else:
                Globals.profiles_several_img += cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15))
        """
        print("i process")
        Globals.profiles_doseplan_dataset_ROI_several.append(img)
        Globals.profiles_number_of_doseplans+=1

        if(Globals.profiles_dataset_doseplan.PixelSpacing==[1, 1]):
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*5,img.shape[0]*5)))
        elif(Globals.profiles_dataset_doseplan.PixelSpacing==[2, 2]):
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*10,img.shape[0]*10)))
        else:
            Globals.profiles_several_img.append(cv2.resize(img, dsize=(img.shape[1]*15,img.shape[0]*15)))
