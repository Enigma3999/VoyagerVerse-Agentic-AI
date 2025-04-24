import requests
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("events_tools")

# API keys would normally be stored in environment variables
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY", "your_eventbrite_api_key")
DUBAI_EVENTS_API_KEY = os.getenv("DUBAI_EVENTS_API_KEY", "your_dubai_events_api_key")

def search_events(location: str, category: str = None, start_date: str = None, end_date: str = None, provider: str = "eventbrite") -> Dict[str, Any]:
    """Search for events in a location."""
    if provider.lower() == "eventbrite":
        return search_events_eventbrite(location, category, start_date, end_date)
    elif provider.lower() == "dubai":
        return search_events_dubai(location, category, start_date, end_date)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def search_events_eventbrite(location: str, category: str = None, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """Search for events using Eventbrite API."""
    url = "https://www.eventbriteapi.com/v3/events/search/"
    
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}"
    }
    
    params = {
        "location.address": location,
        "location.within": "10km",
        "expand": "venue,category"
    }
    
    # Add category filter if provided
    if category:
        params["categories"] = get_eventbrite_category_id(category)
    
    # Add date filters if provided
    if start_date:
        params["start_date.range_start"] = f"{start_date}T00:00:00"
    
    if end_date:
        params["start_date.range_end"] = f"{end_date}T23:59:59"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        events_data = {
            "provider": "Eventbrite",
            "location": location,
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "events": []
        }
        
        for event in data.get("events", []):
            events_data["events"].append({
                "id": event.get("id"),
                "name": event.get("name", {}).get("text", ""),
                "description": event.get("description", {}).get("text", "")[:200] + "..." if event.get("description", {}).get("text", "") else "",
                "category": event.get("category", {}).get("name", "") if event.get("category") else "",
                "start_time": event.get("start", {}).get("local", ""),
                "end_time": event.get("end", {}).get("local", ""),
                "venue": {
                    "name": event.get("venue", {}).get("name", ""),
                    "address": event.get("venue", {}).get("address", {}).get("localized_address_display", ""),
                    "latitude": event.get("venue", {}).get("latitude"),
                    "longitude": event.get("venue", {}).get("longitude")
                },
                "url": event.get("url", ""),
                "is_free": event.get("is_free", False),
                "logo_url": event.get("logo", {}).get("url", "") if event.get("logo") else "",
                "capacity": event.get("capacity"),
                "status": event.get("status"),
                "is_indoor": is_indoor_event(event.get("category", {}).get("name", "") if event.get("category") else "", event.get("venue", {}).get("name", ""))
            })
        
        return {
            "status": "success",
            "data": events_data
        }
    
    except Exception as e:
        logger.error(f"Error searching events with Eventbrite: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_events(location, category, start_date, end_date)
        }

def search_events_dubai(location: str, category: str = None, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """Search for events using Dubai Events API."""
    # In a real implementation, this would connect to Dubai's events API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_events(location, category, start_date, end_date)
    }

def get_eventbrite_category_id(category_name: str) -> str:
    """Get the Eventbrite category ID for a given category name."""
    # This would normally query the Eventbrite API to get the category ID
    # For simplicity, we'll use a hardcoded mapping of common categories
    category_map = {
        "music": "103",
        "business": "101",
        "food": "110",
        "community": "113",
        "arts": "105",
        "film": "104",
        "sports": "108",
        "health": "107",
        "science": "102",
        "travel": "109",
        "charity": "111",
        "family": "115",
        "fashion": "106"
    }
    
    return category_map.get(category_name.lower(), "")

