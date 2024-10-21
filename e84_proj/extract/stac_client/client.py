from typing import List
from pystac_client import Client, ItemSearch
from shapely.geometry import Polygon
from pystac import Item

class StacClient:
    """
    client used to create STAC connections, search STAC API, and create lists 
    of hrefs to assets that are desired to be downloaded
    """
    def __init__(self, catalog_endpoint: str, collection: str):
        """_summary_

        Args:
            catalog_endpoint (str): STAC catalog endpoint
            collection (str): collection string for search
        """
        self.endpoint = catalog_endpoint
        self.collection = collection

    def connection_factory(self) -> Client:
        """
        factory to create client connected to stac catalog endpoint

        Returns:
            Client: client connected to target catalog
        """
        print('hold')
        catalog = Client.open(self.endpoint)
        return catalog

    def aoi_search(self, client: Client, aoi: Polygon, date='str') -> List[Item]:
        """
        search stac API for items in AOI

        Args:
            client (Client): STAC client
            aoi (Polygon): shapely polygon for search
            date: string date like '2015-01-03' for date search too

        Returns:
            List[Item]: List of items from the collection that are in the AOI
        """
        search = client.search(
            collections=self.collection,
            intersects=aoi,
            datetime=date
        )
        items = self.generate_itmes(search)
      
        return items

    def generate_itmes(self, search: ItemSearch) -> List[str]:
        """
        take search results and generate href links for download
        by parsing through item attributes and assets
        Args:
            search (ItemSearch): search results

        Returns:
            List[str]: list of hrefs of items that were found as matches
        """

        item_links = []
        for item in search.items():
            # TODO: what if search results are empty?
            for key in item.assets.keys():
                # could be multiple keys, only have one for now
                link = item.assets[key].href
                item_links.append(link)

        return item_links
