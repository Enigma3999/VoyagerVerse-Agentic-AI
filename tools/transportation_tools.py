import requests
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("transportation_tools")

# API keys would normally be stored in environment variables
UBER_API_KEY = os.getenv("UBER_API_KEY", "your_uber_api_key")
CARREM_API_KEY = os.getenv("CAREEM_API_KEY", "your_careem_api_key")
DUBAI_TRANSIT_API_KEY = os.getenv("DUBAI_TRANSIT_API_KEY", "your_dubai_transit_api_key")

def get_ride_estimate(pickup_location: str, dropoff_location: str, ride_type: str = "standard", provider: str = "uber") -> Dict[str, Any]:
    """Get a ride estimate for a trip."""
    if provider.lower() == "uber":
        return get_ride_estimate_uber(pickup_location, dropoff_location, ride_type)
    elif provider.lower() == "careem":
        return get_ride_estimate_careem(pickup_location, dropoff_location, ride_type)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def get_ride_estimate_uber(pickup_location: str, dropoff_location: str, ride_type: str = "standard") -> Dict[str, Any]:
    """Get a ride estimate using Uber API."""
    url = "https://api.uber.com/v1.2/estimates/price"
    
    headers = {
        "Authorization": f"Bearer {UBER_API_KEY}",
        "Accept-Language": "en_US",
        "Content-Type": "application/json"
    }
    
    # In a real implementation, we would geocode the locations
    # For the prototype, we'll use simulated coordinates
    params = {
        "start_latitude": 25.2048,    # Dubai coordinates
        "start_longitude": 55.2708,
        "end_latitude": 25.1972,     # Burj Khalifa coordinates
        "end_longitude": 55.2744
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract the relevant ride type
        ride_data = None
        for price in data.get("prices", []):
            if price.get("display_name", "").lower() == ride_type.lower():
                ride_data = price
                break
        
        if not ride_data:
            # If the specific ride type is not found, use the first one
            ride_data = data.get("prices", [])[0] if data.get("prices") else None
        
        if ride_data:
            return {
                "status": "success",
                "data": {
                    "provider": "Uber",
                    "pickup_location": pickup_location,
                    "dropoff_location": dropoff_location,
                    "ride_type": ride_data.get("display_name"),
                    "estimate": ride_data.get("estimate"),
                    "price_range": {
                        "min": ride_data.get("low_estimate"),
                        "max": ride_data.get("high_estimate")
                    },
                    "currency": ride_data.get("currency_code"),
                    "duration": ride_data.get("duration"),  # in seconds
                    "distance": ride_data.get("distance"),   # in miles
                    "surge_multiplier": ride_data.get("surge_multiplier", 1.0)
                }
            }
        else:
            return {
                "status": "error",
                "message": "No ride options available",
                "data": get_simulated_ride_estimate(pickup_location, dropoff_location, ride_type)
            }
    
    except Exception as e:
        logger.error(f"Error getting ride estimate with Uber: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_ride_estimate(pickup_location, dropoff_location, ride_type)
        }

def get_ride_estimate_careem(pickup_location: str, dropoff_location: str, ride_type: str = "standard") -> Dict[str, Any]:
    """Get a ride estimate using Careem API."""
    # In a real implementation, this would connect to Careem's API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_ride_estimate(pickup_location, dropoff_location, ride_type, provider="Careem")
    }

def book_ride(pickup_location: str, dropoff_location: str, ride_type: str, pickup_time: str, provider: str = "uber") -> Dict[str, Any]:
    """Book a ride."""
    if provider.lower() == "uber":
        return book_ride_uber(pickup_location, dropoff_location, ride_type, pickup_time)
    elif provider.lower() == "careem":
        return book_ride_careem(pickup_location, dropoff_location, ride_type, pickup_time)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def book_ride_uber(pickup_location: str, dropoff_location: str, ride_type: str, pickup_time: str) -> Dict[str, Any]:
    """Book a ride using Uber API."""
    # In a real implementation, this would connect to Uber's API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_ride_booking(pickup_location, dropoff_location, ride_type, pickup_time, provider="Uber")
    }

def book_ride_careem(pickup_location: str, dropoff_location: str, ride_type: str, pickup_time: str) -> Dict[str, Any]:
    """Book a ride using Careem API."""
    # In a real implementation, this would connect to Careem's API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_ride_booking(pickup_location, dropoff_location, ride_type, pickup_time, provider="Careem")
    }

