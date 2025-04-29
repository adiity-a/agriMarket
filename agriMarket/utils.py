from geopy.geocoders import Nominatim
import math

def reverse_geocode(lat, lng):
    # print("Geocoding:", lat, lng)

    if not lat or not lng:
        return "Invalid coordinates"

    geolocator = Nominatim(user_agent="AgriMarketAI", timeout=10)
    try:
        location = geolocator.reverse((lat, lng), language='en')
        # print("Raw location:", location)  

        if location:
            address = location.raw.get('address', {})
            # print("Address components:", address)

            city = address.get('county') or address.get('town') or address.get('village') or address.get('county')
            state = address.get('state')

            if city and state:
                return f"{city}, {state}"
            elif state:
                return state
            elif city:
                return city
            else:
                return "Location found, but incomplete"
    except Exception as e:
        print("Geocoding error:", e)
        return "Error retrieving location"
    return "Unknown Location"


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c
