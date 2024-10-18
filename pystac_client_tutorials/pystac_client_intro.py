from pystac_client import Client

# set pystac_client logger to debug to see API calls
import logging
logging.basicConfig()
logger = logging.getLogger('pystac_client')
logger.setLevel(logging.DEBUG)

# connect to API
# STAC API root URL
URL = 'https://planetarycomputer.microsoft.com/api/stac/v1'

# custom headers
headers = []

cat = Client.open(URL, headers=headers)
collection = cat.get_collection('aster-l1t')

# ITEMS
items = collection.get_items()
# flush stdout so we can see the exact order that things happen
def get_ten_items(items):
    for i, item in enumerate(items):
        print(f"{i}: {item}", flush=True)
        if i == 9:
            return

print('First page', flush=True)
get_ten_items(items)

print('Second page', flush=True)
get_ten_items(items)


# Search with AOI
# AOI around Delfzijl, in northern Netherlands
geom = {
    "type": "Polygon",
    "coordinates": [
      [
        [
          6.42425537109375,
          53.174765470134616
        ],
        [
          7.344360351562499,
          53.174765470134616
        ],
        [
          7.344360351562499,
          53.67393435835391
        ],
        [
          6.42425537109375,
          53.67393435835391
        ],
        [
          6.42425537109375,
          53.174765470134616
        ]
      ]
    ]
}

# limit sets the # of items per page so we can see multiple pages getting fetched
search = cat.search(
    max_items = 15,
    limit = 5,
    collections = "aster-l1t",
    intersects = geom,
    datetime = "2000-01-01/2010-12-31",
)

items = list(search.items())

len(items)

import json
import uuid
from IPython.display import display_javascript, display_html, display

class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict) or isinstance(json_data, list):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;font: 12px/18px monospace !important;"></div>'.format(self.uuid), raw=True)
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
            renderjson.set_show_to_level(2);
            document.getElementById('%s').appendChild(renderjson(%s))
        });
      """ % (self.uuid, self.json_str), raw=True)


RenderJSON([i.to_dict() for i in items])