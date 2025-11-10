from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail
from config import Config

# Importa la función de ayuda desde functions.py
from functions import enviar_email_contacto, parse_gallery
from hardcoded_data import DATA

app = Flask(__name__)

# Carga la configuración modular desde el objeto Config
app.config.from_object(Config)

# Inicializa la extensión de Mail
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


@app.route("/contacto", methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        exito = enviar_email_contacto(
            mail=mail,
            datos_formulario=request.form,
            archivo_adjunto=request.files.get('archivo')
        )
        
        if exito:
            return redirect(url_for('contacto', status='success'))
        else:
            return redirect(url_for('contacto', status='error'))
    
    return render_template("contacto.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html", servicios=DATA["servicio"])

if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)