import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from utils.osm import geocode_address, create_bbox, query_buildings, osm_to_geojson, check_address, filter_buildings, calculate_average_centroid, add_bbox_to_properties, find_main_and_n_nearest_without_housenumber, Address
from utils.solar_panel import calculate_panel_output, SolarPanelData
from api.calculator_api import router as calculator_router

app = FastAPI()
origins = [
    'http://localhost',
    'http://localhost:8081',
    'localhost'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/storage", StaticFiles(directory="storage"), name="storage")

app.include_router(calculator_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/house_address")
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
        add_bbox_to_properties(output)
        output['properties']['average_centroid'] = [0, 0]
        return output
    else:
        raise HTTPException(status_code=400, detail="No address provided")


@app.post("/api/solar_panel_data")
def solar_panel_data(panel_data: SolarPanelData):
    try:
        result = calculate_panel_output(
            panel_data.lat,
            panel_data.lon,
            panel_data.tilt,
            panel_data.azimuth,
            panel_data.area,
            panel_data.efficiency,
            panel_data.weather,
            panel_data.time
        )
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
