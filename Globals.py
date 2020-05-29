import tkinter as tk
from tkinter import ttk, StringVar, IntVar, Scrollbar, RIGHT, Y, \
    HORIZONTAL, E, W, N, S, BOTH, Frame, Canvas, LEFT, FLAT, INSERT, DISABLED, ALL, X, BOTTOM, \
    DoubleVar, PanedWindow, RAISED, TOP
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


global upload_button_image
global dose_response_dose_border
global save_button
global help_button
global done_button_image


global form 
form = tk.Tk()

#Main-window
over_all_frame = tk.Frame(form, bd=0, relief=FLAT)
over_all_canvas = Canvas(over_all_frame)

xscrollbar = Scrollbar(over_all_frame, orient=HORIZONTAL, command=over_all_canvas.xview)
yscrollbar = Scrollbar(over_all_frame, command=over_all_canvas.yview)

scroll_frame = ttk.Frame(over_all_canvas)
scroll_frame.bind("<Configure>", lambda e: over_all_canvas.configure(scrollregion=over_all_canvas.bbox('all')))

over_all_canvas.create_window((0,0), window=scroll_frame, anchor='nw')
over_all_canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

over_all_frame.config(highlightthickness=0, bg='#ffffff')
over_all_canvas.config(highlightthickness=0, bg='#ffffff')
over_all_frame.pack(expand=True, fill=BOTH)
over_all_canvas.grid(row=0, column=0, sticky=N+S+E+W)
over_all_frame.grid_columnconfigure(0, weight=1)
over_all_frame.grid_rowconfigure(0, weight=1)
xscrollbar.grid(row=1, column=0, sticky=E+W)
over_all_frame.grid_columnconfigure(1, weight=0)
over_all_frame.grid_rowconfigure(1, weight=0)
yscrollbar.grid(row=0, column=1, sticky=N+S)
over_all_frame.grid_columnconfigure(2, weight=0)
over_all_frame.grid_rowconfigure(2, weight=0)

global tab_parent
tab_parent = ttk.Notebook(scroll_frame)
tab_parent.borderWidth=0
tab_parent.grid(row=1, column=0, sticky=E+W+N+S, pady=(0,0), padx =(0,0))

global intro_tab
intro_tab = ttk.Frame(tab_parent)
intro_tab.config(relief=FLAT)
global tab1
tab1 = ttk.Frame(tab_parent)
global tab2
tab2 = ttk.Frame(tab_parent)
global tab3
tab3 = ttk.Frame(tab_parent)
global tab4
tab4 = ttk.Frame(tab_parent)

global tab1_canvas
tab1_canvas = tk.Canvas(tab1)
global tab2_canvas
tab2_canvas = tk.Canvas(tab2)
global tab3_canvas
tab3_canvas = tk.Canvas(tab3)
global tab4_canvas
tab4_canvas = tk.Canvas(tab4)

########################################   CoMet related   ###################################################
global CoMet_progressbar
CoMet_progressbar = ttk.Progressbar(tab1_canvas,orient ="horizontal",length = 550, mode ="determinate")
CoMet_progressbar.grid(row=5, column=0, columnspan=1, sticky=W+S, pady=(27,0), padx=(55,50))
tab1_canvas.grid_columnconfigure(12, weight=0)
tab1_canvas.grid_rowconfigure(12, weight=0)
CoMet_progressbar["maximum"] = 100
CoMet_progressbar["value"] = 0

global CoMet_progressbar_counter
CoMet_progressbar_counter = 0

global CoMet_progressbar_check_file
CoMet_progressbar_check_file = True

global CoMet_progressbar_check_folder
CoMet_progressbar_check_folder = True

global CoMet_progressbar_text
CoMet_progressbar_text = tk.Text(tab1_canvas, height=1, width=5)
CoMet_progressbar_text.grid(row=5, column=0, columnspan=1, sticky=E, padx=(0,158), pady=(27,0))
tab1_canvas.grid_columnconfigure(14, weight=0)
tab1_canvas.grid_rowconfigure(14, weight=0)
CoMet_progressbar_text.insert(INSERT, "0%")
CoMet_progressbar_text.config(state=DISABLED, bd=0, relief=FLAT, bg='#ffffff',font=('calibri', '10', 'bold'))

