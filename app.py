from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN DE FLASK-MAIL ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

# URLs del Backend
app.config['INTERNAL_BACKEND_URL'] = os.getenv('INTERNAL_BACKEND_URL')
app.config['PUBLIC_BACKEND_URL'] = os.getenv('PUBLIC_BACKEND_URL')


mail = Mail(app)


@app.context_processor
def inject_search_data():
    rooms_for_search = []
    services_for_search = []
    activities_for_search = []
    packages_for_search = []

    base_url = app.config['INTERNAL_BACKEND_URL']

    try:
        # Habitaciones
        resp_rooms = requests.get(f"{base_url}/room_types", timeout=5)
        resp_rooms.raise_for_status()
        data_rooms = resp_rooms.json().get("data", [])
        for room in data_rooms:
            nombre = room.get("name") or room.get("nombre")
            if nombre:
                rooms_for_search.append({"id": room.get("id"), "nombre": nombre})

        # Servicios
        resp_services = requests.get(f"{base_url}/services", timeout=5)
        resp_services.raise_for_status()
        data_services = resp_services.json().get("data", [])
        for s in data_services:
            nombre = s.get("name") or s.get("nombre")
            if nombre:
                services_for_search.append({"id": s.get("id"), "nombre": nombre})

        # Actividades
        resp_activities = requests.get(f"{base_url}/activity", timeout=5)
        resp_activities.raise_for_status()
        data_activities = resp_activities.json().get("data", [])
        for a in data_activities:
            nombre = a.get("name") or a.get("nombre")
            if nombre:
                activities_for_search.append({"id": a.get("id"), "nombre": nombre})

        # Paquetes
        resp_packages = requests.get(f"{base_url}/package", timeout=5)
        resp_packages.raise_for_status()
        data_packages = resp_packages.json().get("data", [])
        for p in data_packages:
            nombre = p.get("name") or p.get("nombre")
            if nombre:
                packages_for_search.append({"id": p.get("id"), "nombre": nombre})

        print(
            f"[inject_search_data] rooms={len(rooms_for_search)}, "
            f"services={len(services_for_search)}, "
            f"activities={len(activities_for_search)}, "
            f"packages={len(packages_for_search)}"
        )
    except Exception as e:
        print("Error obteniendo datos para barra de búsqueda:", e)

    return {
        "rooms_for_search": rooms_for_search,
        "services_for_search": services_for_search,
        "activities_for_search": activities_for_search,
        "packages_for_search": packages_for_search,
    }


# --- REGISTRAR BLUEPRINTS ---
from routes.home import home_bp
from routes.habitaciones import habitaciones_bp
from routes.servicios import servicios_bp
from routes.actividades import actividades_bp
from routes.paquetes import paquetes_bp
from routes.contacto import contacto_bp
from routes.reservas import reservas_bp
from routes.confirmacion_mail import bp_confirmacion_mail

app.register_blueprint(home_bp)
app.register_blueprint(habitaciones_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(actividades_bp)
app.register_blueprint(paquetes_bp)
app.register_blueprint(contacto_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(bp_confirmacion_mail)

if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)
