def cities():
    """
    Returns a dictionary of city names and their (latitude, longitude).
    These are mostly towns around Abington, Bucks County, and State College.
    """

    city_coords = {
        "State College, PA": (40.80, -77.86),
        "Altoona, PA": (40.52, -78.39),
        "Harrisburg, PA": (40.27, -76.88),
        "Williamsport, PA": (41.24, -77.00),
        "Lewistown, PA": (40.60, -77.57),
        "Abington, PA": (40.12, -75.13),
        "Willow Grove, PA": (40.14, -75.12),
        "Horsham, PA": (40.18, -75.13),
        "Hatboro, PA": (40.18, -75.10),
        "Jenkintown, PA": (40.10, -75.13),
        "Huntingdon Valley, PA": (40.13, -75.06),
        "Feasterville, PA": (40.15, -74.99),
        "Bensalem, PA": (40.10, -74.95),
        "Croydon, PA": (40.09, -74.90),
        "Bristol, PA": (40.10, -74.85),
        "Langhorne, PA": (40.17, -74.92),
        "Levittown, PA": (40.15, -74.83),
        "Newtown, PA": (40.23, -74.94),
        "Doylestown, PA": (40.31, -75.13),
        "Warminster, PA": (40.21, -75.10),
        "Quakertown, PA": (40.44, -75.34),
        "Norristown, PA": (40.12, -75.34),
        "King of Prussia, PA": (40.10, -75.38),
        "Conshohocken, PA": (40.07, -75.30),
        "Philadelphia, PA": (39.95, -75.16),
        "West Chester, PA": (39.96, -75.60),
        "Allentown, PA": (40.60, -75.47),
        "Trenton, NJ": (40.22, -74.74),
        "Camden, NJ": (39.93, -75.12),
        "Cherry Hill, NJ": (39.93, -75.00),
        "Wilmington, DE": (39.74, -75.54),
        "New York, NY": (40.71, -74.00),
        "Newark, NJ": (40.73, -74.17),
    }
    return city_coords