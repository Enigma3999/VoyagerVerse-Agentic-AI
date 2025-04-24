import json
import logging
import datetime
from typing import Dict, List, Optional, Tuple, Any

# Import the AI model for enhanced capabilities
from ai_model import generate_explanation, generate_alternative_activities, analyze_activity_safety, personalize_recommendation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agentic_core")

class Goal:
    """Represents a high-level traveler goal with measurable success criteria."""
    def __init__(self, name: str, description: str, priority: int = 1, success_criteria: Dict[str, Any] = None):
        self.name = name
        self.description = description
        self.priority = priority  # 1-10, with 10 being highest
        self.success_criteria = success_criteria or {}
        self.satisfaction_score = 0.0  # 0-1 score of how well this goal is being met
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "success_criteria": self.success_criteria,
            "satisfaction_score": self.satisfaction_score
        }

class AgenticCore:
    """The core decision-making engine for the VoyagerVerse agentic AI system.
    
    This class implements true agentic capabilities including:
    - Goal management
    - Autonomous decision-making
    - Self-reflection
    - Proactive problem-solving
    """
    def __init__(self):
        self.traveler_goals = []  # List of Goal objects
        self.current_context = {}  # Current environmental context
        self.decision_history = []  # History of decisions for self-reflection
        self.confidence_threshold = 0.7  # Threshold for autonomous decisions
        self.reflection_interval = datetime.timedelta(hours=6)  # How often to reflect
        self.last_reflection = datetime.datetime.now()
    
    def add_goal(self, goal: Goal) -> None:
        """Add a new traveler goal to the system."""
        self.traveler_goals.append(goal)
        logger.info(f"Added new goal: {goal.name}")
    
    def update_context(self, context_data: Dict[str, Any]) -> None:
        """Update the current environmental and traveler context."""
        self.current_context.update(context_data)
        logger.info(f"Updated context with {len(context_data)} new data points")
        
        # Check if context update should trigger decision-making
        if self._should_reevaluate_plans():
            self.evaluate_current_plan()
    
    def _should_reevaluate_plans(self) -> bool:
        """Determine if current plans should be reevaluated based on context changes."""
        # Check for significant weather changes
        if 'weather' in self.current_context and self.current_context.get('last_weather_check'):
            current_temp = self.current_context['weather'].get('temperature')
            previous_temp = self.current_context.get('last_weather_check', {}).get('temperature')
            
            if current_temp and previous_temp and abs(current_temp - previous_temp) > 5:
                logger.info(f"Significant temperature change detected: {previous_temp}°C -> {current_temp}°C")
                return True
        
        # Check for energy level changes
        if 'traveler_state' in self.current_context:
            energy_level = self.current_context['traveler_state'].get('energy_level')
            if energy_level and energy_level < 0.4:  # If energy is low
                logger.info(f"Low traveler energy detected: {energy_level}")
                return True
        
        return False
    
    def evaluate_current_plan(self) -> Dict[str, Any]:
        """Evaluate if the current plan is still optimal given the updated context."""
        current_plan = self.current_context.get('current_plan', {})
        if not current_plan:
            logger.warning("No current plan found in context")
            return {}
        
        # Check for weather incompatibility
        weather_issue = self._check_weather_compatibility(current_plan)
        if weather_issue:
            return self._generate_alternative_plan(current_plan, issue="weather")
        
        # Check for energy level compatibility
        energy_issue = self._check_energy_compatibility(current_plan)
        if energy_issue:
            return self._generate_alternative_plan(current_plan, issue="energy")
        
        # If we reach here, current plan is still valid
        return current_plan
    
    def _check_weather_compatibility(self, plan: Dict[str, Any]) -> bool:
        """Check if current weather is compatible with planned activities using AI for complex cases."""
        if 'weather' not in self.current_context:
            return False
        
        weather = self.current_context['weather']
        temperature = weather.get('temperature')
        condition = weather.get('condition', '').lower()
        
        # Quick check for obvious cases
        obvious_incompatibility = False
        
        # Check for extreme temperatures
        if temperature and temperature > 40:  # Very hot
            for activity in plan.get('activities', []):
                if activity.get('is_outdoor', False):
                    logger.info(f"Weather incompatibility detected: {temperature}°C is too hot for {activity.get('name', 'outdoor activity')}")
                    obvious_incompatibility = True
        
        # Check for rain
        if 'rain' in condition or 'storm' in condition:
            for activity in plan.get('activities', []):
                if activity.get('is_outdoor', False):
                    logger.info(f"Weather incompatibility detected: {condition} is not suitable for {activity.get('name', 'outdoor activity')}")
                    obvious_incompatibility = True
        
        if obvious_incompatibility:
            return True
            
        # For more complex cases, use the AI model
        try:
            for activity in plan.get('activities', []):
                # Skip indoor activities for efficiency
                if not activity.get('is_outdoor', False):
                    continue
                    
                # Prepare data for AI analysis
                activity_data = {
                    "name": activity.get('name', 'Unknown activity'),
                    "is_outdoor": activity.get('is_outdoor', False),
                    "temperature": temperature,
                    "weather_condition": condition,
                    "traveler_health": self.current_context.get('traveler_state', {}).get('health_status', 'good')
                }
                
                # Get AI safety analysis
                safety_assessment = analyze_activity_safety(activity_data)
                
                if safety_assessment and not safety_assessment.get('is_safe', True):
                    logger.info(f"AI detected weather incompatibility: {safety_assessment.get('reason', 'Unknown reason')} for {activity.get('name', 'activity')}")
                    return True
        except Exception as e:
            logger.error(f"Error using AI for weather compatibility check: {e}")
            # Continue with rule-based approach if AI fails
        
        return False
    
    def _check_energy_compatibility(self, plan: Dict[str, Any]) -> bool:
        """Check if traveler's energy level is compatible with planned activities."""
        if 'traveler_state' not in self.current_context:
            return False
        
        energy_level = self.current_context['traveler_state'].get('energy_level')
        
        # Check if any high-energy activities are planned when energy is low
        for activity in plan.get('activities', []):
            if activity.get('energy_required', 0.5) > 0.7 and energy_level < 0.4:
                logger.info(f"Traveler energy too low ({energy_level}) for high-energy activity: {activity.get('name')}")
                return True
        
        return False
    
    def _generate_alternative_plan(self, original_plan: Dict[str, Any], issue: str) -> Dict[str, Any]:
        """Generate an alternative plan based on the identified issue."""
        # Create a copy of the original plan to modify
        new_plan = original_plan.copy()
        new_plan['activities'] = original_plan.get('activities', []).copy()
        new_plan['is_modified'] = True
        new_plan['modification_reason'] = issue
        
        if issue == "weather":
            # Replace outdoor activities with indoor alternatives
            for i, activity in enumerate(new_plan['activities']):
                if activity.get('is_outdoor', False):
                    # Find an indoor alternative with similar theme
                    alternative = self._find_alternative_activity(
                        activity, 
                        constraints={"is_outdoor": False}
                    )
                    if alternative:
                        new_plan['activities'][i] = alternative
                        logger.info(f"Replaced outdoor activity '{activity.get('name')}' with '{alternative.get('name')}'")
        
        elif issue == "energy":
            # Replace high-energy activities with lower-energy alternatives
            for i, activity in enumerate(new_plan['activities']):
                if activity.get('energy_required', 0.5) > 0.7:
                    # Find a lower-energy alternative
                    alternative = self._find_alternative_activity(
                        activity, 
                        constraints={"energy_required_max": 0.5}
                    )
                    if alternative:
                        new_plan['activities'][i] = alternative
                        logger.info(f"Replaced high-energy activity '{activity.get('name')}' with '{alternative.get('name')}'")
        
        # Record this decision for self-reflection
        self._record_decision({
            "original_plan": original_plan,
            "new_plan": new_plan,
            "issue": issue,
            "timestamp": datetime.datetime.now().isoformat(),
            "context": self.current_context
        })
        
        return new_plan
    
    def _find_alternative_activity(self, original_activity: Dict[str, Any], constraints: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find an alternative activity that meets the given constraints using AI."""
        # Try to use the AI model to generate alternatives
        try:
            # Enhance constraints with current context
            enhanced_constraints = {
                **constraints,
                "weather": self.current_context.get("weather", {}),
                "preferences": self.current_context.get("preferences", {}).get("activity_preferences", []),
                "budget_level": self.current_context.get("preferences", {}).get("budget_level", "standard")
            }
            
            # Get AI-generated alternatives
            alternatives = generate_alternative_activities(enhanced_constraints)
            
            if alternatives and len(alternatives) > 0:
                # Use the first alternative as default
                best_alternative = alternatives[0]
                
                # If we have multiple alternatives, use AI to personalize the selection
                if len(alternatives) > 1:
                    user_data = {
                        "preferences": self.current_context.get("preferences", {}),
                        "history": self.decision_history[-10:] if len(self.decision_history) > 0 else []
                    }
                    
                    personalized = personalize_recommendation(user_data, alternatives)
                    if personalized and personalized.get("recommendation"):
                        best_alternative = personalized.get("recommendation")
                
                logger.info(f"AI generated alternative activity: {best_alternative.get('name', 'Unknown')}")
                return best_alternative
                
        except Exception as e:
            logger.error(f"Error using AI for alternative activity generation: {e}")
            # Fall back to rule-based alternatives if AI fails
        
        # Rule-based fallback alternatives
        if constraints.get("is_outdoor") is False and original_activity.get("category") == "adventure":
            return {
                "name": "Dubai Museum Cultural Tour",
                "description": "Explore Dubai's rich cultural heritage in the air-conditioned Dubai Museum",
                "location": "Al Fahidi Historical District",
                "duration_hours": 2,
                "category": "culture",
                "is_outdoor": False,
                "energy_required": 0.4,
                "price_range": "$$",
                "booking_required": True,
                "booking_details": {
                    "provider": "Dubai Tourism",
                    "availability": ["10:00", "13:00", "16:00"]
                }
            }

        if constraints.get("energy_required_max", 1.0) < 0.6 and original_activity.get("energy_required", 0.5) > 0.7:
            return {
                "name": "Luxury Spa Experience",
                "description": "Relax and rejuvenate with a premium spa treatment",
                "location": "Five Palm Jumeirah Dubai",
                "duration_hours": 2,
                "category": "relaxation",
                "is_outdoor": False,
                "energy_required": 0.2,
                "price_range": "$$$",
                "booking_required": True,
                "booking_details": {
                    "provider": "Five Palm Jumeirah",
                    "availability": ["11:00", "14:00", "17:00"]
                }
            }

        return None
    
    def _record_decision(self, decision_data: Dict[str, Any]) -> None:
        """Record a decision for later self-reflection."""
        self.decision_history.append(decision_data)
        
        # Check if it's time for self-reflection
        now = datetime.datetime.now()
        if now - self.last_reflection >= self.reflection_interval:
            self._perform_self_reflection()
            self.last_reflection = now
    
    def _perform_self_reflection(self) -> None:
        """Analyze past decisions to improve future decision-making."""
        if len(self.decision_history) < 3:
            logger.info("Not enough decision history for meaningful reflection")
            return
        
        # Analyze recent decisions for patterns
        recent_decisions = self.decision_history[-10:]
        weather_changes = sum(1 for d in recent_decisions if d.get("issue") == "weather")
        energy_changes = sum(1 for d in recent_decisions if d.get("issue") == "energy")
        
        # Adjust thresholds based on patterns
        if weather_changes > 5:  # Many weather-based changes
            logger.info("Reflection: Many weather-based changes detected. Adjusting planning to be more conservative with outdoor activities.")
            # In a real implementation, this would update planning parameters
        
        if energy_changes > 5:  # Many energy-based changes
            logger.info("Reflection: Many energy-based changes detected. Adjusting daily activity count downward.")
            # In a real implementation, this would update planning parameters
    
    def explain_decision(self, decision_id: int) -> str:
        """Generate a natural language explanation of a decision using the AI model."""
        if not self.decision_history or decision_id >= len(self.decision_history):
            return "No decision found with that ID."
        
        decision = self.decision_history[decision_id]
        
        # Add current weather context to the decision data
        decision_data = {
            **decision,
            "weather": self.current_context.get("weather", {})
        }
        
        # Use the AI model to generate a natural language explanation
        try:
            explanation = generate_explanation(decision_data)
            return explanation
        except Exception as e:
            logger.error(f"Error using AI model for explanation: {e}")
            
            # Fallback to rule-based explanation if AI fails
            decision_type = decision.get("type", "unknown")
            reason = decision.get("reason", "unknown")
            
            if decision_type == "itinerary_change" and reason == "weather":
                return "I noticed that the weather conditions would make your planned activity uncomfortable or unsafe. I've suggested an alternative indoor activity that aligns with your preferences."
            elif decision_type == "itinerary_change" and reason == "energy":
                return "I noticed that your energy levels might make your planned activity too strenuous. I've suggested a more relaxing alternative that still provides an enjoyable experience."
            else:
                return f"I made a change to your itinerary due to {reason}. The new plan should better accommodate your current situation."
    
    def get_confidence_score(self, decision: Dict[str, Any]) -> float:
        """Calculate confidence score for a decision to determine if user approval is needed."""
        # Base confidence score
        confidence = 0.5
        
        # Increase confidence for weather-related changes (more objective)
        if decision.get("issue") == "weather":
            confidence += 0.3
            
            # If extreme weather, even higher confidence
            temp = decision.get("context", {}).get("weather", {}).get("temperature")
            if temp and temp > 42:
                confidence += 0.1
        
        # Lower confidence for subjective changes like energy levels
        if decision.get("issue") == "energy":
            confidence -= 0.1
        
        # Adjust based on how many similar decisions have been accepted before
        similar_decisions = [d for d in self.decision_history if d.get("issue") == decision.get("issue")]
        accepted_count = sum(1 for d in similar_decisions if d.get("was_accepted", False))
        
        if len(similar_decisions) > 0:
            acceptance_rate = accepted_count / len(similar_decisions)
            confidence += (acceptance_rate - 0.5) * 0.2  # Adjust by at most ±0.1
        
        return min(max(confidence, 0.0), 1.0)  # Ensure between 0 and 1

# Example usage for Tom & Priya scenario
def create_tom_priya_scenario():
    """Create a sample scenario for Tom & Priya's Dubai vacation."""
    core = AgenticCore()
    
    # Add their goals
    core.add_goal(Goal(
        name="Experience local culture",
        description="Discover authentic Dubai cultural experiences",
        priority=8,
        success_criteria={"min_cultural_activities": 3}
    ))
    
    core.add_goal(Goal(
        name="Culinary exploration",
        description="Try diverse local and international cuisine",
        priority=7,
        success_criteria={"min_unique_cuisines": 4}
    ))
    
    core.add_goal(Goal(
        name="Light adventure",
        description="Experience exciting but not physically demanding activities",
        priority=6,
        success_criteria={"min_adventure_activities": 2}
    ))
    
    # Set up their current plan
    current_plan = {
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
    
    # Update context with extreme heat
    core.update_context({
        "current_plan": current_plan,
        "weather": {
            "temperature": 43,
            "humidity": 65,
            "precipitation_chance": 0.05,
            "uv_index": 9
        },
        "last_weather_check": {
            "temperature": 36,
            "humidity": 60,
            "precipitation_chance": 0.0,
            "uv_index": 8
        },
        "traveler_state": {
            "energy_level": 0.8,
            "last_meal_time": "12:30",
            "preferences": {
                "max_comfortable_temperature": 38,
                "preferred_activity_pace": "moderate"
            }
        }
    })
    
    # This should trigger a reevaluation
    new_plan = core.evaluate_current_plan()
    
    # Get explanation for the most recent decision
    explanation = core.explain_decision(len(core.decision_history) - 1)
    
    return {
        "original_plan": current_plan,
        "new_plan": new_plan,
        "explanation": explanation,
        "confidence": core.get_confidence_score(core.decision_history[-1])
    }

if __name__ == "__main__":
    # This can be used for testing the module independently
    scenario_result = create_tom_priya_scenario()
    print(json.dumps(scenario_result, indent=2))