global CoMet_dpi
CoMet_dpi = StringVar(tab1)
CoMet_dpi.set("127")

global CoMet_saveAs
CoMet_saveAs = tk.StringVar(tab1)
CoMet_saveAs.set(".dcm")

global CoMet_uploaded_filename 
CoMet_uploaded_filename=StringVar(tab1)
CoMet_uploaded_filename.set("Error!")

global CoMet_export_folder
CoMet_export_folder=StringVar(tab1)
CoMet_export_folder.set("Error!")

global CoMet_image_to_canvas

global CoMet_correcte_image_filename_box

global CoMet_corrected_image_filename          
CoMet_corrected_image_filename=StringVar(tab1)
CoMet_corrected_image_filename.set("Error!")

global CoMet_patientName
CoMet_patientName=StringVar(tab1)
CoMet_patientName.set("Error!")

global CoMet_correctedImage
CoMet_correctedImage=None

global CoMet_border_1_label
CoMet_border_1_label = tk.Label(tab1_canvas)

global CoMet_border_2_label
CoMet_border_2_label = tk.Label(tab1_canvas)

global CoMet_border_3_label
CoMet_border_3_label = tk.Label(tab1_canvas)

global CoMet_border_4_label
CoMet_border_4_label = tk.Label(tab1_canvas)

global CoMet_save_button_frame_1
CoMet_save_button_frame_1 = tk.Frame(tab1_canvas)

global CoMet_save_button_1
CoMet_save_button_1 = tk.Button(CoMet_save_button_frame_1)

global CoMet_save_filename
CoMet_save_filename = tk.Text(CoMet_border_3_label, height=1, width=30)

global CoMet_print_corrected_image
CoMet_print_corrected_image = tk.Canvas(tab1_canvas)

global CoMet_uploaded_file_text


########################################   Dose response related   ###################################################
tab2_files_frame = tk.Frame(tab2_canvas)
tab2_files_frame.config(relief=FLAT, bg='#ffffff', highlightthickness=0)#, height=200, width=450)
#tab2_files_frame.grid_propagate(0)

tab2_scroll_canvas = tk.Canvas(tab2_files_frame)
tab2_scroll_canvas.config(bg='#ffffff', height=200, width=400,highlightthickness=0)
tab2_scroll_canvas.grid_propagate(0)

scroll = ttk.Scrollbar(tab2_files_frame, command=tab2_scroll_canvas.yview)

scrollable_frame= tk.Frame(tab2_scroll_canvas)

scrollable_frame.bind("<Configure>", lambda e: tab2_scroll_canvas.configure(scrollregion=tab2_scroll_canvas.bbox('all')))
tab2_scroll_canvas.create_window((0,0), window=scrollable_frame, anchor='nw')
tab2_scroll_canvas.configure(yscrollcommand=scroll.set)


global tab2_canvas_files
tab2_canvas_files = tk.Canvas(scrollable_frame)
tab2_canvas_files.config(relief=FLAT, bg='#ffffff', highlightthickness=0, bd=0)
tab2_canvas_files.pack(fill =BOTH, expand=True)

tab2_files_frame.grid(row=2, column=4, columnspan=1, rowspan=3, sticky=N)
tab2_canvas.grid_columnconfigure(1, weight=0)
tab2_canvas.grid_rowconfigure(1, weight=0)
tab2_scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)


global dose_response_save_calibration_button

global doseResponse_dpi
doseResponse_dpi=StringVar()
doseResponse_dpi.set("127")


global dose_response_var1 
dose_response_var1= IntVar()
dose_response_var1.set(1)

global dose_response_var2
dose_response_var2 = IntVar()
dose_response_var2.set(1)

global dose_response_var3
dose_response_var3 = IntVar()
dose_response_var3.set(1)

global dose_response_uploaded_filenames
dose_response_uploaded_filenames = np.array([])

global dose_response_new_window_row_count
dose_response_new_window_row_count = 4

global dose_response_new_window_weight_count
dose_response_new_window_weight_count = 4

global avg_red_vector
avg_red_vector = []

global avg_green_vector
avg_green_vector = []

global avg_blue_vector
avg_blue_vector = []


global dose_response_files_row_count
dose_response_files_row_count = 2

global dose_response_files_weightcount
dose_response_files_weightcount = 8

