
from math import radians, sin, cos, asin, sqrt


def haversine_km(lat1, lon1, lat2, lon2):
    """Distance between two GPS coordinates in km."""
    earth_radius = 6371.0

    lat1, lon1, lat2, lon2 = map(
        radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    return 2 * earth_radius * asin(
        min(1.0, sqrt(a))
    )


def route_hazard_exposure(route_points, hazard_zones):
    """
    Calculate approximate exposure using sampled points
    along illustrative route segments.

    This is a simulation, not a certified safety model.
    """
    if not route_points:
        return {
            "exposure_score": 0,
            "intersecting_hazards": []
        }

    exposure_score = 0
    intersecting = []

    for hazard in hazard_zones:
        if hazard.get("status") == "cleared":
            continue

        center_lat = float(hazard["latitude"])
        center_lon = float(hazard["longitude"])
        radius_km = float(hazard["radius_km"])

        if radius_km <= 0:
            continue

        detected = False

        for start, end in zip(
            route_points, route_points[1:]
        ):
            # Sample points along each route segment.
            for step in range(101):
                t = step / 100

                lat = start[0] + t * (
                    end[0] - start[0]
                )
                lon = start[1] + t * (
                    end[1] - start[1]
                )

                distance = haversine_km(
                    lat, lon, center_lat, center_lon
                )

                if distance <= radius_km:
                    detected = True
                    break

            if detected:
                break

        if detected:
            severity_weights = {
                "low": 1,
                "moderate": 3,
                "high": 6,
                "critical": 10
            }

            exposure_score += severity_weights.get(
                hazard.get("severity"), 1
            )

            intersecting.append(hazard["name"])

    return {
        "exposure_score": exposure_score,
        "intersecting_hazards": intersecting
    }
