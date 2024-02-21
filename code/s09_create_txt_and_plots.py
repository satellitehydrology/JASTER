import os
import numpy as np
import matplotlib.pyplot as plt
from hampel import hampel

def export_txt(ip, FinalSeries, curdir, out_basename, prefix_name, W, sigma):
    BB0 = FinalSeries[:,[0,4,5,1]]
    if W != 0:
        elevation = FinalSeries[:,4]
        elevation_hampel = hampel(elevation, window_size=W, n_sigma=sigma)
        elevation_corr = elevation_hampel.filtered_data
        BB = np.c_[BB0, elevation_corr]
    else:
        BB = BB0
    savepath = os.path.join(curdir, 'timeseries_output')
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    filename = out_basename+'_'+prefix_name
    np.savetxt(os.path.join(savepath, filename+'.txt'), BB)

def create_single_plot_one(ip, FinalSeries, Pass, curdir, out_basename, prefix_name, Series, min_lat, max_lat, min_lon, max_lon, W, sigma):
    if W == 0:
        savepath= os.path.join(curdir, 'timeseries_output')
        filename = out_basename+'_'+prefix_name
        fig, ax = plt.subplots(figsize=(18, 14))
        ax.plot(    FinalSeries[:,1],FinalSeries[:,4], linewidth=3, color='grey', label='Jason-{}'.format(Series))
        ax.errorbar(FinalSeries[:,1],FinalSeries[:,4],FinalSeries[:,5],uplims=True,lolims=True, markersize='6', ecolor='red',capsize=4, elinewidth=3)
        ax.grid(linestyle='--')
        ax.set_xlabel('Year',fontsize=28)
        ax.set_ylabel('Water Elevation w.r.t EGM08 Geoid (m)',fontsize=28)
        ax.set_title('Line Plot with Error Bars')
        ax.set_title('Jason-{} series. {} method. \n Path # {}; Lat = [{} : {}], Lon = [{} : {}]'.format(Series, prefix_name, Pass, min_lat, max_lat, min_lon, max_lon),fontsize=26)
        plt.rcParams['font.size'] = '26' 
        ax.legend(fontsize=20)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        figure = plt.gcf()
        figure.set_size_inches(22, 14)
        plt.savefig(os.path.join(savepath, filename+'.jpg'),dpi=300)
        plt.close()
    else:
        savepath= os.path.join(curdir, 'timeseries_output')
        filename = out_basename+'_'+prefix_name
        elevation = FinalSeries[:,4]
        elevation_hampel = hampel(elevation, window_size=W, n_sigma=sigma)
        elevation_corr = elevation_hampel.filtered_data
        fig, ax = plt.subplots(figsize=(18, 14))
        ax.plot(FinalSeries[:,1], elevation,        linewidth=2,  color='lightgreen', label='Jason-{}'.format(Series))
        ax.scatter(FinalSeries[:,1], elevation, color='black')
        ax.plot(FinalSeries[:,1], elevation_corr,   linewidth=2,  color='green', label='Jason-{} (W = {}, S = {})'.format(Series, W, sigma))
        ax.scatter(FinalSeries[:,1], elevation_corr, color='black')
        ax.grid(linestyle='--')
        ax.set_xlabel('Year',fontsize=28)
        ax.set_ylabel('Water Elevation w.r.t EGM08 Geoid (m)',fontsize=28)
        ax.set_title('Line Plot with Error Bars')
        ax.set_title('Jason-{} series. {} method. \n Path # {}; Lat = [{} : {}], Lon = [{} : {}]'.format(Series, prefix_name, Pass, min_lat, max_lat, min_lon, max_lon),fontsize=26)
        plt.rcParams['font.size'] = '26' 
        ax.legend(fontsize=20)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        figure = plt.gcf()
        figure.set_size_inches(22, 14)
        plt.savefig(os.path.join(savepath, filename+'.jpg'),dpi=300)
        plt.close()

    
