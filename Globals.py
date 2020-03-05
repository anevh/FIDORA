import tkinter as tk
from tkinter import ttk, StringVar, IntVar, Scrollbar, RIGHT, Y, \
    HORIZONTAL, E, W, N, S, BOTH, Frame, Canvas, LEFT, FLAT, INSERT, DISABLED, ALL, X, BOTTOM
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global upload_button_image
global dose_response_dose_border

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

########################################   CoMet related   ###################################################
global CoMet_progressbar
CoMet_progressbar = ttk.Progressbar(tab1_canvas,orient ="horizontal",length = 200, mode ="determinate")
CoMet_progressbar.grid(row=5, column=0, columnspan=3, sticky=E+W+S, pady=(40,0), padx=(50,70))
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
CoMet_progressbar_text.grid(row=5, column=2, columnspan=1, sticky=E, padx=(0,70), pady=(40,0))
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

fig = Figure(figsize=(5,3))
a = fig.add_subplot(111, ylim=(0,40000), xlim=(0,500))
plot_canvas = FigureCanvasTkAgg(fig, master=dose_response_plot_frame)
plot_canvas.get_tk_widget().grid(row=0,column=0,columnspan=4, sticky=N+S+E+W, padx=(5,0), pady=(0,0))
a.set_title ("Dose-response", fontsize=12)
a.set_ylabel("Pixel value", fontsize=12)
a.set_xlabel("Dose", fontsize=12)
fig.tight_layout()


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


############################### Correction matrix ######################################3

global correction127_red
with open('output_red_127.txt', 'r') as f:
    correction127_red = [[float(num) for num in line.split(',')] for line in f]
correction127_red = np.matrix(correction127_red)
global correction127_green
with open('output_green_127.txt', 'r') as f:
    correction127_green = [[float(num) for num in line.split(',')] for line in f]
correction127_green = np.matrix(correction127_green)

global correction127_blue
with open('output_blue_127.txt', 'r') as f:
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
