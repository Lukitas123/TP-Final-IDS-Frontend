from flask import Blueprint, render_template, request, redirect, url_for, current_app
from services.backend_api import api_get
from services.gallery import safe_parse_gallery

bp_reserva = Blueprint("reserva", __name__)


@bp_reserva.route("/reserva", methods=["GET", "POST"])
def reserva():

    if request.method == "POST":
        return redirect(url_for("reserva.confirmacion"))

    paquete_id = request.args.get("paquete_id")
    public_backend_url = current_app.config.get("PUBLIC_BACKEND_URL")

    if paquete_id:
        data = api_get(f"package/{paquete_id}")

        if not data:
            return redirect(url_for("paquetes.paquetes", status="package_error"))

        data["gallery"] = safe_parse_gallery(data.get("gallery"))

        if data.get("room_type"):
            data["room_type"]["gallery"] = safe_parse_gallery(
                data["room_type"].get("gallery")
            )

        return render_template("reserva.html", paquete=data, data=None, public_backend_url=public_backend_url)

    data = {
        "rooms": api_get("room_types"),
        "services": api_get("services"),
        "activities": api_get("activity"),
    }

    for room in data["rooms"]:
        room["nombre"] = room.get("name")

    for service in data["services"]:
        service["nombre"] = service.get("name")

    for activity in data["activities"]:
        activity["nombre"] = activity.get("name")

    return render_template("reserva.html", paquete=None, data=data, public_backend_url=public_backend_url)


@bp_reserva.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")