from shapely.geometry import Polygon
from typing import List
from shapely.ops import transform
import pyproj

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