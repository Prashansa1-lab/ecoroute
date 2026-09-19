def find_fastest_route(routes):
    if not routes:
        return None

    return min(
        routes,
        key=lambda route: route["duration_minutes"]
    )