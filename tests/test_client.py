from unittest.mock import patch, MagicMock
from unittest import mock

import pytest
from shapely.geometry import Polygon

from e84_proj.extract.stac_client.client import StacClient

@pytest.mark.parametrize(
    "catalog_endpoint,collection", 
    [
        pytest.param(
            'fake_endpoint',
            'fake_collection',
            id='mock endpoint call to open client'
        )
    ]
)
@mock.patch('pystac_client.Client.open')
def test_connection_factory(mock_open, catalog_endpoint, collection):
    client = StacClient(catalog_endpoint=catalog_endpoint, collection=collection)
    actual = client.connection_factory()
    mock_open.assert_called_once()