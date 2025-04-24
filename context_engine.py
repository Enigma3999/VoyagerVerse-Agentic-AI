import datetime
import json
import logging
import random
from typing import Dict, List, Any, Optional

# Import the emotional intelligence module
from emotional_intelligence import emotional_intelligence

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("context_engine")

class ContextEngine:
    """The context monitoring system for the VoyagerVerse agentic AI.
    
    This class is responsible for:
    1. Monitoring real-time environmental conditions (weather, time, location)
    2. Tracking traveler state (energy, preferences, history)
    3. Providing contextual awareness to the agentic core
    """
    
    def __init__(self):
        self.current_context = {}
        self.context_history = []
        self.last_update = datetime.datetime.now()
        self.emotional_intelligence = emotional_intelligence  # Use the singleton instance
        self.weather_providers = ["OpenWeatherMap", "AccuWeather", "WeatherAPI"]
        self.location_providers = ["Google Maps", "Here Maps", "TomTom"]
        self.last_update = datetime.datetime.now()
        self.update_frequency = datetime.timedelta(minutes=30)  # Check every 30 minutes
        
        # Initialize with default values
        self._initialize_default_context()
    
    def _initialize_default_context(self):
        """Set up default context values."""
        self.current_context = {
            "timestamp": datetime.datetime.now().isoformat(),
            "weather": {
                "temperature": 35,
                "humidity": 60,
                "precipitation_chance": 0.1,
                "uv_index": 7,
                "wind_speed": 10,
                "conditions": "sunny"
            },
            "location": {
                "city": "Dubai",
                "district": "Downtown Dubai",
                "coordinates": {"lat": 25.2048, "lng": 55.2708},
                "current_venue": "Hotel"
            },
            "time_context": {
                "local_time": datetime.datetime.now().isoformat(),
                "day_of_week": datetime.datetime.now().strftime("%A"),
                "is_weekend": datetime.datetime.now().weekday() >= 5,
                "is_holiday": False,
                "prayer_times": self._get_prayer_times()
            },
            "traveler_state": {
                "energy_level": 1.0,  # Full energy
                "last_meal_time": (datetime.datetime.now() - datetime.timedelta(hours=3)).isoformat(),
                "meal_count_today": 1,
                "step_count": 2000,
                "preferences": {}
            }
        }
    
    def _get_prayer_times(self) -> Dict[str, str]:
        """Get Islamic prayer times for Dubai (important cultural context)."""
        # In a real implementation, this would call a prayer times API
        # For the prototype, we'll use static times
        return {
            "fajr": "04:45",
            "dhuhr": "12:23",
            "asr": "15:43",
            "maghrib": "18:32",
            "isha": "19:46"
        }
    
    def update_weather(self, force_update: bool = False) -> Dict[str, Any]:
        """Update weather information from weather provider."""
        now = datetime.datetime.now()
        
        # Only update if enough time has passed or force update is requested
        if force_update or now - self.last_update >= self.update_frequency:
            logger.info("Updating weather information")
            
            # In a real implementation, this would call a weather API
            # For the prototype, we'll simulate weather data
            weather_provider = random.choice(self.weather_providers)
            logger.info(f"Using weather provider: {weather_provider}")
            
            # Store previous weather for comparison
            self.current_context["last_weather_check"] = self.current_context.get("weather", {})
            
            # Simulate updated weather
            self.current_context["weather"] = self._simulate_weather()
            self.last_update = now
        
        return self.current_context["weather"]
    
    def _simulate_weather(self) -> Dict[str, Any]:
        """Simulate weather data for Dubai."""
        # Base on previous weather if available
        prev_weather = self.current_context.get("weather", {})
        prev_temp = prev_weather.get("temperature", 35)
        
        # Simulate temperature changes
        hour_of_day = datetime.datetime.now().hour
        is_daytime = 7 <= hour_of_day <= 18
        
        # Dubai temperature patterns
        if is_daytime:
            base_temp = random.uniform(35, 45)  # Hot daytime
        else:
            base_temp = random.uniform(25, 32)  # Cooler evening
        
        # Add some randomness but keep it realistic
        temperature = round(base_temp + random.uniform(-2, 2), 1)
        
        # Other weather attributes
        humidity = round(random.uniform(50, 80), 1)
        precipitation_chance = round(random.uniform(0, 0.2), 2)  # Dubai is usually dry
        uv_index = random.randint(7, 11) if is_daytime else random.randint(0, 3)
        wind_speed = round(random.uniform(5, 20), 1)
        
        # Conditions based on other factors
        if precipitation_chance > 0.15:
            conditions = "light rain"
        elif humidity > 70 and temperature > 40:
            conditions = "hazy"
        else:
            conditions = "sunny"
        
        return {
            "temperature": temperature,
            "humidity": humidity,
            "precipitation_chance": precipitation_chance,
            "uv_index": uv_index,
            "wind_speed": wind_speed,
            "conditions": conditions,
            "data_source": f"{random.choice(self.weather_providers)}",
            "last_updated": datetime.datetime.now().isoformat()
        }
    
    def update_traveler_state(self, traveler_state: Dict[str, Any], biometric_data: Optional[Dict[str, Any]] = None,
                             speech_data: Optional[Dict[str, Any]] = None, facial_data: Optional[Dict[str, Any]] = None,
                             behavioral_data: Optional[Dict[str, Any]] = None) -> None:
        """Update the traveler's current state including emotional and physiological data.
        
        Args:
            traveler_state: Dictionary containing traveler state information
            biometric_data: Optional biometric readings from wearables
            speech_data: Optional speech pattern analysis
            facial_data: Optional facial expression analysis
            behavioral_data: Optional behavioral pattern analysis
        """
        if 'traveler_state' not in self.current_context:
            self.current_context['traveler_state'] = {}
            
        # Update basic traveler state
        self.current_context['traveler_state'].update(traveler_state)
        self.current_context['traveler_state']['last_updated'] = datetime.datetime.now().isoformat()
        
        # Process emotional and physiological data if available
        if any([biometric_data, speech_data, facial_data, behavioral_data]):
            emotional_state = self.emotional_intelligence.update_emotional_state(
                biometric_data=biometric_data,
                speech_data=speech_data,
                facial_data=facial_data,
                behavioral_data=behavioral_data
            )
            
            # Add emotional state to traveler state
            self.current_context['traveler_state']['emotional_state'] = emotional_state
            
            # Get adaptation recommendations
            adaptation_recommendations = self.emotional_intelligence.get_adaptation_recommendations()
            self.current_context['traveler_state']['adaptation_recommendations'] = adaptation_recommendations
            
            logger.info(f"Updated traveler emotional state: {emotional_state}")
            logger.info(f"Adaptation recommendations: {adaptation_recommendations}")
        
        logger.info(f"Updated traveler state: {traveler_state}")
    
    def _simulate_traveler_state_changes(self):
        """Simulate natural changes in traveler state over time."""
        traveler_state = self.current_context.get("traveler_state", {})
        
        # Energy level decreases over time and with activity
        current_energy = traveler_state.get("energy_level", 1.0)
        time_factor = 0.05  # Natural energy decline
        activity_factor = 0.0
        
        # If recent activities, factor in their energy impact
        current_plan = self.current_context.get("current_plan", {})
        for activity in current_plan.get("activities", []):
            if "energy_required" in activity:
                activity_factor += activity.get("energy_required", 0) * 0.1
        
        # Calculate new energy level
        new_energy = max(0.1, current_energy - time_factor - activity_factor)
        
        # Meal times affect energy
        last_meal_time = traveler_state.get("last_meal_time")
        if last_meal_time:
            last_meal_dt = datetime.datetime.fromisoformat(last_meal_time)
            hours_since_meal = (datetime.datetime.now() - last_meal_dt).total_seconds() / 3600
            
            if hours_since_meal > 5:  # More than 5 hours since last meal
                new_energy -= 0.1  # Additional energy decrease due to hunger
        
        # Update the state
        traveler_state["energy_level"] = round(new_energy, 2)
        self.current_context["traveler_state"] = traveler_state
    
    def update_location(self, location_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update the traveler's current location."""
        if location_data:
            self.current_context["location"] = location_data
        else:
            # In a real implementation, this would use device GPS
            # For the prototype, we'll keep the existing location
            pass
        
        return self.current_context["location"]
    
    def update_time_context(self) -> Dict[str, Any]:
        """Update time-related context information."""
        now = datetime.datetime.now()
        
        self.current_context["time_context"] = {
            "local_time": now.isoformat(),
            "day_of_week": now.strftime("%A"),
            "is_weekend": now.weekday() >= 5,
            "is_holiday": self._check_if_holiday(now),
            "prayer_times": self._get_prayer_times(),
            "time_of_day": self._get_time_of_day(now)
        }
        
        return self.current_context["time_context"]
    
    def _check_if_holiday(self, date: datetime.datetime) -> bool:
        """Check if the given date is a holiday in Dubai."""
        # In a real implementation, this would check against a holiday calendar
        # For the prototype, we'll assume no holidays
        return False
    
    def _get_time_of_day(self, time: datetime.datetime) -> str:
        """Categorize the time of day."""
        hour = time.hour
        
        if 5 <= hour < 8:
            return "early_morning"
        elif 8 <= hour < 12:
            return "morning"
        elif 12 <= hour < 15:
            return "midday"
        elif 15 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get the current context."""
        return self.current_context
    
    def get_activity_compatibility(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate how compatible an activity is with current context."""
        context = self.get_current_context()
        compatibility = {
            "overall_score": 1.0,  # Start with perfect compatibility
            "factors": {}
        }
        
        # Check weather compatibility
        weather_score = self._check_weather_compatibility(activity, context["weather"])
        compatibility["factors"]["weather"] = weather_score
        
        # Check time compatibility
        time_score = self._check_time_compatibility(activity, context["time_context"])
        compatibility["factors"]["time"] = time_score
        
        # Check energy compatibility
        energy_score = self._check_energy_compatibility(activity, context["traveler_state"])
        compatibility["factors"]["energy"] = energy_score
        
        # Calculate overall score (weighted average)
        compatibility["overall_score"] = (
            weather_score * 0.4 +  # Weather is important in Dubai
            time_score * 0.3 +
            energy_score * 0.3
        )
        
        return compatibility
    
    def _check_weather_compatibility(self, activity: Dict[str, Any], weather: Dict[str, Any]) -> float:
        """Check how compatible the weather is with the activity."""
        if not activity.get("is_outdoor", False):
            return 1.0  # Indoor activities are always weather-compatible
        
        # Check temperature
        temp = weather.get("temperature", 35)
        if temp > 42:  # Extremely hot
            return 0.2  # Very poor compatibility
        elif temp > 38:  # Very hot
            return 0.5  # Poor compatibility
        elif temp > 32:  # Hot but tolerable
            return 0.8  # Decent compatibility
        else:  # Comfortable
            return 1.0  # Perfect compatibility
    
    def _check_time_compatibility(self, activity: Dict[str, Any], time_context: Dict[str, Any]) -> float:
        """Check how compatible the current time is with the activity."""
        time_of_day = time_context.get("time_of_day")
        
        # Some activities are better at specific times
        if activity.get("category") == "adventure" and time_of_day in ["midday", "afternoon"] and activity.get("is_outdoor", False):
            return 0.6  # Outdoor adventures not ideal in midday heat
        
        # Check prayer times for cultural sensitivity
        if time_of_day in ["morning", "midday", "afternoon"] and activity.get("category") == "culture":
            return 1.0  # Cultural activities good during day
        
        # Evening activities
        if time_of_day in ["evening", "night"] and activity.get("category") in ["dining", "entertainment"]:
            return 1.0  # Perfect for evening
        
        # Default is neutral compatibility
        return 0.8
    
    def _check_energy_compatibility(self, activity: Dict[str, Any], traveler_state: Dict[str, Any]) -> float:
        """Check how compatible the traveler's energy level is with the activity."""
        energy_level = traveler_state.get("energy_level", 1.0)
        activity_energy = activity.get("energy_required", 0.5)
        
        if energy_level < activity_energy - 0.3:
            return 0.3  # Very poor compatibility
        elif energy_level < activity_energy - 0.1:
            return 0.6  # Poor compatibility
        elif energy_level < activity_energy:
            return 0.8  # Decent compatibility
        else:
            return 1.0  # Perfect compatibility

# Example usage for Tom & Priya scenario
def create_tom_priya_context():
    """Create a sample context for Tom & Priya's Dubai vacation."""
    context_engine = ContextEngine()
    
    # Set up specific context for the scenario
    context_engine.current_context.update({
        "weather": {
            "temperature": 43,  # Extremely hot
            "humidity": 65,
            "precipitation_chance": 0.05,
            "uv_index": 9,
            "wind_speed": 12,
            "conditions": "sunny"
        },
        "traveler_state": {
            "energy_level": 0.8,  # Good energy
            "last_meal_time": (datetime.datetime.now() - datetime.timedelta(hours=2)).isoformat(),
            "meal_count_today": 2,
            "step_count": 4500,
            "preferences": {
                "max_comfortable_temperature": 38,
                "preferred_activity_pace": "moderate",
                "cuisine_preferences": ["local", "indian", "mediterranean"],
                "avoid_crowds": True
            }
        },
        "current_plan": {
            "day": 3,
            "date": "2025-04-25",
            "activities": [
                {
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
                    "name": "Bedouin Dinner Experience",
                    "time": "19:00-21:30",
                    "location": "Desert Camp",
                    "description": "Authentic Bedouin dinner under the stars with cultural performances",
                    "category": "culture",
                    "is_outdoor": True,
                    "energy_required": 0.4,
                    "booking_reference": "BD67890"
                }
            ]
        }
    })
    
    # Get full context
    full_context = context_engine.get_current_context()
    
    # Check compatibility of the desert safari activity
    desert_safari = full_context["current_plan"]["activities"][0]
    compatibility = context_engine.get_activity_compatibility(desert_safari)
    
    return {
        "full_context": full_context,
        "activity_compatibility": compatibility
    }

if __name__ == "__main__":
    # This can be used for testing the module independently
    scenario_context = create_tom_priya_context()
    print(json.dumps(scenario_context["activity_compatibility"], indent=2))
