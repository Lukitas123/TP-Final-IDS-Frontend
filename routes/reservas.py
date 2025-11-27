from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
import requests
from functions import parse_gallery

reservas_bp = Blueprint('reserva', __name__)


@reservas_bp.route("/reserva", methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        return redirect(url_for("home.confirmacion"))

    paquete_id = request.args.get('paquete_id')
    paquete_data = None

    backend_url = current_app.config['INTERNAL_BACKEND_URL']

    if paquete_id:
        try:
            backend_url = f"{backend_url}/package/{paquete_id}"
            response = requests.get(backend_url)
            response.raise_for_status()
            json_response = response.json()
            if json_response.get("status") == "success":
                paquete_data = json_response.get("data")
                if paquete_data:
                    paquete_data["gallery"] = parse_gallery(paquete_data.get("gallery"))
                    if paquete_data.get("room_type"):
                        paquete_data["room_type"]["gallery"] = parse_gallery(
                            paquete_data["room_type"].get("gallery")
                        )
            else:
                return redirect(url_for("paquetes.paquetes", status="package_error"))
        except Exception as e:
            print(f"Error procesando paquete {paquete_id}: {e}")
            return redirect(url_for("paquetes.paquetes", status="package_error"))

        return render_template("reserva.html", paquete=paquete_data, data=None)
    else:
        data = {"rooms": [], "services": [], "activities": []}
        try:
            # Rooms
            rooms_response = requests.get(f"{backend_url}/room_types")
            rooms_response.raise_for_status()
            data["rooms"] = rooms_response.json().get("data", [])
            for room in data["rooms"]:
                room["nombre"] = room.get("name")

            # Services
            services_response = requests.get(f"{backend_url}/services")
            services_response.raise_for_status()
            data["services"] = services_response.json().get("data", [])
            for service in data["services"]:
                service["nombre"] = service.get("name")

            # Activities
            activities_response = requests.get(f"{backend_url}/activity")
            activities_response.raise_for_status()
            data["activities"] = activities_response.json().get("data", [])
            for activity in data["activities"]:
                activity["nombre"] = activity.get("name")
        except Exception as e:
            print("Error fetching data for reservation form:", e)

        return render_template("reserva.html", paquete=None, data=data)


@reservas_bp.route("/check-availability")
def check_availability():
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')
    if not checkin or not checkout:
        return jsonify({"error": "Faltan fechas de check-in o check-out."}), 400

    available_ids = []
    try:
        backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/availability?checkin={checkin}&checkout={checkout}"
        response = requests.get(backend_url)
        response.raise_for_status()
        data = response.json().get("data", [])
        available_ids = [room['id'] for room in data]
    except Exception as e:
        print(f"Error calling backend availability: {e}")

    return jsonify({"available_room_ids": available_ids})
