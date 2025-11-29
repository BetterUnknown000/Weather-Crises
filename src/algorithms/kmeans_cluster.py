from sklearn.cluster import KMeans
import pandas as pd

def cluster_weather(data_dict, k=2):
    """
    Takes a dictionary that is in the form city -> feature, and groups
    them into clusters using K-Means.
    """
    if not data_dict:
        print("No data passed into cluster_weather() for K-Means to operate.")
        return None, None

    # Turns the dictionary into DataFrame
    df = pd.DataFrame.from_dict(data_dict, orient="index")

    # Save city names for later
    names = df.index.tolist()

    try:
        # Run K-Means with k clusters
        model = KMeans(n_clusters=k, n_init="auto", random_state=42)
        model.fit(df)

        # Add the cluster labels to DataFrame
        df["cluster"] = model.labels_

        return df, model

    except Exception as e:
        print("Error while clustering in kmeans_cluster.py: ", e)
        return None, None