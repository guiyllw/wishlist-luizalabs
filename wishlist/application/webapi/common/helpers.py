from typing import Dict


def format_error(e: Exception) -> Dict:
    return {'detail': str(e)}
