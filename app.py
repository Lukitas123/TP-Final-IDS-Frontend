from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail
from functions import enviar_email_contacto, parse_gallery
from hardcoded_data import DATA
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


# --- ZONA DE RUTAS ---
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/actividades")
def actividades():
    actividades = []

    try:
        backend_url = "http://backend:5001/api/activity"
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
        backend_url = "http://backend:5001/api/services"
        response = requests.get(backend_url)

        json_data = response.json()
        servicios = json_data.get("data", [])

        for service in servicios:
            gallery_str = service.get("gallery")

            try:
                service["gallery"] = json.loads(gallery_str)
            except ValueError:
                service["gallery"] = []

    except Exception as e:
        print("Error al obtener servicios desde el backend:", e)

    return render_template("servicios.html", servicios=servicios)





@app.route("/habitaciones")
def habitaciones():
    room_types = parse_gallery(DATA["tipo_habitacion"])
    print(room_types)
    return render_template("habitaciones.html", habitaciones=room_types)


@app.route("/paquetes")
def paquetes():
    return render_template("paquetes.html", paquetes=DATA["paquete"])


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
        nombre = request.form.get("name")
        email = request.form.get("email")
        tipo_habitacion = request.form.get("room")
        servicio = request.form.get("service")
        actividad = request.form.get("activity")
        checkin = request.form.get("checkin")
        checkout = request.form.get("checkout")
        return redirect(url_for("confirmacion"))

    #si es get
    rooms = DATA["tipo_habitacion"]
    services = DATA["servicio"]
    activities  = DATA["actividad"]
    data = {
        "rooms": rooms,
        "services": services,
        "activities": activities,
    }
    return render_template("reserva.html", paquete=None, data=data)

@app.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")


if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)