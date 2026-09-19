import requests

from services.geometry import decode_route_geometry


OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def sample_route_points(coordinates, max_points=5):
    """
    Select a limited number of evenly distributed points
    from a route to use for scenic analysis.
    """
    if not coordinates:
        return []

    if len(coordinates) <= max_points:
        return coordinates

    step = (len(coordinates) - 1) / (max_points - 1)

    sampled_points = []

    for index in range(max_points):
        point_index = round(index * step)
        sampled_points.append(coordinates[point_index])

    return sampled_points


def get_scenic_features_for_points(points, radius=1000):
    """
    Find scenic OpenStreetMap features near multiple route points
    using a single Overpass API request.
    """
    if not points:
        return []

    queries = []

    for point in points:
        latitude = point["latitude"]
        longitude = point["longitude"]

        queries.extend([
            f'node["tourism"="viewpoint"](around:{radius},{latitude},{longitude});',
            f'node["historic"](around:{radius},{latitude},{longitude});',
            f'way["leisure"="park"](around:{radius},{latitude},{longitude});',
            f'way["natural"="water"](around:{radius},{latitude},{longitude});'
        ])

    query_body = "\n".join(queries)

    query = f"""
    [out:json][timeout:25];
    (
        {query_body}
    );
    out center;
    """

    headers = {
        "User-Agent": "EcoRoute/0.1 (educational project)"
    }

    response = requests.post(
        OVERPASS_URL,
        data={"data": query},
        headers=headers,
        timeout=35
    )

    response.raise_for_status()

    data = response.json()

    return data.get("elements", [])


def calculate_scenic_score(features):
    """
    Calculate a scenic score from OpenStreetMap features.

    Duplicate features are counted only once.
    """
    weights = {
        "viewpoint": 5,
        "park": 4,
        "water": 4,
        "historic": 2
    }

    seen_features = set()
    score = 0

    for feature in features:
        feature_id = (feature.get("type"), feature.get("id"))

        if feature_id in seen_features:
            continue

        seen_features.add(feature_id)

        tags = feature.get("tags", {})

        if tags.get("tourism") == "viewpoint":
            score += weights["viewpoint"]
        elif tags.get("leisure") == "park":
            score += weights["park"]
        elif tags.get("natural") == "water":
            score += weights["water"]
        elif "historic" in tags:
            score += weights["historic"]

    return score


def analyze_route_scenery(encoded_geometry):
    """
    Analyze an encoded route and return its scenic score.

    Return None when scenic data cannot be retrieved.
    """
    coordinates = decode_route_geometry(encoded_geometry)

    sampled_points = sample_route_points(
        coordinates,
        max_points=5
    )

    try:
        features = get_scenic_features_for_points(sampled_points)
    except requests.RequestException as error:
        print(f"Scenic analysis unavailable: {error}")
        return None

    return calculate_scenic_score(features)