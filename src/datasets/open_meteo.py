import requests
import pandas as pd

def get_hourly(lat, lon, hours=24):
    """
    This function simply pulls the recent hourly weather data
    from the Open-Meteo API. This is going to return
    a table with the time, wind speed, gusts, rain, and pressure.
    """

    # URL for API, with State College as a tester location
    url = (
            "https://api.open-meteo.com/v1/forecast?"
            + "latitude=" + str(lat)
            + "&longitude=" + str(lon)
            + "&hourly="
              "temperature_2m,"
              "wind_speed_10m,wind_gusts_10m,"
              "precipitation,precipitation_probability,"
              "surface_pressure,"
              "relative_humidity_2m,dew_point_2m,"
              "cloudcover,snowfall"
            + "&timezone=America/New_York"
    )
    try:
        # Get the data from the API
        r = requests.get(url, timeout=30)
        data = r.json()

        # Turn the hourly data into a table
        df = pd.DataFrame(data["hourly"])

        # Only keep recent data (last few hours)
        df = df.tail(hours)

        return df

    except Exception as e:
        # If an error occurs, print out so we know and return empty
        print("There was a error getting data from open_meteo.py: ", e)
        return pd.DataFrame()

if __name__ == "__main__":
    print("Testing Open-Meteo data pull...")
    df = get_hourly(40.8, -77.86) # State College coords
    print(df.head())
    print("Rows: ", len(df))