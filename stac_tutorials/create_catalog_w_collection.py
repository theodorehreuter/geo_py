import os
import rasterio
import urllib.request
import pystac

from shapely.geometry import Polygon, mapping
from datetime import datetime, timezone
from pystac.extensions.eo import Band, EOExtension
from tempfile import TemporaryDirectory
from shapely.geometry import shape


# Set temporary directory to store source data
tmp_dir = TemporaryDirectory()
img_path1 = os.path.join(tmp_dir.name, 'image1.tif')

# Fetch and store data
url1 = ('https://spacenet-dataset.s3.amazonaws.com/'
       'spacenet/SN5_roads/train/AOI_7_Moscow/MS/'
       'SN5_roads_train_AOI_7_Moscow_MS_chip996.tif')
urllib.request.urlretrieve(url1, img_path1)

url2 = ('https://spacenet-dataset.s3.amazonaws.com/'
       'spacenet/SN5_roads/train/AOI_7_Moscow/MS/'
       'SN5_roads_train_AOI_7_Moscow_MS_chip997.tif')
img_path2 = os.path.join(tmp_dir.name, 'image2.tif')
urllib.request.urlretrieve(url2, img_path2)

print("img_path1: " , img_path1, "\n", "img_path2: ", img_path2)

def get_bbox_and_footprint(raster):
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

# Run the function and print out the results for image 1
bbox, footprint = get_bbox_and_footprint(img_path1)
print("bbox: ", bbox, "\n")
print("footprint: ", footprint)

# Run the function and print out the results for image 2
bbox2, footprint2 = get_bbox_and_footprint(img_path2)
print("bbox: ", bbox2, "\n")
print("footprint: ", footprint2)

# define bands of WorldView-3
wv3_bands = [Band.create(name='Coastal', description='Coastal: 400 - 450 nm', common_name='coastal'),
             Band.create(name='Blue', description='Blue: 450 - 510 nm', common_name='blue'),
             Band.create(name='Green', description='Green: 510 - 580 nm', common_name='green'),
             Band.create(name='Yellow', description='Yellow: 585 - 625 nm', common_name='yellow'),
             Band.create(name='Red', description='Red: 630 - 690 nm', common_name='red'),
             Band.create(name='Red Edge', description='Red Edge: 705 - 745 nm', common_name='rededge'),
             Band.create(name='Near-IR1', description='Near-IR1: 770 - 895 nm', common_name='nir08'),
             Band.create(name='Near-IR2', description='Near-IR2: 860 - 1040 nm', common_name='nir09')]




collection_item = pystac.Item(id='local-image-col-1',
                               geometry=footprint,
                               bbox=bbox,
                               datetime=datetime.utcnow(),
                               properties={})

collection_item.common_metadata.gsd = 0.3
collection_item.common_metadata.platform = 'Maxar'
collection_item.common_metadata.instruments = ['WorldView3']

asset = pystac.Asset(href=img_path1, 
                      media_type=pystac.MediaType.GEOTIFF)
collection_item.add_asset("image", asset)
eo = EOExtension.ext(collection_item.assets["image"], add_if_missing=True)
eo.apply(wv3_bands)

collection_item2 = pystac.Item(id='local-image-col-2',
                               geometry=footprint2,
                               bbox=bbox2,
                               datetime=datetime.utcnow(),
                               properties={})

collection_item2.common_metadata.gsd = 0.3
collection_item2.common_metadata.platform = 'Maxar'
collection_item2.common_metadata.instruments = ['WorldView3']

asset2 = pystac.Asset(href=img_path2,
                     media_type=pystac.MediaType.GEOTIFF)
collection_item2.add_asset("image", asset2)
eo = EOExtension.ext(collection_item2.assets["image"], add_if_missing=True)
eo.apply([
    band for band in wv3_bands if band.name in ["Red", "Green", "Blue"]
])

# use metadata and shapely to find prper bounds
unioned_footprint = shape(footprint).union(shape(footprint2))
collection_bbox = list(unioned_footprint.bounds)
spatial_extent = pystac.SpatialExtent(bboxes=[collection_bbox])\

# get time bounds
collection_interval = sorted([collection_item.datetime, collection_item2.datetime])
temporal_extent = pystac.TemporalExtent(intervals=[collection_interval])
collection_extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)

# create collection with extens
collection = pystac.Collection(id='wv3-images',
                               description='Spacenet 5 images over Moscow',
                               extent=collection_extent,
                               license='CC-BY-SA-4.0')

# add items to collectoon and collection to catalog
collection.add_items([collection_item, collection_item2])
catalog = pystac.Catalog(id='catalog-with-collection', 
                         description='This Catalog is a basic demonstration of how to include a Collection in a STAC Catalog.')
catalog.add_child(collection)
catalog.normalize_and_save(root_href=os.path.join(tmp_dir.name, 'stac-collection'), 
                           catalog_type=pystac.CatalogType.SELF_CONTAINED)
tmp_dir.cleanup()