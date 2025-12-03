import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Adding for speed issues.
_session = requests.Session()
_retry = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET", "HEAD"])
)
_adapter = HTTPAdapter(max_retries=_retry, pool_connections=100, pool_maxsize=100)
_session.mount("https://", _adapter)

_session.headers.update({
    "User-Agent": "Weather-Crises-Project/1.0 (github.com)",
    "Accept": "application/geo+json"
})

# okay so basically, I modeled after your open_meteo dataset loader with some adjustments
def get_alerts(lat, lon, hours=24):

    # URL for API, using NWS API instead of OpenMeteo obv
    url = (
            "https://api.weather.gov/alerts/active?point="
            + str(lat)
            + ","
            + str(lon)
    )

    # okay this was a little wierd, but apparently because NWS is a govertnment org, we need to include these headers to access data
    # otherwise we will not be able to access anything. make sure we aren't spies or somnethig
    headers = {
        "User-Agent": "Weather-Crises-Project/1.0 (github.com)",
        "Accept": "application/geo+json"
    }

    try:
        # Get the data from the API
        r = _session.get(url, headers=headers, timeout=(3.05, 20))
        r.raise_for_status() # Fail fast to stop redundancy

        data = r.json()

        # Extract alert properties from features
        # a lot of meh here, but I think event, severity and description will be useful to us
        alerts = []
        for feature in data.get("features", []):
            properties = feature.get("properties", {})
            alerts.append({
                "id": properties.get("id", ""),
                "event": properties.get("event", ""),
                "severity": properties.get("severity", "Unknown"),
                "certainty": properties.get("certainty", "Unknown"),
                "urgency": properties.get("urgency", "Unknown"),
                "headline": properties.get("headline", ""),
                "description": properties.get("description", ""),
                "instruction": properties.get("instruction", ""),
                "areaDesc": properties.get("areaDesc", ""),
                "sent": properties.get("sent", ""),
                "effective": properties.get("effective", ""),
                "onset": properties.get("onset", ""),
                "expires": properties.get("expires", ""),
                "ends": properties.get("ends", ""),
                "status": properties.get("status", ""),
                "messageType": properties.get("messageType", ""),
                "category": properties.get("category", ""),
                "sender": properties.get("sender", ""),
                "senderName": properties.get("senderName", ""),
            })

        # Turn the alert data into a table
        df = pd.DataFrame(alerts)

        return df

    except Exception as e:
        # If an error occurs, print out so we know and return empty
        print("There was a error getting data from nws_alerts.py: ", e)
        return pd.DataFrame()


if __name__ == "__main__":
    print("Testing NWS alerts data pull...")

    # Test with state-wide query for PA (I treid using the state college area that you used for OpenMeteo but there is nothing. Even searching all of PA only gives me 3 results.
    # this is because NWS searches for active alerts. Maybe I can search for alerts in a period of time, but idk yet
    url = "https://api.weather.gov/alerts/active?area=PA"
    headers = {
        "User-Agent": "Weather-Crises-Project/1.0 (github.com)",
        "Accept": "application/geo+json"
    }
    try:
        r = _session.get(url, headers=headers, timeout=(3.05, 20))
        r.raise_for_status()
        data = r.json()

        # Extract alert properties from features
        # just picked stuff I thought might be useful
        # severity is issued in a word format like "Moderate"
        # so we will need to identify the severity words and transfer them into numbvers
        alerts = []
        for feature in data.get("features", []):
            properties = feature.get("properties", {})
            alerts.append({
                "id": properties.get("id", ""),
                "event": properties.get("event", ""),
                "severity": properties.get("severity", "Unknown"),
                "certainty": properties.get("certainty", "Unknown"),
                "urgency": properties.get("urgency", "Unknown"),
                "headline": properties.get("headline", ""),
                "areaDesc": properties.get("areaDesc", ""),
            })

        df = pd.DataFrame(alerts)
        print(f"Found {len(df)} active alerts in Pennsylvania")
        print(df.head())
        print("Rows: ", len(df))

    except Exception as e:
        print(f"Error: {e}")