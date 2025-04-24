from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import logging
import json
import random
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Import our agentic components
from agentic_core import AgenticCore, Goal, create_tom_priya_scenario
from context_engine import ContextEngine, create_tom_priya_context
from preference_system import PreferenceSystem, create_tom_priya_preferences
from booking_system import BookingSystem, create_tom_priya_booking_scenario

# Import our tool modules
from tools.tool_registry import ToolRegistry
from tools.weather_tools import *
from tools.mapping_tools import *
from tools.booking_tools import *
from tools.attraction_tools import *
from tools.dining_tools import *
from tools.transportation_tools import *
from tools.events_tools import *
from tools.local_info_tools import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voyagerverse")

# Initialize FastAPI app
app = FastAPI(title="VoyagerVerse Agentic AI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize our agentic components
agentic_core = AgenticCore()
context_engine = ContextEngine()
preference_system = PreferenceSystem()
booking_system = BookingSystem()

# Initialize the tool registry
tool_registry = ToolRegistry()

# Store active itineraries
itineraries = {}

# Store active notifications
notifications = []

# Model for incoming chat messages
class ChatMessage(BaseModel):
    message: str
    language: str = "en-US"

# Model for itinerary operations
class ItineraryRequest(BaseModel):
    traveler_name: str
    start_date: str
    end_date: str
    preferences: Dict[str, Any] = {}

# Model for activity feedback
class ActivityFeedback(BaseModel):
    activity_id: str
    reaction: str  # loved, liked, neutral, disliked, hated
    comments: Optional[str] = None

# Model for notification response
class NotificationResponse(BaseModel):
    notification_id: str
    response: bool  # True for accept, False for reject

# Initialize Tom & Priya scenario for demo
def initialize_tom_priya_scenario():
    # Create their goals
    agentic_core.add_goal(Goal(
        name="Experience local culture",
        description="Discover authentic Dubai cultural experiences",
        priority=8,
        success_criteria={"min_cultural_activities": 3}
    ))
    
    agentic_core.add_goal(Goal(
        name="Culinary exploration",
        description="Try diverse local and international cuisine",
        priority=7,
        success_criteria={"min_unique_cuisines": 4}
    ))
    
    agentic_core.add_goal(Goal(
        name="Light adventure",
        description="Experience exciting but not physically demanding activities",
        priority=6,
        success_criteria={"min_adventure_activities": 2}
    ))
    
    # Initialize preferences
    preference_system.initialize_preferences({
        "max_comfortable_temperature": 38,
        "preferred_activity_pace": "moderate",
        "cuisine_preferences": ["local", "indian", "mediterranean"],
        "avoid_crowds": True,
        "category_culture_score": 0.8,  # High interest in culture
        "category_adventure_score": 0.7,  # Good interest in light adventure
        "category_relaxation_score": 0.5,  # Neutral on relaxation
        "outdoor_preference": 0.6,  # Slight preference for outdoor activities
        "preferred_price_range": "$$$"  # Luxury vacation
    })
    
    # Set up their 7-day itinerary
    start_date = datetime.now().date()
    itineraries["Tom_and_Priya"] = create_sample_itinerary("Tom_and_Priya", start_date)
    
    # Set up extreme heat context for demo
    # Update weather for extreme heat
    context_engine.current_context["weather"] = {
        "temperature": 43,  # Extremely hot
        "humidity": 65,
        "precipitation_chance": 0.05,
        "uv_index": 9,
        "wind_speed": 12,
        "conditions": "sunny"
    }
    
    # Set last weather check
    context_engine.current_context["last_weather_check"] = {
        "temperature": 36,
        "humidity": 60,
        "precipitation_chance": 0.0,
        "uv_index": 8
    }
    
    # Update traveler state
    context_engine.update_traveler_state({
        "energy_level": 0.8,  # Good energy
        "last_meal_time": (datetime.now() - timedelta(hours=2)).isoformat(),
        "meal_count_today": 2,
        "step_count": 4500,
        "preferences": preference_system.preference_model
    })
    
    logger.info("Tom & Priya scenario initialized")

# Create a sample itinerary for demo purposes
def create_sample_itinerary(traveler_id: str, start_date: datetime.date) -> Dict[str, Any]:
    itinerary = {
        "traveler_id": traveler_id,
        "start_date": start_date.isoformat(),
        "end_date": (start_date + timedelta(days=6)).isoformat(),
        "days": []
    }
    
    # Sample activities
    activities = [
        {
            "id": "act1",
            "name": "Burj Khalifa Visit",
            "time": "10:00-12:00",
            "location": "Downtown Dubai",
            "description": "Visit the world's tallest building and enjoy panoramic views of Dubai",
            "category": "sightseeing",
            "is_outdoor": False,
            "energy_required": 0.4,
            "booking_reference": "BK12345"
        },
        {
            "id": "act2",
            "name": "Dubai Mall Shopping",
            "time": "12:30-15:30",
            "location": "Downtown Dubai",
            "description": "Explore one of the world's largest shopping malls",
            "category": "shopping",
            "is_outdoor": False,
            "energy_required": 0.6,
            "booking_reference": None
        },
        {
            "id": "act3",
            "name": "Dinner at Al Dawaar",
            "time": "19:00-21:00",
            "location": "Deira",
            "description": "Enjoy dinner at Dubai's only revolving restaurant with panoramic views",
            "category": "dining",
            "is_outdoor": False,
            "energy_required": 0.3,
            "booking_reference": "AD67890"
        },
        {
            "id": "act4",
            "name": "Old Dubai Cultural Tour",
            "time": "09:00-12:00",
            "location": "Al Fahidi",
            "description": "Explore the historic Al Fahidi district and Dubai Creek",
            "category": "culture",
            "is_outdoor": True,
            "energy_required": 0.5,
            "booking_reference": "OD54321"
        },
        {
            "id": "act5",
            "name": "Dubai Aquarium Visit",
            "time": "13:00-15:00",
            "location": "Downtown Dubai",
            "description": "See thousands of aquatic animals at one of the world's largest aquariums",
            "category": "attraction",
            "is_outdoor": False,
            "energy_required": 0.3,
            "booking_reference": "DA98765"
        },
        {
            "id": "act6",
            "name": "Desert Safari",
            "time": "14:00-18:00",
            "location": "Al Marmoom Desert",
            "description": "Experience the thrill of dune bashing followed by a traditional desert camp experience",
            "category": "adventure",
            "is_outdoor": True,
            "energy_required": 0.7,
            "booking_reference": "DS12345"
        },
        {
            "id": "act7",
            "name": "Bedouin Dinner Experience",
            "time": "19:00-21:30",
            "location": "Desert Camp",
            "description": "Authentic Bedouin dinner under the stars with cultural performances",
            "category": "culture",
            "is_outdoor": True,
            "energy_required": 0.4,
            "booking_reference": "BD67890"
        },
        {
            "id": "act8",
            "name": "Dubai Marina Yacht Tour",
            "time": "16:00-18:00",
            "location": "Dubai Marina",
            "description": "Cruise around Dubai Marina and Palm Jumeirah on a luxury yacht",
            "category": "leisure",
            "is_outdoor": True,
            "energy_required": 0.4,
            "booking_reference": "YT24680"
        },
        {
            "id": "act9",
            "name": "Spice Souk Visit",
            "time": "10:00-12:00",
            "location": "Deira",
            "description": "Explore the aromatic spice souk and gold souk in old Dubai",
            "category": "culture",
            "is_outdoor": True,
            "energy_required": 0.5,
            "booking_reference": "SS13579"
        },
        {
            "id": "act10",
            "name": "Jumeirah Mosque Tour",
            "time": "09:00-11:00",
            "location": "Jumeirah",
            "description": "Visit one of the few mosques in Dubai open to non-Muslims",
            "category": "culture",
            "is_outdoor": False,
            "energy_required": 0.3,
            "booking_reference": "JM97531"
        }
    ]
    
    # Create 7 days of activities
    for i in range(7):
        day_date = start_date + timedelta(days=i)
        
        # For day 3, add the desert safari scenario
        if i == 2:  # Third day (index 2)
            day_activities = [activities[5], activities[6]]  # Desert Safari and Bedouin Dinner
        else:
            # Randomly select 2-3 activities for each day
            num_activities = random.randint(2, 3)
            day_activities = random.sample([a for a in activities if a["id"] not in ["act6", "act7"]], num_activities)
        
        day = {
            "day_number": i + 1,
            "date": day_date.isoformat(),
            "activities": day_activities
        }
        
        itinerary["days"].append(day)
    
    return itinerary

# Process weather updates and trigger adaptations if needed
async def process_weather_updates(background_tasks: BackgroundTasks):
    # Try to get real weather data using our weather tools
    try:
        weather_result = get_current_weather("Dubai", provider="weatherapi")
        if weather_result["status"] == "success":
            weather_data = weather_result["data"]
            weather = {
                "temperature": weather_data["temperature"],
                "conditions": weather_data["conditions"],
                "humidity": weather_data["humidity"],
                "precipitation_chance": weather_data["precipitation_chance"],
                "uv_index": weather_data["uv_index"],
                "wind_speed": weather_data["wind_speed"]
            }
            # Update context with real weather data
            context_engine.current_context["weather"] = weather
            logger.info(f"Updated weather using real API: {weather['temperature']}°C, {weather['conditions']}")
        else:
            # Fall back to simulated data
            weather = context_engine.update_weather(force_update=True)
            logger.info(f"Updated weather using simulation: {weather['temperature']}°C, {weather['conditions']}")
    except Exception as e:
        logger.error(f"Error getting real weather data: {e}")
        # Fall back to simulated data
        weather = context_engine.update_weather(force_update=True)
        logger.info(f"Updated weather using simulation: {weather['temperature']}°C, {weather['conditions']}")
    
    # Check if we need to adapt any itineraries
    for traveler_id, itinerary in itineraries.items():
        # Find today's itinerary
        today = datetime.now().date().isoformat()
        today_index = next((i for i, day in enumerate(itinerary["days"]) if day["date"] == today), None)
        
        if today_index is not None:
            today_plan = itinerary["days"][today_index]
            
            # Update context with current plan
            context_engine.current_context["current_plan"] = today_plan
            
            # Let the agentic core evaluate if changes are needed
            new_plan = agentic_core.evaluate_current_plan()
            
            if new_plan.get("is_modified", False):
                # Plan was modified, create a notification
                notification_id = f"notif-{len(notifications)+1}"
                explanation = agentic_core.explain_decision(len(agentic_core.decision_history) - 1)
                confidence = agentic_core.get_confidence_score(agentic_core.decision_history[-1])
                
                notification = {
                    "id": notification_id,
                    "traveler_id": traveler_id,
                    "timestamp": datetime.now().isoformat(),
                    "type": "itinerary_change",
                    "title": "Itinerary Update Suggested",
                    "message": explanation,
                    "original_plan": today_plan,
                    "new_plan": new_plan,
                    "confidence": confidence,
                    "status": "pending",
                    "requires_approval": confidence < agentic_core.confidence_threshold
                }
                
                notifications.append(notification)
                logger.info(f"Created notification {notification_id} for {traveler_id}")
                
                # If confidence is high enough, automatically apply the change
                if confidence >= agentic_core.confidence_threshold:
                    # Auto-approve high-confidence changes
                    await handle_notification_response(notification_id, True)

# Handle notification responses
async def handle_notification_response(notification_id: str, approved: bool):
    # Find the notification
    notification = next((n for n in notifications if n["id"] == notification_id), None)
    
    if not notification:
        logger.error(f"Notification {notification_id} not found")
        return
    
    # Update notification status
    notification["status"] = "approved" if approved else "rejected"
    notification["response_time"] = datetime.now().isoformat()
    
    if approved:
        # Apply the changes to the itinerary
        traveler_id = notification["traveler_id"]
        itinerary = itineraries.get(traveler_id)
        
        if itinerary:
            # Find the day to update
            today = datetime.now().date().isoformat()
            today_index = next((i for i, day in enumerate(itinerary["days"]) if day["date"] == today), None)
            
            if today_index is not None:
                # Update the activities
                itinerary["days"][today_index]["activities"] = notification["new_plan"]["activities"]
                itinerary["days"][today_index]["is_modified"] = True
                itinerary["days"][today_index]["modification_reason"] = notification["new_plan"]["modification_reason"]
                
                logger.info(f"Updated itinerary for {traveler_id} based on notification {notification_id}")
                
                # Record the decision acceptance in the agentic core
                if len(agentic_core.decision_history) > 0:
                    agentic_core.decision_history[-1]["was_accepted"] = True
    else:
        # Record the decision rejection in the agentic core
        if len(agentic_core.decision_history) > 0:
            agentic_core.decision_history[-1]["was_accepted"] = False

# API Endpoints

@app.post("/chat")
async def chat(msg: ChatMessage):
    """Process a chat message and return a response."""
    # Extract the message and language
    message = msg.message
    language = msg.language
    
    # Update preferences from natural language
    preference_system.update_from_natural_language(message)
    
    # Generate a response based on the message
    english_reply = generate_chat_response(message)
    
    # Translate reply to user-selected language
    target_lang = language.split("-")[0]  # e.g., 'hi' from 'hi-IN'
    
    try:
        if target_lang != "en":
            translated_reply = GoogleTranslator(source='auto', target=target_lang).translate(english_reply)
        else:
            translated_reply = english_reply
    except Exception as e:
        logger.error(f"Translation error: {e}")
        translated_reply = english_reply + " (Translation failed)"

    return {"reply": translated_reply}

def generate_chat_response(message: str) -> str:
    """Generate a response to a chat message."""
    # Get current context
    current_context = context_engine.get_current_context()

    # Get current preferences
    current_preferences = preference_system.get_current_preferences()

    # Basic keyword-based response for demo with tool integration
    if "weather" in message.lower():
        try:
            # Try to use the weather tools
            weather_result = get_current_weather("Dubai", provider="weatherapi")
            if weather_result["status"] == "success":
                weather_data = weather_result["data"]
                temp = weather_data["temperature"]
                conditions = weather_data["conditions"]
                humidity = weather_data["humidity"]
                return f"The current weather in Dubai is {temp}°C and {conditions} with {humidity}% humidity."
            else:
                # Fall back to simulated data
                temp = current_context.get("weather", {}).get("temperature", 35)
                conditions = current_context.get("weather", {}).get("conditions", "sunny")
                return f"The current weather in Dubai is {temp}°C and {conditions}."
        except Exception as e:
            logger.error(f"Error using weather tools: {e}")
            # Fall back to simulated data
            temp = current_context.get("weather", {}).get("temperature", 35)
            conditions = current_context.get("weather", {}).get("conditions", "sunny")
            return f"The current weather in Dubai is {temp}°C and {conditions}."

    elif "restaurant" in message.lower() or "food" in message.lower() or "eat" in message.lower():
        try:
            # Try to use the dining tools
            cuisine = None
            for pref in current_preferences.get("cuisine_preferences", []):
                if pref in message.lower():
                    cuisine = pref
                    break

            restaurants_result = search_restaurants("Dubai", cuisine=cuisine)
            if restaurants_result["status"] == "success":
                restaurants = restaurants_result["data"]["restaurants"][:3]  # Get top 3
                response = "Here are some restaurant recommendations for you:\n"
                for restaurant in restaurants:
                    response += f"- {restaurant['name']} ({restaurant['cuisine']}): {restaurant['price_range']} - {restaurant['rating']}/5 stars\n"
                return response
            else:
                return "I couldn't find any restaurants matching your preferences at the moment."
        except Exception as e:
            logger.error(f"Error using dining tools: {e}")
            return "I can help you find restaurants in Dubai based on your preferences. Please specify any cuisine preferences you might have."

    elif "attraction" in message.lower() or "visit" in message.lower() or "see" in message.lower():
        try:
            # Try to use the attraction tools
            category = None
            if "museum" in message.lower():
                category = "museums"
            elif "beach" in message.lower():
                category = "beaches"
            elif "mall" in message.lower() or "shop" in message.lower():
                category = "shopping"

            attractions_result = search_attractions("Dubai", category=category)
            if attractions_result["status"] == "success":
                attractions = attractions_result["data"]["attractions"][:3]  # Get top 3
                response = "Here are some attractions you might enjoy in Dubai:\n"
                for attraction in attractions:
                    response += f"- {attraction['name']}: {attraction['rating']}/5 stars - {attraction['description'][:100]}...\n"
                return response
            else:
                return "I couldn't find any attractions matching your interests at the moment."
        except Exception as e:
            logger.error(f"Error using attraction tools: {e}")
            return "I can help you find interesting attractions in Dubai. What types of places would you like to visit?"

    elif "event" in message.lower() or "happening" in message.lower() or "festival" in message.lower():
        try:
            # Try to use the events tools
            events_result = search_events("Dubai")
            if events_result["status"] == "success":
                events = events_result["data"]["events"][:3]  # Get top 3
                response = "Here are some upcoming events in Dubai:\n"
                for event in events:
                    event_date = event["start_time"].split("T")[0]
                    response += f"- {event['name']} on {event_date}: {event['venue']['name']}\n"
                return response
            else:
                return "I couldn't find any upcoming events at the moment."
        except Exception as e:
            logger.error(f"Error using events tools: {e}")
            return "I can help you find events and festivals happening in Dubai. Is there a specific type of event you're interested in?"

    elif "transport" in message.lower() or "taxi" in message.lower() or "uber" in message.lower() or "get around" in message.lower():
        try:
            # Try to use the transportation tools
            if "estimate" in message.lower() or "cost" in message.lower() or "price" in message.lower():
                # Extract locations from message or use defaults
                pickup = "Dubai Mall"
                dropoff = "Burj Al Arab"

                ride_result = get_ride_estimate(pickup, dropoff)
                if ride_result["status"] == "success":
                    ride_data = ride_result["data"]
                    return f"A ride from {pickup} to {dropoff} would cost approximately {ride_data['estimate']} and take about {int(ride_data['duration']/60)} minutes."
                else:
                    return "I couldn't get a ride estimate at the moment."
            else:
                # Get transit routes
                transit_result = get_transit_routes("Dubai Mall", "Dubai Marina")
                if transit_result["status"] == "success":
                    routes = transit_result["data"]["routes"][:2]  # Get top 2
                    response = "Here are some public transportation options in Dubai:\n"
                    for route in routes:
                        response += f"- {route['duration_minutes']} min journey with {route['transfers']} transfers, {route['walking_minutes']} min walking\n"
                    return response
                else:
                    return "I couldn't find transportation options at the moment."
        except Exception as e:
            logger.error(f"Error using transportation tools: {e}")
            return "I can help you with transportation options in Dubai, including taxis, ride-sharing, and public transit."

    elif "custom" in message.lower() or "culture" in message.lower() or "local" in message.lower():
        try:
            # Try to use the local info tools
            topic = None
            if "dress" in message.lower() or "wear" in message.lower() or "clothing" in message.lower():
                customs = get_local_customs()
                if customs["status"] == "success":
                    dress_code = customs["data"]["dress_code"]
                    return f"{dress_code['title']}:\n{dress_code['content']}"
            elif "emergency" in message.lower() or "hospital" in message.lower() or "police" in message.lower():
                emergency = get_emergency_info()
                if emergency["status"] == "success":
                    numbers = emergency["data"]["emergency_numbers"][:3]
                    response = "Important emergency numbers in Dubai:\n"
                    for num in numbers:
                        response += f"- {num['service']}: {num['number']}\n"
                    return response
            else:
                cultural_info = get_cultural_info()
                if cultural_info["status"] == "success":
                    # Pick a random cultural topic
                    topics = list(cultural_info["data"].keys())
                    topic = random.choice(topics)
                    info = cultural_info["data"][topic]
                    return f"{info['title']}:\n{info['content']}"
        except Exception as e:
            logger.error(f"Error using local info tools: {e}")
            return "I can provide information about local customs, culture, and practical information for your stay in Dubai."

    elif "itinerary" in message.lower() or "plan" in message.lower() or "schedule" in message.lower():
        # Return info about today's itinerary
        today = datetime.now().date().isoformat()
        traveler_id = "Tom_and_Priya"  # Default for demo

        if traveler_id in itineraries:
            itinerary = itineraries[traveler_id]
            today_index = next((i for i, day in enumerate(itinerary["days"]) if day["date"] == today), None)

            if today_index is not None:
                today_plan = itinerary["days"][today_index]
                activities = today_plan["activities"]

                response = f"Today you have {len(activities)} activities planned:\n"
                for activity in activities:
                    response += f"- {activity['time']}: {activity['name']} at {activity['location']}\n"
                return response

        return "I don't have any itinerary information available at the moment."

    elif "preference" in message.lower() or "like" in message.lower():
        # Return some preference information
        cuisine_prefs = current_preferences.get("cuisine_preferences", [])
        max_temp = current_preferences.get("max_comfortable_temperature", 38)

        return f"Based on your preferences, you enjoy {', '.join(cuisine_prefs)} cuisine and prefer temperatures below {max_temp}°C."

    else:
        # Default response
        return "I'm your VoyagerVerse agentic AI assistant for Dubai. I can help with weather updates, itinerary information, restaurant recommendations, attraction suggestions, transportation options, local customs, and personalized recommendations based on your preferences and current conditions."

async def read_root(request: Request):
    return templates.TemplateResponse("home_v2.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the dashboard UI for Tom & Priya."""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()

@app.get("/mobile", response_class=HTMLResponse)
async def mobile_app(request: Request):
    """Serve the mobile app UI"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("mobile_app.html", {
        "request": request,
        "traveler_name": "Tom & Priya",
        "current_date": datetime.now().strftime("%A, %B %d, %Y")
    })

@app.get("/user-mobile", response_class=HTMLResponse)
async def user_mobile_app(request: Request):
    """Serve the user-focused mobile app UI for Tom & Priya"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("user_mobile_app.html", {
        "request": request,
        "traveler_name": "Tom & Priya",
        "current_date": datetime.now().strftime("%A, %B %d, %Y")
    })

