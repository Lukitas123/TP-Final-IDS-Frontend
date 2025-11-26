import requests

BASE_URL = "http://backend:5001"

def get_rooms_for_search():
    try:
        resp = requests.get(f"{BASE_URL}/room_types", timeout=5)
        data = resp.json().get("data", [])
        return [
            {"id": r.get("id"), "nombre": r.get("name")}
            for r in data
            if r.get("name")
        ]
    except:
        return []

def get_services_for_search():
    try:
        resp = requests.get(f"{BASE_URL}/services", timeout=5)
        data = resp.json().get("data", [])
        return [
            {"id": s.get("id"), "nombre": s.get("name")}
            for s in data
            if s.get("name")
        ]
    except:
        return []

def get_activities_for_search():
    try:
        resp = requests.get(f"{BASE_URL}/activity", timeout=5)
        data = resp.json().get("data", [])
        return [
            {"id": a.get("id"), "nombre": a.get("name")}
            for a in data
            if a.get("name")
        ]
    except:
        return []

def get_packages_for_search():
    try:
        resp = requests.get(f"{BASE_URL}/package", timeout=5)
        data = resp.json().get("data", [])
        return [
            {"id": p.get("id"), "nombre": p.get("name")}
            for p in data
            if p.get("name")
        ]
    except:
        return []
