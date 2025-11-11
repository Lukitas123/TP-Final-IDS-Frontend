from flask_mail import Message
from typing import Dict, List, Any
import ast


def enviar_email_contacto(mail, datos_formulario, archivo_adjunto):
    try:
        nombre_completo = datos_formulario["nombre_completo"]
        email = datos_formulario["email"]
        telefono = datos_formulario["telefono"]
        descripcion = datos_formulario["descripcion"]

        body = f"""
        Nuevo mensaje de contacto de: {nombre_completo}
        Email: {email}
        Teléfono: {telefono}
        -----------------------------------------
        Mensaje:
        {descripcion}
        """

        msg = Message(
            subject=f"Nuevo Contacto de {nombre_completo}",
            recipients=["penefflukas19@gmail.com"],
            body=body,
        )

        if archivo_adjunto and archivo_adjunto.filename != "":
            filename = archivo_adjunto.filename
            msg.attach(
                filename=filename,
                content_type=archivo_adjunto.content_type,
                data=archivo_adjunto.read(),
            )

        mail.send(msg)
        return True

    except Exception as e:
        print(f"Error al enviar el correo desde functions.py: {e}")
        return False


def parse_gallery(dicts_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    proc_list: List[Dict[str, Any]] = []
    for item in dicts_list:
        copied_item = item.copy()
        if "galeria" in copied_item and isinstance(copied_item["galeria"], str):
            try:
                copied_item["galeria"] = ast.literal_eval(copied_item["galeria"])
            except Exception as e:
                print(
                    f"Error parsing gallery for item {item.get('id', 'unknown')}: {e}"
                )
                copied_item["galeria"] = []

        proc_list.append(copied_item)
    return proc_list
