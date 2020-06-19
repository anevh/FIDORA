import tkinter as tk
from tkinter import ttk, StringVar, IntVar, Scrollbar, RIGHT, Y, \
    HORIZONTAL, E, W, N, S, BOTH, Frame, Canvas, LEFT, FLAT, INSERT, DISABLED, ALL, X, BOTTOM, \
    DoubleVar, PanedWindow, RAISED, TOP, Radiobutton, CENTER, BooleanVar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


global upload_button_image
global dose_response_dose_border
global save_button
global help_button
global done_button_image
global profiles_add_doseplan_button_image
global profiles_add_doseplans_button_image
global adjust_button_left_image
global adjust_button_right_image
global adjust_button_up_image
global adjust_button_down_image


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
global tab5
tab5 = ttk.Frame(tab_parent)

global tab1_canvas
tab1_canvas = tk.Canvas(tab1)
global tab2_canvas
tab2_canvas = tk.Canvas(tab2)
global tab3_canvas
tab3_canvas = tk.Canvas(tab3)
global tab4_canvas
tab4_canvas = tk.Canvas(tab4)
global tab5_canvas
tab5_canvas= tk.Canvas(tab5)

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

#Total doseplan
global profiles_film_dataset
#total doseplan in red channel
global profiles_film_dataset_red_channel
#Dose in whole film for red channel
global profiles_film_dataset_red_channel_dose
#Coords to ROI (will vary). Given as [index 0 from, index 0 to, index1 from, index1 to] 
global profiles_film_variable_ROI_coords

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
profile_plot_canvas.grid(row=4, column=0, rowspan=10, columnspan=2, sticky=N+E+W, pady=(0,5), padx=(5,10))
tab4_canvas.grid_columnconfigure(4, weight=0)
tab4_canvas.grid_rowconfigure(4, weight=0)
profile_plot_canvas.config(bg='#E5f9ff', relief=FLAT, highlightthickness=0, width=500, height=500)
profile_plot_canvas.grid_propagate(0)

profiles_fig = Figure(figsize=(5,3))
profiles_a = profiles_fig.add_subplot(111, ylim=(0,40000), xlim=(0,500))
profiles_plot_canvas = FigureCanvasTkAgg(profiles_fig, master=profile_plot_canvas)
profiles_plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+E+W+S, padx=(5,0), pady=(0,0))
profiles_a.set_title ("Profiles", fontsize=12)
profiles_a.set_ylabel("Dose (Gy)", fontsize=12)
profiles_a.set_xlabel("Distance (mm)", fontsize=12)
profiles_fig.tight_layout()


global profiles_showPlanes_image
global profiles_showDirections_image

global profiles_depth
global profiles_depth_float

global profiles_film_factor_input

global profiles_mark_isocenter_button_image
global profiles_mark_ROI_button_image
global profiles_mark_point_button_image

global profiles_iscoenter_coords
profiles_iscoenter_coords = []

#Given from top left corner [right, down]
global profiles_film_isocenter
global profiles_film_reference_point

global profiles_distance_isocenter_ROI
profiles_distance_isocenter_ROI = []
global profiles_distance_reference_point_ROI
profiles_distance_reference_point_ROI = []

global profiles_mark_isocenter_up_down_line
profiles_mark_isocenter_up_down_line = []
global profiles_mark_isocenter_right_left_line
profiles_mark_isocenter_right_left_line = []
global profiles_mark_isocenter_oval
profiles_mark_isocenter_oval = []
global profiles_mark_ROI_rectangle
profiles_mark_ROI_rectangle = []

global profiles_mark_reference_point_oval
profiles_mark_reference_point_oval = []

global profiles_ROI_coords
profiles_ROI_coords = []

global profiles_done_button
profiles_done_button = None
global profiles_done_button_reference_point
profiles_done_button_reference_point = None

global profiles_isocenter_check
profiles_isocenter_check=False
global profiles_reference_point_check
profiles_reference_point_check = False

global profiles_ROI_check
profiles_ROI_check = False
global profiles_ROI_reference_point_check
profiles_ROI_reference_point_check = False

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
profiles_dataset_doseplan = None
global profiles_dataset_rtplan

