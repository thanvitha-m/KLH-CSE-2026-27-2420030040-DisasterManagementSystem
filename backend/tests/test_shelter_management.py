
from unittest.mock import patch

from backend.app.services.shelter_management import get_shelter_status
from backend.app.services.geographic_routing import recommend_geographic_route


def test_shelter_available_capacity():
    shelter = get_shelter_status("Route B - Ring Road")

    assert shelter["capacity"] == 200
    assert shelter["occupied"] == 110
    assert shelter["available"] == 90
    assert shelter["is_full"] is False


def test_unknown_shelter():
    assert get_shelter_status("Unknown Route") is None


def test_route_recommendation_with_shelter():
    result = recommend_geographic_route([])

    assert result["recommended_route"]["name"] == "Route B - Ring Road"
    assert result["recommended_route"]["shelter"]["available"] == 90


def test_full_shelter_triggers_rerouting():
    with patch(
        "backend.app.services.shelter_management.DEMO_SHELTERS",
        {
            "Route A - Main Road": {
                "name": "Demo Shelter Alpha",
                "capacity": 150,
                "occupied": 65,
            },
            "Route B - Ring Road": {
                "name": "Demo Shelter Beta",
                "capacity": 200,
                "occupied": 200,
            },
        },
    ):
        result = recommend_geographic_route([])

    assert result["recommended_route"]["name"] == "Route A - Main Road"
    assert "Route B - Ring Road" in result["full_shelter_routes"]


def test_all_shelters_full():
    with patch(
        "backend.app.services.shelter_management.DEMO_SHELTERS",
        {
            "Route A - Main Road": {
                "name": "Demo Shelter Alpha",
                "capacity": 150,
                "occupied": 150,
            },
            "Route B - Ring Road": {
                "name": "Demo Shelter Beta",
                "capacity": 200,
                "occupied": 200,
            },
        },
    ):
        result = recommend_geographic_route([])

    assert result["recommended_route"] is None
    assert len(result["full_shelter_routes"]) == 2
