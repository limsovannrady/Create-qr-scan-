import os
from flask import Flask, render_template, jsonify
from db import init_db, get_stats, get_recent_activities, get_users

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def api_stats():
    total_users, total_actions = get_stats()
    return jsonify({"total_users": total_users, "total_actions": total_actions})


@app.route("/api/activities")
def api_activities():
    return jsonify(get_recent_activities(50))


@app.route("/api/users")
def api_users():
    return jsonify(get_users())


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
