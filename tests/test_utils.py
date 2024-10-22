from e84_proj.extract.utils import coords_to_polygon
import pytest
from shapely.geometry import Polygon


@pytest.mark.parametrize(
    "coords,out_crs,expected", 
    [
        pytest.param(
            [
                (15.57692, 11.28722),
                (16.69969, 11.29509),
                (16.79151, 10.03066),
                (15.42739, 10.03853),
                (15.57692, 11.28722)
            ],
            'epsg:4326',
            Polygon( [
                (15.57692, 11.28722),
                (16.69969, 11.29509),
                (16.79151, 10.03066),
                (15.42739, 10.03853),
                (15.57692, 11.28722)
            ]),
            id='epsg:4326 to epsg:4326',
        ),
        pytest.param(
            [
                (15.57692, 11.28722),
                (16.69969, 11.29509),
                (16.79151, 10.03066),
                (15.42739, 10.03853),
                (15.57692, 11.28722)
            ],
            'epsg:3857',
            Polygon( [
                (1734014.802527559, 1264694.4344271997),
                (1859000.9872055226, 1265587.8102015776),
                (1869222.342850161, 1122355.8460099674),
                (1717369.1990692408, 1123245.5403012016),
                (1734014.802527559, 1264694.4344271997)
            ]),
            id='epsg:4326 to epsg:3857',
        ),
    ]
)
def test_coords_to_polygon(coords, out_crs, expected):
    actual = coords_to_polygon(coords, out_crs)
    assert actual == expected