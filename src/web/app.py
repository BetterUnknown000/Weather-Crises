from flask import Flask, render_template
from src.main import run
from src.algorithms.utils import tempdiff_to_f

app = Flask(__name__)

@app.route("/")
def index():
    df, _ = run(hours=12, k=None, debug=False, return_df=True)
    if df is None or df.empty:
        return "<h3>No results.</h3>"

    if "avg_temp" in df.columns:
        df["Average Temperature (F)"] = df["avg_temp"].apply(tempdiff_to_f).apply(lambda x: x + 32.0)

    # Labels
    rename_map = {
        "avg_wind":        "Avg Wind (m/s)",
        "max_gust":        "Max Gust (m/s)",
        "total_rain":      "Total Rain (mm)",
        "total_snow":      "Total Snowfall (mm)",
        "precip_prob_max": "Max Precip Prob (%)",
    }
    df.rename(columns=rename_map, inplace=True)

    # Shown
    display_cols = [c for c in [
        "Average Temperature (F)",
        "Avg Wind (m/s)",
        "Total Rain (mm)",
        "Total Snowfall (mm)",
        "Max Precip Prob (%)",
    ] if c in df.columns]

    # Keep coords numeric for the map
    if "lat" in df.columns: df["lat"] = df["lat"].astype(float)
    if "lon" in df.columns: df["lon"] = df["lon"].astype(float)

    # Round only user display columns
    for c in display_cols:
        df[c] = df[c].round(2)

    # Build a slim frame for the UI
    slim = df[["cluster", "lat", "lon"] + display_cols].copy()

    counts = (
        slim["cluster"].value_counts().sort_index()
        .rename_axis("cluster").reset_index(name="count").to_dict(orient="records")
    )
    summary = (
        slim.groupby("cluster")[display_cols].mean().round(2)
        .reset_index().to_dict(orient="records")
    )
    rows = slim.reset_index().to_dict(orient="records")

    return render_template(
        "index.html",
        rows=rows,
        counts=counts,
        summary=summary,
        display_cols=display_cols
    )

if __name__ == "__main__":
    app.run(debug=True)
