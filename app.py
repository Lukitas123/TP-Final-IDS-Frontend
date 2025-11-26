<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mail import Mail, Message
from functions import enviar_email_contacto, parse_gallery
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
=======
from flask import Flask, render_template
from config import init_config
from extensions import mail

# Blueprints
from routes.home import bp_home
from routes.actividades import bp_actividades
from routes.servicios import bp_servicios
from routes.paquetes import bp_paquetes
from routes.habitaciones import bp_habitaciones
from routes.contacto import bp_contacto
from routes.reserva import bp_reserva
from routes.availability import bp_availability
from routes.context_processor import bp_context
>>>>>>> origin/main


app = Flask(__name__)
init_config(app)
mail.init_app(app)

# Registrar blueprints
app.register_blueprint(bp_home)
app.register_blueprint(bp_actividades)
app.register_blueprint(bp_servicios)
app.register_blueprint(bp_paquetes)
app.register_blueprint(bp_habitaciones)
app.register_blueprint(bp_contacto)
app.register_blueprint(bp_reserva)
app.register_blueprint(bp_availability)
app.register_blueprint(bp_context)

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
def error_404(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)