import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("preference_system")

class PreferenceSystem:
    """The preference learning and management system for the VoyagerVerse agentic AI.
    
    This class is responsible for:
    1. Learning traveler preferences from minimal input
    2. Tracking preference evolution throughout the trip
    3. Providing personalized recommendations based on learned preferences
    4. Balancing exploration and exploitation in recommendations
    """
    
    def __init__(self):
        self.preference_model = {}
        self.preference_history = []
        self.feedback_history = []
        self.confidence_scores = {}
        self.exploration_rate = 0.2  # 20% chance of recommending something outside comfort zone
        self.last_update = datetime.datetime.now()
    
    def initialize_preferences(self, initial_preferences: Dict[str, Any]) -> None:
        """Initialize the preference model with explicit preferences."""
        self.preference_model = initial_preferences.copy()
        
        # Record this as the first preference state
        self._record_preference_state("initial_setup")
        
        logger.info(f"Initialized preference model with {len(initial_preferences)} attributes")
    
    def _record_preference_state(self, trigger: str) -> None:
        """Record the current state of preferences for tracking evolution."""
        self.preference_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "trigger": trigger,
            "preferences": self.preference_model.copy(),
            "confidence_scores": self.confidence_scores.copy()
        })
    
    def get_preferences(self, traveler_id: str = None) -> Dict[str, Any]:
        """Get the current preference model."""
        # In a more complex implementation, we would retrieve preferences specific to the traveler_id
        # For now, we'll just return the current preference model
        return self.preference_model
        
    def update_from_explicit_feedback(self, feedback: Dict[str, Any]) -> None:
        """Update preferences based on explicit traveler feedback."""
        # Record the feedback
        self.feedback_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "explicit",
            "content": feedback
        })
        
        # Update preference model
        for category, value in feedback.items():
            if category in self.preference_model:
                # For list-type preferences (e.g., cuisine_preferences)
                if isinstance(self.preference_model[category], list) and isinstance(value, list):
                    # Add new items while keeping existing ones
                    self.preference_model[category] = list(set(self.preference_model[category] + value))
                    
                    # Update confidence
                    self.confidence_scores[category] = min(1.0, self.confidence_scores.get(category, 0.5) + 0.2)
                
                # For numeric preferences (e.g., preferred_activity_pace)
                elif isinstance(self.preference_model[category], (int, float)) and isinstance(value, (int, float)):
                    # Weighted average with new value (giving more weight to explicit feedback)
                    current_confidence = self.confidence_scores.get(category, 0.5)
                    self.preference_model[category] = (
                        self.preference_model[category] * current_confidence + 
                        value * 0.8
                    ) / (current_confidence + 0.8)
                    
                    # Update confidence
                    self.confidence_scores[category] = min(1.0, current_confidence + 0.2)
                
                # For boolean preferences (e.g., avoid_crowds)
                elif isinstance(self.preference_model[category], bool) and isinstance(value, bool):
                    # Direct update for booleans
                    self.preference_model[category] = value
                    self.confidence_scores[category] = 1.0  # High confidence for explicit boolean preferences
                
                # For string preferences (e.g., preferred_cuisine)
                elif isinstance(self.preference_model[category], str) and isinstance(value, str):
                    # Direct update for strings
                    self.preference_model[category] = value
                    self.confidence_scores[category] = 1.0  # High confidence for explicit string preferences
            else:
                # New preference category
                self.preference_model[category] = value
                self.confidence_scores[category] = 0.8  # High initial confidence for explicit feedback
        
        # Record the updated state
        self._record_preference_state("explicit_feedback")
        
        logger.info(f"Updated preference model with explicit feedback on {len(feedback)} attributes")
    
    def update_from_implicit_feedback(self, activity: Dict[str, Any], reaction: str) -> None:
        """Update preferences based on implicit feedback (reactions to activities)."""
        # Record the feedback
        self.feedback_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "implicit",
            "activity": activity,
            "reaction": reaction
        })
        
        # Map reaction to a numeric score
        reaction_scores = {
            "loved": 1.0,
            "liked": 0.75,
            "neutral": 0.5,
            "disliked": 0.25,
            "hated": 0.0
        }
        score = reaction_scores.get(reaction, 0.5)
        
        # Extract activity attributes for preference learning
        category = activity.get("category")
        is_outdoor = activity.get("is_outdoor", False)
        energy_required = activity.get("energy_required", 0.5)
        price_range = activity.get("price_range", "$$")
        
        # Update category preferences
        if category:
            category_key = f"category_{category}_score"
            current_score = self.preference_model.get(category_key, 0.5)
            current_confidence = self.confidence_scores.get(category_key, 0.3)
            
            # Update with weighted average
            self.preference_model[category_key] = (
                current_score * current_confidence + 
                score * 0.3
            ) / (current_confidence + 0.3)
            
            # Update confidence
            self.confidence_scores[category_key] = min(0.9, current_confidence + 0.1)  # Cap at 0.9 for implicit
        
        # Update outdoor preference
        outdoor_key = "outdoor_preference"
        if is_outdoor:
            current_score = self.preference_model.get(outdoor_key, 0.5)
            current_confidence = self.confidence_scores.get(outdoor_key, 0.3)
            
            # Update with weighted average
            self.preference_model[outdoor_key] = (
                current_score * current_confidence + 
                score * 0.3
            ) / (current_confidence + 0.3)
            
            # Update confidence
            self.confidence_scores[outdoor_key] = min(0.9, current_confidence + 0.1)
        
        # Update energy preference
        if energy_required:
            # If they liked a high-energy activity, they probably like active experiences
            if score > 0.6 and energy_required > 0.6:
                self.preference_model["preferred_activity_pace"] = "active"
                self.confidence_scores["preferred_activity_pace"] = min(0.9, self.confidence_scores.get("preferred_activity_pace", 0.3) + 0.1)
            
            # If they disliked a high-energy activity, they might prefer relaxed experiences
            elif score < 0.4 and energy_required > 0.6:
                self.preference_model["preferred_activity_pace"] = "relaxed"
                self.confidence_scores["preferred_activity_pace"] = min(0.9, self.confidence_scores.get("preferred_activity_pace", 0.3) + 0.1)
        
        # Update price range preference
        if price_range and score > 0.7:  # Only update if they really liked it
            price_key = "preferred_price_range"
            self.preference_model[price_key] = price_range
            self.confidence_scores[price_key] = min(0.8, self.confidence_scores.get(price_key, 0.3) + 0.1)
        
        # Record the updated state
        self._record_preference_state("implicit_feedback")
        
        logger.info(f"Updated preference model based on {reaction} reaction to {activity.get('name')}")
    
    def update_from_natural_language(self, message: str) -> None:
        """Extract preferences from natural language messages."""
        # Record the message
        self.feedback_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "natural_language",
            "message": message
        })
        
        # In a real implementation, this would use NLP to extract preferences
        # For the prototype, we'll use simple keyword matching
        
        # Check for temperature preferences
        if "too hot" in message.lower() or "very hot" in message.lower():
            self.preference_model["max_comfortable_temperature"] = 35  # Lower temperature threshold
            self.confidence_scores["max_comfortable_temperature"] = 0.7
        
        # Check for activity pace preferences
        if "tired" in message.lower() or "exhausted" in message.lower():
            self.preference_model["preferred_activity_pace"] = "relaxed"
            self.confidence_scores["preferred_activity_pace"] = 0.7
        elif "bored" in message.lower() or "more adventure" in message.lower():
            self.preference_model["preferred_activity_pace"] = "active"
            self.confidence_scores["preferred_activity_pace"] = 0.7
        
        # Check for cuisine preferences
        if "love" in message.lower() and "food" in message.lower():
            if "spicy" in message.lower():
                if "cuisine_preferences" not in self.preference_model:
                    self.preference_model["cuisine_preferences"] = []
                if "indian" not in self.preference_model.get("cuisine_preferences", []):
                    self.preference_model["cuisine_preferences"].append("indian")
                if "thai" not in self.preference_model.get("cuisine_preferences", []):
                    self.preference_model["cuisine_preferences"].append("thai")
                self.confidence_scores["cuisine_preferences"] = 0.7
        
        # Record the updated state
        self._record_preference_state("natural_language")
        
        logger.info(f"Extracted preferences from natural language message: {message[:50]}...")
    
    def analyze_preference_evolution(self) -> Dict[str, Any]:
        """Analyze how preferences have evolved throughout the trip."""
        if len(self.preference_history) < 2:
            return {"evolution": "insufficient_data"}
        
        evolution_analysis = {}
        first_state = self.preference_history[0]["preferences"]
        current_state = self.preference_model
        
        # Compare each preference between first and current state
        for key in set(list(first_state.keys()) + list(current_state.keys())):
            if key in first_state and key in current_state:
                # Both states have this preference
                if isinstance(first_state[key], (int, float)) and isinstance(current_state[key], (int, float)):
                    # Numeric preference
                    change = current_state[key] - first_state[key]
                    evolution_analysis[key] = {
                        "initial": first_state[key],
                        "current": current_state[key],
                        "change": change,
                        "percent_change": (change / first_state[key]) * 100 if first_state[key] != 0 else float('inf')
                    }
                elif isinstance(first_state[key], list) and isinstance(current_state[key], list):
                    # List preference
                    added = [item for item in current_state[key] if item not in first_state[key]]
                    removed = [item for item in first_state[key] if item not in current_state[key]]
                    evolution_analysis[key] = {
                        "initial": first_state[key],
                        "current": current_state[key],
                        "added": added,
                        "removed": removed
                    }
                else:
                    # Other types (string, bool)
                    evolution_analysis[key] = {
                        "initial": first_state[key],
                        "current": current_state[key],
                        "changed": first_state[key] != current_state[key]
                    }
            elif key in first_state:
                # Only in first state (removed)
                evolution_analysis[key] = {
                    "initial": first_state[key],
                    "current": None,
                    "status": "removed"
                }
            else:
                # Only in current state (added)
                evolution_analysis[key] = {
                    "initial": None,
                    "current": current_state[key],
                    "status": "added"
                }
        
        return {
            "evolution": evolution_analysis,
            "confidence_evolution": self._analyze_confidence_evolution()
        }
    
    def _analyze_confidence_evolution(self) -> Dict[str, Any]:
        """Analyze how confidence in preferences has evolved."""
        if len(self.preference_history) < 2:
            return {"evolution": "insufficient_data"}
        
        first_confidence = self.preference_history[0].get("confidence_scores", {})
        current_confidence = self.confidence_scores
        
        confidence_evolution = {}
        for key in set(list(first_confidence.keys()) + list(current_confidence.keys())):
            if key in first_confidence and key in current_confidence:
                confidence_evolution[key] = {
                    "initial": first_confidence[key],
                    "current": current_confidence[key],
                    "change": current_confidence[key] - first_confidence[key]
                }
            elif key in first_confidence:
                confidence_evolution[key] = {
                    "initial": first_confidence[key],
                    "current": None,
                    "status": "removed"
                }
            else:
                confidence_evolution[key] = {
                    "initial": None,
                    "current": current_confidence[key],
                    "status": "added"
                }
        
        return confidence_evolution
    
    def get_activity_preference_score(self, activity: Dict[str, Any]) -> float:
        """Calculate how well an activity matches the traveler's preferences."""
        if not activity:
            return 0.0
        
        score = 0.5  # Start with neutral score
        factors_considered = 0
        
        # Category preference
        category = activity.get("category")
        if category:
            category_key = f"category_{category}_score"
            if category_key in self.preference_model:
                category_score = self.preference_model[category_key]
                category_confidence = self.confidence_scores.get(category_key, 0.5)
                score += (category_score - 0.5) * category_confidence
                factors_considered += 1
        
        # Outdoor preference
        is_outdoor = activity.get("is_outdoor", False)
        outdoor_key = "outdoor_preference"
        if outdoor_key in self.preference_model:
            if is_outdoor:
                outdoor_score = self.preference_model[outdoor_key]
                outdoor_confidence = self.confidence_scores.get(outdoor_key, 0.5)
                score += (outdoor_score - 0.5) * outdoor_confidence
                factors_considered += 1
        
        # Activity pace preference
        energy_required = activity.get("energy_required", 0.5)
        pace_key = "preferred_activity_pace"
        if pace_key in self.preference_model:
            pace_pref = self.preference_model[pace_key]
            pace_confidence = self.confidence_scores.get(pace_key, 0.5)
            
            # Convert string preference to numeric comparison
            if pace_pref == "active" and energy_required > 0.6:
                score += 0.2 * pace_confidence
            elif pace_pref == "moderate" and 0.4 <= energy_required <= 0.7:
                score += 0.2 * pace_confidence
            elif pace_pref == "relaxed" and energy_required < 0.5:
                score += 0.2 * pace_confidence
            
            factors_considered += 1
        
        # Price range preference
        price_range = activity.get("price_range")
        price_key = "preferred_price_range"
        if price_range and price_key in self.preference_model:
            if price_range == self.preference_model[price_key]:
                price_confidence = self.confidence_scores.get(price_key, 0.5)
                score += 0.1 * price_confidence
                factors_considered += 1
        
        # Normalize score if we considered any factors
        if factors_considered > 0:
            # Ensure score is between 0 and 1
            return max(0.0, min(1.0, score))
        else:
            return 0.5  # Neutral if no preferences matched
    
    def should_explore(self) -> bool:
        """Determine if we should recommend something outside current preferences."""
        import random
        return random.random() < self.exploration_rate
    
    def adjust_exploration_rate(self) -> None:
        """Adjust exploration rate based on trip progress and preference confidence."""
        # As the trip progresses, reduce exploration rate
        days_passed = len(set(f["timestamp"].split("T")[0] for f in self.feedback_history))
        if days_passed > 3:  # More than 3 days into the trip
            self.exploration_rate = max(0.05, self.exploration_rate - 0.05)  # Reduce but keep some exploration
        
        # If confidence is high across preferences, reduce exploration
        avg_confidence = sum(self.confidence_scores.values()) / max(1, len(self.confidence_scores))
        if avg_confidence > 0.8:  # High confidence
            self.exploration_rate = max(0.05, self.exploration_rate - 0.05)
        
        logger.info(f"Adjusted exploration rate to {self.exploration_rate}")

