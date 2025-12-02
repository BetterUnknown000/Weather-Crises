import pandas as pd
from src.datasets.NWS import get_alerts


# ok so we are gonna calculate the score based off these three variables
# severity is most important, followed by urgency and then certainty
def calculate_alert_score(severity, urgency, certainty):
    # Severity weights
    severity_weights = {
        "Extreme": 5,
        "Severe": 4,
        "Moderate": 3,
        "Minor": 2,
        "Unknown": 1
    }

    # Urgency weights
    urgency_weights = {
        "Immediate": 5,
        "Expected": 4,
        "Future": 3,
        "Past": 1,
        "Unknown": 2
    }

    # Certainty weights
    certainty_weights = {
        "Observed": 5,
        "Likely": 4,
        "Possible": 3,
        "Unlikely": 2,
        "Unknown": 1
    }

    # Get weights (default to lowest if not found)
    sev_score = severity_weights.get(severity, 1)
    urg_score = urgency_weights.get(urgency, 1)
    cert_score = certainty_weights.get(certainty, 1)

    # Calculate weighted total (severity is most important, so weight it higher)
    total_score = (sev_score * 0.5) + (urg_score * 0.3) + (cert_score * 0.2)

    return round(total_score, 2)


# return the dataframe with new alert score column
def score_alerts(df):
    if df.empty:
        return df

    # Calculate score for each alert
    df['score'] = df.apply(
        lambda row: calculate_alert_score(row['severity'], row['urgency'], row['certainty']),
        axis=1
    )

    # Sort by score descending, as we are seeing who is sent the alert first
    df_sorted = df.sort_values('score', ascending=False)

    return df_sorted


def get_scored_alerts(lat, lon, hours=24):
    # Get alerts from the dataset loader
    df = get_alerts(lat, lon, hours)

    if df.empty:
        return df

    # Add scores and sort
    df_scored = score_alerts(df)

    return df_scored


# get alerts for all locations and create prioritized list
def prioritize_location_alerts(locations_dict):
    all_alerts = []

    for location_name, (lat, lon) in locations_dict.items():
        df = get_alerts(lat, lon)

        if not df.empty:
            # Add location name to each alert
            df['location'] = location_name
            all_alerts.append(df)

    if not all_alerts:
        print("No active alerts found for any location.")
        return pd.DataFrame()

    # Combine all alerts
    combined_df = pd.concat(all_alerts, ignore_index=True)

    # Score and sort
    scored_df = score_alerts(combined_df)

    return scored_df


if __name__ == "__main__":
    from src.datasets.locations import cities

    # Get all city locations
    all_cities = cities()

    # Get prioritized alerts for all locations
    prioritized_alerts = prioritize_location_alerts(all_cities)

    if prioritized_alerts.empty:
        print("No active alerts for any locations.")
    else:
        print(f"\nFound {len(prioritized_alerts)} total alerts")
        print("\nTop 10 Most Critical Alerts")

        # Display key columns for top 10
        # maybe drop areaDesc... It is kinda fugly
        display_cols = ['location', 'event', 'severity', 'urgency', 'certainty', 'score', 'areaDesc']
        top_alerts = prioritized_alerts[display_cols].head(10)

        print(top_alerts.to_string(index=False))

        print("\nAlert Summary by Location")
        location_summary = prioritized_alerts.groupby('location').agg({
            'score': ['count', 'mean', 'max']
        }).round(2)
        location_summary.columns = ['Alert Count', 'Avg Score', 'Max Score']
        print(location_summary.sort_values('Max Score', ascending=False))