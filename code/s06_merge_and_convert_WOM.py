import rasterio as rio
from rasterio.merge import merge
import shutil, os, subprocess
import tkinter as tk
from s00_get_system_parameters import window_width, window_height, TEXT

def merge_and_convert_wom(new_folder_dir, curdir, download_list_WOM):
    
    os.makedirs(os.path.join(curdir,new_folder_dir), exist_ok=True)

    WOM_dir = os.path.join(new_folder_dir, 'WOM.tif')
    dir_for_WOMs =  os.path.join(curdir, 'Water_Occurrence_Maps')
    
    root = tk.Tk()
    root.geometry('{}x{}'.format(window_width, window_height))
    root.configure(background = 'bisque')
    root.title('Data merging and conversion')
    result_label = tk.Label(root, text='', font=('Arial', TEXT),  fg='black', bg='bisque')
    result_label.place(relx=0.5, rely=0.35, anchor='center')  
    

    if len(download_list_WOM) > 1:
        result_label.config(text = 'WOMs merging started')
        root.update()
        root.after(2000)
        src_files_to_mosaic = []
        for wom in download_list_WOM:
            src = rio.open(os.path.join(dir_for_WOMs,wom))
            src_files_to_mosaic.append(src)
        mosaic, out_trans = merge(src_files_to_mosaic)
        out_meta = src.meta.copy()
        out_meta.update({'driver': 'GTiff','compress': 'lzw','height': mosaic.shape[1],'width': mosaic.shape[2],'transform': out_trans,'crs': 'epsg:4326'})
        with rio.open(WOM_dir, 'w', **out_meta) as tif:
            tif.write(mosaic)  
        result_label.config(text = 'WOMs merging complete')
        root.update()
        root.after(2000)
    else:
        source_dir = os.path.join(dir_for_WOMs, download_list_WOM[0])
        shutil.copy(source_dir, WOM_dir)    
        result_label.config(text = 'WOM transfer complete')
        root.update()
        root.after(2000)
      
    def destroy_root():
        root.after(1, root.destroy())
    close_button = tk.Button(root, text="Close", font=('Arial', TEXT), command=destroy_root)
    close_button.place(relx=0.5, rely=0.75, anchor='center')
    root.after(5000, destroy_root) 
    root.mainloop()

        
            