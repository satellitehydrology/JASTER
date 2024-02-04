import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog
from s00_get_system_parameters import screen_width, screen_height, z, TEXT
      
def create_menu_window(callback):
        
    background_color = 'lavender' 
    error_color = 'lavenderblush'
    def_par = { 'font': ('Arial', TEXT), 'fg': 'black', 'bg': background_color}
    lat_lon_par = { 'font': ("Arial", TEXT),'width': 25, 'validate': 'key','readonlybackground': 'white'}
    
    def aviso_password_visibility():
        password_aviso_entry['show'] = '' if password_aviso_entry['show'] == '*' else '*'
                    
    def destroy_widgets(widgets_to_destroy):
        for widget in widgets_to_destroy:
            widget.destroy() 
                
    def validate_lat_lon_input(P, entry):
        if P == "" or (P == "-" and entry.index("insert") == 0):
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False
    
    def create_label(text, x, y,  rowspan, columnspan):
        frame = tk.Frame(pop_up_window, relief='solid')
        frame.grid(row=x, column=y, rowspan=rowspan, columnspan=columnspan, sticky='nsew')
        label = tk.Label(frame, text=text, **def_par,  anchor='w')
        label.pack(expand=True, fill='both')
        return frame
    
    def create_entry(show, x, y, column_span):
        entry = tk.Entry(pop_up_window, show=show, font=("Arial", TEXT))
        entry.grid(row=x, column=y, columnspan=column_span, sticky='ew')
        return entry
    
    def create_button(text,command, size, x, y, y_pad, x_pad, column_span, row_span):
        button = tk.Button(pop_up_window, text=text, command=command, font=("Arial", size))
        button.grid(row=x, column=y, pady=y_pad, padx=x_pad, columnspan=column_span, rowspan=row_span, sticky='nsew')
        return button
    
    def create_radiobutton(text, variable, value, command, x, y, rowspan, columnspan):
        frame = tk.Frame(pop_up_window, relief='solid')
        frame.grid(row=x, column=y, rowspan=rowspan, columnspan=columnspan, sticky='nsew')
        radiobutton = tk.Radiobutton(frame, text=text, **def_par, variable=variable, value=value, command=command)
        radiobutton.pack(expand=True, fill='both')
        return radiobutton
    
    def create_spinbox(from_, to, x, y, rowspan, columnspan, y_pad, x_pad, w):
        spinbox = tk.Spinbox(pop_up_window, from_=from_, to=to, width = w, font=("Arial", TEXT))
        spinbox.grid(row=x, column=y, rowspan=rowspan, columnspan=columnspan, pady=y_pad, padx=x_pad, sticky='nsew')
        return spinbox
    
    def update_cycle_text():
        destroy_widgets(widgets_to_display)
        selection = series_var.get()
        if selection == '2':
            create_label_and_spinbox_for_2()
        elif selection == '3':
            create_label_and_spinbox_for_3()
        elif selection == '1':
            create_label_and_spinbox_for_both()

    def create_label_and_spinbox_for_2():
        global srt_2o_entry, end_2o_entry
        range_2o_label = create_label('Jason-2 cycle ranges from 1 to 303',  5, 17,  1, 16)
        srt_2o_label   = create_label('Start cycle of Jason-2 time series:', 6, 17,  1, 12)
        end_2o_label   = create_label('End cycle of Jason-2 time series:',   7, 17,  1, 12)
        srt_2o_entry = create_spinbox(1, 303, 6, 29, 1, 7, 6, 6, 4)
        end_2o_entry = create_spinbox(1, 303, 7, 29, 1, 7, 6, 6, 4)
        widgets_to_display.extend([range_2o_label,srt_2o_label,end_2o_label,srt_2o_entry,end_2o_entry])
     
    def create_label_and_spinbox_for_3():
        global srt_3o_entry, end_3o_entry
        range_3o_label = create_label('Jason-3 cycle ranges from 1 to 226',  5, 17,  1, 16)
        srt_3o_label   = create_label('Start cycle of Jason-3 time series:', 6, 17,  1, 12)
        end_3o_label   = create_label('End cycle of Jason-3 time series:',   7, 17,  1, 12)
        srt_3o_entry = create_spinbox(1, 226, 6, 29, 1, 7, 6, 6, 4)
        end_3o_entry = create_spinbox(1, 226, 7, 29, 1, 7, 6, 6, 4)    
        widgets_to_display.extend([range_3o_label,srt_3o_label,end_3o_label,srt_3o_entry,end_3o_entry])
             
    def create_label_and_spinbox_for_both():
        global srt_2b_entry, end_2b_entry, srt_3b_entry, end_3b_entry
        range_2b_label = create_label('Jason-2 (from 1 to 303)', 5, 17, 1, 8)
        srt_2b_label   = create_label('Start cycle:', 6, 17,  1, 4)
        end_2b_label   = create_label('End cycle:',   7, 17,  1, 4)
        range_3b_label = create_label('Jason-3 (from 1 to 226)', 5, 26, 1, 9)
        srt_3b_label   = create_label('Start cycle:', 6, 26,  1, 4)
        end_3b_label   = create_label('End cycle:',   7, 26,  1, 4)
        
        srt_2b_entry = create_spinbox(1, 303, 6, 21, 1, 4, 6, 6, 4)
        end_2b_entry = create_spinbox(1, 303, 7, 21, 1, 4, 6, 6, 4)
        srt_3b_entry = create_spinbox(1, 226, 6, 31, 1, 4, 6, 6, 4)
        end_3b_entry = create_spinbox(1, 226, 7, 31, 1, 4, 6, 6, 4)
            
        widgets_to_display.extend([range_2b_label,srt_2b_label,end_2b_label,srt_2b_entry,end_2b_entry,  range_3b_label,srt_3b_label,end_3b_label,srt_3b_entry,end_3b_entry])
                    
    def open_directory_dialog():
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)
            
    def create_error_warning():
        validation_window = tk.Toplevel(pop_up_window)
        validation_window.title('Inputs validation')
        validation_window.geometry('{}x{}'.format(int(screen_width/4), int(screen_height/6)))
        validation_window.configure(background = error_color) 
        label = tk.Label(validation_window, text = 'Error! Enter valid inputs!', font=("Arial", TEXT, 'bold'), fg='red',bg= error_color)
        label.place(relx=0.5, rely=0.4, anchor="center")
        ok_button = tk.Button(validation_window, text='OK', font=("Arial",TEXT), fg='black',command=validation_window.destroy)
        ok_button.place(relx=0.5, rely=0.8, anchor="center")
        
    def validate_series_input(start, end):
        if start == '' or end == '':
            create_error_warning()
        else:
            try:
                start, end = int(start), int(end)
                if start > end:
                    create_error_warning()
            except ValueError:
                create_error_warning()
            
    def get_inputs():
        def return_inputs():
            pop_up_window.after(1, pop_up_window.destroy())
            callback(Username_aviso, Password_aviso, int(Series), int(Pass), int(Start_2), int(End_2), int(Start_3), int(End_3), Output_dir, Output_file, float(min_lat), float(max_lat), float(min_lon), float(max_lon), api_key, hgt_dem_diff_thrd, wo_thrd, W, sigma)
        try:
            Start_2, End_2, Start_3, End_3 = 0,0,0,0
            Username_aviso = username_aviso_entry.get()
            Password_aviso = password_aviso_entry.get()
            Pass = pass_entry.get()
            Series = series_var.get()
            Output_file = output_file_entry.get()
            Output_dir  = directory_entry.get()
            min_lat = min_lat_entry.get()
            max_lat = max_lat_entry.get()
            min_lon = min_lon_entry.get()
            max_lon = max_lon_entry.get() 
            api_key = api_key_entry.get()
            hgt_dem_diff_thrd =  h_thrd_entry.get()
            wo_thrd = wo_thrd_entry.get()
            W = W_entry.get()
            sigma = sigma_entry.get()
            if Series == '2':
                Start_2 = srt_2o_entry.get()
                End_2   = end_2o_entry.get()
                validate_series_input(Start_2, End_2)
          
            if Series == '3':
                Start_3 = srt_3o_entry.get()
                End_3   = end_3o_entry.get()
                validate_series_input(Start_3, End_3)

            if Series == '1':
                Start_2 = srt_2b_entry.get()
                End_2   = end_2b_entry.get()
                Start_3 = srt_3b_entry.get()
                End_3   = end_3b_entry.get()
                validate_series_input(Start_2, End_2)
                validate_series_input(Start_3, End_3)

                
            if Username_aviso=='' or Password_aviso=='' or Series=='' or Pass=='' or min_lat=='' or max_lat=='' or max_lon=='' or min_lon=='' or api_key == '':
                create_error_warning()
            else:
                try:
                    int(Series), int(Pass), float(min_lat), float(max_lat), float(min_lon), float(max_lon)
                except ValueError:
                    create_error_warning()
                else:
                    if (abs(float(min_lat)) > 60) or (abs(float(max_lat)) > 80) or (float(min_lat) >= float(max_lat)):   
                        create_error_warning()
                    else:
                        return_inputs()
        except ValueError:
            create_error_warning()

    window_width = int(3 * screen_width / 5)
    window_height = int(3 * screen_height / 5)
    pop_up_window = tk.Tk()
    pop_up_window.title('JASTER')
    pop_up_window.geometry('{}x{}'.format(window_width, window_height))
    pop_up_window.configure(background = background_color)
