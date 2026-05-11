import openmeteo_requests
import requests_cache
from retry_requests import retry

# Cache + Retry
cache_session = requests_cache.CachedSession(
    '.cache',
    expire_after=3600
)

retry_session = retry(
    cache_session,
    retries=5,
    backoff_factor=0.2
)

openmeteo = openmeteo_requests.Client(
    session=retry_session
)

def get_air_quality_data():

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {

        # CHANGE THESE COORDINATES
        "latitude": 28.2102,
        "longitude": 76.8606,

        "hourly": [
            "pm10",
            "pm2_5",
            "carbon_monoxide",
            "carbon_dioxide",
            "sulphur_dioxide",
            "methane",
            "dust",
            "total_elementary_carbon"
        ],

        "forecast_hours": 6,
        "past_hours": 6,
    }

    responses = openmeteo.weather_api(
        url,
        params=params
    )

    response = responses[0]
    hourly = response.Hourly()

    data = {
        "pm10": hourly.Variables(0).ValuesAsNumpy()[-1],
        "pm2_5": hourly.Variables(1).ValuesAsNumpy()[-1],
        "carbon_monoxide": hourly.Variables(2).ValuesAsNumpy()[-1],
        "carbon_dioxide": hourly.Variables(3).ValuesAsNumpy()[-1],
        "sulphur_dioxide": hourly.Variables(4).ValuesAsNumpy()[-1],
        "methane": hourly.Variables(5).ValuesAsNumpy()[-1],
        "dust": hourly.Variables(6).ValuesAsNumpy()[-1],
        "total_elementary_carbon": hourly.Variables(7).ValuesAsNumpy()[-1],
    }

    return data