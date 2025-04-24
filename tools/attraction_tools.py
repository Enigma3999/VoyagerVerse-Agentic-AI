import requests
import logging
import os
from typing import Dict, List, Any, Optional

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("attraction_tools")

# API keys would normally be stored in environment variables
TRIPADVISOR_API_KEY = os.getenv("TRIPADVISOR_API_KEY", "your_tripadvisor_api_key")
DUBAI_API_KEY = os.getenv("DUBAI_API_KEY", "your_dubai_api_key")

def search_attractions(location: str, category: str = None, provider: str = "tripadvisor") -> Dict[str, Any]:
    """Search for attractions in a location."""
    if provider.lower() == "tripadvisor":
        return search_attractions_tripadvisor(location, category)
    elif provider.lower() == "dubai":
        return search_attractions_dubai(location, category)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def search_attractions_tripadvisor(location: str, category: str = None) -> Dict[str, Any]:
    """Search for attractions using TripAdvisor API."""
    url = "https://tripadvisor1.p.rapidapi.com/attractions/list"
    
    headers = {
        "X-RapidAPI-Key": TRIPADVISOR_API_KEY,
        "X-RapidAPI-Host": "tripadvisor1.p.rapidapi.com"
    }
    
    params = {
        "location_id": "295424",  # Dubai's location ID in TripAdvisor
        "currency": "AED",
        "lang": "en_US",
        "lunit": "km",
        "limit": "30"
    }
    
    # Add category filter if provided
    if category:
        params["subcategory"] = category
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        attractions_data = {
            "provider": "TripAdvisor",
            "location": location,
            "category": category,
            "attractions": []
        }
        
        for attraction in data.get("data", []):
            if attraction.get("result_type") == "attractions":
                attractions_data["attractions"].append({
                    "id": attraction.get("location_id"),
                    "name": attraction.get("name"),
                    "description": attraction.get("description", ""),
                    "category": attraction.get("subcategory", [{}])[0].get("name", "") if attraction.get("subcategory") else "",
                    "rating": attraction.get("rating"),
                    "review_count": attraction.get("num_reviews"),
                    "price_level": attraction.get("price_level", ""),
                    "website": attraction.get("website", ""),
                    "address": attraction.get("address", ""),
                    "latitude": attraction.get("latitude"),
                    "longitude": attraction.get("longitude"),
                    "image_url": attraction.get("photo", {}).get("images", {}).get("original", {}).get("url", ""),
                    "is_outdoor": is_outdoor_attraction(attraction.get("subcategory", [{}])[0].get("name", "") if attraction.get("subcategory") else "")
                })
        
        return {
            "status": "success",
            "data": attractions_data
        }
    
    except Exception as e:
        logger.error(f"Error searching attractions with TripAdvisor: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_attractions(location, category)
        }

def search_attractions_dubai(location: str, category: str = None) -> Dict[str, Any]:
    """Search for attractions using Dubai API."""
    # In a real implementation, this would connect to Dubai's open data API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_attractions(location, category)
    }

