from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)


@home_bp.route("/")
def home():
    return render_template("index.html")


@home_bp.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")


@home_bp.app_errorhandler(404)
def errorhandler(e):
    return render_template('404.html')
