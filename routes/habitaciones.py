from flask import Blueprint, render_template, current_app
import requests
from functions import parse_gallery

habitaciones_bp = Blueprint('habitaciones', __name__)


@habitaciones_bp.route("/habitaciones")
def habitaciones():
    room_types = []
    try:
        backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/room_types"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        room_types = json_data.get("data", [])
        for room in room_types:
            room["galeria"] = parse_gallery(room.get("gallery"))
            room["nombre"] = room.get("name")
            room["descripcion"] = room.get("description")
    except Exception as e:
        print("Error al obtener tipos de habitación desde el backend:", e)
    return render_template("habitaciones.html", habitaciones=room_types)
