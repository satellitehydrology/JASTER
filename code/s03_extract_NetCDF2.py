import sys, os, requests, glob, netCDF4, shutil
import numpy as np
import tkinter as tk
from s00_get_system_parameters import window_width, window_height, TEXT

data_dir, file_dir = sys.argv[1], sys.argv[2]
Series, Pass, Start, End = int(sys.argv[3]),int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
min_lat, max_lat =  float(sys.argv[7]),float(sys.argv[8])

def detect_missing_data(var_FillValue, number):
    if number == var_FillValue:
        data_Flag=1
    else:
        data_Flag=0
    return data_Flag


model_dry_tropo_corr_FV = 3.2767
model_wet_tropo_corr_FV = 3.2767
iono_corr_gim_ku_FV     = 3.2767
solid_earth_tide_FV     = 3.2767
pole_tide_FV            = 3.2767

lat_20hz_FV              = 2147.483647
lon_20hz_FV              = 2147.483647
time_20hz_FV             = 1.8446744073709552e19
ice_range_20hz_ku_FV     = 1514748.3647
ice_qual_flag_20hz_ku_FV = 127
ice_sig0_20hz_ku_FV      = 327.67
alt_20hz_FV              = 1514748.3647
alt_state_flag_ku_band_status_FV = 127
lat_sc = 0.000001
lon_sc = 0.000001

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

        lat=data.variables['lat'][:]
        lon=data.variables['lon'][:]

        lat_20hz=data.variables['lat_20hz'][:]
        lon_20hz=data.variables['lon_20hz'][:]   
        time_20hz=data.variables['time_20hz'][:]
        ice_range_20hz_ku=data.variables['ice_range_20hz_ku'][:]
        ice_qual_flag_20hz_ku=data.variables['ice_qual_flag_20hz_ku'][:]
        ice_sig0_20hz_ku=data.variables['ice_sig0_20hz_ku'][:]
        alt_20hz=data.variables['alt_20hz'][:]
        alt_state_flag_ku_band_status=data.variables['alt_state_flag_ku_band_status'][:]

        model_dry_tropo_corr=data.variables['model_dry_tropo_corr'][:] 
        model_wet_tropo_corr=data.variables['model_wet_tropo_corr'][:]
        iono_corr_gim_ku=data.variables['iono_corr_gim_ku'][:]
        solid_earth_tide=data.variables['solid_earth_tide'][:]
        pole_tide=data.variables['pole_tide'][:]

        for p in range(len(lat)):
            if lat[p] < min_lat or lat[p] > max_lat:
                continue
            dry_count  = 1 if model_dry_tropo_corr[p] == model_dry_tropo_corr_FV else 0
            wet_count  = 1 if model_wet_tropo_corr[p] == model_wet_tropo_corr_FV else 0
            iono_count = 1 if iono_corr_gim_ku[p] == iono_corr_gim_ku_FV else 0
            sTide_count= 1 if solid_earth_tide[p] == solid_earth_tide_FV else 0
            pTide_count= 1 if pole_tide[p] == pole_tide_FV else 0
            kFlag_count= 1 if alt_state_flag_ku_band_status[p] != 0 else 0
            media_corr = model_dry_tropo_corr[p] + model_wet_tropo_corr[p] + iono_corr_gim_ku[p] + solid_earth_tide[p] + pole_tide[p]
            for q in range(len(lat_20hz[0,:])):
                lat_count= 1 if lat_20hz[p,q] == lat_20hz_FV  else 0
                ice_count= 1 if ice_qual_flag_20hz_ku[p,q]!=0 else 0

                mjd_20hz = time_20hz[p,q] / 86400 + 51544
                icehgt_20hz = alt_20hz[p,q] - media_corr - ice_range_20hz_ku[p,q]
                Flags=dry_count+ wet_count+ iono_count+ sTide_count+pTide_count+ kFlag_count+ lat_count+ ice_count
                if Flags == 0:
                    if np.ma.is_masked(mjd_20hz) or np.ma.is_masked(lon_20hz[p,q]) or np.ma.is_masked(lat_20hz[p,q]) or np.ma.is_masked(icehgt_20hz) or np.ma.is_masked(ice_sig0_20hz_ku[p,q]):
                        pass
                    else:
                        text_file.write('%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%4s\t%20.6f\t%20.6f\t%20.6f\t%20.6f\t%10.3f\n'%(0, 0, 0, 0, 0, 0, 0, 0, 0, single_name[12:15], mjd_20hz,  lon_20hz[p,q], lat_20hz[p,q], icehgt_20hz, ice_sig0_20hz_ku[p,q]))
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