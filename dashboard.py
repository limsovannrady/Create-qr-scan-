import os
import hmac
import hashlib
import json
from functools import wraps
from urllib.parse import parse_qsl
from flask import Flask, render_template, jsonify, request, session
from db import init_db, get_stats, get_recent_activities, get_users

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID = 5002402843
DASHBOARD_SECRET = os.environ.get("DASHBOARD_SECRET", "changeme-set-env-var")

app.secret_key = DASHBOARD_SECRET or "fallback-secret-key"

init_db()


def validate_telegram_init_data(init_data: str) -> dict | None:
    try:
        params = dict(parse_qsl(init_data, strict_parsing=True))
        hash_value = params.pop("hash", None)
        if not hash_value:
            return None

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(params.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            TOKEN.encode(),
            hashlib.sha256
        ).digest()

        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(computed_hash, hash_value):
            return None

        return params
    except Exception:
        return None


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    return render_template("index.html", secret=DASHBOARD_SECRET)


@app.route("/api/auth", methods=["POST"])
def api_auth():
    data = request.get_json(silent=True) or {}

    secret = data.get("secret", "")
    if not DASHBOARD_SECRET or secret != DASHBOARD_SECRET:
        return jsonify({"ok": False, "error": "Invalid secret"}), 403

    init_data = data.get("initData", "")
    params = validate_telegram_init_data(init_data)
    if not params:
        return jsonify({"ok": False, "error": "Invalid Telegram data"}), 403

    user_info = json.loads(params.get("user", "{}"))
    user_id = user_info.get("id")

    if user_id != ADMIN_ID:
        return jsonify({"ok": False, "error": "Access denied"}), 403

    session["is_admin"] = True
    session["user_id"] = user_id
    return jsonify({"ok": True})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/stats")
@require_auth
def api_stats():
    total_users, total_actions = get_stats()
    return jsonify({"total_users": total_users, "total_actions": total_actions})


@app.route("/api/activities")
@require_auth
def api_activities():
    return jsonify(get_recent_activities(50))


@app.route("/api/users")
@require_auth
def api_users():
    return jsonify(get_users())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
