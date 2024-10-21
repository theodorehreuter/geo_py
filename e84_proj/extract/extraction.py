from typing import List
import os

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import urllib.request


from e84_proj.extract.stac_client.client import STAC_CLIENT

class Extract:
    """
    class for handling extraction and clean up 
    """

    def __init__(self, coords: List[tuple]):
        self.coords = coords

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
    

    def download_file(self, bucket: str=None, region: str=None, key: str=None, url: str=None, file_path: str=None) -> str:
        """
        downloader to either download directly from url or if stored in s3 bucket
        use boto3 to download a file and store to local machine

        LOCAL STORAGE IS INEFFICENT.  MORE TIME would have more efficient process
        
        Args:
            bucket (str): name of s3 bucket
            region (str): region of s3 bucket
            key (str): file path like string to target data in bucket
            url (str): url for direct downloads if possible
            file_path (str): location to save files

        Returns:
            file_path (str): file path to where downloaded files are stored.
        """
        if bucket is None:
            urllib.request.urlretrieve(url, file_path)
        else:
            arn = 's3://deafrica-input-datasets/rainfall_chirps_monthly/chirps-v2.0_2022.06.tif'
            s3 = boto3.client('s3', region_name='af-south-1', config=Config(signature_version=UNSIGNED))
            s3.download_file(Bucket='deafrica-input-datasets', Key='rainfall_chirps_monthly/chirps-v2.0_2022.06.tif', Filename=file_pth)
        
        return file_path
    

    def cleanup(self, path: str):
        """
        clean up post download and processing
        take in path to temporary folder for geotiff and delete file
        Args:
            path (str): path to file to delete
        """
        # if path exsits:
        if os.path.exists(path):
            os.remove(path)