@app.get("/fallback-mobile", response_class=HTMLResponse)
async def fallback_mobile_app(request: Request):
    """Serve the fallback mobile app UI with option to decline rescheduling"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("mobile_app_fallback.html", {
        "request": request,
        "traveler_name": "Tom & Priya",
        "current_date": datetime.now().strftime("%A, %B %d, %Y")
    })

@app.get("/demo", response_class=HTMLResponse)
async def demo_mobile_app(request: Request):
    """Serve the simplified demo mobile app UI"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("demo_mobile.html", {
        "request": request,
        "traveler_name": "Tom & Priya",
        "current_date": datetime.now().strftime("%A, %B %d, %Y")
    })

@app.get("/conversation-demo", response_class=HTMLResponse)
async def conversation_demo(request: Request):
    """Serve the conversational demo interface that showcases natural language interaction"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("conversation_demo.html", {
        "request": request
    })

@app.get("/agent-calling-demo", response_class=HTMLResponse)
async def agent_calling_demo(request: Request):
    """Serve the agent calling demo interface that showcases the agentic AI process"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("tool_calling_demo.html", {
        "request": request
    })

@app.get("/conversation-ui", response_class=HTMLResponse)
async def conversation_ui(request: Request):
    """Serve the conversational UI that demonstrates natural language interaction"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("conversation_ui.html", {
        "request": request
    })

@app.get("/simple-chat", response_class=HTMLResponse)
async def simple_chat_demo(request: Request):
    """Serve the simplified chat demo that works reliably for the presentation"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("simple_chat_demo.html", {
        "request": request
    })