def get_transit_routes(origin: str, destination: str, departure_time: str = None) -> Dict[str, Any]:
    """Get public transit routes between two locations."""
    url = "https://api.dubaitransit.ae/routes"
    
    headers = {
        "Authorization": f"Bearer {DUBAI_TRANSIT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # In a real implementation, we would geocode the locations
    # For the prototype, we'll use simulated data
    try:
        # This would be a real API call in a production environment
        # response = requests.get(url, headers=headers, params=params)
        # response.raise_for_status()
        # data = response.json()
        
        return {
            "status": "success",
            "data": get_simulated_transit_routes(origin, destination, departure_time)
        }
    
    except Exception as e:
        logger.error(f"Error getting transit routes: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_transit_routes(origin, destination, departure_time)
        }

def get_simulated_ride_estimate(pickup_location: str, dropoff_location: str, ride_type: str = "standard", provider: str = "Uber") -> Dict[str, Any]:
    """Generate simulated ride estimate data for testing purposes."""
    # Define ride types and their base prices
    ride_types = {
        "economy": {"base_price": 20, "price_per_km": 2.0, "name": "UberX" if provider == "Uber" else "GO"},
        "standard": {"base_price": 30, "price_per_km": 3.0, "name": "Uber Comfort" if provider == "Uber" else "Economy"},
        "premium": {"base_price": 50, "price_per_km": 5.0, "name": "Uber Black" if provider == "Uber" else "Business"},
        "suv": {"base_price": 60, "price_per_km": 6.0, "name": "Uber XL" if provider == "Uber" else "MAX"},
    }
    
    # Get the ride type details, default to standard if not found
    ride_info = ride_types.get(ride_type.lower(), ride_types["standard"])
    
    # Simulate distance and duration based on locations
    # In a real implementation, this would use the Google Maps Distance Matrix API
    if "airport" in pickup_location.lower() or "airport" in dropoff_location.lower():
        distance_km = 15.0
    elif "downtown" in pickup_location.lower() or "downtown" in dropoff_location.lower():
        distance_km = 8.0
    elif "marina" in pickup_location.lower() or "marina" in dropoff_location.lower():
        distance_km = 12.0
    elif "palm" in pickup_location.lower() or "palm" in dropoff_location.lower():
        distance_km = 20.0
    else:
        # Random distance between 5 and 25 km
        distance_km = random.uniform(5.0, 25.0)
    
    # Calculate price
    base_price = ride_info["base_price"]
    price_per_km = ride_info["price_per_km"]
    estimated_price = base_price + (distance_km * price_per_km)
    
    # Add some variability
    min_price = max(1, int(estimated_price * 0.9))
    max_price = int(estimated_price * 1.1)
    
    # Calculate duration (assuming average speed of 40 km/h)
    duration_seconds = int(distance_km * (60 * 60) / 40)
    
    # Simulate surge pricing (10% chance of surge)
    surge_multiplier = 1.5 if random.random() < 0.1 else 1.0
    
    if surge_multiplier > 1.0:
        min_price = int(min_price * surge_multiplier)
        max_price = int(max_price * surge_multiplier)
    
    return {
        "provider": provider,
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,
        "ride_type": ride_info["name"],
        "estimate": f"AED {min_price}-{max_price}",
        "price_range": {
            "min": min_price,
            "max": max_price
        },
        "currency": "AED",
        "duration": duration_seconds,
        "distance": round(distance_km, 1),
        "surge_multiplier": surge_multiplier
    }

def get_simulated_ride_booking(pickup_location: str, dropoff_location: str, ride_type: str, pickup_time: str, provider: str = "Uber") -> Dict[str, Any]:
    """Generate simulated ride booking data for testing purposes."""
    # Get the ride estimate first
    estimate = get_simulated_ride_estimate(pickup_location, dropoff_location, ride_type, provider)
    
    # Generate a booking ID
    booking_id = f"RIDE{random.randint(100000, 999999)}"
    
    # Generate a driver
    drivers = [
        {"name": "Mohammed", "rating": 4.8, "car": "Toyota Camry", "plate": "Dubai A-12345"},
        {"name": "Ahmed", "rating": 4.9, "car": "Honda Accord", "plate": "Dubai B-54321"},
        {"name": "Fatima", "rating": 4.7, "car": "Nissan Altima", "plate": "Dubai C-98765"},
        {"name": "Sara", "rating": 4.9, "car": "Toyota Corolla", "plate": "Dubai D-56789"},
        {"name": "Omar", "rating": 4.6, "car": "Lexus ES", "plate": "Dubai E-24680"}
    ]
    
    driver = random.choice(drivers)
    
    # Parse pickup time
    try:
        pickup_datetime = datetime.strptime(pickup_time, "%Y-%m-%d %H:%M")
    except ValueError:
        # If the format is invalid, use current time + 15 minutes
        pickup_datetime = datetime.now() + timedelta(minutes=15)
    
    # Calculate estimated arrival time (5-15 minutes from now)
    driver_arrival_time = datetime.now() + timedelta(minutes=random.randint(5, 15))
    
    # Calculate estimated dropoff time
    dropoff_time = pickup_datetime + timedelta(seconds=estimate["duration"])
    
    return {
        "booking_id": booking_id,
        "provider": provider,
        "status": "confirmed",
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,
        "ride_type": estimate["ride_type"],
        "estimated_price": estimate["estimate"],
        "currency": "AED",
        "pickup_time": pickup_datetime.strftime("%Y-%m-%d %H:%M"),
        "driver": driver,
        "driver_arrival_time": driver_arrival_time.strftime("%Y-%m-%d %H:%M"),
        "estimated_dropoff_time": dropoff_time.strftime("%Y-%m-%d %H:%M"),
        "cancellation_policy": "Free cancellation until driver arrival",
        "payment_method": "Credit Card",
        "created_at": datetime.now().isoformat()
    }

def get_simulated_transit_routes(origin: str, destination: str, departure_time: str = None) -> Dict[str, Any]:
    """Generate simulated transit route data for testing purposes."""
    # Dubai transit options for simulation
    transit_options = [
        {
            "type": "metro",
            "name": "Dubai Metro Red Line",
            "frequency": "Every 5 minutes",
            "operating_hours": "5:30 AM - 12:00 AM",
            "price": 5
        },
        {
            "type": "metro",
            "name": "Dubai Metro Green Line",
            "frequency": "Every 8 minutes",
            "operating_hours": "5:30 AM - 12:00 AM",
            "price": 5
        },
        {
            "type": "tram",
            "name": "Dubai Tram",
            "frequency": "Every 10 minutes",
            "operating_hours": "6:00 AM - 1:00 AM",
            "price": 3
        },
        {
            "type": "bus",
            "name": "Dubai Bus",
            "frequency": "Every 15-20 minutes",
            "operating_hours": "5:00 AM - 12:30 AM",
            "price": 2
        },
        {
            "type": "water_taxi",
            "name": "Dubai Water Taxi",
            "frequency": "Every 30 minutes",
            "operating_hours": "10:00 AM - 10:00 PM",
            "price": 15
        },
        {
            "type": "abra",
            "name": "Traditional Abra",
            "frequency": "Every 10 minutes",
            "operating_hours": "6:00 AM - 12:00 AM",
            "price": 1
        }
    ]
    
    # Parse departure time
    if departure_time:
        try:
            departure_datetime = datetime.strptime(departure_time, "%Y-%m-%d %H:%M")
        except ValueError:
            departure_datetime = datetime.now() + timedelta(minutes=15)
    else:
        departure_datetime = datetime.now() + timedelta(minutes=15)
    
    # Generate 2-3 route options
    num_routes = random.randint(2, 3)
    routes = []
    
    for i in range(num_routes):
        # Each route has 1-3 segments
        num_segments = random.randint(1, 3)
        segments = []
        total_duration = 0
        total_price = 0
        
        for j in range(num_segments):
            # Select a random transit option
            transit = random.choice(transit_options)
            
            # Generate segment duration (10-45 minutes)
            duration_minutes = random.randint(10, 45)
            total_duration += duration_minutes
            
            # Calculate departure and arrival times
            segment_departure = departure_datetime + timedelta(minutes=total_duration - duration_minutes)
            segment_arrival = segment_departure + timedelta(minutes=duration_minutes)
            
            # Add price
            total_price += transit["price"]
            
            # Generate segment details
            segment = {
                "type": transit["type"],
                "name": transit["name"],
                "departure_time": segment_departure.strftime("%H:%M"),
                "arrival_time": segment_arrival.strftime("%H:%M"),
                "duration_minutes": duration_minutes,
                "from": generate_station_name(origin) if j == 0 else generate_station_name(),
                "to": generate_station_name(destination) if j == num_segments - 1 else generate_station_name(),
                "price": transit["price"],
                "frequency": transit["frequency"],
                "instructions": f"Take the {transit['name']} from {generate_station_name(origin) if j == 0 else generate_station_name()} to {generate_station_name(destination) if j == num_segments - 1 else generate_station_name()}"
            }
            
            segments.append(segment)
        
        # Add some walking segments if there are multiple transit segments
        if num_segments > 1:
            walking_segments = []
            for j in range(num_segments - 1):
                # Generate walking duration (3-10 minutes)
                walk_duration = random.randint(3, 10)
                total_duration += walk_duration
                
                # Calculate departure and arrival times
                walk_departure = departure_datetime + timedelta(minutes=total_duration - walk_duration)
                walk_arrival = walk_departure + timedelta(minutes=walk_duration)
                
                # Generate walking segment
                walking_segment = {
                    "type": "walking",
                    "name": "Walking",
                    "departure_time": walk_departure.strftime("%H:%M"),
                    "arrival_time": walk_arrival.strftime("%H:%M"),
                    "duration_minutes": walk_duration,
                    "from": segments[j]["to"],
                    "to": segments[j+1]["from"],
                    "price": 0,
                    "instructions": f"Walk from {segments[j]['to']} to {segments[j+1]['from']}"
                }
                
                walking_segments.append(walking_segment)
            
            # Merge transit and walking segments
            all_segments = []
            for j in range(num_segments):
                all_segments.append(segments[j])
                if j < len(walking_segments):
                    all_segments.append(walking_segments[j])
            
            segments = all_segments
        
        # Calculate route summary
        route_departure = departure_datetime
        route_arrival = departure_datetime + timedelta(minutes=total_duration)
        
        route = {
            "id": f"ROUTE{i+1}",
            "departure_time": route_departure.strftime("%H:%M"),
            "arrival_time": route_arrival.strftime("%H:%M"),
            "duration_minutes": total_duration,
            "segments": segments,
            "total_price": total_price,
            "currency": "AED",
            "transfers": num_segments - 1,
            "walking_minutes": sum(s["duration_minutes"] for s in segments if s["type"] == "walking")
        }
        
        routes.append(route)
    
    # Sort routes by duration
    routes.sort(key=lambda x: x["duration_minutes"])
    
    return {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_datetime.strftime("%Y-%m-%d"),
        "departure_time": departure_datetime.strftime("%H:%M"),
        "routes": routes
    }

def generate_station_name(location_hint: str = None) -> str:
    """Generate a realistic station name, optionally incorporating a location hint."""
    dubai_areas = [
        "Downtown", "Marina", "JBR", "Palm Jumeirah", "Deira", "Bur Dubai", 
        "Al Barsha", "Business Bay", "DIFC", "Al Quoz", "Jumeirah", "Al Karama"
    ]
    
    station_types = [
        "Metro Station", "Bus Stop", "Tram Station", "Water Taxi Station", "Abra Station"
    ]
    
    if location_hint:
        # Try to incorporate the location hint
        for area in dubai_areas:
            if area.lower() in location_hint.lower():
                return f"{area} {random.choice(station_types)}"
        
        # If no area match, just use the hint
        return f"{location_hint} {random.choice(station_types)}"
    else:
        # Generate a random station name
        return f"{random.choice(dubai_areas)} {random.choice(station_types)}"

# Register tools with the registry
tool_registry.register_tool(
    tool_name="get_ride_estimate",
    tool_function=get_ride_estimate,
    category="transportation",
    description="Get a ride estimate for a trip",
    required_params=["pickup_location", "dropoff_location"],
    optional_params=["ride_type", "provider"]
)

tool_registry.register_tool(
    tool_name="book_ride",
    tool_function=book_ride,
    category="transportation",
    description="Book a ride",
    required_params=["pickup_location", "dropoff_location", "ride_type", "pickup_time"],
    optional_params=["provider"]
)

tool_registry.register_tool(
    tool_name="get_transit_routes",
    tool_function=get_transit_routes,
    category="transportation",
    description="Get public transit routes between two locations",
    required_params=["origin", "destination"],
    optional_params=["departure_time"]
)
