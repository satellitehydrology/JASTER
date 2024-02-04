from s00_get_system_parameters import window_width, window_height, z, TEXT
from s01_create_pop_up_menu_window import create_menu_window
import s01_create_pop_up_menu_window
from s05_get_list_and_download_WOMs import download_WOMs
from s06_merge_and_convert_WOM import merge_and_convert_wom
from s07_download_from_opentopography import download_api

from datetime import datetime
import os, subprocess, sys

from ftplib import FTP
import requests, sys
from requests.auth import HTTPBasicAuth
import tkinter as tk
from screeninfo import get_monitors

Username_aviso, Password_aviso, Series, Pass, Start_2, End_2, Start_3, End_3, Output_dir, Output_file, min_lat, max_lat, min_lon, max_lon, api_key, hgt_dem_diff_thrd, wo_thrd, W, sigma = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

def get_inputs(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19):
    global Username_aviso, Password_aviso, Series, Pass, Start_2, End_2, Start_3, End_3, Output_dir, Output_file, min_lat, max_lat, min_lon, max_lon, api_key, hgt_dem_diff_thrd, wo_thrd, W, sigma
    Username_aviso, Password_aviso, Series, Pass, Start_2, End_2, Start_3, End_3, Output_dir, Output_file, min_lat, max_lat, min_lon, max_lon, api_key, hgt_dem_diff_thrd, wo_thrd, W, sigma = a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19

s01_create_pop_up_menu_window.create_menu_window(get_inputs)

try:
    hgt_dem_diff_thrd = abs(int(hgt_dem_diff_thrd))
except:
    hgt_dem_diff_thrd = 5

try:
    wo_thrd = abs(int(wo_thrd))
except:
    wo_thrd = 50

try:
    W = abs(int(W))
    if W not in range(21):
        W = 0
except:
    W = 0

try:
    sigma = float(sigma)
    if not 0.1 <= sigma <= 5.0:
        sigma = 3.0
except:
    sigma = 3.0
    
hgt_cyc_range_thrd = 5
hgt_cyc_std_thrd = 0.3

root = tk.Tk()
root.geometry('{}x{}'.format(window_width, window_height))
root.configure(background = 'bisque')
root.title('Authorization')

label = tk.Label(root, text='', font=("Arial", TEXT),  background = 'bisque') 
label.place(relx=0.5, rely=0.2, anchor="center")

try:
    ftp=FTP('ftp-access.aviso.altimetry.fr')
    ftp.login(user=Username_aviso,passwd=Password_aviso) 
    label = tk.Label(root, text='AVISO authorization successful', font=("Arial", TEXT),  background = 'bisque') 
    label.place(relx=0.5, rely=0.3, anchor="center")
    FLAG_aviso = False
except:
    FLAG_aviso = True
    label = tk.Label(root, text='AVISO authorization failed', font=("Arial", TEXT),  background = 'bisque') 
    label.place(relx=0.5, rely=0.3, anchor="center")
    

api_url = 'https://portal.opentopography.org/API/globaldem'
params = {'demtype': 'COP30','south': '50','north': '50.1','west': '14.35','east': '14.6','outputFormat': 'GTiff','API_Key': api_key}
response = requests.get(api_url, params=params)
if response.status_code != 200:
    label = tk.Label(root, text='OpenTopography authorization failed', font=("Arial", TEXT),  background = 'bisque') 
    label.place(relx=0.5, rely=0.45, anchor="center")
    FLAG_api = True
else:
    FLAG_api = False
    label = tk.Label(root, text='OpenTopography authorization successful', font=("Arial", TEXT),  background = 'bisque') 
    label.place(relx=0.5, rely=0.45, anchor="center")

def destroy_root():
        root.after(100, root.destroy())
    
close_button = tk.Button(root, text='Close', font=('Arial', TEXT), command=destroy_root)
close_button.place(relx=0.5, rely=0.8, anchor="center")

