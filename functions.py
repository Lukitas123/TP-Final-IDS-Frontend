from flask_mail import Message
from typing import List, Any
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


def parse_gallery(gallery_value: Any) -> List[Any]:
    """
    Normaliza el campo `gallery` que viene del backend usando `isinstance`

    - Si ya viene como lista → se devuelve tal cual.
    - Si viene como string que representa una lista → se intenta parsear.
    - En cualquier otro caso → [].
    """
    # Caso 1: ya es una lista (lo que más nos conviene en los templates)
    if isinstance(gallery_value, list):
        return gallery_value

    # Caso 2: viene como string (por ejemplo '["img1.jpg", "img2.jpg"]')
    if isinstance(gallery_value, str):
        try:
            parsed = ast.literal_eval(gallery_value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            # Si falla el parseo, devolvemos lista vacía y seguimos
            pass
        return []

    # Caso 3: cualquier otro tipo lo normalizamos a lista vacía
    return []
