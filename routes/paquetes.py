from flask import Blueprint, render_template, current_app
import requests
from functions import parse_gallery

paquetes_bp = Blueprint('paquetes', __name__)

@paquetes_bp.route("/paquetes")
def paquetes():
    paquetes = []
    try:
        backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/package"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        paquetes = json_data.get("data", [])
        for paquete in paquetes:
            paquete["gallery"] = parse_gallery(paquete.get("gallery"))
            paquete["galeria"] = paquete.get("gallery")
            paquete["nombre"] = paquete.get("name")
            paquete["descripcion"] = paquete.get("description")
    except Exception as e:
        print("Error al obtener paquetes desde el backend:", e)
    return render_template("paquetes.html", paquetes=paquetes)
