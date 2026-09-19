def sample_route_points(coordinates, max_points=10):
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