@app.get("/agent-calling", response_class=HTMLResponse)
async def agent_calling_ui(request: Request):
    """Serve the agent calling UI that shows the behind-the-scenes process"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("agent_calling_ui.html", {
        "request": request
    })

@app.get("/simple-agent", response_class=HTMLResponse)
async def simple_agent_ui(request: Request):
    """Serve the simplified agent UI that shows the behind-the-scenes process without animations"""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    return templates.TemplateResponse("simple_agent_ui.html", {
        "request": request
    })
    
    # Get current weather
    weather_data = {}
    try:
        weather_result = get_current_weather("Dubai", provider="weatherapi")
        if weather_result["status"] == "success":
            weather_data = weather_result["data"]
        else:
            weather_data = context_engine.get_current_context().get("weather", {})
    except Exception as e:
        logger.error(f"Error getting weather data: {e}")
        weather_data = context_engine.get_current_context().get("weather", {})
    
    # Get itinerary data
    traveler_id = "Tom_and_Priya"
    itinerary_data = {}
    if traveler_id in itineraries:
        itinerary_data = itineraries[traveler_id]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "weather": weather_data,
        "itinerary": itinerary_data,
        "traveler_name": "Tom & Priya",
        "current_date": datetime.now().strftime("%A, %B %d, %Y")
    })

@app.get("/interactive", response_class=HTMLResponse)
async def interactive_demo(request: Request):
    """Serve the interactive demo page showing the agentic AI architecture from user's perspective."""
    # Initialize Tom & Priya scenario data
    initialize_tom_priya_scenario()
    
    # Sample data for the interactive demo
    demo_data = {
        "traveler_name": "Tom & Priya",
        "current_date": datetime.now().strftime("%A, %B %d, %Y"),
        "weather": {
            "temperature": 44,
            "condition": "Sunny",
            "humidity": 28,
            "feels_like": 47,
            "uv_index": "Extreme",
            "wind_speed": 12
        },
        "original_activity": {
            "name": "Desert Safari",
            "location": "Dubai Desert Conservation Reserve",
            "time": "11:00-15:00",
            "is_outdoor": True,
            "category": "adventure"
        },
        "alternative_activity": {
            "name": "Dubai Museum Visit",
            "location": "Al Fahidi Fort",
            "time": "11:00-13:00",
            "is_outdoor": False,
            "category": "cultural"
        },
        "preferences": {
            "max_comfortable_temperature": 38,
            "preferred_dining_time": "19:00",
            "cuisine_preferences": ["Indian", "Mediterranean", "Arabic"],
            "activity_preferences": ["cultural", "adventure", "relaxation"],
            "budget_level": "premium"
        }
    }
    
    return templates.TemplateResponse("interactive_demo.html", {
        "request": request,
        "demo_data": demo_data
    })