# -------------------------------------------------------------------------------------------------------   
    
    # Create grid
# -------------------------------------------------------------------------------------------------------   
    rows = 20
    columns = 40
    for i in range(rows):
        pop_up_window.grid_rowconfigure(i,    weight=1, minsize=int(window_height/rows - 10),  uniform='group1')
    for i in range(columns):
        pop_up_window.grid_columnconfigure(i, weight=1, minsize=int(window_width/columns - 10), uniform='group1')             
# -------------------------------------------------------------------------------------------------------   

    # Get AVISO Username and Password, and OpenTopography API Key
# -------------------------------------------------------------------------------------------------------
    username_aviso_label = create_label('AVISO Username:',  3, 1,  1, 7)
    password_aviso_label = create_label('AVISO Password:',  3, 18, 1, 7)
    username_aviso_entry = create_entry('', 3,  9, 7)
    password_aviso_entry = create_entry('*',3, 25, 7)
    password_aviso_button= create_button('Show', aviso_password_visibility, int(4*TEXT/5), 3, 35, 6, 6, 3, 1)
    api_key_label = create_label('OpenTopography API Key:',  4, 1,  1, 10)
    api_key_entry = create_entry('', 4,  11, 23)
# -------------------------------------------------------------------------------------------------------    

    # Get Series and Pass number