def get_event_details(event_id: str, provider: str = "eventbrite") -> Dict[str, Any]:
    """Get detailed information about an event."""
    if provider.lower() == "eventbrite":
        return get_event_details_eventbrite(event_id)
    elif provider.lower() == "dubai":
        return get_event_details_dubai(event_id)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def get_event_details_eventbrite(event_id: str) -> Dict[str, Any]:
    """Get detailed information about an event using Eventbrite API."""
    url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
    
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}"
    }
    
    params = {
        "expand": "venue,organizer,ticket_classes,category"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        event = response.json()
        
        # Get ticket information
        tickets = []
        for ticket_class in event.get("ticket_classes", []):
            tickets.append({
                "name": ticket_class.get("name"),
                "price": ticket_class.get("cost", {}).get("display") if ticket_class.get("cost") else "Free",
                "currency": ticket_class.get("cost", {}).get("currency") if ticket_class.get("cost") else "",
                "availability": ticket_class.get("quantity_total") - ticket_class.get("quantity_sold") if ticket_class.get("quantity_total") and ticket_class.get("quantity_sold") else "Unknown",
                "sales_start": ticket_class.get("sales_start"),
                "sales_end": ticket_class.get("sales_end")
            })
        
        event_data = {
            "provider": "Eventbrite",
            "id": event.get("id"),
            "name": event.get("name", {}).get("text", ""),
            "description": event.get("description", {}).get("html", ""),
            "category": event.get("category", {}).get("name", "") if event.get("category") else "",
            "subcategory": event.get("subcategory", {}).get("name", "") if event.get("subcategory") else "",
            "start_time": event.get("start", {}).get("local", ""),
            "end_time": event.get("end", {}).get("local", ""),
            "timezone": event.get("start", {}).get("timezone", ""),
            "venue": {
                "name": event.get("venue", {}).get("name", ""),
                "address": event.get("venue", {}).get("address", {}).get("localized_address_display", ""),
                "latitude": event.get("venue", {}).get("latitude"),
                "longitude": event.get("venue", {}).get("longitude")
            },
            "organizer": {
                "name": event.get("organizer", {}).get("name", ""),
                "description": event.get("organizer", {}).get("description", {}).get("text", ""),
                "url": event.get("organizer", {}).get("url", "")
            },
            "url": event.get("url", ""),
            "is_free": event.get("is_free", False),
            "logo_url": event.get("logo", {}).get("url", "") if event.get("logo") else "",
            "capacity": event.get("capacity"),
            "status": event.get("status"),
            "tickets": tickets,
            "is_indoor": is_indoor_event(event.get("category", {}).get("name", "") if event.get("category") else "", event.get("venue", {}).get("name", ""))
        }
        
        return {
            "status": "success",
            "data": event_data
        }
    
    except Exception as e:
        logger.error(f"Error getting event details with Eventbrite: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_event_details(event_id)
        }

def get_event_details_dubai(event_id: str) -> Dict[str, Any]:
    """Get detailed information about an event using Dubai Events API."""
    # In a real implementation, this would connect to Dubai's events API
    # For the prototype, we'll use simulated data
    return {
        "status": "success",
        "data": get_simulated_event_details(event_id)
    }

def is_indoor_event(category: str, venue_name: str) -> bool:
    """Determine if an event is likely to be indoors based on its category and venue."""
    outdoor_keywords = [
        "park", "beach", "garden", "outdoor", "festival", "field", "stadium",
        "desert", "marina", "waterfront", "race", "marathon", "run", "walk"
    ]
    
    indoor_categories = [
        "business", "conference", "seminar", "workshop", "networking",
        "film", "screening", "theatre", "theater", "concert", "exhibition",
        "museum", "gallery", "food", "dining", "tasting"
    ]
    
    # Check venue name for outdoor keywords
    if any(keyword in venue_name.lower() for keyword in outdoor_keywords):
        return False
    
    # Check category for indoor keywords
    if any(indoor_cat in category.lower() for indoor_cat in indoor_categories):
        return True
    
    # Default to indoor (safer assumption in Dubai due to heat)
    return True

def get_simulated_events(location: str, category: str = None, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """Generate simulated event data for testing purposes."""
    # Parse dates
    if start_date:
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            start_datetime = datetime.now()
    else:
        start_datetime = datetime.now()
    
    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            end_datetime = start_datetime + timedelta(days=30)
    else:
        end_datetime = start_datetime + timedelta(days=30)
    
    # Dubai events for simulation
    dubai_events = [
        {
            "id": "EVT123456",
            "name": "Dubai Shopping Festival",
            "description": "The Dubai Shopping Festival (DSF) is an annual event in Dubai featuring shopping discounts, product launches, entertainment, and various activities.",
            "category": "Shopping",
            "start_time": (start_datetime + timedelta(days=2)).strftime("%Y-%m-%dT10:00:00"),
            "end_time": (start_datetime + timedelta(days=32)).strftime("%Y-%m-%dT22:00:00"),
            "venue": {
                "name": "Various Malls across Dubai",
                "address": "Dubai, UAE",
                "latitude": 25.2048,
                "longitude": 55.2708
            },
            "url": "https://www.visitdubai.com/en/events/dubai-shopping-festival",
            "is_free": True,
            "logo_url": "https://example.com/dsf-logo.jpg",
            "capacity": None,
            "status": "live",
            "is_indoor": True
        },
        {
            "id": "EVT789012",
            "name": "Dubai Food Festival",
            "description": "The Dubai Food Festival is a citywide culinary celebration that showcases the emirate's emergence as a gastronomy destination.",
            "category": "Food & Drink",
            "start_time": (start_datetime + timedelta(days=5)).strftime("%Y-%m-%dT12:00:00"),
            "end_time": (start_datetime + timedelta(days=15)).strftime("%Y-%m-%dT23:00:00"),
            "venue": {
                "name": "Various Restaurants across Dubai",
                "address": "Dubai, UAE",
                "latitude": 25.2048,
                "longitude": 55.2708
            },
            "url": "https://www.visitdubai.com/en/events/dubai-food-festival",
            "is_free": False,
            "logo_url": "https://example.com/dff-logo.jpg",
            "capacity": None,
            "status": "live",
            "is_indoor": True
        },
        {
            "id": "EVT345678",
            "name": "Dubai Jazz Festival",
            "description": "The Dubai Jazz Festival is an annual music event featuring international jazz, rock, and pop artists.",
            "category": "Music",
            "start_time": (start_datetime + timedelta(days=10)).strftime("%Y-%m-%dT19:00:00"),
            "end_time": (start_datetime + timedelta(days=12)).strftime("%Y-%m-%dT23:30:00"),
            "venue": {
                "name": "Dubai Media City Amphitheatre",
                "address": "Dubai Media City, Dubai, UAE",
                "latitude": 25.0989,
                "longitude": 55.1560
            },
            "url": "https://www.dubaijazzfest.com",
            "is_free": False,
            "logo_url": "https://example.com/jazz-logo.jpg",
            "capacity": 5000,
            "status": "live",
            "is_indoor": False
        },
        {
            "id": "EVT901234",
            "name": "Dubai International Film Festival",
            "description": "The Dubai International Film Festival (DIFF) is a leading film festival in the Middle East showcasing Arab and international cinema.",
            "category": "Film & Media",
            "start_time": (start_datetime + timedelta(days=15)).strftime("%Y-%m-%dT14:00:00"),
            "end_time": (start_datetime + timedelta(days=22)).strftime("%Y-%m-%dT23:00:00"),
            "venue": {
                "name": "Madinat Jumeirah",
                "address": "Jumeirah Beach Road, Dubai, UAE",
                "latitude": 25.1335,
                "longitude": 55.1839
            },
            "url": "https://www.dubaifilmfest.com",
            "is_free": False,
            "logo_url": "https://example.com/diff-logo.jpg",
            "capacity": 2000,
            "status": "live",
            "is_indoor": True
        },
        {
            "id": "EVT567890",
            "name": "Dubai Desert Classic",
            "description": "The Dubai Desert Classic is a European Tour golf tournament held on the Majlis Course at Emirates Golf Club in Dubai.",
            "category": "Sports",
            "start_time": (start_datetime + timedelta(days=20)).strftime("%Y-%m-%dT08:00:00"),
            "end_time": (start_datetime + timedelta(days=23)).strftime("%Y-%m-%dT18:00:00"),
            "venue": {
                "name": "Emirates Golf Club",
                "address": "Emirates Hills, Dubai, UAE",
                "latitude": 25.0883,
                "longitude": 55.1560
            },
            "url": "https://www.dubaidesertclassic.com",
            "is_free": False,
            "logo_url": "https://example.com/golf-logo.jpg",
            "capacity": 10000,
            "status": "live",
            "is_indoor": False
        }
    ]
    
    # Filter by category if provided
    if category:
        filtered_events = [e for e in dubai_events if category.lower() in e["category"].lower()]
    else:
        filtered_events = dubai_events
    
    # Filter by date range
    date_filtered_events = []
    for event in filtered_events:
        event_start = datetime.strptime(event["start_time"].split("T")[0], "%Y-%m-%d")
        event_end = datetime.strptime(event["end_time"].split("T")[0], "%Y-%m-%d")
        
        # Check if event overlaps with the requested date range
        if (event_start <= end_datetime and event_end >= start_datetime):
            date_filtered_events.append(event)
    
    return {
        "provider": "Simulated",
        "location": location,
        "category": category,
        "start_date": start_date,
        "end_date": end_date,
        "events": date_filtered_events
    }

def get_simulated_event_details(event_id: str) -> Dict[str, Any]:
    """Generate simulated detailed event data for testing purposes."""
    # Find the event in our simulated data
    events = get_simulated_events("Dubai")["events"]
    event = next((e for e in events if e["id"] == event_id), None)
    
    if not event:
        # Default to first event if not found
        event = events[0]
    
    # Add additional details
    tickets = []
    if not event["is_free"]:
        tickets = [
            {
                "name": "General Admission",
                "price": "AED 150",
                "currency": "AED",
                "availability": random.randint(50, 500),
                "sales_start": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT10:00:00"),
                "sales_end": event["start_time"]
            },
            {
                "name": "VIP",
                "price": "AED 500",
                "currency": "AED",
                "availability": random.randint(10, 100),
                "sales_start": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT10:00:00"),
                "sales_end": event["start_time"]
            }
        ]
    
    organizer = {
        "name": "Dubai Events",
        "description": "Official organizer of events in Dubai",
        "url": "https://www.visitdubai.com/en/events"
    }
    
    detailed_event = event.copy()
    detailed_event.update({
        "tickets": tickets,
        "organizer": organizer,
        "timezone": "Asia/Dubai",
        "subcategory": "",
        "tags": ["Dubai", "UAE", "Tourism", event["category"]],
        "facilities": ["Parking", "Restrooms", "Food & Beverages", "Wheelchair Accessible"],
        "restrictions": "No photography allowed" if "Film" in event["category"] else "None",
        "weather_policy": "Event may be postponed in case of severe weather conditions" if not event["is_indoor"] else "Indoor event, not affected by weather"
    })
    
    return detailed_event

# Register tools with the registry
tool_registry.register_tool(
    tool_name="search_events",
    tool_function=search_events,
    category="events",
    description="Search for events in a location",
    required_params=["location"],
    optional_params=["category", "start_date", "end_date", "provider"]
)

tool_registry.register_tool(
    tool_name="get_event_details",
    tool_function=get_event_details,
    category="events",
    description="Get detailed information about an event",
    required_params=["event_id"],
    optional_params=["provider"]
)