@app.get("/weather")
async def get_weather():
    """Get the current weather conditions."""
    try:
        # Try to get real weather data
        weather_result = get_current_weather("Dubai", provider="weatherapi")
        if weather_result["status"] == "success":
            return weather_result["data"]
        else:
            # Fall back to simulated data
            return context_engine.get_current_context().get("weather", {})
    except Exception as e:
        logger.error(f"Error getting weather data: {e}")
        return context_engine.get_current_context().get("weather", {})

def initialize_tom_priya_scenario():
    """Initialize the Tom & Priya scenario with sample data."""
    # Clear any existing data
    notifications.clear()
    if hasattr(agentic_core, 'decision_history'):
        agentic_core.decision_history.clear()
    
    # Set up traveler preferences
    traveler_id = "Tom_and_Priya"
    initial_preferences = {
        "max_comfortable_temperature": 38,  # Celsius
        "preferred_dining_time": "19:00",
        "cuisine_preferences": ["Indian", "Mediterranean", "Arabic"],
        "activity_preferences": ["cultural", "adventure", "relaxation"],
        "budget_level": "premium"  # economy, standard, premium, luxury
    }
    preference_system.initialize_preferences(initial_preferences)
    preference_system.preference_model["traveler_id"] = traveler_id
    
    # Create a sample 5-day itinerary
    start_date = datetime.now().date()
    itinerary = {
        "traveler_id": traveler_id,
        "trip_name": "Dubai Luxury Getaway",
        "start_date": start_date.isoformat(),
        "end_date": (start_date + timedelta(days=4)).isoformat(),
        "days": []
    }
    
    # Day 1: Arrival and City Tour
    day1 = {
        "date": start_date.isoformat(),
        "title": "Arrival and City Introduction",
        "activities": [
            {
                "name": "Airport Pickup and Hotel Check-in",
                "time": "10:00-12:00",
                "location": "Dubai International Airport to Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.3,
                "category": "transportation"
            },
            {
                "name": "Lunch at Al Muntaha",
                "time": "13:00-14:30",
                "location": "Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.2,
                "category": "dining"
            },
            {
                "name": "Dubai City Tour",
                "time": "15:00-18:00",
                "location": "Downtown Dubai",
                "is_outdoor": True,
                "energy_required": 0.6,
                "category": "sightseeing"
            },
            {
                "name": "Dinner at Pierchic",
                "time": "19:30-21:30",
                "location": "Jumeirah Al Qasr",
                "is_outdoor": False,
                "energy_required": 0.3,
                "category": "dining"
            }
        ]
    }
    
    # Day 2: Cultural Experiences
    day2 = {
        "date": (start_date + timedelta(days=1)).isoformat(),
        "title": "Cultural Immersion",
        "activities": [
            {
                "name": "Breakfast at Hotel",
                "time": "08:00-09:00",
                "location": "Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.1,
                "category": "dining"
            },
            {
                "name": "Old Dubai Walking Tour",
                "time": "10:00-12:30",
                "location": "Al Fahidi Historical District",
                "is_outdoor": True,
                "energy_required": 0.7,
                "category": "cultural"
            },
            {
                "name": "Lunch at Arabian Tea House",
                "time": "13:00-14:30",
                "location": "Al Fahidi",
                "is_outdoor": False,
                "energy_required": 0.2,
                "category": "dining"
            },
            {
                "name": "Dubai Museum Visit",
                "time": "15:00-17:00",
                "location": "Al Fahidi Fort",
                "is_outdoor": False,
                "energy_required": 0.4,
                "category": "cultural"
            },
            {
                "name": "Dhow Dinner Cruise",
                "time": "19:00-21:30",
                "location": "Dubai Creek",
                "is_outdoor": True,
                "energy_required": 0.3,
                "category": "dining"
            }
        ]
    }
    
    # Day 3: Desert Adventure (The day that will be modified due to heat)
    day3 = {
        "date": (start_date + timedelta(days=2)).isoformat(),
        "title": "Desert Adventure",
        "activities": [
            {
                "name": "Breakfast at Hotel",
                "time": "08:00-09:00",
                "location": "Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.1,
                "category": "dining"
            },
            {
                "name": "Morning at Leisure",
                "time": "09:30-12:30",
                "location": "Hotel Pool",
                "is_outdoor": True,
                "energy_required": 0.3,
                "category": "relaxation"
            },
            {
                "name": "Lunch at Pai Thai",
                "time": "13:00-14:00",
                "location": "Jumeirah Al Qasr",
                "is_outdoor": False,
                "energy_required": 0.2,
                "category": "dining"
            },
            {
                "name": "Desert Safari with Dune Bashing",
                "time": "14:00-18:00",
                "location": "Dubai Desert Conservation Reserve",
                "is_outdoor": True,
                "energy_required": 0.8,
                "category": "adventure"
            },
            {
                "name": "Bedouin Dinner Experience",
                "time": "18:30-21:30",
                "location": "Desert Camp",
                "is_outdoor": True,
                "energy_required": 0.4,
                "category": "dining"
            }
        ]
    }
    
    # Day 4: Shopping and Entertainment
    day4 = {
        "date": (start_date + timedelta(days=3)).isoformat(),
        "title": "Shopping and Entertainment",
        "activities": [
            {
                "name": "Breakfast at Hotel",
                "time": "08:00-09:00",
                "location": "Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.1,
                "category": "dining"
            },
            {
                "name": "Dubai Mall Shopping",
                "time": "10:00-13:00",
                "location": "Downtown Dubai",
                "is_outdoor": False,
                "energy_required": 0.6,
                "category": "shopping"
            },
            {
                "name": "Lunch at The Cheesecake Factory",
                "time": "13:30-14:30",
                "location": "Dubai Mall",
                "is_outdoor": False,
                "energy_required": 0.2,
                "category": "dining"
            },
            {
                "name": "Dubai Aquarium & Underwater Zoo",
                "time": "15:00-17:00",
                "location": "Dubai Mall",
                "is_outdoor": False,
                "energy_required": 0.4,
                "category": "attraction"
            },
            {
                "name": "Dinner at Atmosphere",
                "time": "19:00-21:00",
                "location": "Burj Khalifa",
                "is_outdoor": False,
                "energy_required": 0.3,
                "category": "dining"
            },
            {
                "name": "Dubai Fountain Show",
                "time": "21:30-22:00",
                "location": "Downtown Dubai",
                "is_outdoor": True,
                "energy_required": 0.2,
                "category": "entertainment"
            }
        ]
    }
    
    # Day 5: Luxury Experiences and Departure
    day5 = {
        "date": (start_date + timedelta(days=4)).isoformat(),
        "title": "Luxury Day and Departure",
        "activities": [
            {
                "name": "Breakfast at Hotel",
                "time": "08:00-09:00",
                "location": "Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.1,
                "category": "dining"
            },
            {
                "name": "Spa Treatment",
                "time": "10:00-12:00",
                "location": "Burj Al Arab Spa",
                "is_outdoor": False,
                "energy_required": 0.2,
                "category": "relaxation"
            },
            {
                "name": "Lunch at Nathan Outlaw at Al Mahara",
                "time": "13:00-14:30",
                "location": "Burj Al Arab",
                "is_outdoor": False,
                "energy_required": 0.2,
                "category": "dining"
            },
            {
                "name": "Hotel Checkout and Airport Transfer",
                "time": "15:00-16:00",
                "location": "Burj Al Arab to Dubai International Airport",
                "is_outdoor": False,
                "energy_required": 0.3,
                "category": "transportation"
            },
            {
                "name": "Flight Departure",
                "time": "19:00-19:30",
                "location": "Dubai International Airport",
                "is_outdoor": False,
                "energy_required": 0.5,
                "category": "transportation"
            }
        ]
    }
    
    # Add all days to the itinerary
    itinerary["days"] = [day1, day2, day3, day4, day5]
    
    # Store the itinerary
    itineraries[traveler_id] = itinerary
    
    # Set up initial context
    context_engine.update_weather({
        "temperature": 36,  # Starting with a hot but manageable temperature
        "humidity": 60,
        "precipitation_chance": 0.0,
        "uv_index": 8,
        "wind_speed": 10,
        "conditions": "sunny",
        "data_source": "Demo",
        "last_updated": datetime.now().isoformat()
    })
    
    # Set traveler state
    context_engine.update_traveler_state({
        "traveler_id": traveler_id,
        "energy_level": 0.8,
        "last_meal_time": (datetime.now() - timedelta(hours=2)).isoformat(),
        "meal_count_today": 1,
        "step_count": 2000,
        "preferences": preference_system.get_preferences(traveler_id)
    })
    
    # Set time context
    # The update_time_context method doesn't take parameters, it updates automatically
    context_engine.update_time_context()
    
    # Initialize agentic core with goals
    goal1 = Goal(
        name="Enjoy Dubai's attractions",
        description="Experience the best attractions Dubai has to offer",
        priority=9,
        success_criteria={"min_attractions": 5}
    )
    
    goal2 = Goal(
        name="Stay comfortable in the heat",
        description="Avoid excessive heat exposure during outdoor activities",
        priority=10,
        success_criteria={"max_temperature": 38}
    )
    
    goal3 = Goal(
        name="Experience local culture",
        description="Immerse in authentic Emirati cultural experiences",
        priority=8,
        success_criteria={"min_cultural_activities": 2}
    )
    
    agentic_core.traveler_goals = [goal1, goal2, goal3]
    
    logger.info("Tom & Priya scenario initialized")
    return {"status": "success", "message": "Tom & Priya scenario initialized"}

