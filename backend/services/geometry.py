import polyline


def decode_route_geometry(encoded_geometry: str):
    """
    Decode an OpenRouteService encoded route geometry
    into latitude/longitude coordinate pairs.
    """
    coordinates = polyline.decode(encoded_geometry)

    return [
        {
            "latitude": latitude,
            "longitude": longitude
        }
        for latitude, longitude in coordinates
    ]