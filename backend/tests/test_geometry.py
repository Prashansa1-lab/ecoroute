import polyline

from services.geometry import decode_route_geometry


def test_decode_route_geometry():
    original_coordinates = [
        (29.8826, -97.9406),
        (29.9000, -97.9300),
        (30.2672, -97.7431)
    ]

    encoded_geometry = polyline.encode(original_coordinates)

    result = decode_route_geometry(encoded_geometry)

    assert len(result) == 3

    assert result[0]["latitude"] == 29.8826
    assert result[0]["longitude"] == -97.9406

    assert result[2]["latitude"] == 30.2672
    assert result[2]["longitude"] == -97.7431