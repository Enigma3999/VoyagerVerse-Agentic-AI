import requests
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dining_tools")

# API keys would normally be stored in environment variables
ZOMATO_API_KEY = os.getenv("ZOMATO_API_KEY", "your_zomato_api_key")
OPENTABLE_API_KEY = os.getenv("OPENTABLE_API_KEY", "your_opentable_api_key")

def search_restaurants(location: str, cuisine: str = None, price_range: str = None, provider: str = "zomato") -> Dict[str, Any]:
    """Search for restaurants in a location."""
    if provider.lower() == "zomato":
        return search_restaurants_zomato(location, cuisine, price_range)
    elif provider.lower() == "opentable":
        return search_restaurants_opentable(location, cuisine, price_range)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def search_restaurants_zomato(location: str, cuisine: str = None, price_range: str = None) -> Dict[str, Any]:
    """Search for restaurants using Zomato API."""
    url = "https://developers.zomato.com/api/v2.1/search"
    
    headers = {
        "user-key": ZOMATO_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "q": location,
        "entity_type": "city",
        "count": 20
    }
    
    # Add cuisine filter if provided
    if cuisine:
        params["cuisines"] = get_cuisine_id(cuisine)
    
    # Add price range filter if provided
    if price_range:
        params["sort"] = "cost"
        params["order"] = "asc" if price_range.lower() == "low" else "desc"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        restaurants_data = {
            "provider": "Zomato",
            "location": location,
            "cuisine": cuisine,
            "price_range": price_range,
            "restaurants": []
        }
        
        for restaurant in data.get("restaurants", []):
            restaurant_info = restaurant.get("restaurant", {})
            restaurants_data["restaurants"].append({
                "id": restaurant_info.get("id"),
                "name": restaurant_info.get("name"),
                "cuisine": restaurant_info.get("cuisines"),
                "rating": restaurant_info.get("user_rating", {}).get("aggregate_rating"),
                "review_count": restaurant_info.get("all_reviews_count"),
                "price_range": "$" * int(restaurant_info.get("price_range", 1)),
                "average_cost_for_two": restaurant_info.get("average_cost_for_two"),
                "currency": restaurant_info.get("currency"),
                "address": restaurant_info.get("location", {}).get("address"),
                "latitude": restaurant_info.get("location", {}).get("latitude"),
                "longitude": restaurant_info.get("location", {}).get("longitude"),
                "image_url": restaurant_info.get("featured_image"),
                "menu_url": restaurant_info.get("menu_url"),
                "has_online_delivery": restaurant_info.get("has_online_delivery") == 1,
                "is_delivering_now": restaurant_info.get("is_delivering_now") == 1,
                "has_table_booking": restaurant_info.get("has_table_booking") == 1
            })
        
        return {
            "status": "success",
            "data": restaurants_data
        }
    
    except Exception as e:
        logger.error(f"Error searching restaurants with Zomato: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_restaurants(location, cuisine, price_range)
        }

def search_restaurants_opentable(location: str, cuisine: str = None, price_range: str = None) -> Dict[str, Any]:
    """Search for restaurants using OpenTable API."""
    # In a real implementation, this would connect to OpenTable's API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_restaurants(location, cuisine, price_range)
    }

def get_cuisine_id(cuisine_name: str) -> str:
    """Get the Zomato cuisine ID for a given cuisine name."""
    # This would normally query the Zomato API to get the cuisine ID
    # For simplicity, we'll use a hardcoded mapping of common cuisines
    cuisine_map = {
        "arabic": "4",
        "middle eastern": "4",
        "indian": "148",
        "italian": "55",
        "chinese": "25",
        "japanese": "60",
        "thai": "95",
        "american": "1",
        "mediterranean": "70",
        "seafood": "83",
        "steakhouse": "168",
        "lebanese": "66"
    }
    
    return cuisine_map.get(cuisine_name.lower(), "")

