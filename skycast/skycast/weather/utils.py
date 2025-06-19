import requests
from django.conf import settings
import re

def get_weather_data(city):
    try:
        if ',' not in city:
            city += ', India'

        api_key = getattr(settings, "WEATHERSTACK_API_KEY", None)
        if not api_key:
            return {
                "success": False,
                "error": "API key not found. Please set WEATHERSTACK_API_KEY in settings."
            }

        base_url = "http://api.weatherstack.com/current"  # use HTTP for free tier
        params = {
            "access_key": api_key,
            "query": city,
            "units": "m"
        }

        response = requests.get(base_url, params=params, timeout=5)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Weather API error: HTTP {response.status_code}"
            }

        data = response.json()

        # ✅ Handle invalid query or API issues
        if data.get("success") is False or "current" not in data:
            return {
                "success": False,
                "error": data.get("error", {}).get("info", "City not found or API limit reached.")
            }

        # ✅ Clean city name from parentheses
        raw_city = data["location"]["name"]
        clean_city = re.sub(r"\s*\(.*?\)", "", raw_city).strip()

        # Optional: Remove "La " prefix if present
        if clean_city.lower().startswith("la "):
            clean_city = clean_city[3:]

        result = {
            "success": True,
            "city": clean_city,
            "country": data["location"]["country"],
            "temperature": data["current"]["temperature"],
            "description": data["current"]["weather_descriptions"][0],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_speed"],
            "icon": data["current"]["weather_icons"][0],
            "feelslike": data["current"]["feelslike"]
        }

        # Add a note if it's not India
        if result["country"].lower() != "india":
            result["note"] = f"Note: Showing result from {result['country']}"

        return result

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "The weather API timed out. Please try again later."
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }
