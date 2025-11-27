from flask import Blueprint, request, jsonify, current_app
from app import mail
from flask_mail import Message
import requests
import json

bp_confirmacion_mail = Blueprint("confirmacion_mail", __name__)

#Se usa para las reservas personalizadas.
#Recibe el precio del cuarto, un array de las actividades y otro de los servicios
def calcular_precio_final(room_price,activities_chosen, services_chosen):
    price_final = room_price
    activities_price = 0
    services_price = 0
    
    if (activities_chosen):
        backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/activity"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        activities = json_data.get("data", [])
        for activity_chosen in activities_chosen:
            for activity in activities:
                if ( int(activity_chosen) == int(activity.get("id")) ):
                    activities_price += int(activity.get("price"))
        price_final += activities_price

    if (services_chosen):
        backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/service"
        response = requests.get(backend_url)
        response.raise_for_status()
        json_data = response.json()
        services = json_data.get("data", [])
        for service_chosen in services_chosen:
            for service in services:
                if (int(service_chosen) == int(service.get("id")) ):
                    services_price += int(service.get("price"))
        price_final += services_price

    return price_final



def mail_reserva_paquete(datos_reserva):
    costumer_name = datos_reserva["customer_name"]
    checkin_date = datos_reserva["checkin_date"]
    checkout_date = datos_reserva["checkout_date"]
    adults = datos_reserva["adults"]
    children = datos_reserva["children"]

    backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/package"
    response = requests.get(backend_url)
    response.raise_for_status()
    json_data = response.json()
    paquetes = json_data.get("data", [])

    for paquete in paquetes:
        if (datos_reserva["package_id"] == int(paquete.get("id"))):
            paquete_name = paquete.get("name")
            paquete_price = paquete.get("price")
    body = f"""
    Hola {costumer_name}
        
    Tu reservación fue registrada con éxito.
    ----------------------------------------
    Detalles de la reservación:
       
    Paquete: {paquete_name}
        
    Fecha de ingreso: {checkin_date}
        
    Fecha de egreso: {checkout_date}
        
    Para {adults} adultos y {children} niños.
    
    Costo final: {paquete_price}
        
    Gracias por elegir nuestro paquete.
    """
    return body

def mail_reserva_personalizada(datos_reserva):
    costumer_name = datos_reserva["customer_name"]
    checkin_date = datos_reserva["checkin_date"]
    checkout_date = datos_reserva["checkout_date"]
    adults = datos_reserva["adults"]
    children = datos_reserva["children"]
    services = datos_reserva["service"]
    activities = datos_reserva["activity"]


    backend_url = f"{current_app.config['INTERNAL_BACKEND_URL']}/room_types"
    response = requests.get(backend_url)
    response.raise_for_status()
    json_data = response.json()
    room_types = json_data.get("data", [])
    for room in room_types:
        if (datos_reserva["roomTypeId"] == int(room.get("id"))):
            room_name = room.get("name")
            room_price = int(room.get("price"))
    
    price_final = calcular_precio_final(room_price,activities,services)
    body = f"""
    Hola {costumer_name}
        
    Tu reservación fue registrada con éxito.
    ----------------------------------------
    Detalles de la reservación:

    Habitación: {room_name}
        
    Fecha de ingreso: {checkin_date}
        
    Fecha de egreso: {checkout_date}
        
    Para {adults} adultos y {children} niños.
        
    Costo total: {price_final}

    Gracias por elegirnos.
    """
    return body


@bp_confirmacion_mail.route("/confirmacion_mail", methods=["POST"])
def confirmacion_mail():
    datos_reserva = request.get_json()
    tipo_reserva = datos_reserva["reservation_type"]
    email_cliente = datos_reserva["customer_email"]

    if (tipo_reserva == "paquete"):
        body = mail_reserva_paquete(datos_reserva)
    else:
        body = mail_reserva_personalizada(datos_reserva)

    msg = Message(
            subject=f"Confirmación de reserva",
            recipients={email_cliente},
            body=body,
        )
    mail.send(msg)
    return jsonify({"message": "Correo de confirmación enviado."}), 200