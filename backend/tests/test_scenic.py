import requests
from unittest.mock import patch

from services.scenic import (
    sample_route_points,
    calculate_scenic_score,
    analyze_route_scenery,
)


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


def test_calculate_scenic_score():
    features = [
        {
            "type": "node",
            "id": 1,
            "tags": {"tourism": "viewpoint"}
        },
        {
            "type": "way",
            "id": 2,
            "tags": {"leisure": "park"}
        },
        {
            "type": "way",
            "id": 3,
            "tags": {"natural": "water"}
        },
        {
            "type": "node",
            "id": 4,
            "tags": {"historic": "memorial"}
        }
    ]

    result = calculate_scenic_score(features)

    assert result == 15


def test_scenic_score_ignores_duplicates():
    features = [
        {
            "type": "node",
            "id": 1,
            "tags": {"tourism": "viewpoint"}
        },
        {
            "type": "node",
            "id": 1,
            "tags": {"tourism": "viewpoint"}
        }
    ]

    result = calculate_scenic_score(features)

    assert result == 5


def test_scenic_score_handles_empty_features():
    result = calculate_scenic_score([])

    assert result == 0


@patch("services.scenic.get_scenic_features_for_points")
@patch("services.scenic.decode_route_geometry")
def test_scenic_analysis_handles_api_failure(
    mock_decode,
    mock_get_features
):
    mock_decode.return_value = [
        {"latitude": 29.88, "longitude": -97.94},
        {"latitude": 30.26, "longitude": -97.74}
    ]

    mock_get_features.side_effect = requests.RequestException(
        "Overpass unavailable"
    )

    result = analyze_route_scenery("fake-geometry")

    assert result is None