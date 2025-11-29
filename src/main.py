from src.datasets.open_meteo import get_hourly
from src.algorithms.features import make_features

# Only having this here so you can install the packages easily
# Once this is ran once, and we have our website setup, we can remove this try block.
# Makes sure everything needed is installed before running
import sys, subprocess, os

try:
    import requests, pandas, numpy, sklearn, flask
except ImportError:
    print("Installing missing packages... please wait.")
    base = os.path.dirname(os.path.dirname(__file__))  # go up to project root
    req_path = os.path.join(base, "requirements.txt")

    # Runs the install
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
    print("All set! Please run this file again.")
    sys.exit()


PLACES = {
    "State College, PA": (40.80, -77.86),
    "Abington, PA": (40.12, -75.13),
}

def run(hours=24):
    print("Testing Open-Meteo fetch + features...")
    for name, (lat, lon) in PLACES.items():
        print(f"\n-- {name} --")
        df = get_hourly(lat, lon, hours=hours)

        if df.empty:
            print("No data came back. This means df is empty. Skipping features.")
            continue

        # Show the first few rows just to know it worked
        print(df.head())

        feats = make_features(df)
        if not feats:
            print("features.py returned an empty dictionary.")
        else:
            print("Features:", feats)

if __name__ == "__main__":
    run(hours=24)