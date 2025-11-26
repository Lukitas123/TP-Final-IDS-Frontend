import os
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

def init_config(app):
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1']
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'false').lower() in ['true', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

    # URLs del Backend
    app.config['INTERNAL_BACKEND_URL'] = os.getenv('INTERNAL_BACKEND_URL')
    app.config['PUBLIC_BACKEND_URL'] = os.getenv('PUBLIC_BACKEND_URL')

    return Mail(app)