global profiles_test_if_added_doseplan
global profiles_test_if_added_rtplan
profiles_test_if_added_doseplan = False
profiles_test_if_added_rtplan = False

global profiles_isocenter_mm


global profiles_dose_scaling_doseplan

global profiles_max_dose_film

global profiles_choose_profile_canvas
profiles_choose_profile_canvas = tk.Canvas(profiles_view_film_doseplan_ROI)
profiles_choose_profile_canvas.pack()
profiles_choose_profile_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0)
global profiles_choice_of_profile_line_type
profiles_choice_of_profile_line_type = StringVar()
profiles_choice_of_profile_line_type.set("h")


profiles_choose_profile_type_text = tk.Text(profiles_choose_profile_canvas, height=1)
profiles_choose_profile_type_text.insert(INSERT, "How to draw the profile:")
profiles_choose_profile_type_text.pack(side=TOP)
profiles_choose_profile_type_text.config(bg='#ffffff', relief=FLAT, \
highlightthickness=0, state=DISABLED, font=('calibri', '11'))



Radiobutton(profiles_choose_profile_canvas, text="Horizontal", variable=profiles_choice_of_profile_line_type, \
    value="h", bg='#ffffff', cursor='hand2').pack(side=LEFT)
Radiobutton(profiles_choose_profile_canvas, text="Vertical", \
    variable=profiles_choice_of_profile_line_type, value='v', bg='#ffffff', cursor='hand2').pack(side=LEFT)
Radiobutton(profiles_choose_profile_canvas, text="Draw", \
    variable=profiles_choice_of_profile_line_type, value="d", bg='#ffffff', cursor='hand2').pack(side=LEFT)

profiles_adjust_ROI_text = tk.Text(profiles_choose_profile_canvas, width=20, height=1)
profiles_adjust_ROI_text.insert(INSERT, "Adjust ROI in film: ")
profiles_adjust_ROI_text.config(state=DISABLED, font=('calibri', '11'), bg='#ffffff', relief=FLAT, bd=0)
profiles_adjust_ROI_text.pack(side=LEFT, padx=(70,0))


global profiles_redefine_film_ROI_frame
profiles_redefine_film_ROI_frame = tk.Frame(profiles_choose_profile_canvas)
profiles_redefine_film_ROI_frame.pack(side=LEFT, padx=(0,100))
profiles_redefine_film_ROI_frame.config(bg='#ffffff')
global profiles_adjust_button_left
global profiles_adjust_button_right
global profiles_adjust_button_down
global profiles_adjust_button_up


global profiles_film_panedwindow
profiles_film_panedwindow = PanedWindow(profiles_view_film_doseplan_ROI, orient='vertical')
profiles_film_panedwindow.pack()
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

global doseplan_write_image
global film_dose_write_image
global film_write_image
global doseplan_write_image_width
global doseplan_write_image_height
global doseplan_write_image_var_x 
doseplan_write_image_var_x= 0
global doseplan_write_image_var_y
doseplan_write_image_var_y = 0
global profiles_coordinate_in_dataset
profiles_coordinate_in_dataset = 0

global profiles_first_time_in_drawProfiles
profiles_first_time_in_drawProfiles = True

global new_window_factor_textbox

global profiles_doseplan_lateral_displacement
global profiles_doseplan_vertical_displacement
global profiles_doseplan_longitudianl_displacement
global profiles_doseplan_patient_position

global profiles_reference_point_in_doseplan

global profiles_input_lateral_displacement
global profiles_input_longitudinal_displacement
global profiles_input_vertical_displacement

global profiles_isocenter_or_reference_point

global profiles_lateral
global profiles_vertical
global profiles_longitudinal

global profiles_number_of_doseplans
profiles_number_of_doseplans = 0
global profiles_number_of_doseplans_row_count
profiles_number_of_doseplans_row_count = 4
global profiles_doseplans_grid_config_count
profiles_doseplans_grid_config_count = 6
global profiles_doseplans_filenames
profiles_doseplans_filenames = []
global profiles_doseplans_factor_text
profiles_doseplans_factor_text = []
global profiles_doseplans_factor_input
profiles_doseplans_factor_input = []


