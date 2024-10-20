from typing import List
from pystac_client import Client, ItemSearch
from shapely.geometry import Polygon
from pystac import Item

class STAC_CLIENT:
    """
    client used to create STAC connections, search STAC API, and create lists 
    of hrefs to assets that are desired to be downloaded
    """
    def __init__(self, endpoint: str, aoi: Polygon):
        """_summary_

        Args:
            endpoint (str): STAC catalog endpoint
            aoi (Polygon): shapely polygon of area of interest
        """
        self.endpoint = endpoint
        self.aoi = aoi

    def connection_factory(self) -> Client:
        """
        factory to create client connected to stac endpoint

        Returns:
            Client: client connected to target catalog
        """
        catalog = Client.open(self.endpoint)
        return catalog

    def AOI_search(self, client: Client) -> List[Item]:
        """
        search stac API for items in AOI

        Args:
            client (Client): STAC client 

        Returns:
            List[Item]: List of items from the collection that are in the AOI
        """
        search = client.search(
            max_items=10,
            collections='aster_green_vegetation',
            intersects=self.aoi
        )
        items = self.generate_itmes(search)
      
        return items
    
    def generate_itmes(self, search: ItemSearch) -> List[Item]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        items = search.get_all_items()
        # WHAT IF ITEM COLLECTION IS EMPTY?   ADD A BIT OF LOGIC 
        result = items.items[0].to_dict()
        pystac_items = items.items
        return pystac_items
