import openmeteo_requests
import pandas as pd
import requests_cache

from retry_requests import retry


# ==========================================
# Setup Open-Meteo API Client
# ==========================================

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


# ==========================================
# Air Quality Function
# ==========================================

def get_air_quality_data():

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": 52.52,
        "longitude": 13.41,

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

    hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
    hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
    hourly_carbon_monoxide = hourly.Variables(2).ValuesAsNumpy()
    hourly_carbon_dioxide = hourly.Variables(3).ValuesAsNumpy()
    hourly_sulphur_dioxide = hourly.Variables(4).ValuesAsNumpy()
    hourly_methane = hourly.Variables(5).ValuesAsNumpy()
    hourly_dust = hourly.Variables(6).ValuesAsNumpy()
    hourly_total_elementary_carbon = hourly.Variables(7).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(
                hourly.Time(),
                unit="s",
                utc=True
            ),

            end=pd.to_datetime(
                hourly.TimeEnd(),
                unit="s",
                utc=True
            ),

            freq=pd.Timedelta(
                seconds=hourly.Interval()
            ),

            inclusive="left"
        ),

        "pm10": hourly_pm10,
        "pm2_5": hourly_pm2_5,
        "carbon_monoxide": hourly_carbon_monoxide,
        "carbon_dioxide": hourly_carbon_dioxide,
        "sulphur_dioxide": hourly_sulphur_dioxide,
        "methane": hourly_methane,
        "dust": hourly_dust,
        "total_elementary_carbon": hourly_total_elementary_carbon
    }

    hourly_dataframe = pd.DataFrame(
        data=hourly_data
    )

    return hourly_dataframe