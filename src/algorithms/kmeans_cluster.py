from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

def _scale(vals):
    return StandardScaler().fit_transform(vals)

# Hard-code a sensible default k for your dataset size
DEFAULT_K = 4

def cluster_weather(data_dict, k: int | None = None):
    if not data_dict:
        return None, None

    # Build full frame (may include non-numeric columns like 'top_alert_event')
    df = pd.DataFrame.from_dict(data_dict, orient="index")

    # Use ONLY numeric features for K-Means
    df_num = df.apply(pd.to_numeric, errors="coerce")
    df_num = df_num.dropna(axis=1, how="all").fillna(0.0)

    X = _scale(df_num.values)

    # Pick fixed k (hard-coded); ignore silhouette for speed
    k = k or DEFAULT_K
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)

    # Attach labels back to original df so you keep all columns for display
    out = df.copy()
    out["cluster"] = labels
    return out, km
