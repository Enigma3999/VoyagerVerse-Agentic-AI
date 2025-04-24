import requests
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather_tools")

# API keys would normally be stored in environment variables
# For the prototype, we'll use placeholder keys
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "your_openweathermap_api_key")
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY", "your_weatherapi_key")

def get_weather_openweathermap(latitude: float, longitude: float) -> Dict[str, Any]:
    """Get current weather data from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric"  # Use metric units (Celsius)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        
        # Extract relevant weather information
        weather_data = {
            "provider": "OpenWeatherMap",
            "timestamp": datetime.now().isoformat(),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "conditions": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "precipitation_chance": 0.0,  # Not provided directly by this API
            "uv_index": 0  # Not provided directly by this API
        }
        
        return {
            "status": "success",
            "data": weather_data
        }
    
    except Exception as e:
        logger.error(f"Error fetching weather from OpenWeatherMap: {e}")
        
        # Fallback to simulated data for the prototype
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_weather_data("Dubai")
        }

def get_weather_forecast_openweathermap(latitude: float, longitude: float, days: int = 5) -> Dict[str, Any]:
    """Get weather forecast from OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Use metric units (Celsius)
        "cnt": min(days * 8, 40)  # 8 forecasts per day (3-hour intervals), max 5 days
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        forecast_data = {
            "provider": "OpenWeatherMap",
            "timestamp": datetime.now().isoformat(),
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": []
        }
        
        for forecast in data["list"]:
            forecast_data["forecasts"].append({
                "timestamp": forecast["dt_txt"],
                "temperature": forecast["main"]["temp"],
                "feels_like": forecast["main"]["feels_like"],
                "humidity": forecast["main"]["humidity"],
                "pressure": forecast["main"]["pressure"],
                "wind_speed": forecast["wind"]["speed"],
                "wind_direction": forecast["wind"]["deg"],
                "conditions": forecast["weather"][0]["main"],
                "description": forecast["weather"][0]["description"],
                "icon": forecast["weather"][0]["icon"],
                "precipitation_chance": forecast.get("pop", 0) * 100  # Probability of precipitation
            })
        
        return {
            "status": "success",
            "data": forecast_data
        }
    
    except Exception as e:
        logger.error(f"Error fetching weather forecast from OpenWeatherMap: {e}")
        
        # Fallback to simulated data
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_forecast_data("Dubai", days)
        }

def get_weather_weatherapi(city: str) -> Dict[str, Any]:
    """Get current weather data from WeatherAPI.com."""
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": city,
        "aqi": "no"  # Don't include air quality data
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            "provider": "WeatherAPI",
            "timestamp": datetime.now().isoformat(),
            "temperature": data["current"]["temp_c"],
            "feels_like": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "pressure": data["current"]["pressure_mb"],
            "wind_speed": data["current"]["wind_kph"],
            "wind_direction": data["current"]["wind_degree"],
            "conditions": data["current"]["condition"]["text"],
            "description": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "precipitation_chance": data["current"].get("precip_mm", 0),
            "uv_index": data["current"]["uv"]
        }
        
        return {
            "status": "success",
            "data": weather_data
        }
    
    except Exception as e:
        logger.error(f"Error fetching weather from WeatherAPI: {e}")
        
        # Fallback to simulated data
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_weather_data(city)
        }

def get_weather_forecast_weatherapi(city: str, days: int = 3) -> Dict[str, Any]:
    """Get weather forecast from WeatherAPI.com."""
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": city,
        "days": min(days, 10),  # Maximum 10 days
        "aqi": "no",
        "alerts": "no"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        forecast_data = {
            "provider": "WeatherAPI",
            "timestamp": datetime.now().isoformat(),
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "forecasts": []
        }
        
        for day in data["forecast"]["forecastday"]:
            forecast_data["forecasts"].append({
                "date": day["date"],
                "max_temp": day["day"]["maxtemp_c"],
                "min_temp": day["day"]["mintemp_c"],
                "avg_temp": day["day"]["avgtemp_c"],
                "max_wind": day["day"]["maxwind_kph"],
                "total_precip": day["day"]["totalprecip_mm"],
                "avg_humidity": day["day"]["avghumidity"],
                "conditions": day["day"]["condition"]["text"],
                "icon": day["day"]["condition"]["icon"],
                "uv_index": day["day"]["uv"],
                "hourly": [{
                    "time": hour["time"],
                    "temp": hour["temp_c"],
                    "conditions": hour["condition"]["text"],
                    "icon": hour["condition"]["icon"],
                    "wind_speed": hour["wind_kph"],
                    "wind_direction": hour["wind_degree"],
                    "humidity": hour["humidity"],
                    "feels_like": hour["feelslike_c"],
                    "precipitation_chance": hour["chance_of_rain"]
                } for hour in day["hour"]]
            })
        
        return {
            "status": "success",
            "data": forecast_data
        }
    
    except Exception as e:
        logger.error(f"Error fetching weather forecast from WeatherAPI: {e}")
        
        # Fallback to simulated data
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_forecast_data(city, days)
        }

