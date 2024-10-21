from typing import List

import geopandas as gpd
import h3
import pandas as pd
import pyproj
from shapely.geometry import Polygon
from shapely.ops import transform

def coords_to_polygon(coords: List[tuple], out_crs: str, in_crs: str='epsg:4326') -> Polygon:
    """
    take in coordinates and turn them into a shapely polygon
    transform coordinates as needed to target coordinate system

    Args:
        coords (List[tuple]): coordinates in form of list of tuples
        in_crs (str): crs of input coordinates in format of `epsg:4326`
        out_crs (str): crs of target output coordinates in format of `epsg:3857`

    Returns:
        Polygon: shapely polygon with coordinates projected to desired coordinate system
    """
    poly = Polygon(coords)
    project = pyproj.Transformer.from_proj(
    pyproj.Proj(init=in_crs), # source crs
    pyproj.Proj(init=out_crs) # dest crs
)
    projected_poly = transform(project.transform, poly)
    
    return projected_poly

def generate_h3_grid(self, resolution: int) -> gpd.GeoDataFrame:
        """
        generate h3 grid over area of interest 

        Args:
            resolution (int): target h3 resolution.  Must be between or equal to 1-15

        Returns:
            gpd.GeoDataFrame: geodataframe with 2 cols 'h3' and 'geometry'
        """

        poly = h3.LatLngPoly(self.coords)
        cells = h3.h3shape_to_cells(poly, res=resolution)

        data = {'h3': cells,}
        df = pd.DataFrame(data)

        df['geometry'] = df['h3'].apply(lambda x: Polygon(h3.cell_to_boundary(x)))
        gdf = gpd.GeoDataFrame(df, geometry=df['geometry'], crs='epsg:4326')

        return gdf