from flask import Flask, render_template, jsonify, request
import json
from datetime import date, timedelta

app = Flask(__name__)

PRESET_COLORS = [
    "#D97A7A", "#D9A15D", "#D8C76A", "#8FBF8F",
    "#6FA8DC", "#8C7CC9", "#D68BB5", "#A9826D", "#7A9AA8"
]

def load_habits():
    try:
        with open("habits.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_habits(habits):
    with open("habits.json", "w") as f:
        json.dump(habits, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/habits", methods=["GET"])
def get_habits():
    habits = load_habits()
    return jsonify(habits)

@app.route("/api/habits/add", methods=["POST"])
def add_habit():
    data = request.json
    habits = load_habits()
    habits.append({
        "name": data.get("name"),
        "goal": int(data.get("goal", 1)),
        "current": 0,
        "streak": 0,
        "period": data.get("period", "Daily"),
        "color": data.get("color", PRESET_COLORS[0]),
        "last_completed": None,
        "last_active": None
    })
    save_habits(habits)
    return jsonify({"status": "success"})

@app.route("/api/habits/increment", methods=["POST"])
def increment_habit():
    idx = request.json.get("index")
    habits = load_habits()
    if 0 <= idx < len(habits):
        habit = habits[idx]
        habit["current"] += 1
        save_habits(habits)
        return jsonify({"status": "success", "habit": habit})
    return jsonify({"status": "error"}), 400

@app.route("/api/habits/delete", methods=["POST"])
def delete_habit():
    idx = request.json.get("index")
    habits = load_habits()
    if 0 <= idx < len(habits):
        habits.pop(idx)
        save_habits(habits)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)