import requests

BASE_URL = "http://backend:5001"


def api_get(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("data", [])
    except Exception as e:
        print(f"[backend_api] Error GET {endpoint}: {e}")
        return []
