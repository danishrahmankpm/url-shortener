
from threading import Lock
from app.models import URLMapping

class InMemoryStorage:
    def __init__(self):
        self.url_map = {}
        self.lock = Lock()

    def save(self, mapping: URLMapping):
        with self.lock:
            self.url_map[mapping.short_code] = mapping

    def get(self, short_code: str) -> URLMapping:
        return self.url_map.get(short_code)

    def increment_click(self, short_code: str):
        with self.lock:
            if short_code in self.url_map:
                self.url_map[short_code].clicks += 1


storage = InMemoryStorage()
