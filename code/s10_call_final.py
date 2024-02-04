from s08_get_final_results import get_finals

from s09_create_txt_and_plots import export_txt
from s09_create_txt_and_plots import create_single_plot_one
from s09_create_txt_and_plots import create_single_plot_both
from s09_create_txt_and_plots import compare_plot_one
from s09_create_txt_and_plots import compare_plot_both

import tkinter as tk
import sys
from s00_get_system_parameters import window_width, window_height, TEXT

Series, Pass, SRTM_DEM_WGS84_dir, WOM_dir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
min_lat, max_lat, min_lon, max_lon  = float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])
hgt_dem_diff_thrd, wo_thrd, hgt_cyc_range_thrd = int(sys.argv[9]), int(sys.argv[10]), int(sys.argv[11])
hgt_cyc_std_thrd, data_dir, file_dir = float(sys.argv[12]), sys.argv[13], sys.argv[14]
W, sigma = int(sys.argv[15]), float(sys.argv[16])


root = tk.Tk()
root.geometry('{}x{}'.format(window_width, window_height))
root.configure(background = 'bisque')
root.title('Time series generation')
label1 = tk.Label(root, text='Time series generation started', font=("Arial", TEXT),  background = 'bisque') 
label1.place(relx=0.5, rely=0.35, anchor='center')
root.update()
root.after(10) 

if Series == 3:
    
    ip3, FinalSeries_iqr3, FinalSeries_dem_wo3, index_retain_dem_wo3  = get_finals(Series, Pass, SRTM_DEM_WGS84_dir,  WOM_dir, min_lat, max_lat, min_lon, max_lon, hgt_dem_diff_thrd, wo_thrd, hgt_cyc_range_thrd, hgt_cyc_std_thrd, data_dir, file_dir)
    out_basename = 'Janon{}_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(Series, min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    export_txt(ip3, FinalSeries_iqr3,    file_dir, out_basename, 'IQR',  W, sigma)
    export_txt(ip3, FinalSeries_dem_wo3, file_dir, out_basename, 'SRTM', W, sigma)
    create_single_plot_one(ip3, FinalSeries_iqr3,   Pass, file_dir,out_basename, 'IQR',      Series, min_lat, max_lat, min_lon, max_lon, W, sigma)
    create_single_plot_one(ip3, FinalSeries_dem_wo3,Pass, file_dir,out_basename, 'SRTM DEM', Series, min_lat, max_lat, min_lon, max_lon, W, sigma)
    FinalSeries_list = [FinalSeries_iqr3, FinalSeries_dem_wo3]
    colors = ['red', 'blue']
    list_of_methods = ['IQR', 'SRTM']
    compare_plot_one(ip3, FinalSeries_list, Pass, list_of_methods, file_dir, out_basename, 'both', Series, min_lat, max_lat, min_lon, max_lon, colors, W, sigma)


if Series == 2:
    ip2, FinalSeries_iqr2, FinalSeries_dem_wo2, index_retain_dem_wo2  = get_finals(Series, Pass, SRTM_DEM_WGS84_dir,  WOM_dir, min_lat, max_lat, min_lon, max_lon, hgt_dem_diff_thrd, wo_thrd, hgt_cyc_range_thrd, hgt_cyc_std_thrd, data_dir, file_dir)
    out_basename = 'Janon{}_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(Series, min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    export_txt(ip2, FinalSeries_iqr2,    file_dir, out_basename, 'IQR',  W, sigma)
    export_txt(ip2, FinalSeries_dem_wo2, file_dir, out_basename, 'SRTM', W, sigma)
    create_single_plot_one(ip2, FinalSeries_iqr2,   Pass, file_dir,out_basename, 'IQR',      Series, min_lat, max_lat, min_lon, max_lon, W, sigma)
    create_single_plot_one(ip2, FinalSeries_dem_wo2,Pass, file_dir,out_basename, 'SRTM DEM', Series, min_lat, max_lat, min_lon, max_lon, W, sigma)
    FinalSeries_list = [FinalSeries_iqr2, FinalSeries_dem_wo2]
    colors = ['red', 'blue']
    list_of_methods = ['IQR', 'SRTM']
    compare_plot_one(ip2, FinalSeries_list, Pass, list_of_methods, file_dir, out_basename, 'both', Series, min_lat, max_lat, min_lon, max_lon, colors, W, sigma)


