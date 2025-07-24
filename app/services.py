import string
import random
from app.storage import storage
from app.models import URLMapping
from urllib.parse import urlparse
from app.utils import is_valid_url, generate_short_code


def shorten_url(original_url: str) -> URLMapping:
    if not is_valid_url(original_url):
        raise ValueError("Invalid URL")

    short_code = generate_short_code()
    while storage.get(short_code):
        short_code = generate_short_code()

    mapping = URLMapping(original_url, short_code)
    storage.save(mapping)
    return mapping

def get_original_url(short_code: str) -> str:
    mapping = storage.get(short_code)
    if mapping:
        storage.increment_click(short_code)
        return mapping.original_url
    return None

def get_stats(short_code: str):
    mapping = storage.get(short_code)
    if mapping:
        return {
            "url": mapping.original_url,
            "clicks": mapping.clicks,
            "created_at": mapping.created_at.isoformat()
        }
    return None
