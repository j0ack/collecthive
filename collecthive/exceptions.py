from typing import Dict

from pydantic import ValidationError


def parse_validation_error(err: ValidationError) -> Dict[str, str]:
    """Pase ValidationError to InertiaJS error format."""
    error_dict = {}
    for error in err.errors():
        key = error["loc"][0]
        value = error["msg"]
        error_dict[key] = value

    return error_dict
