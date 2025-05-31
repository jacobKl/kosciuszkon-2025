import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.osm import geocode_address, create_bbox, query_buildings, osm_to_geojson, check_address, filter_buildings, calculate_average_centroid, find_main_and_n_nearest_without_housenumber, Address
app = FastAPI()
origins = [
    'http://localhost',
    'localhost'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/house_address")
async def house_address(address: Address) -> dict[str, str] | dict:
    dict_address = address.as_dict()
    if address and check_address(dict_address):
        lat, lon = geocode_address(str(address))
        bbox = create_bbox(lat, lon)
        buildings_osm = query_buildings(bbox)
        geojson = osm_to_geojson(buildings_osm)
        output = find_main_and_n_nearest_without_housenumber(
            geojson, lat, lon, int(dict_address['external_garage_count']))
        average_centroid = calculate_average_centroid(output)
        output['properties'] = {}
        output['properties']['average_centroid'] = {
            "lat": average_centroid[0], "lon": average_centroid[1]}
        output['properties']['address'] = str(address)
        output['properties']['garages_found'] = len(output['features']) - 1
        return output
    else:
        raise HTTPException(status_code=400, detail="No address provided")