# -------------------------------------------------------------------------------------------------------
    series_label = create_label('Jason Series:',  5, 1,  1, 6)
    widgets_to_display = []
    series_var = tk.StringVar()
    series_button_1 = create_radiobutton('2',    series_var, 2, update_cycle_text, 5, 6,  1, 2)
    series_button_2 = create_radiobutton('3',    series_var, 3, update_cycle_text, 5, 8,  1, 2)
    series_button_3 = create_radiobutton('Both', series_var, 1, update_cycle_text, 5, 10, 1, 3)
    pass_label = create_label('Pass number:\n (from 1 to 254)', 6, 1,  2, 6)
    pass_entry = create_spinbox(1, 254, 6, 7, 2, 6, 15, 6, 4)  
# -------------------------------------------------------------------------------------------------------

    # Get Max & Min Latitude and Longitude
# -------------------------------------------------------------------------------------------------------
    max_lat_entry = tk.Entry(pop_up_window,  **lat_lon_par)
    max_lon_entry = tk.Entry(pop_up_window,  **lat_lon_par)
    min_lat_entry = tk.Entry(pop_up_window,  **lat_lon_par)
    min_lon_entry = tk.Entry(pop_up_window,  **lat_lon_par)
    validate_max_lat_cmd = pop_up_window.register(lambda P, entry=max_lat_entry: validate_lat_lon_input(P, entry))
    validate_max_lon_cmd = pop_up_window.register(lambda P, entry=max_lon_entry: validate_lat_lon_input(P, entry))
    validate_min_lat_cmd = pop_up_window.register(lambda P, entry=min_lat_entry: validate_lat_lon_input(P, entry))
    validate_min_lon_cmd = pop_up_window.register(lambda P, entry=min_lon_entry: validate_lat_lon_input(P, entry))
    max_lat_entry['validatecommand'] = (validate_max_lat_cmd, '%P')
    max_lon_entry['validatecommand'] = (validate_max_lon_cmd, '%P')
    min_lat_entry['validatecommand'] = (validate_min_lat_cmd, '%P')
    min_lon_entry['validatecommand'] = (validate_min_lon_cmd, '%P')
    
    min_lat_entry.grid(row=10, column=8, columnspan=6, sticky='ew')
    max_lat_entry.grid(row=11, column=8, columnspan=6, sticky='ew')
    min_lon_entry.grid(row=10, column=28, columnspan=6, sticky='ew')
    max_lon_entry.grid(row=11, column=28, columnspan=6, sticky='ew')
    
    lat_label = create_label('Latitude: from 80 to -60 deg  (or from 80N to 60S)',     9, 1,  1, 17)
    lon_label = create_label('Longitude: from 179 to -180 deg (or from 179E to 180W)', 9, 19, 1, 20)
    min_lat_label = create_label('Minimum Latitude:',  10, 1,   1, 7)
    #min_lat_entry = create_entry('',10,7,9)
    max_lat_label = create_label('Maximum Latitude:',  11, 1,  1, 7)
    min_lon_label = create_label('Minimum Longitude:', 10, 19,   1, 7)
    max_lon_label = create_label('Maximum Longitude:', 11, 19,  1, 7)