global dose_response_inOrOut
dose_response_inOrOut = True

global dose_response_delete_buttons
dose_response_delete_buttons = []


global dose_response_red_list
dose_response_red_list = []

global dose_response_green_list
dose_response_green_list = []

global dose_response_blue_list
dose_response_blue_list = []

global dose_response_dose_list
dose_response_dose_list = []

global popt_red
popt_red = np.zeros(3)

global dose_response_batch_number
dose_response_batch_number = "-"

global dose_response_equation_frame
dose_response_equation_frame = tk.Frame(tab2_canvas)
dose_response_equation_frame.grid(row=1, column=4, columnspan=1, sticky=E+W+N, padx=(0,10), pady=(0,0))
tab2_canvas.grid_columnconfigure(8, weight=0)
tab2_canvas.grid_rowconfigure(8, weight=0)
dose_response_equation_frame.config(bg='#E5f9ff', relief=FLAT, highlightthickness=0, width=400, height=200)
dose_response_equation_frame.grid_propagate(0)


global dose_response_plot_frame
dose_response_plot_frame = tk.Frame(tab2_canvas)
dose_response_plot_frame.grid(row=1, column=0, rowspan=2, columnspan=4, sticky=N+S+E+W, pady=(0,5), padx=(5,5))
tab2_canvas.grid_columnconfigure(9, weight=0)
tab2_canvas.grid_rowconfigure(9, weight=0)
dose_response_plot_frame.config(bg='#ffffff', relief=FLAT, highlightthickness=0, height=350,width=500)
dose_response_plot_frame.grid_propagate(0)

dose_response_fig = Figure(figsize=(5,3))
dose_response_a = dose_response_fig.add_subplot(111, ylim=(0,40000), xlim=(0,500))
dose_response_plot_canvas = FigureCanvasTkAgg(dose_response_fig, master=dose_response_plot_frame)
dose_response_plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+S+E+W, padx=(5,0), pady=(0,0))
dose_response_a.set_title ("Dose-response", fontsize=12)
dose_response_a.set_ylabel("Pixel value", fontsize=12)
dose_response_a.set_xlabel("Dose", fontsize=12)
dose_response_fig.tight_layout()

global dose_response_sd_list_red
dose_response_sd_list_red = []

global dose_response_sd_list_green
dose_response_sd_list_green = []

global dose_response_sd_list_blue
dose_response_sd_list_blue = []

global dose_response_sd_avg_red
dose_response_sd_avg_red = DoubleVar()
dose_response_sd_avg_red.set(0)

global dose_response_sd_avg_green
dose_response_sd_avg_green = DoubleVar()
dose_response_sd_avg_green.set(0)

global dose_response_sd_avg_blue
dose_response_sd_avg_blue = DoubleVar()
dose_response_sd_avg_blue.set(0)

global dose_response_sd_min_red
dose_response_sd_min_red = DoubleVar()
dose_response_sd_min_red.set(0)

global dose_response_sd_min_red_dose
dose_response_sd_min_red_dose = StringVar()
dose_response_sd_min_red_dose.set('-')

global dose_response_sd_min_green
dose_response_sd_min_green = DoubleVar()
dose_response_sd_min_green.set(0)

global dose_response_sd_min_green_dose
dose_response_sd_min_green_dose = StringVar()
dose_response_sd_min_green_dose.set('-')

global dose_response_sd_min_blue
dose_response_sd_min_blue = DoubleVar()
dose_response_sd_min_blue.set(0)

global dose_response_sd_min_blue_dose
dose_response_sd_min_blue_dose = StringVar()
dose_response_sd_min_blue_dose.set('-')

global dose_response_sd_max_red
dose_response_sd_max_red = DoubleVar()
dose_response_sd_max_red.set(0)

global dose_response_sd_max_red_dose
dose_response_sd_max_red_dose = StringVar()
dose_response_sd_max_red_dose.set('-')

global dose_response_sd_max_green
dose_response_sd_max_green = DoubleVar()
dose_response_sd_max_green.set(0)

global dose_response_sd_max_green_dose
dose_response_sd_max_green_dose = StringVar()
dose_response_sd_max_green_dose.set('-')

global dose_response_sd_max_blue
dose_response_sd_max_blue = DoubleVar()
dose_response_sd_max_blue.set(0)

