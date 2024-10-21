from typing import List

import rioxarray as rx
from rioxarray.raster_dataset import RasterDataset

from e84_proj.extract.utils import coords_to_polygon

class Preprocessor:
    """
    class to hold preprocesing functionality for doing basic data housekeeping
    on rasterio datasets for e84 intervie project
    """

    def __init__(self, coords: List[tuple]):
        self.coords = coords
        pass

    def open_raster(self, path: str):
        xds = rx.open_rasterio(path)
        return

    def clip_raster(self, xds: RasterDataset) -> RasterDataset:
        """
        PROBABLY WRONG TYPING
        take in an opened raster dataset and clip it to input geometry to 
        keep data volume down

        Args:
            xds (RasterDataset): opened raster

        Returns:
            RasterDataset: clipped raster
        """
        raster_crs = xds.rio.crs
        print(f'raster crs is: {raster_crs}')
        # clip_geom = self.clip_prep(raster_crs)
        # clipped: RasterDataset = xds.rio.clip(clip_geom)
        # return clipped
    
    def clip_prep(self, raster_crs: str) -> dict:
        """
        take input coords and create clipping geometry compatible with rioxarray
        Ensure that clipping geometry is projected to raster crs

        Args:
            raster_crs (str): raster crs in string

        Returns:
            dict: geoJSON like polygon dict for clipping raster
        """
        
        projected_poly = coords_to_polygon(self.coords, raster_crs, 'epsg:4326')
        clip_geom = [
            {
                'type': 'Polygon',
                'coordinates': [list(projected_poly.exterior.coords)]
            }
        ]
        return clip_geom
    
    def merge_tiles(self):
        return
    
    def reproject(self):
        return
    
    def resample(self):
        return