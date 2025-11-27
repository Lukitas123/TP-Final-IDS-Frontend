from flask import Blueprint, render_template, current_app
import requests

actividades_bp = Blueprint("actividades", __name__)


@actividades_bp.route("/actividades")
def actividades():
    actividades = []
    try:
        backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/activity"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        actividades = json_data.get("data", [])

        for actividad in actividades:
            actividad["nombre"] = actividad.get("name")
            actividad["descripcion"] = actividad.get("description")
            actividad["cronograma"] = actividad.get("schedule")
            actividad["precio"] = actividad.get("price")
            actividad["galeria"] = actividad.get("gallery")
    except Exception as e:
        print("Error al obtener actividades desde el backend:", e)
    return render_template("actividades.html", actividades=actividades)
