from services.route_scoring import find_fastest_route, find_eco_route


def test_find_fastest_route():
    routes = [
        {
            "route_number": 1,
            "distance_miles": 31.3,
            "duration_minutes": 36
        },
        {
            "route_number": 2,
            "distance_miles": 28.0,
            "duration_minutes": 45
        },
        {
            "route_number": 3,
            "distance_miles": 35.0,
            "duration_minutes": 40
        }
    ]

    result = find_fastest_route(routes)

    assert result["route_number"] == 1


def test_find_eco_route():
    routes = [
        {
            "route_number": 1,
            "distance_miles": 31.3,
            "duration_minutes": 36
        },
        {
            "route_number": 2,
            "distance_miles": 28.0,
            "duration_minutes": 45
        },
        {
            "route_number": 3,
            "distance_miles": 35.0,
            "duration_minutes": 40
        }
    ]

    result = find_eco_route(routes)

    assert result["route_number"] == 2


def test_empty_routes():
    assert find_fastest_route([]) is None
    assert find_eco_route([]) is None