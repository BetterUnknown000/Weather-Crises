def tempdiff_to_f(x: float) -> float:
    # Convert C to F
    return x * 9.0 / 5.0

def display_subset(df, preferred_cols):
    # Return only the selected columns if they exist
    display_cols = [c for c in preferred_cols if c in df.columns]
    return df[display_cols].sort_values("cluster").round(2)