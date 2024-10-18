

WORLD_POP_PATH = ''
CHIRPS_STAC_ENDPONT = "https://explorer.digitalearth.africa/stac/collections/rainfall_chirps_daily"
IO_LULC_STAC_ENDPOINT = "https://api.impactobservatory.com/stac-aws/collections/io-10m-annual-lulc/items"



def main():
    """
    1. Pull data
    2. Preprocess - resample, reproject, masking, stitch tiles
    3. Analysis
    4. Export
    """

    return 