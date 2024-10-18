import xarray as xr
import rioxarray
import numpy as np



# some DEM elevation data from national map, in WV area
ras = "/home/treuter/repos/geo_py/data/USGS_1_n39w080_20230816.tif"
download_link = 'https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/historical/n39w079/USGS_1_n39w079_20211229.tif'

# xarray_data = xr.open_dataset(ras, engine='rasterio')
# xarray_data.crs

rxr = rioxarray.open_rasterio(ras)
classes_rxr = list(np.unique(rxr))

# get crs
rxr.rio.crs
# get bounds
rxr.rio.bounds()
# get no data value
rxr.rio.nodata
print('hold')

# sum of each x axis values for each y axis value
rxr.sum(dim='x') 


# get average of elevation

# get med of elevation

# get max/min 