def get_restaurant_details(restaurant_id: str, provider: str = "zomato") -> Dict[str, Any]:
    """Get detailed information about a restaurant."""
    if provider.lower() == "zomato":
        return get_restaurant_details_zomato(restaurant_id)
    elif provider.lower() == "opentable":
        return get_restaurant_details_opentable(restaurant_id)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def get_restaurant_details_zomato(restaurant_id: str) -> Dict[str, Any]:
    """Get detailed information about a restaurant using Zomato API."""
    url = f"https://developers.zomato.com/api/v2.1/restaurant"
    
    headers = {
        "user-key": ZOMATO_API_KEY,
        "Accept": "application/json"
    }
    
    params = {
        "res_id": restaurant_id
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract opening hours
        opening_hours = []
        for day, hours in data.get("timings", "").split(","):
            opening_hours.append(f"{day.strip()}: {hours.strip()}")
        
        # Extract contact info
        contact_info = {
            "phone": data.get("phone_numbers", ""),
            "email": "",  # Zomato API doesn't provide email
            "website": data.get("url", "")
        }
        
        # Extract reviews
        reviews = []
        for review in data.get("all_reviews", {}).get("reviews", []):
            review_data = review.get("review", {})
            reviews.append({
                "rating": review_data.get("rating"),
                "text": review_data.get("review_text"),
                "date": review_data.get("timestamp"),
                "username": review_data.get("user", {}).get("name")
            })
        
        restaurant_data = {
            "provider": "Zomato",
            "id": restaurant_id,
            "name": data.get("name"),
            "cuisine": data.get("cuisines"),
            "rating": data.get("user_rating", {}).get("aggregate_rating"),
            "review_count": data.get("all_reviews_count"),
            "price_range": "$" * int(data.get("price_range", 1)),
            "average_cost_for_two": data.get("average_cost_for_two"),
            "currency": data.get("currency"),
            "address": data.get("location", {}).get("address"),
            "latitude": data.get("location", {}).get("latitude"),
            "longitude": data.get("location", {}).get("longitude"),
            "image_url": data.get("featured_image"),
            "menu_url": data.get("menu_url"),
            "photos_url": data.get("photos_url"),
            "opening_hours": opening_hours,
            "contact_info": contact_info,
            "reviews": reviews,
            "has_online_delivery": data.get("has_online_delivery") == 1,
            "is_delivering_now": data.get("is_delivering_now") == 1,
            "has_table_booking": data.get("has_table_booking") == 1
        }
        
        return {
            "status": "success",
            "data": restaurant_data
        }
    
    except Exception as e:
        logger.error(f"Error getting restaurant details with Zomato: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_restaurant_details(restaurant_id)
        }

def get_restaurant_details_opentable(restaurant_id: str) -> Dict[str, Any]:
    """Get detailed information about a restaurant using OpenTable API."""
    # In a real implementation, this would connect to OpenTable's API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_restaurant_details(restaurant_id)
    }

def check_restaurant_availability(restaurant_id: str, date: str, time: str, party_size: int, provider: str = "opentable") -> Dict[str, Any]:
    """Check if a restaurant has availability for a reservation."""
    if provider.lower() == "opentable":
        return check_restaurant_availability_opentable(restaurant_id, date, time, party_size)
    elif provider.lower() == "zomato":
        return check_restaurant_availability_zomato(restaurant_id, date, time, party_size)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def check_restaurant_availability_opentable(restaurant_id: str, date: str, time: str, party_size: int) -> Dict[str, Any]:
    """Check if a restaurant has availability using OpenTable API."""
    # In a real implementation, this would connect to OpenTable's API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_availability(restaurant_id, date, time, party_size)
    }

def check_restaurant_availability_zomato(restaurant_id: str, date: str, time: str, party_size: int) -> Dict[str, Any]:
    """Check if a restaurant has availability using Zomato API."""
    # Zomato doesn't provide availability checking
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_availability(restaurant_id, date, time, party_size)
    }

def make_restaurant_reservation(restaurant_id: str, date: str, time: str, party_size: int, name: str, email: str, phone: str, provider: str = "opentable") -> Dict[str, Any]:
    """Make a restaurant reservation."""
    if provider.lower() == "opentable":
        return make_restaurant_reservation_opentable(restaurant_id, date, time, party_size, name, email, phone)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def make_restaurant_reservation_opentable(restaurant_id: str, date: str, time: str, party_size: int, name: str, email: str, phone: str) -> Dict[str, Any]:
    """Make a restaurant reservation using OpenTable API."""
    # In a real implementation, this would connect to OpenTable's API
    # For the prototype, we'll use simulated data
    
    # Check availability first
    availability = check_restaurant_availability_opentable(restaurant_id, date, time, party_size)
    
    if availability["data"]["available"]:
        # Generate a reservation ID
        reservation_id = f"RES{random.randint(100000, 999999)}"
        
        return {
            "status": "success",
            "data": {
                "provider": "OpenTable",
                "reservation_id": reservation_id,
                "restaurant_id": restaurant_id,
                "restaurant_name": availability["data"]["restaurant_name"],
                "date": date,
                "time": time,
                "party_size": party_size,
                "name": name,
                "email": email,
                "phone": phone,
                "confirmation_code": f"OT{random.randint(1000000, 9999999)}",
                "status": "confirmed",
                "created_at": datetime.now().isoformat()
            }
        }
    else:
        return {
            "status": "error",
            "message": "No availability for the requested time",
            "data": availability["data"]
        }

