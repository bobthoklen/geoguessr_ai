from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)

locations = [
    {"name": "Pashupatinath Temple", "lat": 27.7104, "lon": 85.3486},
    {"name": "Boudhanath", "lat": 27.7215, "lon": 85.3616},
    {"name": "Krishna Temple", "lat": 27.6732, "lon": 85.3240},
    {"name": "Dakshinkali Temple", "lat": 27.605122104672738, "lon": 85.26333218236458},
    {"name": "Bajrayogini Temple", "lat": 27.74390179981689, "lon": 85.4670758373625},
    {"name": "ISKCON Temple", "lat": 27.783, "lon": 85.356},
    {"name": "Soaltee Hotel", "lat": 27.700,"lon": 85.291},
    {"name": "Gokarna Temple", "lat": 27.7392,"lon": 85.387},
    {"name": "Chagunarayan Temple", "lat": 27.7164,"lon": 85.4279},
    {"name": "Salinadi Temple", "lat": 27.7283,"lon": 85.4692},
    {"name": "Nyatpola Temple", "lat": 27.6713,"lon": 85.4293},
    {"name": "Syambhunath Stupa", "lat": 27.7148,"lon": 85.2904},
    {"name": "Phulchoki Temple", "lat": 27.57093653611957,"lon": 85.4065153644325},
    {"name": "Kasthamandap", "lat": 27.703894382731374,"lon": 85.30591121402817},
    {"name": "Taleju Bhawani Temple", "lat": 27.704871130977043,"lon": 85.3079356756657},
    {"name": "Buddhanilkantha Temple", "lat": 27.778034494882753,"lon": 85.36234887813993},
    {"name": "Manamaiju Temple", "lat": 27.752074699991287,"lon": 85.31206556894665},
    {"name": "Bajrabarahi Temple", "lat": 27.606081377185443,"lon":  85.32935523423666},
    {"name": "Santaneshwor Mahadev Temple", "lat": 27.615189856899836,"lon": 85.34439641946199},
    {"name": "Kalanki Mai Temple", "lat": 27.6940931686871,"lon": 85.28494644211399},
    {"name": "Suryabinayak Ganesh Temple", "lat": 27.65629984688918,"lon": 85.4234714659616},
    {"name": "Sikali Temple", "lat": 27.643504724772573,"lon": 85.285529522234},
   ]

TOTAL_ROUNDS = 5
game_data = {
    "round": 1,
    "total_score": 0,
    "current_location": None
}

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.route("/")
def index():
    game_data["round"] = 1
    game_data["total_score"] = 0
    game_data["current_location"] = random.choice(locations)
    return render_template("index.html",
                           location_name=game_data["current_location"]["name"],
                           round=game_data["round"],
                           total_score=game_data["total_score"])

@app.route("/guess", methods=["POST"])
def guess():
    data = request.json
    guessed_lat = float(data["lat"])
    guessed_lon = float(data["lon"])

    correct = game_data["current_location"]

    distance = calculate_distance(
        guessed_lat, guessed_lon,
        correct["lat"], correct["lon"]
    )

    score = max(0, int(500 - distance * 100))
    game_data["total_score"] += score

    return jsonify({
        "distance": round(distance, 2),
        "score": score,
        "total_score": game_data["total_score"],
        "correct_lat": correct["lat"],
        "correct_lon": correct["lon"],
        "game_over": game_data["round"] >= TOTAL_ROUNDS
    })

@app.route("/next")
def next_round():
    game_data["round"] += 1
    game_data["current_location"] = random.choice(locations)

    return jsonify({
        "location_name": game_data["current_location"]["name"],
        "round": game_data["round"]
    })

if __name__ == "__main__":
    app.run(debug=True)
    
