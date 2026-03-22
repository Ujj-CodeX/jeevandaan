from geopy.distance import geodesic

def get_nearby_partners(user_lat,user_lng , partners , radius_km=10):
   
    """
    Returns partners within radius_km of user location
    sorted by distance closest first
    """
    nearby =[]

    for partner in partners:
      if partner.latitude and partner.longitude:
        partner_location = (float(partner.latitude), float(partner.longitude))
        user_location = (float(user_lat), float(user_lng))
        distance = geodesic(user_location, partner_location).km
        if distance <= radius_km:
            nearby.append({
                    'partner': partner,
                    'distance_km': round(distance, 2)
                }) 
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

            distance = geodesic(user_location, donor_location).km

            if distance <= radius_km:
                nearby.append({
                    'donor': donor,
                    'distance_km': round(distance, 2)
                })

    nearby.sort(key=lambda x: x['distance_km'])
    return nearby