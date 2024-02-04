import sys, os, requests, glob, netCDF4, shutil
import numpy as np
import tkinter as tk
from s00_get_system_parameters import window_width, window_height, TEXT

data_dir, file_dir = sys.argv[1], sys.argv[2]
Series, Pass, Start, End = int(sys.argv[3]),int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
min_lat, max_lat =  float(sys.argv[7]),float(sys.argv[8])

iono_corr_gim_ku_FV     = 3.2767
solid_earth_tide_FV     = 3.2767
pole_tide_FV            = 3.2767
model_dry_tropo_corr_FV = 3.2767
model_wet_tropo_corr_FV = 3.2767

alt_20hz_FV           = 1514748.3647
ice_range_20hz_ku_FV  = 1514748.3647
ice_sig0_20hz_ku_FV   = 327.67
        
lat_20hz_FV = 2147.483647
lon_20hz_FV = 2147.483647

savepath = file_dir+'/j{}_{:03d}/'.format(Series,Pass) 
try:
    os.makedirs(os.path.dirname(savepath))
except:
    shutil.rmtree(savepath)
    os.makedirs(os.path.dirname(savepath))
complete_name = os.path.join(savepath, 'j{}_p{:03d}_{}_{}_info.txt'.format(Series,Pass, min_lat, max_lat))

text_file = open(complete_name,"w")

count = 0
all_path = glob.glob(data_dir+'/j{}_{:03d}/'.format(Series,Pass)+'cycle_*'+'/*.nc')   
all_path.sort()

root = tk.Tk()
root.geometry('{}x{}'.format(window_width, window_height))
root.configure(background = 'bisque')
root.title('NetCDF extraction from Jason-{}'.format(Series))

result_label = tk.Label(root, text='Extraction started', font=('Arial', TEXT), fg='black', bg='bisque')
result_label.place(relx=0.5, rely=0.35, anchor='center')
root.update()
root.after(1000) 
        
for single_path in all_path:
    try:
        single_name = os.path.basename(single_path)
        data=netCDF4.Dataset(single_path)    
        iono_corr_gim_ku     = data.groups['data_01'].groups['ku'].variables['iono_cor_gim'][:]
        solid_earth_tide     = data.groups['data_01'].variables['solid_earth_tide'][:]
        pole_tide            = data.groups['data_01'].variables['pole_tide'][:]
        model_dry_tropo_corr = data.groups['data_20'].variables['model_dry_tropo_cor_measurement_altitude'][:]
        model_wet_tropo_corr = data.groups['data_20'].variables['model_wet_tropo_cor_measurement_altitude'][:]

        indx_20hzIn01hz = data.groups['data_20'].variables['index_1hz_measurement'][:]

        alt_20hz  = data.groups['data_20'].variables['altitude'][:]
        lat_20hz  = data.groups['data_20'].variables['latitude'][:]
        lon_20hz  = data.groups['data_20'].variables['longitude'][:]
        time_20hz = data.groups['data_20'].variables['time'][:]

        ice_range_20hz_ku     = data.groups['data_20'].groups['ku'].variables['range_ocog'][:]
        ice_sig0_20hz_ku      = data.groups['data_20'].groups['ku'].variables['sig0_ocog'][:]
        ice_qual_flag_20hz_ku = data.groups['data_20'].groups['ku'].variables['ocog_qual'][:]
        alt_state_band_status_flag=data.groups['data_01'].groups['ku'].variables['alt_state_band_status_flag'][:]


        for p in range(len(alt_20hz)):
            if lat_20hz[p] < min_lat or lat_20hz[p] > max_lat:
                continue
            wet_count  = 1 if model_wet_tropo_corr[p] == model_wet_tropo_corr_FV else 0
            dry_count  = 1 if model_dry_tropo_corr[p] == model_dry_tropo_corr_FV else 0
            iono_count = 1 if iono_corr_gim_ku[indx_20hzIn01hz[p]] == iono_corr_gim_ku_FV else 0
            sTide_count= 1 if solid_earth_tide[indx_20hzIn01hz[p]] == solid_earth_tide_FV else 0
            pTide_count= 1 if pole_tide[indx_20hzIn01hz[p]] == pole_tide_FV else 0
            kFlag_count= 1 if alt_state_band_status_flag[indx_20hzIn01hz[p]] != 0 else 0
            lat_count  = 1 if lat_20hz[p] == lat_20hz_FV else 0
            ice_count  = 1 if ice_qual_flag_20hz_ku[p] != 0 else 0

            media_corr = model_dry_tropo_corr[p] + model_wet_tropo_corr[p] + iono_corr_gim_ku[indx_20hzIn01hz[p]] + solid_earth_tide[indx_20hzIn01hz[p]] + pole_tide[indx_20hzIn01hz[p]]  

            mjd_20hz = time_20hz[p]/86400 + 51544
            icehgt_20hz = alt_20hz[p] - media_corr - ice_range_20hz_ku[p] + 0.7
            Flags=dry_count+ wet_count+ iono_count+ sTide_count+pTide_count + kFlag_count+ lat_count+ ice_count
            if Flags == 0:
                if np.ma.is_masked(mjd_20hz) or np.ma.is_masked(lon_20hz[p]) or np.ma.is_masked(lat_20hz[p]) or np.ma.is_masked(icehgt_20hz) or np.ma.is_masked(ice_sig0_20hz_ku[p]):
                    pass
                else:
                    text_file.write('%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%20.6f\t%20.6f\t%20.6f\t%20.6f\t%10.3f\n'%(0, 0, 0, 0, 0, 0, 0, 0, 0, single_name[12:15], mjd_20hz, lon_20hz[p], lat_20hz[p], icehgt_20hz, ice_sig0_20hz_ku[p]))
        count += 1      
        result_label.config(text='{:6.2f} % complete'.format(100 * count / len(all_path)))
        root.update()
        root.after(100)
    except:
        count += 1      
        result_label.config(text='{:6.2f} % complete'.format(100 * count / len(all_path)))
        root.update()
        root.after(100)
        
text_file.close()

result_label.config(text = 'Data extraction complete')
root.update()
root.after(2000)
def destroy_root():
        root.after(1, root.destroy())
close_button = tk.Button(root, text="Close", font=('Arial', TEXT), command=destroy_root)
close_button.place(relx=0.5, rely=0.75, anchor='center')
root.after(5000, root.destroy) 
root.mainloop()