@app.get("/demo/tom-priya-scenario")
async def run_tom_priya_scenario(background_tasks: BackgroundTasks):
    """Run the Tom & Priya scenario for demonstration."""
    try:
        # Initialize the scenario
        initialize_tom_priya_scenario()
        
        # Create a simulated demo scenario with a specific day plan
        # Find the day with the desert safari (day 3)
        traveler_id = "Tom_and_Priya"
        
        if traveler_id in itineraries:
            itinerary = itineraries[traveler_id]
            # Find the day with the desert safari (should be day 3)
            safari_day = None
            for day in itinerary["days"]:
                for activity in day["activities"]:
                    if "Desert Safari" in activity["name"]:
                        safari_day = day
                        break
                if safari_day:
                    break
            
            if not safari_day:
                # If not found, use the first day as fallback
                safari_day = itinerary["days"][0] if itinerary["days"] else None
            
            if safari_day:
                # Set this as the current plan in context
                context_engine.current_context["current_plan"] = safari_day
                
                # Force extreme heat for demo purposes
                context_engine.current_context["weather"] = {
                    "temperature": 45,  # Extremely hot
                    "humidity": 65,
                    "precipitation_chance": 0.05,
                    "uv_index": 10,
                    "wind_speed": 12,
                    "conditions": "sunny",
                    "data_source": "Demo",
                    "last_updated": datetime.now().isoformat()
                }
                
                # Set last weather check for comparison
                context_engine.current_context["last_weather_check"] = {
                    "temperature": 36,  # Previous temperature was lower
                    "humidity": 60,
                    "precipitation_chance": 0.0,
                    "uv_index": 8
                }
                
                # Create a modified plan directly for the demo
                # This ensures we have a proper demonstration even if the evaluate_current_plan method has issues
                modified_plan = safari_day.copy()
                modified_plan["is_modified"] = True
                modified_plan["modification_reason"] = "weather"
                
                # Copy activities and modify them
                modified_plan["activities"] = safari_day["activities"].copy()
                
                # Find the Desert Safari activity and modify its time
                for i, activity in enumerate(modified_plan["activities"]):
                    if "Desert Safari" in activity["name"]:
                        # Create a modified version of the activity with an earlier time slot
                        modified_activity = activity.copy()
                        modified_activity["time"] = "06:00-10:00"  # Early morning to avoid heat
                        modified_activity["description"] = "Early morning desert safari to avoid extreme daytime heat"
                        modified_plan["activities"][i] = modified_activity
                    
                    # Also adjust the Bedouin Dinner Experience to follow directly after
                    elif "Bedouin Dinner" in activity["name"]:
                        modified_activity = activity.copy()
                        modified_activity["time"] = "10:30-13:30"  # Moved to brunch time
                        modified_activity["name"] = "Bedouin Brunch Experience"
                        modified_activity["description"] = "Authentic Bedouin brunch experience following the early morning safari"
                        modified_plan["activities"][i] = modified_activity
                
                # Add an indoor activity for the afternoon
                modified_plan["activities"].append({
                    "name": "Dubai Museum and Cultural Tour",
                    "time": "15:00-18:00",
                    "location": "Al Fahidi Historical District",
                    "is_outdoor": False,
                    "energy_required": 0.4,
                    "category": "cultural",
                    "description": "Air-conditioned indoor cultural experience during the hottest part of the day"
                })
                
                # Create a notification for the change
                notification_id = f"notif-{len(notifications)+1}"
                confidence = 0.85  # High confidence for demo
                
                notification = {
                    "id": notification_id,
                    "traveler_id": traveler_id,
                    "timestamp": datetime.now().isoformat(),
                    "type": "itinerary_change",
                    "title": "Itinerary Update Suggested",
                    "message": "Due to extreme heat (45°C), outdoor activities have been rescheduled.",
                    "original_plan": safari_day,
                    "new_plan": modified_plan,
                    "confidence": confidence,
                    "status": "pending",
                    "requires_approval": confidence < agentic_core.confidence_threshold
                }
                
                notifications.append(notification)
                
                # Record the decision
                decision_data = {
                    "type": "itinerary_change",
                    "reason": "weather",
                    "details": "Extreme heat (45°C) detected, which exceeds the traveler's comfort threshold of 38°C. Outdoor activities rescheduled to cooler hours or replaced with indoor alternatives.",
                    "original_plan": safari_day,
                    "new_plan": modified_plan,
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat(),
                    "was_accepted": None  # Not yet decided
                }
                
                agentic_core.decision_history.append(decision_data)
                
                # Get the latest notification and decision
                latest_notification = notifications[-1]
                latest_decision = agentic_core.decision_history[-1]
                explanation = "Detected extreme heat (45°C) which exceeds Tom & Priya's comfort threshold (38°C). The Desert Safari scheduled for 14:00-18:00 would expose them to dangerous heat levels. Rescheduled to early morning (06:00-10:00) when temperatures are cooler, moved the Bedouin Dinner Experience to a brunch (10:30-13:30), and added an indoor cultural tour during the hottest part of the day (15:00-18:00)."
            else:
                raise ValueError("Could not find a valid day plan in the itinerary")
        else:
            raise ValueError(f"Traveler {traveler_id} not found in itineraries")
        
        return {
            "scenario": "Tom & Priya in Dubai",
            "context": context_engine.get_current_context(),
            "preferences": preference_system.get_preferences(traveler_id),
            "notification": latest_notification,
            "decision": latest_decision,
            "explanation": explanation
        }
    except Exception as e:
        logger.error(f"Error running Tom & Priya scenario: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": f"Error running Tom & Priya scenario: {str(e)}",
            "scenario": "Tom & Priya in Dubai"
        }

@app.on_event("startup")
def startup_event():
    # Initialize the Tom & Priya scenario
    initialize_tom_priya_scenario()

    # Log available tools
    logger.info(f"Available tools: {list(tool_registry.get_all_tools().keys())}")
    logger.info(f"Tool categories: {list(tool_registry.tool_categories.keys())}")

    logger.info("VoyagerVerse Agentic AI initialized")

if __name__ == "__main__":
    uvicorn.run("main_v2:app", host="0.0.0.0", port=8000, reload=True)
