from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def get_nearby_partners(user_lat, user_lng, partners, radius_km=10):
    """
    Returns partners within radius_km of user location
    sorted by distance (closest first)
    """

    nearby = []

    try:
        user_location = (float(user_lat), float(user_lng))
    except:
        return []

    for partner in partners:
        if partner.latitude is not None and partner.longitude is not None:
            try:
                partner_location = (
                    float(partner.latitude),
                    float(partner.longitude)
                )

                distance = calculate_distance(
    user_location[0],
    user_location[1],
    partner_location[0],
    partner_location[1]
)

                if distance <= radius_km:
                    nearby.append({
                        'partner': partner,
                        'distance_km': round(distance, 2)
                    })

            except Exception as e:
                print(f"Error for partner {partner.id}: {e}")
                continue

    nearby.sort(key=lambda x: x['distance_km'])
    return nearby
    
def get_nearby_donors(user_lat, user_lng, donors, radius_km=10):
    """
    Returns donors within radius_km
    sorted by distance closest first
    """
    nearby = []

    for donor in donors:
        if donor.latitude and donor.longitude:
            donor_location = (float(donor.latitude), float(donor.longitude))
            user_location = (float(user_lat), float(user_lng))

            distance = calculate_distance(
                user_location[0],
                user_location[1],
                donor_location[0],
                donor_location[1]
            )

            if distance <= radius_km:
                nearby.append({
                    'donor': donor,
                    'distance_km': round(distance, 2)
                })

    nearby.sort(key=lambda x: x['distance_km'])
    return nearby