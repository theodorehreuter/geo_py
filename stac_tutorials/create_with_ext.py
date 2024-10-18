import os
import json
import rasterio
import urllib.request
import pystac

from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from tempfile import TemporaryDirectory

from pystac.extensions.eo import Band, EOExtension
from pystac.extensions.view import ViewExtension
from pystac.extensions.projection  import ProjectionExtension

# set tempo dir to store source data
tmp_dir = TemporaryDirectory()
img_path = os.path.join(tmp_dir.name, 'image.tif')

# Fetch and store data
url = ('https://spacenet-dataset.s3.amazonaws.com/'
       'spacenet/SN5_roads/train/AOI_7_Moscow/MS/'
       'SN5_roads_train_AOI_7_Moscow_MS_chip996.tif')
urllib.request.urlretrieve(url, img_path)

wv3_bands = [Band.create(name='Coastal', description='Coastal: 400 - 450 nm', common_name='coastal'),
             Band.create(name='Blue', description='Blue: 450 - 510 nm', common_name='blue'),
             Band.create(name='Green', description='Green: 510 - 580 nm', common_name='green'),
             Band.create(name='Yellow', description='Yellow: 585 - 625 nm', common_name='yellow'),
             Band.create(name='Red', description='Red: 630 - 690 nm', common_name='red'),
             Band.create(name='Red Edge', description='Red Edge: 705 - 745 nm', common_name='rededge'),
             Band.create(name='Near-IR1', description='Near-IR1: 770 - 895 nm', common_name='nir08'),
             Band.create(name='Near-IR2', description='Near-IR2: 860 - 1040 nm', common_name='nir09')]


def get_bbox_and_footprint(raster):
    with rasterio.open(raster) as r:
        crs = r.crs
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon([
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom]
        ])
        
        return (bbox, mapping(footprint),crs)

bbox, footprint, crs = get_bbox_and_footprint(img_path)
# create item
item = pystac.Item(
       id='local-image-eo',
       geometry=footprint,
       bbox=bbox,
       datetime=datetime.utcnow(),
       properties={}
)

eo = EOExtension.ext(item, add_if_missing=True)
eo.apply(bands=wv3_bands)

# add common metadata
item.common_metadata.platform = 'Maxar'
item.common_metadata.instruments = ['WorldView3']
item.common_metadata.gsd = 0.3
# print('hold)')



# add bands to assetts we add to the item
asset = pystac.Asset(
       href=img_path,
       media_type=pystac.MediaType.GEOTIFF
)
item.add_asset('image', asset)
eo_on_asset = EOExtension.ext(item.assets['image'])
eo_on_asset.apply(wv3_bands)


# View Extension - about angle of sensors and other radiance angles that affect viewing of data
view_ext = ViewExtension.ext(item, add_if_missing=True)
view_ext.sun_azimuth = 160.86021018
view_ext.sun_elevation = 23.81656674

# Projection Extension
proj_ext = ProjectionExtension.ext(item, add_if_missing=True)
proj_ext.epsg = 4326

# Make catalog
catalog = pystac.Catalog(id='tutorial-catalog',
       description='This catalog is a basic demo catalog to teach use of extension ')
catalog.add_item(item)

catalog.normalize_and_save(root_href=os.path.join(tmp_dir.name, 'stac-extension'), 
                           catalog_type=pystac.CatalogType.SELF_CONTAINED)


# Read catalog from file system and pstac recognizes item implements extensions and uses their functionality
catalog2 = pystac.read_file(os.path.join(tmp_dir.name, 'stac-extension', 'catalog.json'))
assert isinstance(catalog2, pystac.Catalog)
list(catalog2.get_items())
item: pystac.Item = next(catalog2.get_all_items())
assert EOExtension.has_extension(item)
eo_on_asset = EOExtension.ext(item.assets["image"])
print(eo_on_asset.bands)
tmp_dir.cleanup()