def get_attraction_details(attraction_id: str, provider: str = "tripadvisor") -> Dict[str, Any]:
    """Get detailed information about an attraction."""
    if provider.lower() == "tripadvisor":
        return get_attraction_details_tripadvisor(attraction_id)
    elif provider.lower() == "dubai":
        return get_attraction_details_dubai(attraction_id)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def get_attraction_details_tripadvisor(attraction_id: str) -> Dict[str, Any]:
    """Get detailed information about an attraction using TripAdvisor API."""
    url = "https://tripadvisor1.p.rapidapi.com/attractions/get-details"
    
    headers = {
        "X-RapidAPI-Key": TRIPADVISOR_API_KEY,
        "X-RapidAPI-Host": "tripadvisor1.p.rapidapi.com"
    }
    
    params = {
        "location_id": attraction_id,
        "currency": "AED",
        "lang": "en_US"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract opening hours
        opening_hours = []
        for day, hours in data.get("hours", {}).get("weekday_text", {}).items():
            opening_hours.append(f"{day}: {hours}")
        
        # Extract contact info
        contact_info = {
            "phone": data.get("phone", ""),
            "email": data.get("email", ""),
            "website": data.get("website", "")
        }
        
        # Extract reviews
        reviews = []
        for review in data.get("reviews", []):
            reviews.append({
                "rating": review.get("rating"),
                "title": review.get("title"),
                "text": review.get("text"),
                "date": review.get("published_date"),
                "username": review.get("username")
            })
        
        attraction_data = {
            "provider": "TripAdvisor",
            "id": attraction_id,
            "name": data.get("name"),
            "description": data.get("description", ""),
            "category": data.get("subcategory", {}).get("name", ""),
            "rating": data.get("rating"),
            "review_count": data.get("num_reviews"),
            "price_level": data.get("price_level", ""),
            "price_range": data.get("price", ""),
            "address": data.get("address", ""),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "image_url": data.get("photo", {}).get("images", {}).get("original", {}).get("url", ""),
            "opening_hours": opening_hours,
            "contact_info": contact_info,
            "reviews": reviews,
            "is_outdoor": is_outdoor_attraction(data.get("subcategory", {}).get("name", ""))
        }
        
        return {
            "status": "success",
            "data": attraction_data
        }
    
    except Exception as e:
        logger.error(f"Error getting attraction details with TripAdvisor: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_attraction_details(attraction_id)
        }

def get_attraction_details_dubai(attraction_id: str) -> Dict[str, Any]:
    """Get detailed information about an attraction using Dubai API."""
    # In a real implementation, this would connect to Dubai's open data API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_attraction_details(attraction_id)
    }

def is_outdoor_attraction(category: str) -> bool:
    """Determine if an attraction is likely to be outdoors based on its category."""
    outdoor_categories = [
        "outdoor activities",
        "nature & parks",
        "beaches",
        "gardens",
        "desert",
        "water parks",
        "theme parks",
        "boat tours",
        "water sports",
        "golf courses"
    ]
    
    return any(outdoor_cat.lower() in category.lower() for outdoor_cat in outdoor_categories)

def get_simulated_attractions(location: str, category: str = None) -> Dict[str, Any]:
    """Generate simulated attraction data for testing purposes."""
    # Dubai attractions for simulation
    dubai_attractions = [
        {
            "id": "ATT123456",
            "name": "Burj Khalifa",
            "description": "The world's tallest building with observation decks offering panoramic views of Dubai",
            "category": "landmarks",
            "rating": 4.8,
            "review_count": 5000,
            "price_level": "$$$",
            "website": "https://www.burjkhalifa.ae",
            "address": "1 Sheikh Mohammed bin Rashid Blvd, Downtown Dubai",
            "latitude": 25.197197,
            "longitude": 55.274376,
            "image_url": "https://example.com/burj-khalifa.jpg",
            "is_outdoor": False
        },
        {
            "id": "ATT789012",
            "name": "Dubai Mall",
            "description": "One of the world's largest shopping malls with over 1,200 shops, an aquarium, and an ice rink",
            "category": "shopping",
            "rating": 4.7,
            "review_count": 4500,
            "price_level": "$$",
            "website": "https://www.thedubaimall.com",
            "address": "Financial Centre Road, Downtown Dubai",
            "latitude": 25.198765,
            "longitude": 55.279503,
            "image_url": "https://example.com/dubai-mall.jpg",
            "is_outdoor": False
        },
        {
            "id": "ATT345678",
            "name": "Palm Jumeirah",
            "description": "Artificial archipelago in the shape of a palm tree, home to luxury hotels and residences",
            "category": "landmarks",
            "rating": 4.6,
            "review_count": 3500,
            "price_level": "Free",
            "website": "https://www.palmjumeirah.ae",
            "address": "Palm Jumeirah, Dubai",
            "latitude": 25.112350,
            "longitude": 55.138379,
            "image_url": "https://example.com/palm-jumeirah.jpg",
            "is_outdoor": True
        },
        {
            "id": "ATT901234",
            "name": "Dubai Museum",
            "description": "Museum showcasing the history and cultural heritage of Dubai",
            "category": "museums",
            "rating": 4.5,
            "review_count": 2500,
            "price_level": "$",
            "website": "https://www.dubaimuseum.ae",
            "address": "Al Fahidi Fort, Al Fahidi Street, Bur Dubai",
            "latitude": 25.263395,
            "longitude": 55.297371,
            "image_url": "https://example.com/dubai-museum.jpg",
            "is_outdoor": False
        },
        {
            "id": "ATT567890",
            "name": "Dubai Desert Conservation Reserve",
            "description": "Protected desert habitat offering wildlife viewing and desert activities",
            "category": "nature & parks",
            "rating": 4.9,
            "review_count": 2000,
            "price_level": "$$$",
            "website": "https://www.ddcr.org",
            "address": "Al Marmoom Desert Conservation Reserve, Dubai",
            "latitude": 24.826313,
            "longitude": 55.277814,
            "image_url": "https://example.com/desert-reserve.jpg",
            "is_outdoor": True
        }
    ]
    
    # Filter by category if provided
    if category:
        filtered_attractions = [a for a in dubai_attractions if category.lower() in a["category"].lower()]
    else:
        filtered_attractions = dubai_attractions
    
    return {
        "provider": "Simulated",
        "location": location,
        "category": category,
        "attractions": filtered_attractions
    }