global profiles_doseplan_dataset_ROI_several
profiles_doseplan_dataset_ROI_several = []
global profiles_several_img
profiles_several_img = []

global profiles_film_factor

global profiles_lines
profiles_lines = []

global end_point
end_point = None

global profiles_line_coords_film
global profiles_line_coords_doseplan


global profiles_dataset_film_variable_draw
global profiles_dataset_doesplan_variable_draw

global max_dose_doseplan
############################## DVH related ############################################
"""
global DVH_film_orientation
DVH_film_orientation = StringVar()
DVH_film_orientation.set('-')
global doseplans_scroll_frame

global profiles_number_of_doseplans
profiles_number_of_doseplans = 0
global profiles_number_of_doseplans_row_count
profiles_number_of_doseplans_row_count = 4
global profiles_doseplans_grid_config_count
profiles_doseplans_grid_config_count = 6
global profiles_doseplans_filenames
profiles_doseplans_filenames = []
global profiles_doseplans_factor_text
profiles_doseplans_factor_text = []
global profiles_doseplans_factor_input
profiles_doseplans_factor_input = []


global profiles_doseplan_dataset_ROI_several
profiles_doseplan_dataset_ROI_several = []
global profiles_several_img
profiles_several_img = []

global profiles_film_factor

global profiles_lines
profiles_lines = []

global end_point
end_point = None

global profiles_line_coords_film
global profiles_line_coords_doseplan

global DVH_film_orientation_menu


global DVH_film_dataset
global DVH_film_dataset_red_channel
global DVH_film_dataset_ROI
global DVH_film_dataset_ROI_red_channel
global DVH_doseplan_dataset_ROI
global DVH_film_dataset_ROI_red_channel_dose

global DVH_view_film_doseplan_ROI
DVH_view_film_doseplan_ROI = tk.Canvas(tab5_canvas)
DVH_view_film_doseplan_ROI.grid(row=2, column=3, rowspan=25, sticky=E+W+N, pady=(0,5), padx=(5,10))
tab5_canvas.grid_columnconfigure(11, weight=0)
tab5_canvas.grid_rowconfigure(11, weight=0)
DVH_view_film_doseplan_ROI.config(bg='#E5f9ff', relief=FLAT, highlightthickness=0)


global DVH_plot_canvas
DVH_plot_canvas = tk.Canvas(tab4_canvas)
DVH_plot_canvas.grid(row=3, column=0, rowspan=10, columnspan=2, sticky=N+E+W, pady=(0,5), padx=(5,10))
tab5_canvas.grid_columnconfigure(4, weight=0)
tab5_canvas.grid_rowconfigure(4, weight=0)
DVH_plot_canvas.config(bg='#E5f9ff', relief=FLAT, highlightthickness=0)

DVH_fig = Figure(figsize=(5,3))
DVH_a = profiles_fig.add_subplot(111, ylim=(0,40000), xlim=(0,500))
DVH_plot_canvas = FigureCanvasTkAgg(profiles_fig, master=profile_plot_canvas)
DVH_plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+E+W, padx=(5,0), pady=(0,0))
DVH_a.set_title ("Profiles", fontsize=12)
DVH_a.set_ylabel("Pixel value", fontsize=12)
DVH_a.set_xlabel("Distance (mm)", fontsize=12)
DVH_fig.tight_layout()

global DVH_showPlanes_image
global DVH_showDirections_image

global DVH_depth
global DVH_depth_float

#global DVH_mark_isocenter_button_image
#global DVH_mark_ROI_button_image
#global DVH_mark_point_button_image

global DVH_iscoenter_coords
DVH_iscoenter_coords = []

#Given from top left corner [right, down]
global DVH_film_isocenter
global DVH_film_reference_point

global DVH_distance_isocenter_ROI
DVH_distance_isocenter_ROI = []
global DVH_distance_reference_point_ROI
DVH_distance_reference_point_ROI = []

global DVH_mark_isocenter_up_down_line
DVH_mark_isocenter_up_down_line = []
global DVH_mark_isocenter_right_left_line
DVH_mark_isocenter_right_left_line = []
global DVH_mark_isocenter_oval
DVHs_mark_isocenter_oval = []
global DVH_mark_ROI_rectangle
DVH_mark_ROI_rectangle = []

global DVH_mark_reference_point_oval
DVH_mark_reference_point_oval = []

global DVH_ROI_coords
DVH_ROI_coords = []

global DVH_done_button
DVH_done_button = None
global DVH_done_button_reference_point
DVH_done_button_reference_point = None

global DVH_isocenter_check
DVH_isocenter_check=False
global DVH_reference_point_check
DVH_reference_point_check = False

global DVH_ROI_check
DVH_ROI_check = False
global DVH_ROI_reference_point_check
DVH_ROI_reference_point_check = False

global DVH_film_batch
DVH_film_batch = IntVar()
DVH_film_batch.set(0)

global DVH_popt_red
DVH_popt_red = np.zeros(3)

global DVH_upload_button_doseplan
global DVH_upload_button_film
global DVH_upload_button_rtplan

global DVH_dataset_doseplan
global DVH_dataset_rtplan

global DVH_test_if_added_doseplan
global DVH_test_if_added_rtplan
DVH_test_if_added_doseplan = False
DVH_test_if_added_rtplan = False

global DVH_isocenter_mm


global DVH_dose_scaling_doseplan

global DVH_max_dose_film


############## probably comment out this section ##############
DVH_choose_profile_canvas = tk.Canvas(DVH_view_film_doseplan_ROI)
DVH_choose_profile_canvas.pack()
DVH_choose_profile_canvas.config(bg='#ffffff', relief=FLAT, highlightthickness=0)
global DVH_choice_of_profile_line_type
DVH_choice_of_profile_line_type = StringVar()
DVH_choice_of_profile_line_type.set("h")

DVH_choose_profile_type_text = tk.Text(DVH_choose_profile_canvas, height=1)
DVH_choose_profile_type_text.insert(INSERT, "How to draw the profile:")
DVH_choose_profile_type_text.pack(side=TOP)
DVH_choose_profile_type_text.config(bg='#ffffff', relief=FLAT, \
highlightthickness=0, state=DISABLED, font=('calibri', '11'))
Radiobutton(DVH_choose_profile_canvas, text="Horizontal", variable=DVH_choice_of_profile_line_type, \
    value="h", bg='#ffffff', cursor='hand2').pack(side=LEFT)
Radiobutton(DVH_choose_profile_canvas, text="Vertical", \
    variable=DVH_choice_of_profile_line_type, value='v', bg='#ffffff', cursor='hand2').pack(side=LEFT)
Radiobutton(DVH_choose_profile_canvas, text="Draw", \
    variable=DVH_choice_of_profile_line_type, value="d", bg='#ffffff', cursor='hand2').pack(side=LEFT)
##################################################################################################3

global DVH_film_panedwindow
DVH_film_panedwindow = PanedWindow(DVH_view_film_doseplan_ROI, orient='vertical')
DVH_film_panedwindow.pack()
DVH_film_panedwindow.configure(sashrelief = RAISED, showhandle=True)


global DVH_scanned_image_text_image
global DVH_film_dose_map_text_image
global DVH_doseplan_text_image

global DVH_doseplan_write_image
global DVH_doseplan_write_image_width
global DVH_doseplan_write_image_height
global DVH_doseplan_write_image_var_x 
DVH_doseplan_write_image_var_x= 0


global DVH_new_window_factor_textbox ###

global DVH_doseplan_lateral_displacement
global DVH_doseplan_vertical_displacement
global DVH_doseplan_longitudianl_displacement
global DVH_doseplan_patient_position

global DVH_reference_point_in_doseplan

global DVH_input_lateral_displacement
global DVH_input_longitudinal_displacement
global DVH_input_vertical_displacement

global DVH_isocenter_or_reference_point

global DVH_lateral
global DVH_vertical
global DVH_longitudinal
"""
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
