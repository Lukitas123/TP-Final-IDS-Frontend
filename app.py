from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuracion de flask-mail

# Zona de rutas
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run("localhost", 3000, debug=True)