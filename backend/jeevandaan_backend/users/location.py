# users/location.py  — drop-in replacement
# Adds a SQL bounding-box pre-filter BEFORE the expensive geodesic loop.
# This drastically reduces CPU work and prevents worker SIGKILL on Render.

from geopy.distance import geodesic
import hashlib
from django.core.cache import cache



def _bounding_box(lat, lng, radius_km):
    """
    Returns (min_lat, max_lat, min_lng, max_lng) for a rough square
    around the point. 1 degree lat ≈ 111 km everywhere.
    1 degree lng ≈ 111 km * cos(lat).
    """
    import math
    lat, lng = float(lat), float(lng)
    delta_lat = radius_km / 111.0
    delta_lng = radius_km / (111.0 * math.cos(math.radians(lat)))
    return (
        lat - delta_lat,
        lat + delta_lat,
        lng - delta_lng,
        lng + delta_lng,
    )


def get_nearby_partners(lat, lng, partners_qs, radius_km=10):
    """
    Returns a list of dicts: [{'partner': <obj>, 'distance_km': float}, ...]
    sorted by distance ascending.

    partners_qs can be a QuerySet or a plain Python list.
    """
    lat, lng = float(lat), float(lng)

    # --- Step 1: cheap bounding-box SQL filter (only if it's a QuerySet) ---
    try:
        min_lat, max_lat, min_lng, max_lng = _bounding_box(lat, lng, radius_km)
        partners_qs = partners_qs.filter(
            latitude__gte=min_lat,
            latitude__lte=max_lat,
            longitude__gte=min_lng,
            longitude__lte=max_lng,
        )
    except (AttributeError, TypeError):
        # It's a plain list — skip SQL filter, geodesic will handle it
        pass

    # --- Step 2: precise geodesic filter on the (now small) subset ---
    result = []
    for partner in partners_qs:
        try:
            p_lat = float(partner.latitude)
            p_lng = float(partner.longitude)
        except (TypeError, ValueError):
            continue

        distance = geodesic((lat, lng), (p_lat, p_lng)).km
        if distance <= radius_km:
            result.append({
                'partner': partner,
                'distance_km': round(distance, 1),
            })

    result.sort(key=lambda x: x['distance_km'])
    return result


def get_nearby_donors(lat, lng, donors_qs, radius_km=10):
    """
    Same pattern for donors.
    """
    lat, lng = float(lat), float(lng)

    try:
        min_lat, max_lat, min_lng, max_lng = _bounding_box(lat, lng, radius_km)
        donors_qs = donors_qs.filter(
            latitude__gte=min_lat,
            latitude__lte=max_lat,
            longitude__gte=min_lng,
            longitude__lte=max_lng,
        )
    except (AttributeError, TypeError):
        pass

    result = []
    for donor in donors_qs:
        try:
            d_lat = float(donor.latitude)
            d_lng = float(donor.longitude)
        except (TypeError, ValueError):
            continue

        distance = geodesic((lat, lng), (d_lat, d_lng)).km
        if distance <= radius_km:
            result.append({
                'donor': donor,
                'distance_km': round(distance, 1),
            })

    result.sort(key=lambda x: x['distance_km'])
    return result

def get_cache_key(lat, lng, blood_group, radius):
    """
    Builds a stable cache key for nearby-partner lookups.
    
    """
    lat_r = round(float(lat), 3)
    lng_r = round(float(lng), 3)
    bg = blood_group or 'any'   
    raw = f"nearby_partners:{lat_r}:{lng_r}:{bg}:{radius}"
    return hashlib.sha256(raw.encode()).hexdigest()