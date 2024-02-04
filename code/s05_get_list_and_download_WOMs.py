import  os, subprocess, requests
import tkinter as tk
from s00_get_system_parameters import window_width, window_height, TEXT

def download_WOMs(min_lat, max_lat, min_lon, max_lon, curdir):

    min_lat, max_lat  =  min_lat + 10, max_lat + 10

    longitude_min = 'E' if min_lon >= 0 else 'W'
    longitude_max = 'E' if max_lon >= 0 else 'W'
    latitude_min  = 'N' if min_lat >= 0 else 'S'
    latitude_max  = 'N' if max_lat >= 0 else 'S'


    if latitude_max == latitude_min:
        if latitude_min == 'N' :
            lat_list = ['{}N'.format(int(i*10)) for i in range(int(abs(min_lat) // 10), int(abs(max_lat) // 10) + 1)]
        else:
            lat_list = ['{}S'.format(int(i*10)) for i in range(int(abs(max_lat) // 10)+1, int(abs(min_lat) // 10) + 2)]

    else:
        positive_lat_list = ['{}N'.format(int(i*10)) for i in range(0, int(abs(max_lat) // 10) + 1)]
        if abs(min_lat) % 10 == 0:
            negative_lat_list = ['{}S'.format(int(i*10)) for i in range(int(abs(min_lat) // 10), 0, -1)]
        else:
            negative_lat_list = ['{}S'.format(int(i*10)) for i in range(int(abs(min_lat) // 10) + 1, 0, -1)]
        lat_list = positive_lat_list + negative_lat_list

    if longitude_max == longitude_min:
        if longitude_min == 'E':
            lon_list = ['{}E'.format(int(i*10)) for i in range(int(abs(min_lon) // 10), int(abs(max_lon) // 10) + 1)]
        else:
            lon_list = ['{}W'.format(int(i*10)) for i in range(int(abs(max_lon) // 10)+1, int(abs(min_lon) // 10) + 2)]

    else:
        positive_lon_list = ['{}E'.format(int(i*10)) for i in range(0, int(abs(max_lon) // 10) + 1)]
        if abs(min_lat) % 5 == 0:
            negative_lon_list = ['{}W'.format(int(i*10)) for i in range(int(abs(min_lon) // 10), 0, -1)]
        else:
            negative_lon_list = ['{}W'.format(int(i*10)) for i in range(int(abs(min_lon) // 10) + 1, 0, -1)]
        lon_list = positive_lon_list + negative_lon_list


    root = tk.Tk()
    root.geometry('{}x{}'.format(window_width, window_height))

    root.configure(background = 'bisque')
    root.title('Water Occurrence Maps (WOMs) Download')
    
    message = 'Following Water Occurrence Maps (WOMs) were requested: \n'
    
    result_label = tk.Label(root, text='', font=('Arial', TEXT),  fg='black', bg='bisque')

    count = 1
    download_list = []    
    for lat_num in lat_list:
        for lon_num in lon_list:
            download_list.append('occurrence_{}_{}v1_4_2021.tif'.format(lon_num, lat_num))
            message += '{:4d}. occurrence_{}_{}v1_4_2021.tif \n'.format(count, lon_num, lat_num)
            count += 1
    
    result_label.config(text=message)
    result_label.place(relx=0.5, rely=0.35, anchor='center')
    root.update()
    root.after(2000) 


    download_dir = curdir+'/Water_Occurrence_Maps'
    os.makedirs(download_dir, exist_ok=True)

    for download_file in download_list:
        tiff_path   = os.path.join(download_dir, download_file)
        if os.path.exists(tiff_path):
            result_label.config(text = 'occurrence_{}_{}v1_4_2021.tif already exists'.format(lon_num, lat_num))
            root.update()
            root.after(2000)
        else:
            url = 'https://storage.googleapis.com/global-surface-water/downloads2021/occurrence/{}'.format(download_file)
            result_label.config(text = 'Download of {} started'.format(download_file))
            root.update()
            root.after(2000)
            
            download_dir_file = os.path.join(download_dir, download_file)
            responce = requests.get(url, stream=True)
            if responce.status_code == 200:
                with open(download_dir_file, 'wb') as f:
                    for chunk in responce.iter_content(chunk_size = 4096):
                        if chunk:
                            f.write(chunk)
                result_label.config(text = 'Download of {} complete'.format(download_file))
                root.update()
                root.after(2000)
            else:
                result_label.config(text = 'Failed to download {}'.format(download_file))
                root.update()
                root.after(2000)
                
    def destroy_root():
        root.after(1, root.destroy())
    
    close_button = tk.Button(root, text='Close', font=('Arial', TEXT), command=destroy_root)
    close_button.place(relx=0.5, rely=0.75, anchor='center')
    root.after(5000, destroy_root) 
    root.mainloop()    
    
    return download_list