if Series == 1:
    ip3, FinalSeries_iqr3, FinalSeries_dem_wo3, index_retain_dem_wo3  = get_finals(3, Pass, SRTM_DEM_WGS84_dir,  WOM_dir, min_lat, max_lat, min_lon, max_lon, hgt_dem_diff_thrd, wo_thrd, hgt_cyc_range_thrd, hgt_cyc_std_thrd, data_dir, file_dir)
    ip2, FinalSeries_iqr2, FinalSeries_dem_wo2, index_retain_dem_wo2  = get_finals(2, Pass, SRTM_DEM_WGS84_dir,  WOM_dir, min_lat, max_lat, min_lon, max_lon, hgt_dem_diff_thrd, wo_thrd, hgt_cyc_range_thrd, hgt_cyc_std_thrd, data_dir, file_dir)
    out_basename = 'Janon2_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    export_txt(ip2, FinalSeries_iqr2,    file_dir, out_basename, 'IQR',  W, sigma)
    export_txt(ip2, FinalSeries_dem_wo2, file_dir, out_basename, 'SRTM', W, sigma)
    
    out_basename = 'Janon3_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    export_txt(ip3, FinalSeries_iqr3,    file_dir, out_basename, 'IQR',  W, sigma)
    export_txt(ip3, FinalSeries_dem_wo3, file_dir, out_basename, 'SRTM', W, sigma)
    
    out_basename = 'Janon2_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    create_single_plot_one(ip2, FinalSeries_iqr2,    Pass,file_dir,out_basename, 'IQR',  2, min_lat, max_lat, min_lon, max_lon, W, sigma)
    create_single_plot_one(ip2, FinalSeries_dem_wo2, Pass,file_dir,out_basename, 'SRTM', 2, min_lat, max_lat, min_lon, max_lon, W, sigma)
    
    out_basename = 'Janon3_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    create_single_plot_one(ip3, FinalSeries_iqr3,    Pass,file_dir,out_basename, 'IQR',  3, min_lat, max_lat, min_lon, max_lon, W, sigma)
    create_single_plot_one(ip3, FinalSeries_dem_wo3, Pass,file_dir,out_basename, 'SRTM', 3, min_lat, max_lat, min_lon, max_lon, W, sigma)
    
    out_basename = 'Janon2both_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    FinalSeries_list_2 = [FinalSeries_iqr2, FinalSeries_dem_wo2]
    colors = ['red', 'blue']
    list_of_methods = ['IQR', 'SRTM']
    compare_plot_one(ip3, FinalSeries_list_2, Pass, list_of_methods, file_dir, out_basename, 'both', 2, min_lat, max_lat, min_lon, max_lon, colors, W, sigma)
    
    out_basename = 'Janon3both_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    FinalSeries_list_3 = [FinalSeries_iqr3, FinalSeries_dem_wo3]
    compare_plot_one(ip3, FinalSeries_list_3, Pass, list_of_methods, file_dir, out_basename, 'both', 3, min_lat, max_lat, min_lon, max_lon, colors, W, sigma)

    out_basename = 'Janon2and3_IQR_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    create_single_plot_both(ip2,ip3,FinalSeries_iqr2,FinalSeries_iqr3, Pass, file_dir, out_basename, 'IQR', min_lat, max_lat, min_lon, max_lon, W, sigma)
    out_basename = 'Janon2and3_SRTM_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    create_single_plot_both(ip2,ip3,FinalSeries_dem_wo2,FinalSeries_dem_wo3, Pass, file_dir, out_basename, 'SRTM', min_lat, max_lat, min_lon, max_lon, W, sigma)
    
    colors2 = ['red', 'blue']
    colors3 = ['black', 'green']
    out_basename = 'Janon_all_lat{}_{}_Hthrd{}_Wthrd{}_W{}_S{}'.format(min_lat, max_lat, hgt_dem_diff_thrd, wo_thrd, W, sigma)
    compare_plot_both(ip2, ip3, FinalSeries_list_2, FinalSeries_list_3, Pass, list_of_methods, file_dir, out_basename, 'both', min_lat, max_lat, min_lon, max_lon, colors2, colors3, W, sigma)


def destroy_root():
    root.after(1, root.destroy())

close_button1 = tk.Button(root, text='Close', font=('Arial', TEXT), command=destroy_root)
close_button1.place(relx=0.5, rely=0.75, anchor='center')
label1 = tk.Label(root, text='Time series generation complete', font=("Arial", TEXT),  background = 'bisque') 
label1.place(relx=0.5, rely=0.35, anchor='center')
root.update()
root.after(50000, destroy_root) 
root.mainloop() 
