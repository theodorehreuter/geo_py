import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd
from statistics import mean


def adder(x: int, y: int) -> int:
    return x + y

output = adder(1, 2)
print(f"actual {output}")


def coords_to_poly(xmin, xmax, ymin, ymax, EPSG_val=4326) -> gpd.GeoDataFrame:

    poly = Polygon([
        [xmin, ymin],
        [xmin, ymax],
        [xmax, ymin],
        [ymax, ymax]
    ])
    d = {'col1': ['p1'], 'geometry': [poly]}

    bbox_poly_gdf = gpd.GeoDataFrame(d, crs='EPSG:4326')
    return bbox_poly_gdf

gdf = gpd.read_file("/home/treuter/repos/geo_py/geo_py/Census_Block_Groups_in_2000.geojson")
areas = gdf['SQMI']
sum = 0
for x in areas:
    sum = sum + x
mean_area = sum/len(areas)
print(mean_area)

sub_gdf = gdf[['SQMI', 'GIS_ID']]
print(sub_gdf)
print(mean(areas))