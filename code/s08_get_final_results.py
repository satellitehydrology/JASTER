from scipy.stats import iqr, mode
from scipy import interpolate
from sklearn.cluster import KMeans
from scipy import io
from scipy.interpolate import RegularGridInterpolator
import os, rioxarray
import numpy as np



def get_finals(Series,Pass, MERIT_DEM_WGS84_dir, WOM_dir, min_lat, max_lat, min_lon, max_lon, hgt_dem_diff_thrd, wo_thrd, hgt_cyc_range_thrd, hgt_cyc_std_thrd, data_dir, file_dir):

    def iqr_deoutlier(cyc_hgt_profile):
        IQR = iqr(cyc_hgt_profile, nan_policy='omit')   
        return np.logical_and(cyc_hgt_profile > np.nanquantile(cyc_hgt_profile, 0.25) - 1.5 * IQR, cyc_hgt_profile < np.nanquantile(cyc_hgt_profile, 0.75) + 1.5*IQR).flatten()   


    def dem_wo_interpolate(dem, wo, cyc_lon_profile, cyc_lat_profile):
        lat_lon_buf = 0.01

        min_lon, max_lon = np.nanmin(cyc_lon_profile), np.nanmax(cyc_lon_profile)
        min_lat, max_lat = np.nanmin(cyc_lat_profile), np.nanmax(cyc_lat_profile)

        dem_clip = dem.sel(x=slice(min_lon-lat_lon_buf, max_lon+lat_lon_buf)).sel(y=slice(max_lat+lat_lon_buf, min_lat-lat_lon_buf))
        wo_clip  =  wo.sel(x=slice(min_lon-lat_lon_buf, max_lon+lat_lon_buf)).sel(y=slice(max_lat+lat_lon_buf, min_lat-lat_lon_buf))

        dem_lon_mesh, dem_lat_mesh = np.meshgrid(dem_clip.x.values, dem_clip.y.values)
        wo_lon_mesh,  wo_lat_mesh  = np.meshgrid( wo_clip.x.values,  wo_clip.y.values)
        interp_dem = interpolate.griddata((dem_lat_mesh.reshape(-1), dem_lon_mesh.reshape(-1)), dem_clip.values.reshape(-1), (cyc_lat_profile,cyc_lon_profile)).reshape(-1,1)
        interp_wo  = interpolate.griddata((wo_lat_mesh.reshape(-1),  wo_lon_mesh.reshape(-1)),  wo_clip.values.reshape(-1),  (cyc_lat_profile,cyc_lon_profile)).reshape(-1,1)

        return interp_dem, interp_wo

    def dem_wo_deoutlier(dem, wo, cyc_lon_profile, cyc_lat_profile, cyc_hgt_profile, hgt_dem_diff_thrd, wo_thrd):
        interp_dem, interp_wo = dem_wo_interpolate(dem, wo, cyc_lon_profile, cyc_lat_profile)
        index_retain_dem_wo = np.logical_and(interp_wo >= wo_thrd, np.abs(cyc_hgt_profile - interp_dem) <= hgt_dem_diff_thrd).flatten()
        index_retain_dem = interp_wo >= wo_thrd
        index_retain_wo = np.abs(cyc_hgt_profile - interp_dem) <= hgt_dem_diff_thrd
        return index_retain_dem_wo, index_retain_dem.flatten(), index_retain_wo.flatten()


    def kmean_water_cluster(cyc_hgt_profile, cyc_sig_profile, hgt_cyc_range_thrd, hgt_cyc_std_thrd):
        hgt_cyc_range = np.nanmax(cyc_hgt_profile) - np.nanmin(cyc_hgt_profile)
        while hgt_cyc_range > hgt_cyc_range_thrd:
            kmeans_cluster = KMeans(n_clusters=2, random_state=42, n_init=10).fit_predict(cyc_hgt_profile)                
            cyc_hgt_profile = cyc_hgt_profile[kmeans_cluster==mode(kmeans_cluster, keepdims=True)[0]]
            cyc_sig_profile = cyc_sig_profile[kmeans_cluster==mode(kmeans_cluster, keepdims=True)[0]]
            hgt_cyc_range = np.nanmax(cyc_hgt_profile) - np.nanmin(cyc_hgt_profile)
        hgt_cyc_mean = np.nanmean(cyc_hgt_profile)
        hgt_cyc_std = np.nanstd(cyc_hgt_profile)
        hgt_cyc_errmean = cyc_hgt_profile[:,0] - hgt_cyc_mean
        while hgt_cyc_std > hgt_cyc_std_thrd:
            if np.count_nonzero(~np.isnan(cyc_hgt_profile))==2:
                break
            hgt_cyc_errmean = cyc_hgt_profile - hgt_cyc_mean
            cyc_hgt_profile = cyc_hgt_profile[np.abs(hgt_cyc_errmean)!=np.nanmax(np.abs(hgt_cyc_errmean))]
            cyc_sig_profile = cyc_sig_profile[np.abs(hgt_cyc_errmean)!=np.nanmax(np.abs(hgt_cyc_errmean))]
            hgt_cyc_std = np.nanstd(cyc_hgt_profile)
            hgt_cyc_mean = np.nanmean(cyc_hgt_profile)
        return cyc_hgt_profile, cyc_sig_profile


    def get_time_series(input_data, index_retain):
        input_data = input_data[index_retain,:]
        cycno_list = input_data[:,0]
        uniq_cycno = np.unique(cycno_list)
        ct_cyc=0
        timeseries_report=np.empty((len(uniq_cycno),8))
        timeseries_report[:]=np.nan
        for cycno in uniq_cycno[:]:
            index_cyc = cycno_list==cycno
            cyc_data = input_data[index_cyc,:]
            mjd = cyc_data[:,1].reshape(-1,1)
            lon = cyc_data[:,2].reshape(-1,1)
            lat = cyc_data[:,3].reshape(-1,1)
            hgt = cyc_data[:,4].reshape(-1,1)
            sig = cyc_data[:,5].reshape(-1,1)    
            hgt, sig = kmean_water_cluster(hgt, sig, hgt_cyc_range_thrd, hgt_cyc_std_thrd)
            cyc_time = (np.nanmean(mjd)+2108-50000)/365.25 +1990
            cyc_lon = np.nanmean(lon)
            cyc_lat = np.nanmean(lat)
            cyc_hgt = np.nanmean(hgt)
            cyc_std_hgt = np.nanstd(hgt)      
            cyc_sig = np.nanmean(sig)
            cyc_retain_rate = hgt.shape[0] / cyc_data.shape[0]
            timeseries_report[ct_cyc,:] = [cycno, cyc_time, cyc_lon, cyc_lat, cyc_hgt, cyc_std_hgt, cyc_sig, cyc_retain_rate]  
            ct_cyc += 1 
        index_retain_iqr2 = iqr_deoutlier(timeseries_report[:,4])  
        FinalSeries = timeseries_report[index_retain_iqr2,:]
        return FinalSeries


    lonbp = io.loadmat(os.path.join(data_dir, 'geoidegm2008grid.mat'))['lonbp']
    latbp = io.loadmat(os.path.join(data_dir, 'geoidegm2008grid.mat'))['latbp']
    grid  = io.loadmat(os.path.join(data_dir, 'geoidegm2008grid.mat'))['grid']

    ip = RegularGridInterpolator(points=(latbp.flatten(),lonbp.flatten()), values=grid, bounds_error=False, fill_value=np.nan)

    dem = rioxarray.open_rasterio(MERIT_DEM_WGS84_dir).squeeze().drop('band')
    dem.x.values[dem.x.values < 0] = dem.x.values[dem.x.values < 0] + 360

    wo = rioxarray.open_rasterio(WOM_dir).squeeze().drop('band')
    wo.x.values[wo.x.values < 0] = wo.x.values[wo.x.values<0] + 360

    Extracted_Data_Path = os.path.join(file_dir, 'j{}_{:03d}'.format(Series,Pass), 'j{}_p{:03d}_{}_{}_info.txt'.format(Series,Pass, min_lat, max_lat))

    input_data = np.loadtxt(Extracted_Data_Path)[:,9:]

    lat_all = input_data[:,3] 
    index_lat_range = np.logical_and(lat_all > min_lat, lat_all < max_lat)                
    input_data=input_data[index_lat_range,:]

    lon_all = input_data[:,2].reshape(-1,1)
    lat_all = input_data[:,3].reshape(-1,1)
    hgt_all = input_data[:,4].reshape(-1,1)
    index_retain_iqr = iqr_deoutlier(hgt_all)
    index_retain_dem_wo, index_retain_dem, index_retain_wo  = dem_wo_deoutlier(dem, wo, lon_all, lat_all, hgt_all, hgt_dem_diff_thrd, wo_thrd)

    FinalSeries_iqr    = get_time_series(input_data, index_retain_iqr)
    FinalSeries_dem_wo = get_time_series(input_data, index_retain_dem_wo)
    
    return ip, FinalSeries_iqr, FinalSeries_dem_wo, index_retain_dem_wo