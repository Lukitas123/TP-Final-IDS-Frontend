from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mail import Mail, Message
from functions import enviar_email_contacto, parse_gallery
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json


app = Flask(__name__)

# --- CONFIGURACIÓN DE FLASK-MAIL ---
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME')) 
mail = Mail(app)


def safe_parse_gallery(gallery_value):
    if isinstance(gallery_value, list):
        return gallery_value

    if isinstance(gallery_value, str):
        try:
            return json.loads(gallery_value)
        except ValueError:
            return []
    return []

@app.context_processor
def inject_search_data():
    rooms_for_search = []
    services_for_search = []
    activities_for_search = []
    packages_for_search = []

    try:
        base_url = "http://backend:5001"
        # Habitaciones
        resp_rooms = requests.get(f"{base_url}/room_types", timeout=5)
        resp_rooms.raise_for_status()
        data_rooms = resp_rooms.json().get("data", [])
        for room in data_rooms:
            nombre = room.get("name") or room.get("nombre")
            if nombre:
                rooms_for_search.append({
                    "id": room.get("id"),
                    "nombre": nombre,
                })

        # Servicios
        resp_services = requests.get(f"{base_url}/services", timeout=5)
        resp_services.raise_for_status()
        data_services = resp_services.json().get("data", [])
        for s in data_services:
            nombre = s.get("name") or s.get("nombre")
            if nombre:
                services_for_search.append({
                    "id": s.get("id"),
                    "nombre": nombre,
                })

        # Actividades 
        resp_activities = requests.get(f"{base_url}/activity", timeout=5)
        resp_activities.raise_for_status()
        data_activities = resp_activities.json().get("data", [])
        for a in data_activities:
            nombre = a.get("name") or a.get("nombre")
            if nombre:
                activities_for_search.append({
                    "id": a.get("id"),
                    "nombre": nombre,
                })

        # Paquetes
        resp_packages = requests.get(f"{base_url}/package", timeout=5)
        resp_packages.raise_for_status()
        data_packages = resp_packages.json().get("data", [])
        for p in data_packages:
            nombre = p.get("name") or p.get("nombre")
            if nombre:
                packages_for_search.append({
                    "id": p.get("id"),
                    "nombre": nombre,
                })

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


# --- ZONA DE RUTAS ---

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/actividades")
def actividades():
    actividades = []

    try:
        backend_url = "http://backend:5001/activity"
        response = requests.get(backend_url)

        json_data = response.json()
        actividades = json_data.get("data", [])

    except Exception as e:
        print("Error al obtener actividades desde el backend:", e)

    return render_template("actividades.html", actividades=actividades)


@app.route("/servicios")
def servicios():
    servicios = []

    try:
        backend_url = "http://backend:5001/services"
        response = requests.get(backend_url)

        json_data = response.json()
        servicios = json_data.get("data", [])

        for service in servicios:
            service["gallery"] = safe_parse_gallery(service.get("gallery"))

    except Exception as e:
        print("Error al obtener servicios desde el backend:", e)

    return render_template("servicios.html", servicios=servicios)


@app.route("/paquetes")
def paquetes():
    paquetes = []

    try:
        backend_url = "http://backend:5001/package"
        response = requests.get(backend_url)

        json_data = response.json()
        paquetes = json_data.get("data", [])

        for paquete in paquetes:
            paquete["gallery"] = safe_parse_gallery(paquete.get("gallery"))

    except Exception as e:
        print("Error al obtener paquetes desde el backend:", e)

    return render_template("paquetes.html", paquetes=paquetes)



@app.route("/habitaciones")
def habitaciones():
    room_types = []
    try:
        backend_url = "http://backend:5001/room_types"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        room_types = json_data.get("data", [])

        for room in room_types:
            room["galeria"] = safe_parse_gallery(room.get("gallery"))
            room["nombre"] = room.get("name")
            room["descripcion"] = room.get("description")

    except requests.exceptions.RequestException as e:
        print("Error al obtener tipos de habitación desde el backend:", e)
    except Exception as e:
        print("Error inesperado:", e)

    return render_template("habitaciones.html", habitaciones=room_types)


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        exito = enviar_email_contacto(
            mail=mail,
            datos_formulario=request.form,
            archivo_adjunto=request.files.get("archivo"),
        )

        if exito:
            return redirect(url_for("contacto", status="success"))
        else:
            return redirect(url_for("contacto", status="error"))
    return render_template("contacto.html")

