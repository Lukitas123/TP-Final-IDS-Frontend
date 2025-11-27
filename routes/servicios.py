from flask import Blueprint, render_template, current_app
import requests
from functions import parse_gallery

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route("/servicios")
def servicios():
    servicios = []
    backend_url = current_app.config['INTERNAL_BACKEND_URL']
    try:
        response = requests.get(f"{backend_url}/services")
        response.raise_for_status()
        json_data = response.json()
        servicios = json_data.get("data", [])
        for service in servicios:
            parsed_gallery = parse_gallery(service.get("gallery"))
            service["galeria"] = parsed_gallery
            service["nombre"] = service.get("name")
            service["descripcion"] = service.get("description")
            service["precio"] = service.get("price")
    except Exception as e:
        print("Error al obtener servicios desde el backend:", e)
    return render_template("servicios.html", servicios=servicios)
