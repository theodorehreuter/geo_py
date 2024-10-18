import pytest
from geo_py.geopandas_wk import adder


# def adder(x: int, y: int) -> int:
#     return x + y

def test_initial_pass():
    assert 1 == 1

# def test_initial_fail(): 
#     assert 1 != 1


adder_testdata = [
    (1, 2, 3),
    (2, 2, 4)
]
@pytest.mark.parametrize("a, b, expected", adder_testdata)
def test_adder(a, b, expected):
    actual = adder(a, b)
    print(f"actual! {actual}")
    assert actual == expected