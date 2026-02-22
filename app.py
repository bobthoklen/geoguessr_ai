from flask import Flask, render_template, request, jsonify
import random
from geopy.distance import geodesic

app = Flask(__name__)

# Sample locations (lat, lon)
LOCATIONS = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"name": "Cairo", "lat": 30.0444, "lon": 31.2357},
]

current_location = {}

@app.route("/")
def index():
    global current_location
    current_location = random.choice(LOCATIONS)
    return render_template("index.html")

@app.route("/guess", methods=["POST"])
def guess():
    user_lat = float(request.form["lat"])
    user_lon = float(request.form["lon"])

    actual_coords = (current_location["lat"], current_location["lon"])
    user_coords = (user_lat, user_lon)

    distance_km = geodesic(actual_coords, user_coords).km

    # Simple scoring logic
    score = max(0, int(5000 - distance_km))

    return jsonify({
        "distance": round(distance_km, 2),
        "score": score,
        "actual_lat": current_location["lat"],
        "actual_lon": current_location["lon"],
        "city": current_location["name"]
    })

if __name__ == "__main__":
    app.run(debug=True)