def get_simulated_restaurants(location: str, cuisine: str = None, price_range: str = None) -> Dict[str, Any]:
    """Generate simulated restaurant data for testing purposes."""
    # Dubai restaurants for simulation
    dubai_restaurants = [
        {
            "id": "RES123456",
            "name": "Al Mahara",
            "cuisine": "Seafood, Mediterranean",
            "rating": 4.8,
            "review_count": 500,
            "price_range": "$$$$",
            "average_cost_for_two": 2000,
            "currency": "AED",
            "address": "Burj Al Arab, Jumeirah Beach Road, Dubai",
            "latitude": 25.141254,
            "longitude": 55.185869,
            "image_url": "https://example.com/al-mahara.jpg",
            "menu_url": "https://example.com/al-mahara-menu",
            "has_online_delivery": False,
            "is_delivering_now": False,
            "has_table_booking": True
        },
        {
            "id": "RES789012",
            "name": "Pierchic",
            "cuisine": "Seafood, Italian",
            "rating": 4.7,
            "review_count": 450,
            "price_range": "$$$$",
            "average_cost_for_two": 1800,
            "currency": "AED",
            "address": "Jumeirah Al Qasr, Madinat Jumeirah, Dubai",
            "latitude": 25.132876,
            "longitude": 55.184764,
            "image_url": "https://example.com/pierchic.jpg",
            "menu_url": "https://example.com/pierchic-menu",
            "has_online_delivery": False,
            "is_delivering_now": False,
            "has_table_booking": True
        },
        {
            "id": "RES345678",
            "name": "Arabian Tea House",
            "cuisine": "Middle Eastern, Arabic",
            "rating": 4.6,
            "review_count": 350,
            "price_range": "$$",
            "average_cost_for_two": 300,
            "currency": "AED",
            "address": "Al Fahidi Street, Bur Dubai",
            "latitude": 25.263395,
            "longitude": 55.297371,
            "image_url": "https://example.com/arabian-tea-house.jpg",
            "menu_url": "https://example.com/arabian-tea-house-menu",
            "has_online_delivery": True,
            "is_delivering_now": True,
            "has_table_booking": True
        },
        {
            "id": "RES901234",
            "name": "Ravi Restaurant",
            "cuisine": "Indian, Pakistani",
            "rating": 4.5,
            "review_count": 1000,
            "price_range": "$",
            "average_cost_for_two": 100,
            "currency": "AED",
            "address": "Satwa Road, Al Satwa, Dubai",
            "latitude": 25.240532,
            "longitude": 55.266487,
            "image_url": "https://example.com/ravi-restaurant.jpg",
            "menu_url": "https://example.com/ravi-restaurant-menu",
            "has_online_delivery": True,
            "is_delivering_now": True,
            "has_table_booking": False
        },
        {
            "id": "RES567890",
            "name": "Zuma",
            "cuisine": "Japanese, Asian",
            "rating": 4.9,
            "review_count": 800,
            "price_range": "$$$$",
            "average_cost_for_two": 1500,
            "currency": "AED",
            "address": "Gate Village 06, DIFC, Dubai",
            "latitude": 25.215815,
            "longitude": 55.280647,
            "image_url": "https://example.com/zuma.jpg",
            "menu_url": "https://example.com/zuma-menu",
            "has_online_delivery": False,
            "is_delivering_now": False,
            "has_table_booking": True
        }
    ]
    
    # Filter by cuisine if provided
    if cuisine:
        filtered_restaurants = [r for r in dubai_restaurants if cuisine.lower() in r["cuisine"].lower()]
    else:
        filtered_restaurants = dubai_restaurants
    
    # Filter by price range if provided
    if price_range:
        if price_range.lower() == "low":
            filtered_restaurants = [r for r in filtered_restaurants if len(r["price_range"]) <= 2]
        elif price_range.lower() == "medium":
            filtered_restaurants = [r for r in filtered_restaurants if len(r["price_range"]) == 3]
        elif price_range.lower() == "high":
            filtered_restaurants = [r for r in filtered_restaurants if len(r["price_range"]) >= 4]
    
    return {
        "provider": "Simulated",
        "location": location,
        "cuisine": cuisine,
        "price_range": price_range,
        "restaurants": filtered_restaurants
    }

