from pystac_client import Client, ItemSearch
from typing import Any, Dict
import json
import shapely.geometry
from shapely.geometry import Polygon
import pyproj
from shapely.ops import transform

# SAMPLE_CAT = "https://explorer.sandbox.dea.ga.gov.au/stac/catalogs/aster_green_vegetation/2004-3"
SAMPLE_CAT = "https://explorer.sandbox.dea.ga.gov.au/stac/"
COORDS = ((133.8255, -23.3256), (134.1556, -23.3115), (134.1199, -23.4673), (133.7947, -23.4553)) # NE of Alice Springs AUS
# SAMPLE_CAT = "https://earth-search.aws.element84.com/v1"
AOI: Polygon = Polygon(COORDS)

project = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:4326'), # source crs
    pyproj.Proj(init='epsg:4283') # dest crs
)
projected_poly = transform(project.transform, AOI)
print(f'projected poly: {projected_poly}')

def coords_to_shapely(coords: tuple, trgt_crs: int) -> Polygon:
    input = pyproj.CRS('EPSG:4326')
    output = pyproj.CRS('EPSG:4283')
    projected = []
    # transform if needed to coord system of target
    return 0

# CREATE STAC CONNECTION
client = Client.open(SAMPLE_CAT)
search = client.search(
    max_items=10,
    collections='aster_green_vegetation',
    intersects=AOI
)
items = search.get_all_items()
result = items.items[0].to_dict()
pystac_item = items.items[0]
# print(result)
# for i in items:
#     item = i
#     print('hold')
# print('hold')
# get a list basic info on collection
# convert to geodataframe for easier viewing
# add asset items as col to gdf

# USE INPUT COORDINATES TO IDENTFY DOWN A LAYER


# DOWNLOAD DATA ONLY FOR INPUT AOI

# reproject input AOI to match layer downloaded

# GET BASIC INFO ABOUT LAYER
# crs, bounds

# Do some clean up 


# client = Client.open(SAMPLE_CAT)

# def stac_search(aoi: Polygon) -> ItemSearch:
#     return []
# search = client.search(
#     max_items=10,
#     collections=['sentinel-2-l2a'],
#     bbox=[-72.5, 40.5, -72, 41]
# )

# for item in search.items():
#     print(f"item assets {item.assets}")
#     print(f"item bbox {item.bbox}")
#     print(f"geom {item.geometry}")
#     print(item)
# item_collection = search.item_collection()
# item_collection.save_object("test_collection.json")
# # cat = pystac.Catalog("https://explorer.sandbox.dea.ga.gov.au/stac/")
