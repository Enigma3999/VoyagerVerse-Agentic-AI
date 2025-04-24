import requests
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("booking_tools")

# API keys would normally be stored in environment variables
BOOKING_API_KEY = os.getenv("BOOKING_API_KEY", "your_booking_api_key")
VIATOR_API_KEY = os.getenv("VIATOR_API_KEY", "your_viator_api_key")

def search_hotels(location: str, check_in: str, check_out: str, 
                guests: int = 2, rooms: int = 1, provider: str = "booking") -> Dict[str, Any]:
    """Search for hotels in a location."""
    if provider.lower() == "booking":
        return search_hotels_booking(location, check_in, check_out, guests, rooms)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def search_hotels_booking(location: str, check_in: str, check_out: str, 
                         guests: int = 2, rooms: int = 1) -> Dict[str, Any]:
    """Search for hotels using Booking.com API."""
    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
    
    # Format dates if needed
    try:
        # Check if dates are in YYYY-MM-DD format and convert if needed
        datetime.strptime(check_in, "%Y-%m-%d")
        datetime.strptime(check_out, "%Y-%m-%d")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date format. Use YYYY-MM-DD",
            "data": get_simulated_hotels(location, check_in, check_out, guests, rooms)
        }
    
    headers = {
        "X-RapidAPI-Key": BOOKING_API_KEY,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }
    
    params = {
        "dest_id": "-782831",  # Dubai's destination ID in Booking.com
        "order_by": "popularity",
        "filter_by_currency": "AED",
        "adults_number": guests,
        "room_number": rooms,
        "checkout_date": check_out,
        "checkin_date": check_in,
        "units": "metric",
        "dest_type": "city",
        "locale": "en-gb"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        hotels_data = {
            "provider": "Booking.com",
            "location": location,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "rooms": rooms,
            "hotels": []
        }
        
        for hotel in data.get("result", []):
            hotels_data["hotels"].append({
                "id": hotel.get("hotel_id"),
                "name": hotel.get("hotel_name"),
                "address": hotel.get("address", ""),
                "city": hotel.get("city", ""),
                "latitude": hotel.get("latitude"),
                "longitude": hotel.get("longitude"),
                "review_score": hotel.get("review_score"),
                "price": {
                    "currency": hotel.get("price_breakdown", {}).get("currency", "AED"),
                    "value": hotel.get("price_breakdown", {}).get("gross_price", 0)
                },
                "is_free_cancellable": hotel.get("is_free_cancellable", False),
                "main_photo_url": hotel.get("main_photo_url", ""),
                "url": hotel.get("url", "")
            })
        
        return {
            "status": "success",
            "data": hotels_data
        }
    
    except Exception as e:
        logger.error(f"Error searching hotels with Booking.com: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_hotels(location, check_in, check_out, guests, rooms)
        }

def search_activities(location: str, date: str, category: str = None, 
                     provider: str = "viator") -> Dict[str, Any]:
    """Search for activities in a location."""
    if provider.lower() == "viator":
        return search_activities_viator(location, date, category)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def search_activities_viator(location: str, date: str, category: str = None) -> Dict[str, Any]:
    """Search for activities using Viator API."""
    url = "https://viator.p.rapidapi.com/search"
    
    headers = {
        "X-RapidAPI-Key": VIATOR_API_KEY,
        "X-RapidAPI-Host": "viator.p.rapidapi.com"
    }
    
    # Map common categories to Viator categories
    category_map = {
        "adventure": "adventure",
        "culture": "culture",
        "food": "food-and-drink",
        "nature": "outdoor-activities",
        "sightseeing": "sightseeing",
        "water": "water-activities",
        "desert": "desert-safari"
    }
    
    mapped_category = category_map.get(category.lower(), "") if category else ""
    
    params = {
        "destination": location,
        "start": date,
        "end": date
    }
    
    if mapped_category:
        params["category"] = mapped_category
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        activities_data = {
            "provider": "Viator",
            "location": location,
            "date": date,
            "category": category,
            "activities": []
        }
        
        for activity in data.get("data", {}).get("products", []):
            activities_data["activities"].append({
                "id": activity.get("productCode"),
                "name": activity.get("title"),
                "description": activity.get("description"),
                "duration": activity.get("duration"),
                "price": {
                    "currency": activity.get("price", {}).get("currencyCode", "AED"),
                    "value": activity.get("price", {}).get("amount", 0)
                },
                "rating": activity.get("rating"),
                "review_count": activity.get("reviewCount"),
                "image_url": activity.get("imageUrl"),
                "booking_url": activity.get("webURL")
            })
        
        return {
            "status": "success",
            "data": activities_data
        }
    
    except Exception as e:
        logger.error(f"Error searching activities with Viator: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_activities(location, date, category)
        }

def book_hotel(hotel_id: str, check_in: str, check_out: str, 
              guests: int, rooms: int, guest_info: Dict[str, Any],
              payment_info: Dict[str, Any], provider: str = "booking") -> Dict[str, Any]:
    """Book a hotel room."""
    # In a real implementation, this would connect to the booking API
    # For the prototype, we'll simulate a booking
    
    try:
        # Validate dates
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        
        if check_in_date >= check_out_date:
            return {
                "status": "error",
                "message": "Check-out date must be after check-in date"
            }
        
        # Validate guest info
        required_fields = ["first_name", "last_name", "email"]
        for field in required_fields:
            if field not in guest_info:
                return {
                    "status": "error",
                    "message": f"Missing required guest information: {field}"
                }
        
        # In a real implementation, we would validate payment info
        # and make the actual booking API call
        
        # Generate a booking reference
        import random
        import string
        booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        booking_data = {
            "provider": provider,
            "booking_reference": booking_ref,
            "status": "confirmed",
            "hotel_id": hotel_id,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "rooms": rooms,
            "guest_name": f"{guest_info['first_name']} {guest_info['last_name']}",
            "booking_date": datetime.now().strftime("%Y-%m-%d"),
            "cancellation_policy": "Free cancellation until 24 hours before check-in"
        }
        
        return {
            "status": "success",
            "data": booking_data
        }
    
    except Exception as e:
        logger.error(f"Error booking hotel: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def book_activity(activity_id: str, date: str, time_slot: str, 
                 participants: int, guest_info: Dict[str, Any],
                 payment_info: Dict[str, Any], provider: str = "viator") -> Dict[str, Any]:
    """Book an activity."""
    # In a real implementation, this would connect to the activity booking API
    # For the prototype, we'll simulate a booking
    
    try:
        # Validate date
        activity_date = datetime.strptime(date, "%Y-%m-%d")
        
        if activity_date < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            return {
                "status": "error",
                "message": "Activity date must be in the future"
            }
        
        # Validate guest info
        required_fields = ["first_name", "last_name", "email"]
        for field in required_fields:
            if field not in guest_info:
                return {
                    "status": "error",
                    "message": f"Missing required guest information: {field}"
                }
        
        # In a real implementation, we would validate payment info
        # and make the actual booking API call
        
        # Generate a booking reference
        import random
        import string
        booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        booking_data = {
            "provider": provider,
            "booking_reference": booking_ref,
            "status": "confirmed",
            "activity_id": activity_id,
            "date": date,
            "time_slot": time_slot,
            "participants": participants,
            "guest_name": f"{guest_info['first_name']} {guest_info['last_name']}",
            "booking_date": datetime.now().strftime("%Y-%m-%d"),
            "cancellation_policy": "Free cancellation until 24 hours before activity"
        }
        
        return {
            "status": "success",
            "data": booking_data
        }
    
    except Exception as e:
        logger.error(f"Error booking activity: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def cancel_booking(booking_reference: str, booking_type: str) -> Dict[str, Any]:
    """Cancel a hotel or activity booking."""
    # In a real implementation, this would connect to the booking API
    # For the prototype, we'll simulate a cancellation
    
    try:
        # Generate a cancellation reference
        import random
        import string
        cancellation_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        cancellation_data = {
            "booking_reference": booking_reference,
            "cancellation_reference": cancellation_ref,
            "booking_type": booking_type,
            "status": "cancelled",
            "cancellation_date": datetime.now().strftime("%Y-%m-%d"),
            "refund_status": "processed",
            "refund_amount": "100%"  # In a real implementation, this would depend on the cancellation policy
        }
        
        return {
            "status": "success",
            "data": cancellation_data
        }
    
    except Exception as e:
        logger.error(f"Error cancelling booking: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def get_simulated_hotels(location: str, check_in: str, check_out: str, 
                        guests: int = 2, rooms: int = 1) -> Dict[str, Any]:
    """Generate simulated hotel data for testing purposes."""
    # Dubai luxury hotels for simulation
    dubai_hotels = [
        {
            "id": "BH123456",
            "name": "Burj Al Arab Jumeirah",
            "address": "Jumeirah Beach Road",
            "city": "Dubai",
            "latitude": 25.1412,
            "longitude": 55.1853,
            "review_score": 9.4,
            "price": {"currency": "AED", "value": 5000},
            "is_free_cancellable": True,
            "main_photo_url": "https://example.com/burj-al-arab.jpg",
            "url": "https://example.com/hotels/burj-al-arab"
        },
        {
            "id": "BH789012",
            "name": "Atlantis, The Palm",
            "address": "Crescent Road, The Palm",
            "city": "Dubai",
            "latitude": 25.1304,
            "longitude": 55.1171,
            "review_score": 9.1,
            "price": {"currency": "AED", "value": 2500},
            "is_free_cancellable": True,
            "main_photo_url": "https://example.com/atlantis.jpg",
            "url": "https://example.com/hotels/atlantis"
        },
        {
            "id": "BH345678",
            "name": "Armani Hotel Dubai",
            "address": "Burj Khalifa, Downtown Dubai",
            "city": "Dubai",
            "latitude": 25.1972,
            "longitude": 55.2744,
            "review_score": 9.2,
            "price": {"currency": "AED", "value": 3000},
            "is_free_cancellable": True,
            "main_photo_url": "https://example.com/armani.jpg",
            "url": "https://example.com/hotels/armani"
        },
        {
            "id": "BH901234",
            "name": "Four Seasons Resort Dubai",
            "address": "Jumeirah Beach Road",
            "city": "Dubai",
            "latitude": 25.2048,
            "longitude": 55.2708,
            "review_score": 9.3,
            "price": {"currency": "AED", "value": 2800},
            "is_free_cancellable": True,
            "main_photo_url": "https://example.com/four-seasons.jpg",
            "url": "https://example.com/hotels/four-seasons"
        },
        {
            "id": "BH567890",
            "name": "Jumeirah Emirates Towers",
            "address": "Sheikh Zayed Road",
            "city": "Dubai",
            "latitude": 25.2184,
            "longitude": 55.2826,
            "review_score": 8.9,
            "price": {"currency": "AED", "value": 1800},
            "is_free_cancellable": True,
            "main_photo_url": "https://example.com/emirates-towers.jpg",
            "url": "https://example.com/hotels/emirates-towers"
        }
    ]
    
    return {
        "provider": "Simulated",
        "location": location,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "rooms": rooms,
        "hotels": dubai_hotels
    }

def get_simulated_activities(location: str, date: str, category: str = None) -> Dict[str, Any]:
    """Generate simulated activity data for testing purposes."""
    # Base activities
    activities = [
        {
            "id": "ACT12345",
            "name": "Desert Safari with BBQ Dinner",
            "description": "Experience the thrill of dune bashing followed by a traditional desert camp experience with BBQ dinner",
            "duration": "6 hours",
            "price": {"currency": "AED", "value": 350},
            "rating": 4.7,
            "review_count": 1250,
            "image_url": "https://example.com/desert-safari.jpg",
            "booking_url": "https://example.com/activities/desert-safari",
            "category": "adventure",
            "is_outdoor": True,
            "time_slots": ["07:00-13:00", "14:00-20:00"]
        },
        {
            "id": "ACT67890",
            "name": "Burj Khalifa: At the Top Observation Deck",
            "description": "Visit the world's tallest building and enjoy panoramic views of Dubai from the observation deck",
            "duration": "1.5 hours",
            "price": {"currency": "AED", "value": 250},
            "rating": 4.8,
            "review_count": 3000,
            "image_url": "https://example.com/burj-khalifa.jpg",
            "booking_url": "https://example.com/activities/burj-khalifa",
            "category": "sightseeing",
            "is_outdoor": False,
            "time_slots": ["09:00-10:30", "11:00-12:30", "13:00-14:30", "15:00-16:30", "17:00-18:30", "19:00-20:30"]
        },
        {
            "id": "ACT13579",
            "name": "Dubai Museum Cultural Tour",
            "description": "Explore Dubai's rich cultural heritage in the air-conditioned Dubai Museum",
            "duration": "2 hours",
            "price": {"currency": "AED", "value": 120},
            "rating": 4.5,
            "review_count": 850,
            "image_url": "https://example.com/dubai-museum.jpg",
            "booking_url": "https://example.com/activities/dubai-museum",
            "category": "culture",
            "is_outdoor": False,
            "time_slots": ["10:00-12:00", "13:00-15:00", "16:00-18:00"]
        },
        {
            "id": "ACT24680",
            "name": "Dubai Marina Yacht Tour",
            "description": "Cruise around Dubai Marina and Palm Jumeirah on a luxury yacht",
            "duration": "2 hours",
            "price": {"currency": "AED", "value": 400},
            "rating": 4.6,
            "review_count": 750,
            "image_url": "https://example.com/yacht-tour.jpg",
            "booking_url": "https://example.com/activities/yacht-tour",
            "category": "water",
            "is_outdoor": True,
            "time_slots": ["10:00-12:00", "13:00-15:00", "16:00-18:00", "19:00-21:00"]
        },
        {
            "id": "ACT97531",
            "name": "Old Dubai Food Tour",
            "description": "Taste authentic Emirati cuisine and learn about Dubai's culinary traditions",
            "duration": "3 hours",
            "price": {"currency": "AED", "value": 300},
            "rating": 4.9,
            "review_count": 500,
            "image_url": "https://example.com/food-tour.jpg",
            "booking_url": "https://example.com/activities/food-tour",
            "category": "food",
            "is_outdoor": True,
            "time_slots": ["11:00-14:00", "17:00-20:00"]
        }
    ]
    
    # Filter by category if provided
    if category:
        filtered_activities = [a for a in activities if a.get("category", "").lower() == category.lower()]
    else:
        filtered_activities = activities
    
    return {
        "provider": "Simulated",
        "location": location,
        "date": date,
        "category": category,
        "activities": filtered_activities
    }

# Register tools with the registry
tool_registry.register_tool(
    tool_name="search_hotels",
    tool_function=search_hotels,
    category="accommodation",
    description="Search for hotels in a location",
    required_params=["location", "check_in", "check_out"],
    optional_params=["guests", "rooms", "provider"]
)

tool_registry.register_tool(
    tool_name="search_activities",
    tool_function=search_activities,
    category="attractions",
    description="Search for activities in a location",
    required_params=["location", "date"],
    optional_params=["category", "provider"]
)

tool_registry.register_tool(
    tool_name="book_hotel",
    tool_function=book_hotel,
    category="accommodation",
    description="Book a hotel room",
    required_params=["hotel_id", "check_in", "check_out", "guests", "rooms", "guest_info", "payment_info"],
    optional_params=["provider"]
)

tool_registry.register_tool(
    tool_name="book_activity",
    tool_function=book_activity,
    category="attractions",
    description="Book an activity",
    required_params=["activity_id", "date", "time_slot", "participants", "guest_info", "payment_info"],
    optional_params=["provider"]
)

tool_registry.register_tool(
    tool_name="cancel_booking",
    tool_function=cancel_booking,
    category="accommodation",
    description="Cancel a hotel or activity booking",
    required_params=["booking_reference", "booking_type"]
)
