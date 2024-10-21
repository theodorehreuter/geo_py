import argparse
from typing import List

from e84_proj.extract.stac_client.client import StacClient
from e84_proj.extract.utils import coords_to_polygon
from e84_proj.extract.extraction import Extract
from e84_proj.preprocess.preprocess import Preprocessor


parser = argparse.ArgumentParser()

parser.add_argument(
    '--coords',
    required=True,
    help="input coordinates for search area, like [(0,0), (0,1), (1,1), (0,1), (0,0)]")

WORLD_POP_PATH = 'https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2020/TCD/tcd_ppp_2020_1km_Aggregated.tif'
# CHIRPS_STAC_ENDPONT = "https://explorer.digitalearth.africa/stac/collections/rainfall_chirps_daily"
DE_AFRICA_STAC = "https://explorer.digitalearth.africa/stac"
CHIRPS_COLLECTION = 'rainfall_chirps_monthly'


# lulc items = https://api.impactobservatory.com/stac-aws/collections/io-10m-annual-lulc/items
IO_LULC_STAC_ENDPOINT = "https://api.impactobservatory.com/stac-aws"
LULC_COLLECTION = 'io-10m-annual-lulc' 
LULC_REGION = 'us-west-2'

# target coordinates in central Chad where I expect there to be some change
# about 60mi on a side
TARGET_COORDS_CHAD = [(15.57692, 11.28722), (16.69969, 11.29509), (16.79151, 10.03066), (15.42739, 10.03853), (15.57692, 11.28722)]
# (15.57692, 11.28722), (16.69969, 11.29509), (16.79151, 10.03066), (15.42739, 10.03853), (15.57692, 11.28722)

CHIRPS_START = '2022-06-15'
CHIRPS_END = '2023-06-15'

LULC_START = '2022-01-01'
LULC_END = '2023-01-01'


def main(
        coords: List[tuple],
        de_africa_stac: str = DE_AFRICA_STAC,
        io_stac: str = IO_LULC_STAC_ENDPOINT,
        world_pop: str = WORLD_POP_PATH,
        chirps: str = CHIRPS_COLLECTION,
        lulc: str = LULC_COLLECTION,
    ):
    """
    1. Pull data
    2. Preprocess - resample, reproject, masking, stitch tiles
    3. Analysis
    4. Export

    Args:
        world_pop (str): path to the target world pop dataset
        chirps (str): path to STAC v1.0 endpoint for chirps rainfall dataset
        lulc (str): path to STAC v1.0 endpoint for LULC dataset
    """
    polygon = coords_to_polygon(coords, in_crs='epsg:4326', out_crs='epsg:4326')
    chirps = StacClient(de_africa_stac, chirps)
    chirps_catalog = chirps.connection_factory()
    chirps_start_items = chirps.aoi_search(chirps_catalog, polygon, CHIRPS_START)
    chirps_end_items = chirps.aoi_search(chirps_catalog, polygon, CHIRPS_END)

    lulc = StacClient(io_stac, lulc)
    lulc_catalog = lulc.connection_factory()
    lulc_start_items = lulc.aoi_search(lulc_catalog, polygon, LULC_START)
    lulc_end_items = lulc.aoi_search(lulc_catalog, polygon, LULC_END)
    
    links = {
        "chirps": {
            "start": chirps_start_items[0],
            "end": chirps_end_items[0]
        },
        "lulc": {
            "start": lulc_start_items[0],
            "end": lulc_end_items[0]
        }, 
        "worldpop": WORLD_POP_PATH
    }
    extractor = Extract(coords)
    download_paths = extractor.execute_downloads(links)

    preprocessor = Preprocessor(coords)

    return 

# run command: /home/treuter/repos/geo_py/.venv/bin/python /home/treuter/repos/geo_py/e84_proj/main.py --coords "(16.78711,14.40821), (17.73743,14.43018), (17.74292,13.64466), (16.83105,13.60072), (16.79260,14.38624), (16.78711,14.40821)"

if __name__ == "__main__":
    args = parser.parse_args()


    # UNSAFE UNSAFE UNSAFE use of eval.  Using only for demo expediency
    coords = [eval(x) for x in args.coords.split(', ')]


    print(f'coords are: {coords}')
    main(coords)
