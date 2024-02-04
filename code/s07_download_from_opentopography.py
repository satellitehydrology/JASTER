import subprocess, os, requests
import tkinter as tk
from s00_get_system_parameters import window_width, window_height, TEXT

def download_api(min_lat,max_lat,min_lon,max_lon,api_key, file_dir):
    
    api_url = 'https://portal.opentopography.org/API/globaldem'
    
    download_dir = os.path.join(file_dir, 'DEM_and_WO_processing', 'SRTM_DEM_WGS84.tif')

    params = {'demtype':'SRTMGL1_E','south': min_lat-0.1,'north': max_lat+0.1,'west': min_lon-0.1,'east': max_lon+0.1,'outputFormat': 'GTiff','API_Key': api_key}
    response = requests.get(api_url, params=params)
    
    root = tk.Tk()
    root.geometry('{}x{}'.format(window_width, window_height))
    root.configure(background = 'bisque')
    root.title('Data download from OpenTopography')
    result_label = tk.Label(root, text='SRTM DEM download started', font=('Arial', TEXT),  fg='black', bg='bisque')
    result_label.place(relx=0.5, rely=0.35, anchor='center')  
    root.update()
    root.after(2000)

    if response.status_code == 200:
        with open(download_dir, 'wb') as f:
            f.write(response.content)
        result_label.config(text='SRTM DEM download complete')
        root.update()
        root.after(2000)
    else:
        result_label.config(text='Failed to download SRTM DEM')
        root.update()
        root.after(2000)

    def destroy_root():
        root.after(1, root.destroy())
                  
    close_button = tk.Button(root, text="Close", font=('Arial', TEXT), command=destroy_root)
    close_button.place(relx=0.5, rely=0.75, anchor='center')
    root.after(5000, destroy_root) 
    root.mainloop()
