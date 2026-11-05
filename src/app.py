from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "disasterguard-demo-key"

API_URL = "http://127.0.0.1:8000"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    try:
        response = requests.get(
            f"{API_URL}/api/v1/disasters/",
            timeout=3
        )
        response.raise_for_status()
        disasters = response.json()
        api_status = "Connected"
    except requests.RequestException:
        disasters = []
        api_status = "Disconnected"

    return render_template(
        "dashboard.html",
        disasters=disasters,
        api_status=api_status
    )


@app.route("/hazards")
def hazards():
    try:
        response = requests.get(
            f"{API_URL}/api/v1/hazard-zones/",
            timeout=3
        )
        response.raise_for_status()
        hazard_zones = response.json()
        api_status = "Connected"
    except requests.RequestException:
        hazard_zones = []
        api_status = "Disconnected"

    return render_template(
        "hazard_zones.html",
        hazard_zones=hazard_zones,
        api_status=api_status
    )

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "disaster_type": request.form.get("disaster_type"),
            "severity": request.form.get("severity"),
            "location": request.form.get("location"),
            "description": request.form.get("description"),
            "status": "active"
        }

        try:
            response = requests.post(
                f"{API_URL}/api/v1/disasters/",
                json=data,
                timeout=5
            )
            response.raise_for_status()
            flash("Emergency report submitted successfully!", "success")
            return redirect(url_for("dashboard"))

        except requests.RequestException:
            flash("Could not submit report. Please check the backend.", "error")

    return render_template("report.html")



@app.route("/evacuation", methods=["GET", "POST"])
def evacuation():
    result = None
    api_status = "Connected"

    try:
        if request.method == "POST":
            data = {
                "route_a_hazard": int(request.form.get("route_a_hazard", 4)),
                "route_a_crowd": float(request.form.get("route_a_crowd", 0.8)),
                "route_a_blocked": "route_a_blocked" in request.form,
                "route_b_hazard": int(request.form.get("route_b_hazard", 1)),
                "route_b_crowd": float(request.form.get("route_b_crowd", 0.2)),
                "route_b_blocked": "route_b_blocked" in request.form
            }

            response = requests.post(
                f"{API_URL}/api/v1/evacuation/recommend",
                json=data,
                timeout=5
            )
        else:
            data = {
                "route_a_hazard": 4,
                "route_a_crowd": 0.8,
                "route_a_blocked": False,
                "route_b_hazard": 1,
                "route_b_crowd": 0.2,
                "route_b_blocked": False
            }
            response = requests.get(
                f"{API_URL}/api/v1/evacuation/recommend",
                timeout=5
            )

        response.raise_for_status()
        result = response.json()

    except (requests.RequestException, ValueError):
        api_status = "Disconnected"
        result = {
            "recommended_route": None,
            "alternatives": [],
            "message": "Unable to calculate a recommendation.",
            "disclaimer": "Simulation only."
        }
        data = request.form.to_dict() if request.method == "POST" else {}

    return render_template(
        "evacuation.html",
        result=result,
        api_status=api_status,
        conditions=data
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)