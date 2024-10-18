import json
from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension


TARGET_ITEM = "LC80140332018166LGN00"
# read teh example catalog
root_catalog = Catalog.from_file('https://raw.githubusercontent.com/stac-utils/pystac/main/docs/example-catalog/catalog.json')

root_catalog.describe()

# print(f"ID: {root_catalog.id}")
# print(f"Title: {root_catalog.title or 'N/A'}")
# print(f"Description: {root_catalog.description or 'N/A'}")

# print(get_stac_version())

# Crawl STAC CHild Catalog and or colections
collections = list(root_catalog.get_collections())

print(f"Number of collections: {len(collections)}")
print("Collections IDs:")
for collection in collections:
    print(f"- {collection.id}")


collection = root_catalog.get_child('landsat-8-11')
if collection is None:
    print("Collection is Empty. Check your downloads and try again.")
else:
    print("Collection has a root child. You may proceed to the following steps.")

items = list(root_catalog.get_all_items())
print(f"number of items: {len(items)}")
for item in items:
    print(f"- {item.id}")

item = root_catalog.get_item(TARGET_ITEM, recursive=True)
print(f'item geometry: {item.geometry}')
print(f' item bbox - {item.bbox}')
print(f'item datetie - {item.datetime}')
print(f'item collection - {item.collection_id}')

itcol = item.get_collection()
print('hold')

# common metadata that might be found in other assets as well
item.common_metadata.instruments
item.common_metadata.platform
# https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md#gsd
item.common_metadata.gsd # ground sample distance (GSD) measured in meters, related to res at sensor, not pixel size

# stac extensions
print(item.stac_extensions)
print(EOExtension.has_extension(item))
print(LabelExtension.has_extension(item))
eo_item_ext = EOExtension.ext(item)
# access cloud props 
print(eo_item_ext.cloud_cover)
# OR
print(item.properties['eo:cloud_cover'])


# ACCESS ASSETS
for asset_key in item.assets:
    asset = item.assets[asset_key]
    print(f'{asset_key}: {asset.href} ({asset.media_type})')

asset = item.assets['B3']
asset.to_dict()
print(asset.to_dict())

eo_asset_ext = EOExtension.ext(asset)
bands = eo_asset_ext.bands
print(bands)
bands[0].to_dict()