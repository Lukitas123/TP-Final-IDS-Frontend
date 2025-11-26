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


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)
