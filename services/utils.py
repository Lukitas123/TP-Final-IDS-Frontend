import ast
from typing import Dict, List, Any

def parse_gallery(dicts_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    proc_list: List[Dict[str, Any]] = []
    
    for item in dicts_list:
        copied_item = item.copy()

        if "galeria" in copied_item and isinstance(copied_item["galeria"], str):
            try:
                copied_item["galeria"] = ast.literal_eval(copied_item["galeria"])
            except Exception as e:
                print(
                    f"Error parsing gallery for item {item.get('id', 'unknown')}: {e}"
                )
                copied_item["galeria"] = []

        proc_list.append(copied_item)

    return proc_list
