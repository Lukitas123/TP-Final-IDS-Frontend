from flask import Blueprint, render_template
from services.backend_api import api_get
from services.gallery import safe_parse_gallery

bp_habitaciones = Blueprint("habitaciones", __name__)


@bp_habitaciones.route("/habitaciones")
def habitaciones():
    rooms = api_get("room_types")

    for room in rooms:
        room["galeria"] = safe_parse_gallery(room.get("gallery"))
        room["nombre"] = room.get("name")
        room["descripcion"] = room.get("description")

    return render_template("habitaciones.html", habitaciones=rooms)
