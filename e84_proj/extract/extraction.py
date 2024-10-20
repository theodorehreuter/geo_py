from typing import List
import os
from e84_proj.extract.stac_client.client import STAC_CLIENT

class Extract:
    def __init__(self, coords: List[tuple]):
        self.coords = coords

    def coords_to_poly(self):

        return
    
    def input_transformer(self, path: str) -> List[tuple]:
        """
        extract input geometry from file
        return file in list of coordinate tuples in 4326

        Args:
            path (str): path to file to pull geometry from.  Geojson, GPKG, kmz, etc

        Returns:
            List[tuple]: _description_
        """
        return [(0,0)]
    

    def download_file(self, href: str) -> str:
        """
        take in geotiff file path, save to temporary folder
        return path to file in temp folder

        Args:_description_
            href (str): 

        Returns:
            str: _description_
        """
        return ''
    

    def cleanup(self, folder_path: str):
        """
        clean up post download and processing
        take in path to temporary folder for geotiff and delete file
        Args:
            path (str): _description_
        """
        # if path exsits:
        if os.path.exists():
            return
            # remove folder
        return