from flask import Blueprint, Flask, render_template, request
from config import init_config
from extensions import mail
from flask_mail import Message
import requests
import json

bp_confirmacion_mail = Blueprint("confirmacion_mail", __name__)

@bp_confirmacion_mail.route("/confirmacion_mail", methods=["POST"])
def confirmacion_mail():
    datos_reserva = request.get_json()
    tipo_reserva = datos_reserva["reservation_type"]
    costumer_name = datos_reserva["customer_name"]
    checkin_date = datos_reserva["checkin_date"]
    checkout_date = datos_reserva["checkout_date"]
    adults = datos_reserva["adults"]
    children = datos_reserva["children"]
    email_cliente = datos_reserva["customer_email"]
    if (tipo_reserva == "paquete"):
        backend_url = "http://localhost:5001/package"
        response = requests.get(backend_url)
        json_data = response.json()
        paquetes = json_data.get("data", [])

        for paquete in paquetes:
            if (datos_reserva["package_id"] == int(paquete.get("id"))):
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
        backend_url = "http://localhost:5001/room_types"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        room_types = json_data.get("data", [])

        for room in room_types:
            if (datos_reserva["roomTypeId"] == int(room.get("id"))):
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
        
        Gracias por elegirnos.
        """
    msg = Message(
            subject=f"Confirmación de reserva",
            recipients={email_cliente},
            body=body,
        )
    mail.send(msg)
    return
