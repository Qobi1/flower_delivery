import json
from rest_framework.exceptions import ValidationError

def parse_list_param(param):
    try:
        return json.loads(param) if param else []
    except json.JSONDecodeError:
        raise ValidationError(f"Invalid list format: {param}")