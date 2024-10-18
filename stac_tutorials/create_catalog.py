import os
import json
import rasterio
import urllib.request
import pystac

from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from tempfile import TemporaryDirectory

# set tempo dir to store source data
tmp_dir = TemporaryDirectory()
img_path = os.path.join(tmp_dir.name, 'image.tif')

# Fetch and store data
url = ('https://spacenet-dataset.s3.amazonaws.com/'
       'spacenet/SN5_roads/train/AOI_7_Moscow/MS/'
       'SN5_roads_train_AOI_7_Moscow_MS_chip996.tif')
urllib.request.urlretrieve(url, img_path)

catalog = pystac.Catalog(id='tutorial-catalog', description='This catalog is a basic catalog for tutorial')

print(json.dumps(catalog.to_dict(), indent=4))


def get_bbox_and_footprint(raster: str):
    with rasterio.open(raster) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon([
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom]
        ])
    return (bbox, mapping(footprint))


bbox, footprint = get_bbox_and_footprint(img_path)
print('bbox: ', bbox, "\n")
print("footprint: ", footprint)
datetime_utc = datetime.now(tz=timezone.utc)

item = pystac.Item(
    id='local-image',
    geometry=footprint,
    bbox=bbox,
    datetime=datetime_utc,
    properties={}
    )

# prints true to show that item hasn't been added to catalog yet
print(item.get_parent() is None)

# add item to catalog - BUT THIS DOESNT INLCUDE THE ASSET
catalog.add_item(item)
check = item.get_parent()
print(item.get_parent())

item.add_asset(
    key='image',
    asset=pystac.Asset(
        href=img_path,
        media_type=pystac.MediaType.GEOTIFF
    )
)
print(json.dumps(item.to_dict(), indent=4))


# evaluates to true since haven't set links yet
print(catalog.get_self_href() is None)
print(item.get_self_href() is None)

# set refs
catalog.normalize_hrefs(os.path.join(tmp_dir.name, 'stac'))
# now links are set
print("Catalog HREF: ", catalog.get_self_href())
print("Item HREF: ", item.get_self_href())


# self published for portability, like using on local machine
# catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
catalog.save(catalog_type=pystac.CatalogType.ABSOLUTE_PUBLISHED)

# look at now existing catalog
with open(catalog.self_href) as f:
    print(f.read())

with  open(item.self_href) as f:
    print(f.read())

catalog.make_all_asset_hrefs_relative()
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

tmp_dir.cleanup()