
from backend.app.services.evacuation_engine import (
    DEMO_ROUTES,
    recommend_route
)


def test_default_recommendation():
    result = recommend_route(DEMO_ROUTES)

    assert result["recommended_route"]["name"] == (
        "Route B - Ring Road"
    )
    assert result["recommended_route"]["risk_score"] == 11.6


def test_adaptive_recommendation():
    routes = [route.copy() for route in DEMO_ROUTES]

    routes[0]["hazard_level"] = 0
    routes[0]["crowd_density"] = 0.1

    routes[1]["hazard_level"] = 5
    routes[1]["crowd_density"] = 0.9

    result = recommend_route(routes)

    assert result["recommended_route"]["name"] == (
        "Route A - Main Road"
    )
    assert result["recommended_route"]["risk_score"] == 4.3


def test_blocked_route_excluded():
    routes = [route.copy() for route in DEMO_ROUTES]
    routes[1]["blocked"] = True

    result = recommend_route(routes)

    assert result["recommended_route"]["name"] == (
        "Route A - Main Road"
    )


def test_all_routes_blocked():
    routes = [
        {**route, "blocked": True}
        for route in DEMO_ROUTES
    ]

    result = recommend_route(routes)

    assert result["recommended_route"] is None
    assert result["alternatives"] == []
