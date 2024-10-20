from cloudpathlib import CloudPath
import urllib.request
import boto3
from botocore import UNSIGNED
from botocore.client import Config

arn = 's3://deafrica-input-datasets/rainfall_chirps_monthly/chirps-v2.0_2022.06.tif'
down_pth = '/home/treuter/repos/geo_py/e84_proj/test_chirps.tif'
bucket = 'deafrica-input-datasets/rainfall_chirps_monthly'


# WORKS
s3 = boto3.client('s3', region_name='af-south-1', config=Config(signature_version=UNSIGNED))
s3.download_file(Bucket='deafrica-input-datasets', Key='rainfall_chirps_monthly/chirps-v2.0_2022.06.tif', Filename=down_pth)
