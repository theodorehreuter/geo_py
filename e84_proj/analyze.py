from typing import List

import geopandas as gpd
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
from rasterstats import zonal_stats
from xarray import DataArray
from xrspatial.classify import reclassify

TARGET_RESOLUTION_METERS = 1000

class Analyzer:
    """
    class for doing analysis
    """

    def __init__(self, coords: List[tuple]):
        self.coords = coords
        pass

    def difference(self, start_path: str, end_path: str, output_path: str):
        """
        raster difference claculator for getting difference of two rasters
        for exammple to find CHANGE in ranfaill between two years

        Args:
            start_path (str): path to start raster 
            end_path (str): path to end raster
            output_path (str): location to write out difference raster
        """
        rast_start = rio.open(start_path).read()
        rast_end = rio.open(end_path).read()

        result = rast_end - rast_start

        kwargs = rast_start.meta
        kwargs.update(
            dtype=rio.int32,
            count=1
        )

        with rio.open(output_path, 'w', **kwargs) as output:
            output.write_band(1, result.astype(rio.int32))
        
        return output_path

    def reclassify(self, agg: DataArray):
        """
        reclassify land use and land cover rasters into binary rasters for easier 
        calculations and filtering.  Use numpy + xarray for speed

        Args:
            agg (DataArray): xarray
        """
        # use either numpy WHERE 
        agg[np.where( agg < 2 )] = 0
        agg[np.where( agg > 2)] = 0
        agg[np.where( agg == 2)] = 1

        return 
    
    def resample(self, path: str, method: str, out_path: str, input_resolution_m: int=1000):
        """
        resample rasters to target resolution
        destination resolution must be in meters
        Use nearest neighbor for categorical LULC because of speed and non continuous data 
            and upsampling
        use bilinear resampling to downsammpling to interpolate rainfall values to 
            increase resolution

        Args:
            input_resolution_m (int): target destination resolution
            path (str): path of input raster
            method (str): method to resample with
            out_path (str): path to save out resampled raster
        
        Returns: 
            output_path (str): output path where resampled raster is saved
        """
        scale_factor = input_resolution_m/TARGET_RESOLUTION_METERS
        resampling_method = None
        if method == 'nearest_neighbor':
            resampling_method = Resampling.nearest
        elif method == 'bilinear':
            resampling_method = Resampling.bilinear
        with rio.open(path) as dataset:
            profile = dataset.profile.copy()

            data = dataset.read(
                out_shape=(
                    dataset.count,
                    int(dataset.height * scale_factor),
                    int(dataset.width * scale_factor)
                ),
                resampling=resampling_method
            )
            transform = dataset.transform * dataset.transform.scale(
                (1 / scale_factor),
                (1 / scale_factor)
            )
            profile.update({"height": data.shape[-2],
                    "width": data.shape[-1],
                   "transform": transform})
        

        with rio.open(out_path, "w", **profile) as dataset:
            dataset.write(data)

        return out_path
    
    def spatial_statistics(self, poly_path: str, raster_path: str) -> gpd.GeoDataFrame:
        """
        generate spatial statistics.  Input raster and use zonal stats to generate 
        some statistics for each polygon

        Args:
            poly_path (str): _description_
            raster_path (str): _description_

        Returns:
            gpd.GeoDataFrame: _description_
        """

        stats = zonal_stats(poly_path, raster_path)
        gdf = gpd.read_file(poly_path)

        # use pandas vectorized operations and list comprehension to speed up
        # get index as pandas series
        # loop over stats list of dicts and add index to each item using list comprehension
        # turn list into series with index
        # join to geodataframe on index using pd.merge()


        return gdf