# Example usage for Tom & Priya scenario
def create_tom_priya_preferences():
    """Create a sample preference model for Tom & Priya's Dubai vacation."""
    preference_system = PreferenceSystem()
    
    # Initialize with their known preferences
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
    
    # Set initial confidence scores
    preference_system.confidence_scores = {
        "max_comfortable_temperature": 0.6,
        "preferred_activity_pace": 0.7,
        "cuisine_preferences": 0.8,
        "avoid_crowds": 0.9,
        "category_culture_score": 0.7,
        "category_adventure_score": 0.6,
        "category_relaxation_score": 0.5,
        "outdoor_preference": 0.6,
        "preferred_price_range": 0.8
    }
    
    # Simulate some feedback to evolve preferences
    
    # They loved a cultural activity
    preference_system.update_from_implicit_feedback(
        activity={
            "name": "Old Dubai Cultural Tour",
            "category": "culture",
            "is_outdoor": False,
            "energy_required": 0.4,
            "price_range": "$$$"
        },
        reaction="loved"
    )
    
    # They had a neutral reaction to a high-energy adventure
    preference_system.update_from_implicit_feedback(
        activity={
            "name": "Jet Ski Adventure",
            "category": "adventure",
            "is_outdoor": True,
            "energy_required": 0.9,
            "price_range": "$$$"
        },
        reaction="neutral"
    )
    
    # They mentioned being affected by heat
    preference_system.update_from_natural_language(
        "It was too hot today during our outdoor activities. We'd prefer to do those in the morning or evening."
    )
    
    # Get their current preference model and analyze evolution
    current_preferences = preference_system.preference_model
    preference_evolution = preference_system.analyze_preference_evolution()
    
    # Calculate preference score for desert safari
    desert_safari = {
        "name": "Desert Safari",
        "category": "adventure",
        "is_outdoor": True,
        "energy_required": 0.7,
        "price_range": "$$$"
    }
    safari_score = preference_system.get_activity_preference_score(desert_safari)
    
    # Calculate preference score for museum visit (alternative)
    museum_visit = {
        "name": "Dubai Museum Cultural Tour",
        "category": "culture",
        "is_outdoor": False,
        "energy_required": 0.4,
        "price_range": "$$"
    }
    museum_score = preference_system.get_activity_preference_score(museum_visit)
    
    return {
        "current_preferences": current_preferences,
        "preference_evolution": preference_evolution,
        "activity_scores": {
            "desert_safari": safari_score,
            "museum_visit": museum_score
        }
    }

if __name__ == "__main__":
    # This can be used for testing the module independently
    scenario_preferences = create_tom_priya_preferences()
    print(json.dumps(scenario_preferences["activity_scores"], indent=2))