def get_simulated_weather_data(city: str) -> Dict[str, Any]:
    """Generate simulated weather data for testing purposes."""
    import random
    
    # Simulate Dubai's hot climate
    if city.lower() == "dubai":
        temperature = random.uniform(35, 45)  # Hot temperature in Dubai
        humidity = random.uniform(50, 80)     # Moderate to high humidity
        conditions = random.choice(["Sunny", "Clear", "Partly cloudy", "Hazy"])
        uv_index = random.randint(8, 11)      # High UV index
    else:
        temperature = random.uniform(20, 35)  # Default temperature range
        humidity = random.uniform(40, 70)     # Default humidity range
        conditions = random.choice(["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Clear"])
        uv_index = random.randint(3, 8)       # Default UV index range
    
    return {
        "provider": "Simulated",
        "timestamp": datetime.now().isoformat(),
        "temperature": round(temperature, 1),
        "feels_like": round(temperature + random.uniform(-2, 2), 1),
        "humidity": round(humidity, 1),
        "pressure": round(random.uniform(1000, 1020), 1),
        "wind_speed": round(random.uniform(5, 20), 1),
        "wind_direction": random.randint(0, 359),
        "conditions": conditions,
        "description": conditions,
        "icon": "",  # No icon for simulated data
        "precipitation_chance": round(random.uniform(0, 0.2), 2),
        "uv_index": uv_index
    }

def get_simulated_forecast_data(city: str, days: int) -> Dict[str, Any]:
    """Generate simulated forecast data for testing purposes."""
    import random
    from datetime import datetime, timedelta
    
    forecast_data = {
        "provider": "Simulated",
        "timestamp": datetime.now().isoformat(),
        "city": city,
        "country": "United Arab Emirates" if city.lower() == "dubai" else "Unknown",
        "forecasts": []
    }
    
    # Base temperature that will vary slightly day by day
    if city.lower() == "dubai":
        base_temp = random.uniform(38, 42)  # Hot base temperature for Dubai
    else:
        base_temp = random.uniform(25, 35)  # Default base temperature
    
    # Generate forecast for each day
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        day_temp_variation = random.uniform(-2, 2)  # Temperature varies slightly each day
        
        # For Dubai, make it progressively hotter
        if city.lower() == "dubai":
            day_temp = base_temp + day_temp_variation + (i * 0.5)  # Gets hotter each day
            conditions = random.choice(["Sunny", "Clear", "Partly cloudy", "Hazy"])
            uv_index = random.randint(8, 11)  # High UV index
        else:
            day_temp = base_temp + day_temp_variation
            conditions = random.choice(["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Clear"])
            uv_index = random.randint(3, 8)  # Default UV index range
        
        forecast_data["forecasts"].append({
            "date": date,
            "max_temp": round(day_temp + random.uniform(2, 4), 1),
            "min_temp": round(day_temp - random.uniform(5, 8), 1),
            "avg_temp": round(day_temp, 1),
            "max_wind": round(random.uniform(10, 25), 1),
            "total_precip": round(random.uniform(0, 2), 1),
            "avg_humidity": round(random.uniform(50, 80), 1),
            "conditions": conditions,
            "icon": "",  # No icon for simulated data
            "uv_index": uv_index,
            "hourly": []
        })
        
        # Generate hourly forecast
        for hour in range(24):
            time_str = f"{date} {hour:02d}:00"
            hour_temp_variation = random.uniform(-3, 3)  # Temperature varies by hour
            
            # Temperature is higher during the day, lower at night
            if 6 <= hour <= 18:  # Daytime hours
                hour_temp = day_temp + hour_temp_variation
                if 11 <= hour <= 15:  # Peak heat hours
                    hour_temp += random.uniform(1, 3)
            else:  # Nighttime hours
                hour_temp = day_temp - random.uniform(5, 8) + hour_temp_variation
            
            forecast_data["forecasts"][-1]["hourly"].append({
                "time": time_str,
                "temp": round(hour_temp, 1),
                "conditions": conditions,
                "icon": "",
                "wind_speed": round(random.uniform(5, 20), 1),
                "wind_direction": random.randint(0, 359),
                "humidity": round(random.uniform(50, 80), 1),
                "feels_like": round(hour_temp + random.uniform(-2, 2), 1),
                "precipitation_chance": round(random.uniform(0, 0.2) * 100, 1)
            })
    
    return forecast_data

# Register tools with the registry
tool_registry.register_tool(
    tool_name="get_current_weather_openweathermap",
    tool_function=get_weather_openweathermap,
    category="weather",
    description="Get current weather conditions from OpenWeatherMap API",
    required_params=["latitude", "longitude"]
)

tool_registry.register_tool(
    tool_name="get_weather_forecast_openweathermap",
    tool_function=get_weather_forecast_openweathermap,
    category="weather",
    description="Get weather forecast from OpenWeatherMap API",
    required_params=["latitude", "longitude"],
    optional_params=["days"]
)

tool_registry.register_tool(
    tool_name="get_current_weather_weatherapi",
    tool_function=get_weather_weatherapi,
    category="weather",
    description="Get current weather conditions from WeatherAPI.com",
    required_params=["city"]
)

tool_registry.register_tool(
    tool_name="get_weather_forecast_weatherapi",
    tool_function=get_weather_forecast_weatherapi,
    category="weather",
    description="Get weather forecast from WeatherAPI.com",
    required_params=["city"],
    optional_params=["days"]
)
