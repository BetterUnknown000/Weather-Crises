import pandas as pd

def make_features(df):
    """
    Turn an hourly Open-Meteo dataframe into features for K-Means.
    """
    if df.empty:
        print("Got call from Open-Meteo.py, but features.py finds it empty.")
        return {}

    try:
        # Ensure numeric types
        for col in ["temperature_2m", "wind_speed_10m", "wind_gusts_10m", "precipitation", "surface_pressure", "relative_humidity_2m", "dew_point_2m", "precipitation_probability", "cloudcover", "snowfall",]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Wind
        avg_wind = df["wind_speed_10m"].mean()
        max_gust = df["wind_gusts_10m"].max()
        wind_var = df["wind_speed_10m"].var()
        gust_ratio = (max_gust / avg_wind) if avg_wind else 0.0

        # Rain / precipitation
        total_rain = df["precipitation"].sum()
        mean_rain = df["precipitation"].mean()
        rain_hours = int((df["precipitation"] > 0).sum())

        # Pressure
        pressure_change = df["surface_pressure"].iloc[-1] - df["surface_pressure"].iloc[0]
        avg_pressure = df["surface_pressure"].mean()

        # Temperature
        max_temp = df["temperature_2m"].max()
        min_temp = df["temperature_2m"].min()
        temp_range = max_temp - min_temp
        avg_temp = df["temperature_2m"].mean()

        temp_diff = df["temperature_2m"].iloc[-1] - df["temperature_2m"].iloc[0]

        humidity_mean = df["relative_humidity_2m"].mean() if "relative_humidity_2m" in df else 0.0
        dewpoint_change = (df["dew_point_2m"].iloc[-1] - df["dew_point_2m"].iloc[0]) if "dew_point_2m" in df else 0.0
        precip_prob_max = df["precipitation_probability"].max() if "precipitation_probability" in df else 0.0
        cloudcover_mean = df["cloudcover"].mean() if "cloudcover" in df else 0.0
        total_snow = df["snowfall"].sum() if "snowfall" in df else 0.0

        return {
            "temp_diff": float(temp_diff),
            "avg_temp": float(avg_temp),
            "temp_range": float(temp_range),
            "avg_wind": float(avg_wind),
            "max_gust": float(max_gust),
            "gust_ratio": float(gust_ratio),
            "total_rain": float(total_rain),
            "mean_rain": float(mean_rain),
            "rain_hours": float(rain_hours),
            "pressure_change": float(pressure_change),
            "avg_pressure": float(avg_pressure),
            "wind_var": float(wind_var),
            "humidity_mean": float(humidity_mean),
            "dewpoint_change": float(dewpoint_change),
            "precip_prob_max": float(precip_prob_max),
            "cloudcover_mean": float(cloudcover_mean),
            "total_snow": float(total_snow)
        }

    except Exception as e:
        print("Error while making features in features.py:", e)
        return {}
