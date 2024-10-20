

WORLD_POP_PATH = ''
CHIRPS_STAC_ENDPONT = "https://explorer.digitalearth.africa/stac/collections/rainfall_chirps_daily"
IO_LULC_STAC_ENDPOINT = "https://api.impactobservatory.com/stac-aws/collections/io-10m-annual-lulc/items"



def main(world_pop: str = WORLD_POP_PATH, chirps: str = CHIRPS_STAC_ENDPONT, lulc: str = IO_LULC_STAC_ENDPOINT):
    """
    1. Pull data
    2. Preprocess - resample, reproject, masking, stitch tiles
    3. Analysis
    4. Export

    Args:
        world_pop (str): path to the target world pop dataset
        chirps (str): path to STAC v1.0 endpoint for chirps rainfall dataset
        lulc (str): path to STAC v1.0 endpoint for LULC dataset
    """
    print('hello from main!')
    return 

if __name__ == "__main__":
    main()
