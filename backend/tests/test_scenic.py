from services.scenic import sample_route_points


def test_sample_route_points_limits_number_of_points():
    coordinates = [
        {"latitude": i, "longitude": i}
        for i in range(20)
    ]

    result = sample_route_points(coordinates, max_points=5)

    assert len(result) == 5
    assert result[0] == coordinates[0]
    assert result[-1] == coordinates[-1]


def test_sample_route_points_keeps_small_routes():
    coordinates = [
        {"latitude": 1, "longitude": 1},
        {"latitude": 2, "longitude": 2},
        {"latitude": 3, "longitude": 3}
    ]

    result = sample_route_points(coordinates, max_points=5)

    assert result == coordinates


def test_sample_route_points_handles_empty_route():
    result = sample_route_points([])

    assert result == []