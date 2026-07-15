def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

import hashlib

def hash_email_for_cache(email):
    """
    Hash email before using as a cache key. If Redis/cache is ever shared
    with another service, raw emails (or worse, OTPs tied to them) shouldn't
    be readable as plain keys.
    """
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()

def mask_otp(code: str) -> str:
    """Masks all but the last 2 digits — e.g. '482913' -> '****13'"""
    if not code or len(code) <= 2:
        return '*' * len(code or '')
    return '*' * (len(code) - 2) + code[-2:]