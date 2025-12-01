from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np
import pandas as pd

def _scale(vals):
    return StandardScaler().fit_transform(vals)

def cluster_weather(data_dict, k=3):
    if not data_dict:
        return None, None
    df = pd.DataFrame.from_dict(data_dict, orient="index")
    X = _scale(df.values)
    km = KMeans(n_clusters=k, n_init="auto", random_state=42)
    labels = km.fit_predict(X)
    df["cluster"] = labels
    return df, km

def choose_k(data_dict, min_k=3, max_k=6, tie_k=4):
    """Silhouette only, forbid k=2. If scores are flat, fall back to tie_k."""
    if not data_dict:
        return tie_k
    df = pd.DataFrame.from_dict(data_dict, orient="index")
    X = _scale(df.values)

    ks, scores = [], []
    for k in range(min_k, max_k + 1):
        try:
            km = KMeans(n_clusters=k, n_init="auto", random_state=42)
            labels = km.fit_predict(X)
            s = silhouette_score(X, labels)
            ks.append(k); scores.append(s)
        except Exception:
            pass

    if not scores:
        return tie_k

    best_k = ks[int(np.argmax(scores))]
    # if all scores within 0.02 of each other, pick tie_k (e.g., 4)
    if (max(scores) - min(scores)) < 0.02 and tie_k in ks:
        return tie_k
    return best_k