global dose_response_sd_max_blue_dose
dose_response_sd_max_blue_dose = StringVar()
dose_response_sd_max_blue_dose.set('-')


########################################   Map dose related   ###################################################


global map_dose_film_dataset
map_dose_film_dataset=StringVar(tab3)
map_dose_film_dataset.set("Error!")

global map_dose_isocenter_map_x_coord_scaled
map_dose_isocenter_map_x_coord_scaled = []

global map_dose_isocenter_map_x_coord_unscaled
map_dose_isocenter_map_x_coord_unscaled = []

global map_dose_isocenter_map_y_coord_scaled
map_dose_isocenter_map_y_coord_scaled = []

global map_dose_isocenter_map_y_coord_unscaled
map_dose_isocenter_map_y_coord_unscaled = []

global map_dose_icocenter_film   #Oppgitt ved [<,v] = [bortover, nedover]

global map_dose_film_batch
map_dose_film_batch = IntVar()
map_dose_film_batch.set(0)

global map_dose_ROI_x_start
map_dose_ROI_x_start = IntVar()
map_dose_ROI_x_start.set(0)

global map_dose_ROI_y_start
map_dose_ROI_y_start = IntVar()
map_dose_ROI_y_start.set(0)

global map_dose_ROI_x_end
map_dose_ROI_x_end = IntVar()
map_dose_ROI_x_end.set(0)

global map_dose_ROI_y_end
map_dose_ROI_y_end = IntVar()
map_dose_ROI_y_end.set(0)

############################### Profiles ######################################

global profiles_film_orientation
profiles_film_orientation = StringVar()
profiles_film_orientation.set('-')

global profiles_film_orientation_menu


global profiles_film_dataset
global profiles_film_dataset_red_channel
global profiles_film_dataset_ROI
global profiles_film_dataset_ROI_red_channel
global profiles_doseplan_dataset_ROI
global profiles_film_dataset_ROI_red_channel_dose

global profiles_view_film_doseplan_ROI
profiles_view_film_doseplan_ROI = tk.Canvas(tab4_canvas)
profiles_view_film_doseplan_ROI.grid(row=2, column=3, rowspan=25, sticky=E+W+N, pady=(0,5), padx=(5,10))
tab4_canvas.grid_columnconfigure(11, weight=0)
tab4_canvas.grid_rowconfigure(11, weight=0)
profiles_view_film_doseplan_ROI.config(bg='#E5f9ff', relief=FLAT, highlightthickness=0)


global profile_plot_canvas
profile_plot_canvas = tk.Canvas(tab4_canvas)
profile_plot_canvas.grid(row=4, column=0, rowspan=3, columnspan=2, sticky=N+S+E+W, pady=(0,5), padx=(5,10))
tab4_canvas.grid_columnconfigure(4, weight=0)
tab4_canvas.grid_rowconfigure(4, weight=0)
profile_plot_canvas.config(bg='#E5f9ff', relief=FLAT, highlightthickness=0)

profiles_fig = Figure(figsize=(5,3))
profiles_a = profiles_fig.add_subplot(111, ylim=(0,40000), xlim=(0,500))
profiles_plot_canvas = FigureCanvasTkAgg(profiles_fig, master=profile_plot_canvas)
profiles_plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+S+E+W, padx=(5,0), pady=(0,0))
profiles_a.set_title ("Profiles", fontsize=12)
profiles_a.set_ylabel("Pixel value", fontsize=12)
profiles_a.set_xlabel("Distance (mm)", fontsize=12)
profiles_fig.tight_layout()

global profiles_showPlanes_image
global profiles_showDirections_image

global profiles_depth
global profiles_depth_float

global profiles_mark_isocenter_button_image
global profiles_mark_ROI_button_image

global profiles_iscoenter_coords
profiles_iscoenter_coords = []

#Given from top left corner [right, down]
global profiles_film_isocenter

global profiles_distance_isocenter_ROI
profiles_distance_isocenter_ROI = []

global profiles_mark_isocenter_up_down_line
profiles_mark_isocenter_up_down_line = []
global profiles_mark_isocenter_right_left_line
profiles_mark_isocenter_right_left_line = []
global profiles_mark_isocenter_oval
profiles_mark_isocenter_oval = []
global profiles_mark_ROI_rectangle
profiles_mark_ROI_rectangle = []

