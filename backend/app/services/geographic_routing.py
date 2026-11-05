
from backend.app.services.evacuation_engine import DEMO_ROUTES
from backend.app.services.geo_risk import route_hazard_exposure

# These coordinates match the illustrative routes on our map.
# They are NOT verified road-network paths.
DEMO_ROUTE_POINTS = {
    "Route A - Main Road": [
        [17.4050, 78.4650],
        [17.4120, 78.4550],
        [17.4200, 78.4480],
        [17.4300, 78.4400],
    ],
    "Route B - Ring Road": [
        [17.4050, 78.4650],
        [17.4180, 78.4750],
        [17.4400, 78.4800],
        [17.4550, 78.4900],
    ],
}

GEO_RISK_WEIGHT = 5


def recommend_geographic_route(hazard_zones):
    ranked_routes = []
    blocked_routes = []

    for route in DEMO_ROUTES:
        name = route["name"]
        # Skip blocked routes before accessing coordinates
        if route["blocked"]:
                blocked_routes.append(name)
                continue
        
        # Skip routes without geographic coordinates
        points = DEMO_ROUTE_POINTS.get(name)
        if not points:
            blocked_routes.append(name)
            continue

        exposure = route_hazard_exposure(
            points, hazard_zones
        )

        base_score = (
            route["distance_km"]
            + route["hazard_level"] * 5
            + route["crowd_density"] * 3
        )

        geo_penalty = (
            exposure["exposure_score"] * GEO_RISK_WEIGHT
        )

        total_score = round(base_score + geo_penalty, 2)

        ranked_routes.append({
            **route,
            "base_score": round(base_score, 2),
            "geographic_penalty": round(geo_penalty, 2),
            "risk_score": total_score,
            "intersecting_hazards": exposure[
                "intersecting_hazards"
            ],
            "coordinates": points,
        })

    ranked_routes.sort(key=lambda r: r["risk_score"])

    if not ranked_routes:
        return {
            "recommended_route": None,
            "alternatives": [],
            "blocked_routes": blocked_routes,
            "message": "No available simulated route.",
            "disclaimer": "Simulation only."
        }

    best = ranked_routes[0]

    return {
        "recommended_route": best,
        "alternatives": ranked_routes[1:],
        "blocked_routes": blocked_routes,
        "message": (
            f"{best['name']} has the lowest modeled score. "
            f"Base score: {best['base_score']}; "
            f"geographic penalty: {best['geographic_penalty']}."
        ),
        "disclaimer": (
            "Demonstration only. Coordinates and scores are "
            "illustrative, not verified emergency guidance."
        )
    }
