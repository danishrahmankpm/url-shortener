# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

    
def is_valid_url(url: str) -> bool:
        from urllib.parse import urlparse
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

def generate_short_code(length=6) -> str:
        import string
        import random
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))