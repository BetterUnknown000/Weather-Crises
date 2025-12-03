import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Adding Retry, something I looked up would help with speed. also considering getting rid of auto k for k-means, since it runs slow.
_session = requests.Session()
_retry = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET", "HEAD"])
)
_adapter = HTTPAdapter(max_retries=_retry, pool_connections=100, pool_maxsize=100)
_session.mount("https://", _adapter)
_session.headers.update({"User-Agent": "Weather-Crises-Project/1.0"})

def get_hourly(lat: float, lon: float, hours: int = 12) -> pd.DataFrame:
    """
    Fetch hourly weather data from Open-Meteo for the given coordinates.
    Returns the last `hours` rows as a DataFrame.
    Returns an empty DataFrame on error.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly="
        "temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation,precipitation_probability,"
        "surface_pressure,relative_humidity_2m,dew_point_2m,cloudcover,snowfall"
        "&timezone=America/New_York"
    )
    try:
        r = _session.get(url, timeout=(3.05, 20))
        r.raise_for_status()
        data = r.json()
        if "hourly" not in data:
            return pd.DataFrame()
        return pd.DataFrame(data["hourly"]).tail(hours)

    except Exception as e:
        print("There was an error getting data from open_meteo.py:", e)
        return pd.DataFrame()
