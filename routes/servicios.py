from flask import Blueprint, render_template
from services.backend_api import api_get
from services.gallery import safe_parse_gallery

bp_servicios = Blueprint("servicios", __name__)


@bp_servicios.route("/servicios")
def servicios():
    servicios = api_get("services")
    for servicio in servicios:
        servicio["gallery"] = safe_parse_gallery(servicio.get("gallery"))
    return render_template("servicios.html", servicios=servicios)
