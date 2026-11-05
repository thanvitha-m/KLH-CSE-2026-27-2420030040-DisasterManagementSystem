
# DisasterGuard AI - Evacuation Recommendation Engine
# Prototype using simulated route data.

DEMO_ROUTES = [
    {
        "name": "Route A - Main Road",
        "distance_km": 4.0,
        "hazard_level": 4,
        "crowd_density": 0.8,
        "blocked": False
    },
    {
        "name": "Route B - Ring Road",
        "distance_km": 6.0,
        "hazard_level": 1,
        "crowd_density": 0.2,
        "blocked": False
    },
    {
        "name": "Route C - Bridge Road",
        "distance_km": 3.0,
        "hazard_level": 2,
        "crowd_density": 0.4,
        "blocked": True
    }
]


def recommend_route(routes):
    recommendations = []

    for route in routes:
        if route["blocked"]:
            continue

        score = (
            route["distance_km"] * 1
            + route["hazard_level"] * 5
            + route["crowd_density"] * 3
        )

        result = route.copy()
        result["risk_score"] = round(score, 2)
        recommendations.append(result)

    recommendations.sort(key=lambda x: x["risk_score"])

    if not recommendations:
        return {
            "recommended_route": None,
            "alternatives": [],
            "message": "No available route in the simulation."
        }

    best = recommendations[0]

    return {
        "recommended_route": best,
        "alternatives": recommendations[1:],
        "message": (
            f"{best['name']} has the lowest calculated score "
            "among the available simulated routes."
        ),
        "disclaimer": (
            "Simulation only. Not verified for real-world "
            "emergency navigation."
        )
    }


if __name__ == "__main__":
    import json

    result = recommend_route(DEMO_ROUTES)
    print(json.dumps(result, indent=4))
