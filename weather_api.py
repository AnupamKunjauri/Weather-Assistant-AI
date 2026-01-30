import requests

API_KEY = "5b9bc74b914343a842fe9c7c7baff917"   # 🔴 put your key here
BASE_URL = "https://api.openweathermap.org/data/2.5"


# =================================================
# 📍 GET COORDINATES (GEOCODING)
# =================================================
def get_coordinates(city):
    try:
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct"
            f"?q={city}&limit=1&appid={API_KEY}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            return None, "City not found"

        loc = data[0]   # ✅ dict

        lat = loc.get("lat")
        lon = loc.get("lon")

        if lat is None or lon is None:
            return None, "Coordinates unavailable"

        return (lat, lon), None

    except Exception as e:
        return None, str(e)


# =================================================
# 🌤️ CURRENT WEATHER
# =================================================
def get_current_weather(lat, lon):
    url = (
        f"{BASE_URL}/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url, timeout=10)
    return response.json()


# =================================================
# 📅 FORECAST (5 DAY / 3 HOUR)
# =================================================
def get_forecast(lat, lon):
    url = (
        f"{BASE_URL}/forecast"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url, timeout=10)
    return response.json()


# =================================================
# 🌫️ AIR QUALITY INDEX
# =================================================
def get_air_quality(lat, lon):
    url = (
        f"{BASE_URL}/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )
    response = requests.get(url, timeout=10)
    return response.json()
