from flask import Flask, render_template
from src.main import run

app = Flask(__name__)

@app.route("/")
def index():
    # Faster page loads: avoid silhouette sweeps here
    df, _ = run(hours=12, k=4, debug=False, return_df=True)
    if df is None or df.empty:
        return "<h3>No results.</h3>"

    # -------- Alerts (banner only) --------
    alerts = []
    if "top_alert_score" in df.columns and "top_alert_event" in df.columns:
        for city, row in df.iterrows():
            score = float(row.get("top_alert_score", 0.0) or 0.0)
            event = (row.get("top_alert_event") or "").strip()
            if score > 0 and event:
                alerts.append({
                    "city": city,
                    "event": event,
                    "score": round(score, 2),
                    "lat": float(row.get("lat", 0.0) or 0.0),
                    "lon": float(row.get("lon", 0.0) or 0.0),
                })

    # sort alerts by severity desc, then state, then city
    def _state_of(city: str) -> str:
        if not city:
            return ""
        parts = city.rsplit(", ", 1)
        return parts[1] if len(parts) == 2 else ""

    alerts.sort(key=lambda a: (-a["score"], _state_of(a["city"]), a["city"]))
    banner_alerts = alerts[:5]   # top 5 chips

    # -------- Main weather table prep --------
    # Optional: show Fahrenheit average temp if available
    if "avg_temp" in df.columns:
        df["Average Temperature (F)"] = (df["avg_temp"] * 9.0 / 5.0) + 32.0

    # Friendly labels
    rename_map = {
        "avg_wind":        "Avg Wind (m/s)",
        "max_gust":        "Max Gust (m/s)",
        "total_rain":      "Total Rain (mm)",
        "total_snow":      "Total Snowfall (mm)",
        "precip_prob_max": "Max Precip Prob (%)",
        "top_alert_score": "Top Alert Score",
        "top_alert_event": "Top Alert Event",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Keep coords numeric for mapping
    if "lat" in df.columns: df["lat"] = df["lat"].astype(float)
    if "lon" in df.columns: df["lon"] = df["lon"].astype(float)

    # Round numeric display columns
    for c in df.columns:
        try:
            if df[c].dtype.kind in "fc":
                df[c] = df[c].round(2)
        except Exception:
            pass

    display_cols = [c for c in [
        "Average Temperature (F)",
        "Avg Wind (m/s)",
        "Total Rain (mm)",
        "Total Snowfall (mm)",
        "Max Precip Prob (%)",
        "Top Alert Score",
        "Top Alert Event",
    ] if c in df.columns]

    # Sort by state, then city BEFORE building rows
    def _split_state_city(s: str):
        if not s:
            return ("", "")
        parts = s.rsplit(", ", 1)
        if len(parts) == 2:
            return (parts[1], parts[0])  # (state, city)
        return ("", s)

    df_sorted = (
        df.reset_index(names=["city"])
          .assign(_state=lambda x: x["city"].apply(lambda s: _split_state_city(s)[0]),
                  _city=lambda x: x["city"].apply(lambda s: _split_state_city(s)[1]))
          .sort_values(["_state", "_city"], kind="mergesort")
    )

    # Rows for your existing table/map
    rows = (
        df_sorted[["city", "cluster", "lat", "lon"] + display_cols]
        .to_dict(orient="records")
    )

    # Cluster counts and numeric means
    from collections import Counter
    counts = [{"cluster": k, "count": v} for k, v in sorted(Counter(df["cluster"]).items())]

    num_cols = [c for c in display_cols if c in df.columns and df[c].dtype.kind in "fc"]
    summary = (
        df.groupby("cluster")[num_cols].mean().round(2).reset_index().to_dict(orient="records")
        if num_cols else []
    )

    # -------- Single return --------
    return render_template(
        "index.html",
        rows=rows,
        counts=counts,
        summary=summary,
        display_cols=display_cols,
        banner_alerts=banner_alerts,
    )


if __name__ == "__main__":
    app.run(debug=True)
