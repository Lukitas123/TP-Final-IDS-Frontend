from flask import Blueprint, render_template
from services.backend_api import api_get

bp_actividades = Blueprint("actividades", __name__)


@bp_actividades.route("/actividades")
def actividades():
    actividades = api_get("activity")
    return render_template("actividades.html", actividades=actividades)
