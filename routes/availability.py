from flask import Blueprint, request, jsonify
from services.backend_api import api_get

bp_availability = Blueprint("availability", __name__)

@bp_availability.route("/check-availability")
def check_availability():
    checkin = request.args.get("checkin")
    checkout = request.args.get("checkout")

    if not checkin or not checkout:
        return jsonify({"error": "Faltan fechas de check-in o check-out."}), 400

    data = api_get(f"availability?checkin={checkin}&checkout={checkout}")
    available_ids = [room["id"] for room in data]

    return jsonify({"available_room_ids": available_ids})
