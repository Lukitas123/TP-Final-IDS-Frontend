from flask import Blueprint, render_template, request, redirect, url_for
from services.email_service import enviar_email_contacto
from extensions import mail

bp_contacto = Blueprint("contacto", __name__)


@bp_contacto.route("/contacto", methods=["GET", "POST"])
def contacto():

    if request.method == "POST":
        exito = enviar_email_contacto(
            mail=mail,
            datos_formulario=request.form,
            archivo_adjunto=request.files.get("archivo"),
        )

        if exito:
            return redirect(url_for("contacto.contacto", status="success"))
        else:
            return redirect(url_for("contacto.contacto", status="error"))

    return render_template("contacto.html")
