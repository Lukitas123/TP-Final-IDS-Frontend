import requests
from flask import current_app


def api_get(endpoint):
    base_url = current_app.config.get("INTERNAL_BACKEND_URL")
    if not base_url:
        print("[backend_api] Error: INTERNAL_BACKEND_URL no está configurada.")
        return []

    try:
        response = requests.get(f"{base_url}/{endpoint}")
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("data", [])
    except Exception as e:
        print(f"[backend_api] Error GET {endpoint}: {e}")
        return []
