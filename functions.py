from flask_mail import Message

def enviar_email_contacto(mail, datos_formulario, archivo_adjunto):
    try:
        nombre_completo = datos_formulario['nombre_completo']
        email = datos_formulario['email']
        telefono = datos_formulario['telefono']
        descripcion = datos_formulario['descripcion']
        
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
            recipients=['penefflukas19@gmail.com'],
            body=body
        )

        if archivo_adjunto and archivo_adjunto.filename != '':
            filename = archivo_adjunto.filename
            msg.attach(
                filename=filename,
                content_type=archivo_adjunto.content_type,
                data=archivo_adjunto.read()
            )
        
        mail.send(msg)
        return True

    except Exception as e:
        print(f"Error al enviar el correo desde functions.py: {e}")
        return False
