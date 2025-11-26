from flask import Blueprint
from services.search_service import (
    get_rooms_for_search,
    get_services_for_search,
    get_activities_for_search,
    get_packages_for_search
)

bp_context = Blueprint("context_processor", __name__)


@bp_context.app_context_processor
def inject_search_data():
    return {
        "rooms_for_search": get_rooms_for_search(),
        "services_for_search": get_services_for_search(),
        "activities_for_search": get_activities_for_search(),
        "packages_for_search": get_packages_for_search(),
    }