def get_simulated_restaurant_details(restaurant_id: str) -> Dict[str, Any]:
    """Generate simulated detailed restaurant data for testing purposes."""
    # Find the restaurant in our simulated data
    restaurants = get_simulated_restaurants("Dubai")["restaurants"]
    restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
    
    if not restaurant:
        # Default to first restaurant if not found
        restaurant = restaurants[0]
    
    # Add additional details
    opening_hours = [
        "Monday: 12:00 PM - 11:00 PM",
        "Tuesday: 12:00 PM - 11:00 PM",
        "Wednesday: 12:00 PM - 11:00 PM",
        "Thursday: 12:00 PM - 11:00 PM",
        "Friday: 12:00 PM - 12:00 AM",
        "Saturday: 12:00 PM - 12:00 AM",
        "Sunday: 12:00 PM - 11:00 PM"
    ]
    
    contact_info = {
        "phone": "+971 4 123 4567",
        "email": "info@example.com",
        "website": "https://example.com/restaurant"
    }
    
    reviews = [
        {
            "rating": 5,
            "title": "Exceptional dining experience",
            "text": "The food was amazing and the service was impeccable.",
            "date": "2023-05-15",
            "username": "FoodLover123"
        },
        {
            "rating": 4,
            "title": "Great food, a bit pricey",
            "text": "The food was excellent but a bit on the expensive side.",
            "date": "2023-04-22",
            "username": "DubaiDiner456"
        },
        {
            "rating": 5,
            "title": "Best restaurant in Dubai",
            "text": "Absolutely stunning food and ambiance. A must-visit in Dubai.",
            "date": "2023-03-10",
            "username": "GourmetTraveler"
        }
    ]
    
    detailed_restaurant = restaurant.copy()
    detailed_restaurant.update({
        "opening_hours": opening_hours,
        "contact_info": contact_info,
        "reviews": reviews,
        "facilities": ["Parking", "Outdoor Seating", "Private Dining", "Wheelchair Accessible"],
        "payment_methods": ["Cash", "Credit Card", "Debit Card"],
        "dress_code": "Smart Casual" if "$$$$" in restaurant["price_range"] else "Casual",
        "special_diets": ["Vegetarian Friendly", "Vegan Options", "Gluten Free Options"],
        "special_features": ["Romantic", "View", "Business meetings"] if "$$$$" in restaurant["price_range"] else ["Family friendly", "Casual dining"]
    })
    
    return detailed_restaurant

def get_simulated_availability(restaurant_id: str, date: str, time: str, party_size: int) -> Dict[str, Any]:
    """Generate simulated availability data for testing purposes."""
    # Find the restaurant in our simulated data
    restaurants = get_simulated_restaurants("Dubai")["restaurants"]
    restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
    
    if not restaurant:
        # Default to first restaurant if not found
        restaurant = restaurants[0]
    
    # Parse the requested date and time
    try:
        requested_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return {
            "available": False,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant["name"],
            "date": date,
            "time": time,
            "party_size": party_size,
            "error": "Invalid date or time format"
        }
    
    # Check if the restaurant has table booking
    if not restaurant.get("has_table_booking", False):
        return {
            "available": False,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant["name"],
            "date": date,
            "time": time,
            "party_size": party_size,
            "error": "Restaurant does not accept table bookings"
        }
    
    # Check if party size is too large
    if party_size > 10:
        return {
            "available": False,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant["name"],
            "date": date,
            "time": time,
            "party_size": party_size,
            "error": "Party size too large, please call the restaurant directly",
            "alternative_times": []
        }
    
    # Simulate availability - 80% chance of availability
    is_available = random.random() < 0.8
    
    if is_available:
        return {
            "available": True,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant["name"],
            "date": date,
            "time": time,
            "party_size": party_size
        }
    else:
        # Generate alternative times
        alternative_times = []
        for hour_offset in [-1, 1, 2]:
            alt_datetime = requested_datetime + timedelta(hours=hour_offset)
            alternative_times.append(alt_datetime.strftime("%H:%M"))
        
        return {
            "available": False,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant["name"],
            "date": date,
            "time": time,
            "party_size": party_size,
            "error": "No availability for the requested time",
            "alternative_times": alternative_times
        }

# Register tools with the registry
tool_registry.register_tool(
    tool_name="search_restaurants",
    tool_function=search_restaurants,
    category="dining",
    description="Search for restaurants in a location",
    required_params=["location"],
    optional_params=["cuisine", "price_range", "provider"]
)

tool_registry.register_tool(
    tool_name="get_restaurant_details",
    tool_function=get_restaurant_details,
    category="dining",
    description="Get detailed information about a restaurant",
    required_params=["restaurant_id"],
    optional_params=["provider"]
)

tool_registry.register_tool(
    tool_name="check_restaurant_availability",
    tool_function=check_restaurant_availability,
    category="dining",
    description="Check if a restaurant has availability for a reservation",
    required_params=["restaurant_id", "date", "time", "party_size"],
    optional_params=["provider"]
)

tool_registry.register_tool(
    tool_name="make_restaurant_reservation",
    tool_function=make_restaurant_reservation,
    category="dining",
    description="Make a restaurant reservation",
    required_params=["restaurant_id", "date", "time", "party_size", "name", "email", "phone"],
    optional_params=["provider"]
)