global profiles_ROI_coords
profiles_ROI_coords = []

global profiles_done_button
profiles_done_button = None

global profiles_isocenter_check
profiles_isocenter_check=False

global profiles_ROI_check
profiles_ROI_check = False

global profiles_film_batch
profiles_film_batch = IntVar()
profiles_film_batch.set(0)

global profiles_popt_red
profiles_popt_red = np.zeros(3)

#global profiles_film_window
#global profiles_film_window_open
#profiles_film_window_open = False

global profiles_upload_button_doseplan
global profiles_upload_button_film
global profiles_upload_button_rtplan

global profiles_dataset_doseplan
global profiles_dataset_rtplan

global profiles_test_if_added_doseplan
global profiles_test_if_added_rtplan
profiles_test_if_added_doseplan = False
profiles_test_if_added_rtplan = False

global profiles_isocenter_mm
global profiles_longitudinal_displacement_mm
global profiles_lateral_displacement_mm
global profiles_vertical_displacement_mm

global profiles_dose_scaling_doseplan

global profiles_max_dose_film


#global profiles_film_notebook_canvas
#profiles_film_notebook_canvas = tk.Canvas(profiles_view_film_doseplan_ROI)
#profiles_film_notebook_canvas.pack()
#profiles_film_notebook_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0)
global profiles_film_panedwindow
profiles_film_panedwindow = PanedWindow(profiles_view_film_doseplan_ROI, orient='vertical')
profiles_film_panedwindow.pack(side=TOP)
profiles_film_panedwindow.configure(sashrelief = RAISED, showhandle=True)


#global profiles_film_tab_parent
#profiles_film_tab_parent = ttk.Notebook(profiles_film_notebook_canvas)
#profiles_film_tab_parent.borderWidth=0
#profiles_film_tab_parent.pack()

#global profiles_film_tab_image
#profiles_film_tab_image = ttk.Frame(profiles_film_tab_parent)
#profiles_film_tab_image.config(relief=FLAT)



#global profiles_film_tab_dose
#profiles_film_tab_dose = ttk.Frame(profiles_film_tab_parent)
#profiles_film_tab_dose.config(relief=FLAT,padding=[0,0,0,0])


#profiles_film_tab_parent.add(profiles_film_tab_image, text='Scanned film')
#profiles_film_tab_parent.add(profiles_film_tab_dose, text='Dose on film')

global profiles_scanned_image_text_image
global profiles_film_dose_map_text_image
global profiles_doseplan_text_image
############################### Correction matrix ######################################

global correction127_red
with open('red_127.txt', 'r') as f:
    correction127_red = [[float(num) for num in line.split(',')] for line in f]
correction127_red = np.matrix(correction127_red)
global correction127_green
with open('green_127.txt', 'r') as f:
    correction127_green = [[float(num) for num in line.split(',')] for line in f]
correction127_green = np.matrix(correction127_green)

global correction127_blue
with open('blue_127.txt', 'r') as f:
    correction127_blue = [[float(num) for num in line.split(',')] for line in f]
correction127_blue = np.matrix(correction127_blue)

global correction72_red
with open('output_red_72.txt', 'r') as f:
    correction72_red = [[float(num) for num in line.split(',')] for line in f]
correction72_red = np.matrix(correction72_red)

global correction72_green
with open('output_green_72.txt', 'r') as f:
    correction72_green = [[float(num) for num in line.split(',')] for line in f]
correction72_green = np.matrix(correction72_green)

global correction72_blue
with open('output_blue_72.txt', 'r') as f:
    correction72_blue = [[float(num) for num in line.split(',')] for line in f]
correction72_blue = np.matrix(correction72_blue)


global correctionMatrix127
correctionMatrix127 = np.zeros((1270,1016,3))
correctionMatrix127[:,:,0] = correction127_blue[:,:]
correctionMatrix127[:,:,1] = correction127_green[:,:]
correctionMatrix127[:,:,2] = correction127_red[:,:]

global correctionMatrix72
correctionMatrix72 = np.zeros((720,576,3))
correctionMatrix72[:,:,0] = correction72_blue[:,:]
correctionMatrix72[:,:,1] = correction72_green[:,:]
correctionMatrix72[:,:,2] = correction72_red[:,:]
