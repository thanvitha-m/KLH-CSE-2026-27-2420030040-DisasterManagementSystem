
# Simulated shelter information for the academic prototype.
# These values are not live emergency shelter data.

DEMO_SHELTERS = {
    "Route A - Main Road": {
        "name": "Demo Shelter Alpha",
        "capacity": 150,
        "occupied": 65,
    },
    "Route B - Ring Road": {
        "name": "Demo Shelter Beta",
        "capacity": 200,
        "occupied": 110,
    },
}


def get_shelter_status(route_name):
    shelter = DEMO_SHELTERS.get(route_name)

    if shelter is None:
        return None

    capacity = shelter["capacity"]
    occupied = shelter["occupied"]
    available = max(capacity - occupied, 0)

    return {
        "name": shelter["name"],
        "capacity": capacity,
        "occupied": occupied,
        "available": available,
        "is_full": available == 0,
    }
