from flask import Blueprint, render_template
from services.backend_api import api_get
from services.gallery import safe_parse_gallery

bp_paquetes = Blueprint("paquetes", __name__)


@bp_paquetes.route("/paquetes")
def paquetes():
    paquetes = api_get("package")

    for paquete in paquetes:
        paquete["gallery"] = safe_parse_gallery(paquete.get("gallery"))

    return render_template("paquetes.html", paquetes=paquetes)