@app.route("/reserva", methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        # Esta parte del POST es manejada por JavaScript que hace la llamada directa al backend.
        # Aquí solo redirigimos a la confirmación si el POST llega a este endpoint directamente.
        # La lógica de formulario real está en el JS.
        return redirect(url_for("confirmacion"))

    # Si es GET
    paquete_id = request.args.get('paquete_id')
    paquete_data = None

    if paquete_id:
        # Flujo de reserva por paquete
        try:
            backend_url = f"http://backend:5001/package/{paquete_id}"
            response = requests.get(backend_url)
            response.raise_for_status() # Lanza una excepción para errores HTTP (4xx o 5xx)
            json_response = response.json()
            if json_response.get("status") == "success":
                paquete_data = json_response.get("data")
                # Asegurarse de que las galerías se parseen correctamente si son strings JSON
                if paquete_data:
                    paquete_data["gallery"] = safe_parse_gallery(paquete_data.get("gallery"))
                    if paquete_data.get("room_type"):
                        paquete_data["room_type"]["gallery"] = safe_parse_gallery(paquete_data["room_type"].get("gallery"))
            else:
                print(f"Error del backend al obtener paquete: {json_response.get('message')}")
                # Podrías agregar un flash message o algo más amigable
                return redirect(url_for("paquetes", status="package_error")) # Redirigir con error
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al obtener paquete {paquete_id} desde el backend: {e}")
            # Podrías agregar un flash message o algo más amigable
            return redirect(url_for("paquetes", status="package_error")) # Redirigir con error
        except Exception as e:
            print(f"Error inesperado al procesar el paquete {paquete_id}: {e}")
            # Podrías agregar un flash message o algo más amigable
            return redirect(url_for("paquetes", status="package_error")) # Redirigir con error

        return render_template("reserva.html", paquete=paquete_data, data=None)
    else:
        # Flujo de reserva personalizada (el que ya existía)
        data = {
            "rooms": [],
            "services": [],
            "activities": [],
        }
        try:
            # Fetch room types
            rooms_response = requests.get("http://backend:5001/room_types")
            rooms_response.raise_for_status()
            data["rooms"] = rooms_response.json().get("data", [])
            for room in data["rooms"]:
                room["nombre"] = room.get("name")

            # Fetch services
            services_response = requests.get("http://backend:5001/services")
            services_response.raise_for_status()
            data["services"] = services_response.json().get("data", [])
            for service in data["services"]:
                service["nombre"] = service.get("name")

            # Fetch activities
            activities_response = requests.get("http://backend:5001/activity")
            activities_response.raise_for_status()
            data["activities"] = activities_response.json().get("data", [])
            for activity in data["activities"]:
                activity["nombre"] = activity.get("name")

        except requests.exceptions.RequestException as e:
            print("Error fetching data for reservation form:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)

        return render_template("reserva.html", paquete=None, data=data)

@app.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")


@app.route("/check-availability")
def check_availability():
    checkin = request.args.get('checkin')
    checkout = request.args.get('checkout')

    if not checkin or not checkout:
        return jsonify({"error": "Faltan fechas de check-in o check-out."}), 400

    available_ids = []
    try:
        backend_url = f"http://backend:5001/availability?checkin={checkin}&checkout={checkout}"
        response = requests.get(backend_url)
        data = response.json().get("data", [])
        available_ids = [room['id'] for room in data]
        
    except Exception as e:
        print(f"Error calling backend availability: {e}")

    return jsonify({"available_room_ids": available_ids})

@app.route("/confirmacion-mail", methods=["POST"])
def confirmacion_mail():
    datos_reserva = request.get_json
    tipo_reserva = datos_reserva.get("reservation_type")
    costumer_name = datos_reserva.get("costumer_Name")
    checkin_date = datos_reserva.get("checkinDate")
    checkout_date = datos_reserva.get("checkoutDate")
    adults = datos_reserva.get("adults")
    children = datos_reserva.get("children")
    email_cliente = datos_reserva.get("costumer_Email")
    if (tipo_reserva == "paquete"):
        backend_url = "http://backend:5001/package"
        response = requests.get(backend_url)
        json_data = response.json()
        paquetes = json_data.get("data", [])

        for paquete in paquetes:
            if (datos_reserva.get("package_id") == int(paquetes.get("id"))):
                paquete_name = paquete.get("name")
        body = f"""
        Hola {costumer_name}
        Tu reservación fue registrada con éxito.
        ----------------------------------------
        Detalles de la reservación:
        Paquete: {paquete_name}
        Fecha de ingreso: {checkin_date}
        Fecha de egreso: {checkout_date}
        Para {adults} adultos y {children} niños.
        Gracias por elegir nuestro paquete.
        """
    else:
        backend_url = "http://backend:5001/room_types"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        room_types = json_data.get("data", [])

        for room in room_types:
            if (datos_reserva.get("roomTypeId") == int(room.get("id"))):
                room_name = room.get("name")
        
        body = f"""
        Hola {costumer_name}
        Tu reservación fue registrada con éxito.
        ----------------------------------------
        Detalles de la reservación:

        Habitación: {room_name}
        Fecha de ingreso: {checkin_date}
        Fecha de egreso: {checkout_date}
        Para {adults} adultos y {children} niños.
        Gracias por elegir nuestro paquete.
        """
    msg = Message(
            subject=f"Confirmación de reserva",
            recipients={email_cliente},
            body=body,
        )
    mail.send(msg)
    return True

@app.errorhandler(404)
def errorhandler(e):
    return render_template('404.html')


if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)