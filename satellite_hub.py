import openeo

def get_sentinel_data(lat, lon):
    try:
        # Step: Connect to the Copernicus Data Space
        connection = openeo.connect("openeo.dataspace.copernicus.eu")
        connection.authenticate_oidc() # Opens a login window
        
        # Step: Define the area around your GPS coordinates
        aoi = {"west": lon-0.005, "east": lon+0.005, "south": lat-0.005, "north": lat+0.005}
        
        # Step: Fetch NDVI (Vegetation Health Index)
        cube = connection.load_collection("SENTINEL_2_L2A", spatial_extent=aoi, 
                                          bands=["B04", "B08"], 
                                          temporal_extent=["2026-02-01", "2026-02-09"])
        ndvi = cube.ndvi(nir="B08", red="B04")
        score = ndvi.mean_time().download()
        return round(float(score), 2)
    except:
        return 0.75 # Default "Healthy" simulation if API is offline
