from typing import List
import os

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import urllib.request

from e84_proj.extract.stac_client.client import StacClient

DOWNLOAD_FOLDER = "/home/treuter/repos/geo_py/e84_proj/data/"
CHIRPS_REGION = 'af-south-1'

class Extract:
    """
    class for handling extraction and clean up 
    """

    def __init__(self, coords: List[tuple], path=DOWNLOAD_FOLDER, chirps_region: str= CHIRPS_REGION):
        self.coords = coords
        self.path = path
        self.chirps_region = chirps_region


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
    

    def download_file(
            self,
            bucket: str=None,
            region: str=None,
            key: str=None,
            url: str=None,
            file_path: str=None
    ) -> str:
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
            s3 = boto3.client('s3', region_name=region, config=Config(signature_version=UNSIGNED))
            s3.download_file(Bucket=bucket, Key=key, Filename=file_path)
            # arn = 's3://deafrica-input-datasets/rainfall_chirps_monthly/chirps-v2.0_2022.06.tif'
            # s3 = boto3.client('s3', region_name='af-south-1', config=Config(signature_version=UNSIGNED))
            # s3.download_file(Bucket='deafrica-input-datasets', Key='rainfall_chirps_monthly/chirps-v2.0_2022.06.tif', Filename=file_path)
        
        return file_path
    
    def execute_downloads(self, links: dict) -> dict:
        """
        take in file paths and execute downloads of files to local machine.

        Args:
            links (dict): dict containing file links to parse for download

        Returns:
            outputs (dict): dict of file paths where files are stored for procesing and analysis
        """
        outputs =  {
            "chirps": {
                "start": "",
                "end": ""
            },
            "lulc": {
                "start": "",
                "end": ""
            }, 
            "worldpop": ""
        }

        for key in links.keys():
            if isinstance(links.get(key), dict):
                for sub_key in links.get(key).keys():
                    url_path: str = links.get(key).get(sub_key)
                    if url_path.startswith('s3'):
                        bucket = url_path.split("://")[1].split("/")[0]
                        split = url_path.split("://")[1].split("/")
                        s3_key = split[1] + '/' + split[2]
                        file_path = self.path + sub_key + '_rainfall.tif'
                        if not os.path.isfile(file_path):
                            out_path = self.download_file(bucket=bucket, key=s3_key, file_path=file_path, region=self.chirps_region)
                        outputs[key][sub_key] = file_path
                    else:
                        file_path = self.path + sub_key + "_lulc.tif"
                        if not os.path.isfile(file_path):
                            out_path = self.download_file(url=url_path, file_path=file_path)
                        outputs[key][sub_key] = file_path
            else:
                file_path = self.path + 'pop.tif'
                if not os.path.isfile(file_path):
                    out_path = self.download_file(url=links.get(key), file_path=self.path+'pop.tif')
                outputs['worldpop'] = file_path
        
        return outputs

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