quit_flag = 0
if (FLAG_aviso==True) or (FLAG_api==True):
    label = tk.Label(root, text='Authorization failed! The code will be terminated.', font=("Arial", TEXT,'bold'),fg='crimson',  background = 'bisque') 
    label.place(relx=0.5, rely=0.6, anchor="center")
    quit_flag = 1
else:
    root.after(5000, destroy_root) 

root.mainloop() 

if quit_flag == 1:
    sys.exit() 


parent_dir = os.path.dirname(os.getcwd())
data_dir = os.path.join(parent_dir, 'data')
os.makedirs(data_dir, exist_ok=True)
current_date_time_name = datetime.now().strftime('%Y%m%d-%H%M')

if not os.path.exists(Output_dir):
    Output_dir = os.path.join(parent_dir, 'results')
    os.makedirs(Output_dir, exist_ok=True)
if Output_file == '':
    file_dir = os.path.join(Output_dir, 'processing_{}'.format(current_date_time_name))
    os.makedirs(file_dir, exist_ok=True)
else:
    file_dir = os.path.join(Output_dir, Output_file)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)
    else:
        file_dir = os.path.join(Output_dir, 'processing_{}'.format(current_date_time_name))
        os.makedirs(file_dir, exist_ok=True)

if Series == 1:
    subprocess.call(['python', 's02_download_Jason_data.py' , data_dir, Username_aviso, Password_aviso, str(2), str(Pass), str(Start_2), str(End_2)])
    subprocess.call(['python', 's02_download_Jason_data.py' , data_dir, Username_aviso, Password_aviso, str(3), str(Pass), str(Start_3), str(End_3)])
if Series == 2:
    subprocess.call(['python', 's02_download_Jason_data.py' , data_dir, Username_aviso, Password_aviso, str(2), str(Pass), str(Start_2), str(End_2)])
if Series == 3:
    subprocess.call(['python', 's02_download_Jason_data.py' , data_dir, Username_aviso, Password_aviso, str(3), str(Pass), str(Start_3), str(End_3)])

if Series == 1:
    subprocess.call(['python', 's03_extract_NetCDF2.py', data_dir, file_dir, str(2), str(Pass), str(Start_2), str(End_2), str(min_lat),str(max_lat) ])
    subprocess.call(['python', 's04_extract_NetCDF3.py', data_dir, file_dir, str(3), str(Pass), str(Start_3), str(End_3), str(min_lat),str(max_lat) ])
if Series == 2:
    subprocess.call(['python', 's03_extract_NetCDF2.py', data_dir, file_dir, str(2), str(Pass), str(Start_2), str(End_2), str(min_lat),str(max_lat) ])
if Series == 3:
    subprocess.call(['python', 's04_extract_NetCDF3.py', data_dir, file_dir, str(3), str(Pass), str(Start_3), str(End_3), str(min_lat),str(max_lat) ])

new_folder_dir = os.path.join(file_dir, 'DEM_and_WO_processing')
os.makedirs(new_folder_dir, exist_ok=True)
download_list_WOM = download_WOMs(min_lat, max_lat, min_lon, max_lon, data_dir)
merge_and_convert_wom(new_folder_dir, data_dir, download_list_WOM)
download_api(min_lat,max_lat,min_lon,max_lon,api_key, file_dir)
SRTM_DEM_WGS84_dir  = os.path.join(file_dir, 'DEM_and_WO_processing', 'SRTM_DEM_WGS84.tif')
WOM_dir             = os.path.join(file_dir, 'DEM_and_WO_processing', 'WOM.tif')

subprocess.call(['python', 's10_call_final.py', str(Series), str(Pass), SRTM_DEM_WGS84_dir,  WOM_dir, str(min_lat), str(max_lat), str(min_lon), str(max_lon), str(hgt_dem_diff_thrd), str(wo_thrd), str(hgt_cyc_range_thrd), str(hgt_cyc_std_thrd), data_dir, file_dir, str(W), str(sigma) ])