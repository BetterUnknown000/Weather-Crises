import pandas as pd

def make_features(df):
    """
    This function takes the weather data from Open-Meteo.py in datasets
    and turns it into stats that can be used for our K-Means algorithm for clustering
    """
    if df.empty:
        print("Got call from Open-Meteo.py, but features.py finds it empty.")
        return {}

    try:
        # Make sure everything is numeric
        for col in ["wind_speed_10m", "wind_gusts_10m", "precipitation", "surface_pressure"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Basic stats that we should be getting
        avg_wind = df["wind_speed_10m"].mean()
        max_gust = df["wind_gusts_10m"].max()
        total_rain = df["precipitation"].sum()
        pressure_change = df["surface_pressure"].iloc[-1] - df["surface_pressure"].iloc[0]
        wind_var = df["wind_speed_10m"].var()

        return {
            "avg_wind": float(avg_wind),
            "max_gust": float(max_gust),
            "total_rain": float(total_rain),
            "pressure_change": float(pressure_change),
            "wind_var": float(wind_var),
        }

    except Exception as e:
        print("Error while making features in features.py: ", e)
        return {}