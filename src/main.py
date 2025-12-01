from src.datasets.open_meteo import get_hourly
from src.algorithms.features import make_features
from src.algorithms.kmeans_cluster import cluster_weather, choose_k  # <-- import choose_k
from src.algorithms.utils import tempdiff_to_f, display_subset
from src.datasets.locations import cities

PLACES = cities()

def run(hours=24, k=5, debug=False, return_df=False):
    # build features per city
    city_features = {}
    for name, (lat, lon) in PLACES.items():
        df = get_hourly(lat, lon, hours=hours)
        if df.empty:
            if debug: print(f"skip {name}: empty data")
            continue
        feats = make_features(df)
        if feats:
            city_features[name] = feats
        elif debug:
            print(f"skip {name}: no features")

    # pick k automatically if k is None (choose_k lives in kmeans_cluster.py)
    if k is None:
        k = choose_k(city_features)

    clustered_df, model = cluster_weather(city_features, k=k)
    if clustered_df is None or clustered_df.empty:
        if debug: print("no clustering results")
        return (None, None) if return_df else None

    # add display columns (fahrenheit temp change and lat/lon)
    clustered_df = clustered_df.copy()
    if "temp_diff" in clustered_df.columns:
        clustered_df["temp_diff_F"] = clustered_df["temp_diff"].apply(tempdiff_to_f)
    clustered_df["lat"] = [PLACES[name][0] for name in clustered_df.index]
    clustered_df["lon"] = [PLACES[name][1] for name in clustered_df.index]

    if return_df:
        return clustered_df, model

    # minimal console view (only if debug)
    if debug:
        preferred_cols = ["cluster", "temp_diff_F", "avg_wind", "max_gust",
                          "total_rain", "rain_hours"]  # pressure_change dropped from print
        print(f"\n=== K-Means Clustering Results (k={k}) ===")
        print(display_subset(clustered_df, preferred_cols))
    return None