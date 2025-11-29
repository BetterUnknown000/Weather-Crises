from src.datasets.open_meteo import get_hourly
from src.algorithms.features import make_features
from src.algorithms.kmeans_cluster import cluster_weather
from src.datasets.locations import cities

PLACES = cities()

def tempdiff_to_f(x: float) -> float:
    # Convert Celsius difference to Fahrenheit difference (no offset)
    return x * 9.0 / 5.0

def run(hours=24, k=5, debug=False):
    city_features = {}

    # Collect features per city
    for name, (lat, lon) in PLACES.items():
        df = get_hourly(lat, lon, hours=hours)
        if df.empty:
            if debug:
                print(f"Skipping {name}: empty data frame")
            continue

        if debug:
            # Optional quick peek at raw data for troubleshooting
            print(f"\n-- {name} --")
            print(df.head())

        feats = make_features(df)
        if feats:
            city_features[name] = feats
        elif debug:
            print(f"Skipping {name}: features empty")

    clustered_df, model = cluster_weather(city_features, k=k)
    if clustered_df is None or clustered_df.empty:
        print("No clustering results.")
        return

    # Keep temp_diff for modeling, add Fahrenheit display column
    clustered_df = clustered_df.copy()
    if "temp_diff" in clustered_df.columns:
        clustered_df["temp_diff_F"] = clustered_df["temp_diff"].apply(tempdiff_to_f)

    # Columns to show in console / drive website view
    preferred_cols = [
        "cluster",
        "temp_diff_F",
        "avg_wind",
        "max_gust",
        "total_rain",
        "rain_hours",
        "pressure_change"
    ]
    display_cols = [c for c in preferred_cols if c in clustered_df.columns]
    display_df = clustered_df[display_cols].sort_values("cluster").round(2)

    print(f"\n=== K-Means Clustering Results (k={k}) ===")
    print(display_df)

    # Summaries and compact labels
    byc = clustered_df.groupby("cluster")
    stats_cols = [c for c in ["temp_diff", "avg_wind", "max_gust", "total_rain", "rain_hours", "pressure_change"]
                  if c in clustered_df.columns]
    means = byc[stats_cols].mean().round(2)
    counts = byc.size()

    # Medians used to create simple relative labels
    med = clustered_df[[c for c in ["temp_diff", "avg_wind", "max_gust", "total_rain"]
                        if c in clustered_df.columns]].median()

    def label_for(mrow):
        parts = []
        if "temp_diff" in mrow and "temp_diff" in med:
            parts.append("warming" if mrow["temp_diff"] >= med["temp_diff"] else "cooling")
        if "avg_wind" in mrow and "avg_wind" in med:
            parts.append("windy" if mrow["avg_wind"] >= med["avg_wind"] else "not-windy")
        if "max_gust" in mrow and "max_gust" in med:
            parts.append("gusty" if mrow["max_gust"] >= med["max_gust"] else "low-gust")
        if "total_rain" in mrow and "total_rain" in med:
            parts.append("wet" if mrow["total_rain"] >= med["total_rain"] else "dry")
        return ", ".join(parts)

    for c in sorted(means.index):
        m = means.loc[c]
        n = int(counts.loc[c])
        members = sorted(clustered_df[clustered_df["cluster"] == c].index.tolist())

        tdF_center = m["temp_diff"] * 9.0 / 5.0 if "temp_diff" in m else None
        center_bits = []
        if tdF_center is not None:
            center_bits.append(f"temp change {tdF_center:.2f} F")
        if "avg_wind" in m:
            center_bits.append(f"wind {m['avg_wind']:.2f} m/s")
        if "max_gust" in m:
            center_bits.append(f"gust {m['max_gust']:.2f} m/s")
        if "total_rain" in m:
            center_bits.append(f"rain {m['total_rain']:.2f} mm")
        if "rain_hours" in m:
            center_bits.append(f"rain_hours {m['rain_hours']:.2f}")
        if "pressure_change" in m:
            center_bits.append(f"pressure change {m['pressure_change']:.2f} hPa")

        print(f"\nCluster {c} ({n} cities)")
        print(f"Label: {label_for(m)}")
        print("Center: " + ", ".join(center_bits))
        print("Cities: " + "; ".join(members))

if __name__ == "__main__":
    run(hours=24, k=5, debug=False)