def get_simulated_attraction_details(attraction_id: str) -> Dict[str, Any]:
    """Generate simulated detailed attraction data for testing purposes."""
    # Find the attraction in our simulated data
    attractions = get_simulated_attractions("Dubai")["attractions"]
    attraction = next((a for a in attractions if a["id"] == attraction_id), None)
    
    if not attraction:
        # Default to Burj Khalifa if attraction not found
        attraction = attractions[0]
    
    # Add additional details
    opening_hours = [
        "Monday: 9:00 AM - 11:00 PM",
        "Tuesday: 9:00 AM - 11:00 PM",
        "Wednesday: 9:00 AM - 11:00 PM",
        "Thursday: 9:00 AM - 11:00 PM",
        "Friday: 9:00 AM - 11:00 PM",
        "Saturday: 9:00 AM - 11:00 PM",
        "Sunday: 9:00 AM - 11:00 PM"
    ]
    
    contact_info = {
        "phone": "+971 4 123 4567",
        "email": "info@example.com",
        "website": attraction["website"]
    }
    
    reviews = [
        {
            "rating": 5,
            "title": "Amazing experience!",
            "text": "One of the best attractions in Dubai. Highly recommended!",
            "date": "2023-05-15",
            "username": "TravelLover123"
        },
        {
            "rating": 4,
            "title": "Great place to visit",
            "text": "Really enjoyed our time here. The views are spectacular.",
            "date": "2023-04-22",
            "username": "Globetrotter456"
        },
        {
            "rating": 5,
            "title": "Must-see in Dubai",
            "text": "Absolutely stunning. A must-visit when in Dubai.",
            "date": "2023-03-10",
            "username": "DubaiExplorer"
        }
    ]
    
    detailed_attraction = attraction.copy()
    detailed_attraction.update({
        "opening_hours": opening_hours,
        "contact_info": contact_info,
        "reviews": reviews,
        "facilities": ["Restrooms", "Gift Shop", "Cafe", "Wheelchair Accessible"],
        "best_time_to_visit": "Early morning or late afternoon to avoid crowds",
        "tips": "Book tickets online in advance to avoid long queues",
        "nearby_attractions": [a["name"] for a in attractions if a["id"] != attraction_id][:3]
    })
    
    return detailed_attraction

# Register tools with the registry
tool_registry.register_tool(
    tool_name="search_attractions",
    tool_function=search_attractions,
    category="attractions",
    description="Search for attractions in a location",
    required_params=["location"],
    optional_params=["category", "provider"]
)

tool_registry.register_tool(
    tool_name="get_attraction_details",
    tool_function=get_attraction_details,
    category="attractions",
    description="Get detailed information about an attraction",
    required_params=["attraction_id"],
    optional_params=["provider"]
)