def create_single_plot_both(ip2, ip3, FinalSeries2, FinalSeries3, Pass, curdir, out_basename, prefix_name, min_lat, max_lat, min_lon, max_lon, W, sigma):
    if W == 0:
        savepath= os.path.join(curdir, 'timeseries_output')
        filename = out_basename+'_'+prefix_name
        fig, ax = plt.subplots(figsize=(18, 8))
        ax.plot(FinalSeries2[:,1],FinalSeries2[:,4],linewidth=2, color='blue',label='Jason-2')
        ax.plot(FinalSeries3[:,1],FinalSeries3[:,4],linewidth=2, color='grey', label='Jason-3')
        ax.errorbar(FinalSeries2[:,1],FinalSeries2[:,4],FinalSeries2[:,5],uplims=True,lolims=True, markersize='3', ecolor='navy',capsize=2, elinewidth=1)
        ax.errorbar(FinalSeries3[:,1],FinalSeries3[:,4],FinalSeries3[:,5],uplims=True,lolims=True, markersize='3', ecolor='black',capsize=2, elinewidth=1)
        ax.grid(linestyle='--')
        ax.set_xlabel('Year',fontsize=28)
        ax.set_ylabel('Water Elevation w.r.t EGM08 Geoid (m)',fontsize=28)
        ax.set_title('Line Plot with Error Bars')
        ax.set_title('Jason 2 & 3 series. {} method. \n Path # {}; Lat = [{} : {}], Lon = [{} : {}]'.format(prefix_name, Pass, min_lat, max_lat, min_lon, max_lon),fontsize=26)
        plt.rcParams['font.size'] = '26' 
        ax.legend(fontsize=20)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        figure = plt.gcf()
        figure.set_size_inches(22, 14)
        plt.savefig(os.path.join(savepath, filename+'.jpg'),dpi=300)
        plt.close()
    else:
        savepath= os.path.join(curdir, 'timeseries_output')
        filename = out_basename+'_'+prefix_name
        elevation2 = FinalSeries2[:,4]
        elevation_hampel2 = hampel(elevation2, window_size=W, n_sigma=sigma)
        elevation_corr2 = elevation_hampel2.filtered_data
        elevation3 = FinalSeries3[:,4]
        elevation_hampel3 = hampel(elevation3, window_size=W, n_sigma=sigma)
        elevation_corr3 = elevation_hampel3.filtered_data
        fig, ax = plt.subplots(figsize=(18, 8))
        ax.plot(FinalSeries2[:,1], elevation2,        linewidth=2,  color='lightgreen', label='Jason-2')
        ax.scatter(FinalSeries2[:,1], elevation2, color='black')
        ax.plot(FinalSeries2[:,1], elevation_corr2,   linewidth=2,  color='green', label='Jason-2 (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries2[:,1], elevation_corr2, color='black')
        ax.plot(FinalSeries3[:,1], elevation3,        linewidth=2,  color='lightblue', label='Jason-3')
        ax.scatter(FinalSeries3[:,1], elevation3, color='black')
        ax.plot(FinalSeries3[:,1], elevation_corr3,  linewidth=2,  color='blue', label='Jason-3 (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries3[:,1], elevation_corr3, color='black')
        ax.grid(linestyle='--')
        ax.set_xlabel('Year',fontsize=28)
        ax.set_ylabel('Water Elevation w.r.t EGM08 Geoid (m)',fontsize=28)
        plt.xticks(fontsize=24)
        plt.yticks(fontsize=24)
        ax.set_title('Line Plot with Error Bars')
        ax.set_title('Jason 2 & 3 series. {} method. \n Path # {}; Lat = [{} : {}], Lon = [{} : {}]'.format(prefix_name, Pass, min_lat, max_lat, min_lon, max_lon),fontsize=24)
        plt.rcParams['font.size'] = '26' 
        
        ax.legend(fontsize=20)
        figure = plt.gcf()
        figure.set_size_inches(22, 14)
        plt.savefig(os.path.join(savepath, filename+'.jpg'),dpi=300)
        plt.close()
        

    
def compare_plot_one(ip, FinalSeries_list, Pass, list_of_methods, curdir, out_basename, prefix_name, Series,min_lat, max_lat, min_lon, max_lon, colors, W, sigma):   
    fig, ax = plt.subplots(figsize=(18, 14))
    
    savepath= os.path.join(curdir, 'timeseries_output')
    filename = out_basename+'_'+prefix_name
    
    if W != 0:
        FinalSeries_iqr = FinalSeries_list[0]
        FinalSeries_srt = FinalSeries_list[1]
        
        elevation_iqr = FinalSeries_iqr[:,4]
        elevation_iqr_hampel = hampel(elevation_iqr, window_size=W, n_sigma=sigma)
        elevation_corr_iqr = elevation_iqr_hampel.filtered_data
        elevation_srt = FinalSeries_srt[:,4]
        elevation_srt_hampel = hampel(elevation_srt, window_size=W, n_sigma=sigma)
        elevation_corr_srt = elevation_srt_hampel.filtered_data
        
        ax.plot(FinalSeries_iqr[:,1], elevation_iqr,        linewidth=2,  color='lightgreen', label='IQR')
        ax.scatter(FinalSeries_iqr[:,1], elevation_iqr,  color='black')
        ax.plot(FinalSeries_iqr[:,1], elevation_corr_iqr,   linewidth=2,  color='green', label='IQR (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries_iqr[:,1], elevation_corr_iqr,  color='black')
        ax.plot(FinalSeries_srt[:,1], elevation_srt,        linewidth=2,  color='lightblue', label='SRTM')
        ax.scatter(FinalSeries_srt[:,1], elevation_srt,  color='black')
        ax.plot(FinalSeries_srt[:,1], elevation_corr_srt,   linewidth=2,  color='blue', label='SRTM (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries_srt[:,1], elevation_corr_srt,  color='black')
        
    if W == 0:
        for i in range(len(FinalSeries_list)):
            FinalSeries = FinalSeries_list[i]
            color = colors[i]
            label = list_of_methods[i]
            ax.plot(    FinalSeries[:,1],FinalSeries[:,4],linewidth=2, label=label, color=color)
            ax.errorbar(FinalSeries[:,1],FinalSeries[:,4],FinalSeries[:,5],uplims=True,lolims=True, markersize='2',color=color,capsize=2, elinewidth=1)
    
    ax.grid(linestyle='--')
    ax.set_xlabel('Year',fontsize=28)
    ax.set_ylabel('Water Elevation w.r.t EGM08 Geoid (m)',fontsize=28)
    ax.set_title('Line Plot with Error Bars')
    ax.set_title('Jason-{} series. \n Path # {}; Lat = [{} : {}], Lon = [{} : {}]'.format(Series, Pass, min_lat, max_lat, min_lon, max_lon),fontsize=26)
    plt.rcParams['font.size'] = '26' 
    ax.legend(fontsize=20)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    figure = plt.gcf()
    figure.set_size_inches(22, 14)
    plt.savefig(os.path.join(savepath, filename+'.jpg'),dpi=300)
    plt.close()

    
def compare_plot_both(ip2,ip3, FinalSeries_list_2, FinalSeries_list_3,Pass, list_of_methods, curdir, out_basename, prefix_name, min_lat, max_lat, min_lon, max_lon, colors2, colors3, W, sigma):
    savepath= os.path.join(curdir, 'timeseries_output')
    filename = out_basename+'_'+prefix_name
    
    fig, ax = plt.subplots(figsize=(18, 12))
    if W == 0:
        for i in range(len(FinalSeries_list_2)):
            FinalSeries2 = FinalSeries_list_2[i]
            FinalSeries3 = FinalSeries_list_3[i]
            color2 = colors2[i]
            color3 = colors3[i]
            label = list_of_methods[i]
            ax.plot(    FinalSeries2[:,1],FinalSeries2[:,4],linewidth=2, label='Jason-2 ({})'.format(label), color=color2)
            ax.errorbar(FinalSeries2[:,1],FinalSeries2[:,4],FinalSeries2[:,5],uplims=True,lolims=True, markersize='2',color=color2,capsize=2, elinewidth=1)
            ax.plot(    FinalSeries3[:,1],FinalSeries3[:,4],linewidth=2, label='Jason-3 ({})'.format(label), color=color3)
            ax.errorbar(FinalSeries3[:,1],FinalSeries3[:,4],FinalSeries3[:,5],uplims=True,lolims=True, markersize='2',color=color3,capsize=2, elinewidth=1)
    else:
        FinalSeries_iqr2 = FinalSeries_list_2[0] 
        FinalSeries_srt2 = FinalSeries_list_2[1]
        FinalSeries_iqr3 = FinalSeries_list_3[0]
        FinalSeries_srt3 = FinalSeries_list_3[1]
                
        elevation_iqr2 = FinalSeries_iqr2[:,4]
        elevation_iqr2_hampel = hampel(elevation_iqr2, window_size=W, n_sigma=sigma)
        elevation_corr_iqr2 = elevation_iqr2_hampel.filtered_data
        elevation_srt2 = FinalSeries_srt2[:,4]
        elevation_srt2_hampel = hampel(elevation_srt2, window_size=W, n_sigma=sigma)
        elevation_corr_srt2 = elevation_srt2_hampel.filtered_data
        elevation_iqr3 = FinalSeries_iqr3[:,4]
        elevation_iqr3_hampel = hampel(elevation_iqr3, window_size=W, n_sigma=sigma)
        elevation_corr_iqr3 = elevation_iqr3_hampel.filtered_data
        elevation_srt3 = FinalSeries_srt3[:,4]
        elevation_srt3_hampel = hampel(elevation_srt3, window_size=W, n_sigma=sigma)
        elevation_corr_srt3 = elevation_srt3_hampel.filtered_data
        
        
        ax.plot(FinalSeries_iqr2[:,1], elevation_iqr2,        linewidth=2,  color='lightgreen', label='Jason-2 IQR')
        ax.scatter(FinalSeries_iqr2[:,1], elevation_iqr2,  color='black')
        ax.plot(FinalSeries_iqr2[:,1], elevation_corr_iqr2,   linewidth=2,  color='green', label='Jason-2 IQR (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries_iqr2[:,1], elevation_corr_iqr2,  color='black')
        ax.plot(FinalSeries_srt2[:,1], elevation_srt2,        linewidth=2,  color='lightblue', label='Jason-2 SRTM')
        ax.scatter(FinalSeries_srt2[:,1], elevation_srt2,  color='black')
        ax.plot(FinalSeries_srt2[:,1], elevation_corr_srt2,   linewidth=2,  color='blue', label='Jason-2 SRTM (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries_srt2[:,1], elevation_corr_srt2,  color='black')
        
        ax.plot(FinalSeries_iqr3[:,1], elevation_iqr3,        linewidth=2,  color='silver', label='Jason-3 IQR')
        ax.scatter(FinalSeries_iqr3[:,1], elevation_iqr3,  color='black')
        ax.plot(FinalSeries_iqr3[:,1], elevation_corr_iqr3,   linewidth=2,  color='black', label='Jason-3 IQR (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries_iqr3[:,1], elevation_corr_iqr3,  color='black')
        ax.plot(FinalSeries_srt3[:,1], elevation_srt3,        linewidth=2,  color='pink', label='Jason-3 SRTM')
        ax.scatter(FinalSeries_srt3[:,1], elevation_srt3,  color='black')
        ax.plot(FinalSeries_srt3[:,1], elevation_corr_srt3,   linewidth=2,  color='red', label='Jason-3 SRTM (W = {}, S = {})'.format(W, sigma))
        ax.scatter(FinalSeries_srt3[:,1], elevation_corr_srt3,  color='black')
            
    ax.grid(linestyle='--')
    ax.set_xlabel('Year',fontsize=28)
    ax.set_ylabel('Water Elevation w.r.t EGM08 Geoid (m)',fontsize=28)
    ax.set_title('Line Plot with Error Bars')
    ax.set_title('Jason-2 & 3 series. \n Path # {}; Lat = [{} : {}], Lon = [{} : {}]'.format(Pass, min_lat, max_lat, min_lon, max_lon),fontsize=26)
    plt.rcParams['font.size'] = '26' 
    ax.legend(fontsize=20, ncol=2)
    plt.xticks(fontsize=24)
    plt.yticks(fontsize=24)
    figure = plt.gcf()
    figure.set_size_inches(22, 14)
    plt.savefig(os.path.join(savepath, filename+'.jpg'),dpi=300)
    plt.close()
