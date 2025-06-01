import pvlib
from pvlib.location import Location
from datetime import datetime, timezone
from pydantic import BaseModel


class SolarPanelData(BaseModel):
    lat: float
    lon: float
    tilt: float
    azimuth: float
    area: float
    efficiency: float
    weather: str = ""
    time: datetime | None = None

    def as_dict(self):
        return {
            "lat": self.lat,
            "lon": self.lon,
            "tilt": self.tilt,
            "azimuth": self.azimuth,
            "area": self.area,
            "efficiency": self.efficiency,
            "weather": self.weather,
            "time": self.time.isoformat() if self.time else None
        }


def estimate_dni(weather):
    """Zwraca przybliżone DNI na podstawie warunków pogodowych."""
    dni_map = {
        'clear': 950,
        'partly_cloudy': 600,
        'cloudy': 200,
        'rain': 50
    }
    return dni_map.get(weather, 0)


def calculate_panel_output(lat, lon, tilt, azimuth, area, efficiency, weather='clear', time=None):
    if time is None:
        time = datetime.now(timezone.utc)

    site = Location(latitude=lat, longitude=lon)

    solpos = site.get_solarposition(time)
    zenith = solpos['apparent_zenith'].iloc[0]
    azim = solpos['azimuth'].iloc[0]

    if zenith > 90:
        return {
            'time': time,
            'aoi': None,
            'incident_power': 0,
            'power_output': 0,
            'note': 'Sun is below horizon'
        }

    dni = estimate_dni(weather)

    aoi = pvlib.irradiance.aoi(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        solar_zenith=zenith,
        solar_azimuth=azim
    )

    incident_power = dni * pvlib.tools.cosd(aoi)
    incident_power = max(0, incident_power)

    power_output = incident_power * area * efficiency

    return {
        'time': time,
        'weather': weather,
        'dni': dni,
        'aoi': float(aoi),
        'incident_power': incident_power,
        'power_output': power_output,
        'estimated_production_per_hour': power_output + calculate_panel_output(
            lat, lon, tilt, azimuth, area, efficiency, weather, time.replace(
                hour=time.hour + 1)
        )['power_output'] / 2
    }
