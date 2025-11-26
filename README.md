# Frontend – TP-Final-IDS-Frontend (Hotel Bugbusters)

Este repositorio contiene el **frontend del proyecto Hotel Bugbusters**, desarrollado como parte del TP final de Introducción al Desarrollo de Software (FIUBA).  
Es una aplicación web en **Flask** que funciona como sitio público del hotel y como capa de presentación que consume la API REST del backend.

## Objetivo del Frontend

- Mostrar el sitio web principal del proyecto.
- Permitir reservas por paquete o personalizadas.
- Consumir y renderizar los datos provenientes del backend.
- Gestionar envío de correos desde formulario de contacto.

## Tecnologías utilizadas
Utilizamos la convención [Block element modifier](https://getbem.com/naming/) para los nombres de los elementos en html y [snake_case](https://developer.mozilla.org/en-US/docs/Glossary/Snake_case) para los nombres de variables.
- Python + Flask 
- Jinja2 
- HTML / CSS / JavaScript  
- Leaflet.js 
- Flask-Mail  
- Requests
- Docker
- Git


## Integración con Backend

El frontend consume datos del backend mediante requests HTTP:

Base: http://backend:5001

## Inicialización
**Crear entorno virtual**<br>
Desde la carpeta de cada proyecto TP-Final-IDS-Frontend y TP-Final-IDS-Backend.
<br>
```
# Linux 
python3 -m venv .venv

# Windows
python -m venv .venv
```


**Activar el entorno virtual**
```
# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**Instalar dependencias**
```
pip install -r requirements.txt
```
**Iniciar el servidor de desarrollo**
```
flask run
```

**Desactivar el entorno virtual**
```
# Linux
deactivate .venv/bin/activate

# Windows
deactivate .venv\Scripts\activate
```