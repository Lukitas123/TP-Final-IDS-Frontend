from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail
from functions import enviar_email_contacto, parse_gallery
from hardcoded_data import DATA
import os
from dotenv import load_dotenv
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
mail = Mail(app)


# --- ZONA DE RUTAS ---
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/actividades")
def actividades():
    return render_template("actividades.html", actividades=DATA["actividad"])


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


@app.route("/servicios")
def servicios():

    return render_template("servicios.html", servicios=DATA["servicio"])


@app.route("/reserva")
def reserva():
    rooms = DATA["tipo_habitacion"]
    services = DATA["servicio"]
    activities  = DATA["actividad"]
    data = {
        "rooms": rooms,
        "services": services,
        "activities": activities,
    }
    return render_template("reserva.html", paquete=None, data=data)


if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)