# -------------------------------------------------------------------------------------------------------

    # Establish an output directory
# -------------------------------------------------------------------------------------------------------
    output_dir_label = create_label('Output directory*:', 12, 1, 1, 6)
    directory_entry  = create_entry('', 12, 8, 6)        
    output_dir_button= create_button('Select', open_directory_dialog, int(4*TEXT/5), 13, 11, 6, 6, 2, 1)
    output_file_label = create_label('Output folder name*:', 12, 19,  1, 7)
    output_file_entry = create_entry('', 12, 28, 6)
# -------------------------------------------------------------------------------------------------------    

    # Get optional thresholds
# -------------------------------------------------------------------------------------------------------

    dem_label = create_label('SRTM DEM-based outlier detection parameters*:', 14, 1, 1, 17)
    h_thrd_label = create_label('Height threshold* (default 5 m):', 15, 1, 1, 12)
    h_thrd_entry = create_entry('', 15,  15, 1)
    wo_thrd_label = create_label('Water occurrence threshold* (default 50):',  16, 1, 1, 14)
    wo_thrd_entry = create_entry('', 16,  15, 1)
    
    hampel_label = create_label('Hampel filter parameters* (set window to 0 to disable):', 14, 19, 1, 18)
    W_label = create_label('Window size* 0-20 (default 0):', 15, 19,  1, 13)
    W_entry = create_entry('', 15,  30, 2)
    
    sigma_label = create_label('Sensitivity* 0.1-5.0 (default 3):', 16, 19, 1, 13)
    sigma_entry = create_entry('', 16,  30, 2)   
# -------------------------------------------------------------------------------------------------------    

    # Create LOGOs and labels
# -------------------------------------------------------------------------------------------------------
    image_UH = PhotoImage(file='UH_Logo.png')
    image_UH_label = tk.Label(pop_up_window, image=image_UH , bg=pop_up_window.cget('bg'))
    image_UH_label.grid(row=0, column=0, columnspan=7, rowspan=2, sticky='nsew')
    
    
    image_NASA = PhotoImage(file='logo_NASA.png')
    image_NASA_label = tk.Label(pop_up_window, image=image_NASA, bg=pop_up_window.cget('bg'))
    image_NASA_label.grid(row=0, column=36, columnspan=2, rowspan=2, sticky='nsew')
    
    opt_frame = tk.Frame(pop_up_window, relief='solid')
    opt_frame.grid(row=18, column=1, rowspan=1, columnspan=6, sticky='nsew')
    opt_label = tk.Label(opt_frame, text='* - optional fields', font=('Arial', TEXT, 'italic'), fg='black', bg= background_color, anchor='w')
    opt_label.pack(expand=True, fill='both')
   
    greetings_frame = tk.Frame(pop_up_window, relief='solid')
    greetings_frame.grid(row=0, column=10, rowspan=2, columnspan=21, sticky='nsew')
    greetings_label = tk.Label(greetings_frame, text='Welcome to JASTER \n (Jason Altimetry Stand-alone Tool for Enhanced Research)', font=("Cubano", int(21-2*z), 'bold'), fg='black', bg= background_color)
    greetings_label.pack(expand=True, fill='both') 
    
    
    
    author_frame = tk.Frame(pop_up_window, relief='solid')
    author_frame.grid(row=18, column=24, rowspan=3, columnspan=15, sticky='nsew')
    author_label = tk.Label(author_frame, text='Developed by Natalya Maslennikova (nmaslenn@cougarnet.uh.edu) \n Amirhossein Rostami (arostami@cougarnet.uh.edu) \n Chi-Hung Chang (cchang37@cougarnet.uh.edu) \n Hyongki Lee (hlee45@central.uh.edu)', font=("DIN Alternate", int(11-z),'bold'), fg='crimson', bg= background_color)
    author_label.pack(expand=True, fill='both')
# -------------------------------------------------------------------------------------------------------
    
    submit_button = create_button('Submit', get_inputs, int(18-z/2), 18, 16, 12, 2, 5, 2) 
    
    pop_up_window.mainloop()