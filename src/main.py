from src.datasets.open_meteo import get_hourly
from src.algorithms.features import make_features
from src.algorithms.kmeans_cluster import cluster_weather
from src.algorithms.utils import display_subset
from src.algorithms.weighted_scoring_model import get_scored_alerts
from src.datasets.locations import cities
from concurrent.futures import ThreadPoolExecutor, as_completed

PLACES = cities()

def _build_city_row(name, lat, lon, hours):
    df = get_hourly(lat, lon, hours=hours)
    if df.empty:
        return name, None
    feats = make_features(df)
    if not feats:
        return name, None

    try:
        alerts = get_scored_alerts(lat, lon, hours=hours)
        if alerts is not None and not alerts.empty:
            top = alerts.iloc[0]
            feats["top_alert_score"] = float(top.get("score", 0.0))
            feats["top_alert_event"] = str(top.get("event", ""))
        else:
            feats["top_alert_score"] = 0.0
            feats["top_alert_event"] = ""
    except Exception as e:
        feats["top_alert_score"] = 0.0
        feats["top_alert_event"] = ""

    return name, feats

def run(hours=24, k=5, debug=False, return_df=False):
    # build features per city
    city_features = {}

    workers = min(32, max(4, len(PLACES) * 2))

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {
            ex.submit(_build_city_row, name, lat, lon, hours): name
            for name, (lat, lon) in PLACES.items()
        }
        for fut in as_completed(futures):
            name = futures[fut]
            try:
                name, feats = fut.result()
                if feats:
                    city_features[name] = feats
                elif debug:
                    print(f"skipping {name}: empty data, causing me issues.")
            except Exception as e:
                if debug:
                    print(f"Process failed entirely (ThreadPoolExecutor in main.py): {e}")

    clustered_df, model = cluster_weather(city_features, k=k)
    if clustered_df is None or clustered_df.empty:
        if debug: print("no clustering results")
        return (None, None) if return_df else None

    # add display columns (fahrenheit temp and lat/lon)
    clustered_df = clustered_df.copy()
    if "temp_diff" in clustered_df.columns:
        clustered_df["temp_diff_F"] = clustered_df["temp_diff"] * 9.0 / 5.0
    clustered_df["lat"] = [PLACES[name][0] for name in clustered_df.index]
    clustered_df["lon"] = [PLACES[name][1] for name in clustered_df.index]

    if return_df:
        return clustered_df, model

    # minimal console view (only if debug)
    if debug:
        preferred_cols = ["cluster", "temp_diff_F", "avg_wind", "max_gust",
                          "total_rain", "rain_hours", "top_alert_score", "top_alert_event"]
        print(f"\n=== K-Means Clustering Results (k={k}) ===")
        print(display_subset(clustered_df, preferred_cols))
    return None