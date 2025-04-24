import os
import json
import logging
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

import openai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_model")

# Initialize OpenAI client with API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables. AI model functionality will be limited.")

try:
    client = openai.OpenAI(api_key=api_key) if api_key else None
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {e}")
    client = None

# Fallback responses for when the API is not available
FALLBACK_RESPONSES = {
    "explain_decision": "Based on current conditions, I've adjusted your itinerary to ensure safety and comfort.",
    "generate_alternatives": [
        {"name": "Dubai Museum", "type": "cultural", "location": "Al Fahidi Fort", "is_indoor": True},
        {"name": "Mall of the Emirates", "type": "shopping", "location": "Sheikh Zayed Road", "is_indoor": True},
        {"name": "Burj Khalifa Observation Deck", "type": "attraction", "location": "Downtown Dubai", "is_indoor": True}
    ],
    "analyze_safety": {"is_safe": False, "risk_level": "High", "reason": "Temperature exceeds safety threshold"},
    "personalize_recommendation": "Based on your preferences for cultural experiences and indoor activities during hot weather, I recommend the Dubai Museum."
}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_explanation(decision_data: Dict[str, Any]) -> str:
    """
    Generate a natural language explanation for an agentic decision.
    
    Args:
        decision_data: Dictionary containing decision context and details
        
    Returns:
        A natural language explanation of the decision
    """
    if not client:
        logger.warning("OpenAI client not available. Using fallback response.")
        return FALLBACK_RESPONSES["explain_decision"]
    
    try:
        # Format the decision data for the prompt
        decision_type = decision_data.get("type", "unknown")
        reason = decision_data.get("reason", "")
        original_activity = decision_data.get("original_activity", {})
        new_activity = decision_data.get("new_activity", {})
        weather = decision_data.get("weather", {})
        
        # Create a prompt for the language model
        prompt = f"""As an agentic AI travel assistant, explain the following decision to a traveler in a helpful, 
        conversational way that emphasizes safety and personalization:
        
        Decision Type: {decision_type}
        Reason: {reason}
        Weather: {json.dumps(weather, indent=2)}
        Original Activity: {json.dumps(original_activity, indent=2)}
        New Activity: {json.dumps(new_activity, indent=2)}
        
        Your explanation should be concise, empathetic, and highlight how this decision benefits the traveler.
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are VoyagerVerse, an agentic AI travel assistant that helps travelers adapt to changing conditions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        # Extract and return the explanation
        explanation = response.choices[0].message.content.strip()
        return explanation
    
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        return FALLBACK_RESPONSES["explain_decision"]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_alternative_activities(constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate alternative activities based on constraints using AI.
    
    Args:
        constraints: Dictionary containing constraints like weather, preferences, etc.
        
    Returns:
        A list of alternative activities
    """
    if not client:
        logger.warning("OpenAI client not available. Using fallback alternatives.")
        return FALLBACK_RESPONSES["generate_alternatives"]
    
    try:
        # Format the constraints for the prompt
        weather = constraints.get("weather", {})
        preferences = constraints.get("preferences", [])
        is_outdoor = constraints.get("is_outdoor", False)
        budget_level = constraints.get("budget_level", "standard")
        
        # Create a prompt for the language model
        prompt = f"""As an agentic AI travel assistant for Dubai, suggest 3 alternative activities based on these constraints:
        
        Weather: {json.dumps(weather, indent=2)}
        Traveler Preferences: {', '.join(preferences)}
        Outdoor Activity Allowed: {is_outdoor}
        Budget Level: {budget_level}
        
        Format your response as a JSON array of objects with these fields: name, type, location, is_indoor, description, price_range.
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are VoyagerVerse, an agentic AI travel assistant that helps travelers in Dubai. You always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Extract and parse the alternatives
        alternatives_json = response.choices[0].message.content.strip()
        alternatives = json.loads(alternatives_json).get("activities", [])
        
        # Ensure we have at least one alternative
        if not alternatives:
            return FALLBACK_RESPONSES["generate_alternatives"]
        
        return alternatives
    
    except Exception as e:
        logger.error(f"Error generating alternatives: {e}")
        return FALLBACK_RESPONSES["generate_alternatives"]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def analyze_activity_safety(activity_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the safety of an activity based on current conditions using AI.
    
    Args:
        activity_data: Dictionary containing activity details and conditions
        
    Returns:
        A safety assessment with risk level and recommendations
    """
    if not client:
        logger.warning("OpenAI client not available. Using fallback safety analysis.")
        return FALLBACK_RESPONSES["analyze_safety"]
    
    try:
        # Format the activity data for the prompt
        activity_name = activity_data.get("name", "")
        is_outdoor = activity_data.get("is_outdoor", False)
        temperature = activity_data.get("temperature", 0)
        weather_condition = activity_data.get("weather_condition", "")
        traveler_health = activity_data.get("traveler_health", "good")
        
        # Create a prompt for the language model
        prompt = f"""As an agentic AI travel assistant, analyze the safety of this activity:
        
        Activity: {activity_name}
        Outdoor Activity: {is_outdoor}
        Temperature: {temperature}°C
        Weather Condition: {weather_condition}
        Traveler Health Status: {traveler_health}
        
        Format your response as a JSON object with these fields: is_safe (boolean), risk_level (string: 'Low', 'Medium', 'High'), reason (string), recommendation (string).
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are VoyagerVerse, an agentic AI travel assistant that prioritizes traveler safety. You always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        # Extract and parse the safety assessment
        safety_json = response.choices[0].message.content.strip()
        safety_assessment = json.loads(safety_json)
        
        return safety_assessment
    
    except Exception as e:
        logger.error(f"Error analyzing activity safety: {e}")
        return FALLBACK_RESPONSES["analyze_safety"]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def personalize_recommendation(user_data: Dict[str, Any], options: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Personalize activity recommendations based on user preferences using AI.
    
    Args:
        user_data: Dictionary containing user preferences and history
        options: List of activity options to choose from
        
    Returns:
        The best personalized recommendation with explanation
    """
    if not client or not options:
        logger.warning("OpenAI client not available or no options provided. Using fallback recommendation.")
        return {"recommendation": options[0] if options else {}, "explanation": FALLBACK_RESPONSES["personalize_recommendation"]}
    
    try:
        # Format the user data and options for the prompt
        preferences = user_data.get("preferences", {})
        history = user_data.get("history", [])
        
        # Create a prompt for the language model
        prompt = f"""As an agentic AI travel assistant, select the best activity for this traveler:
        
        Traveler Preferences: {json.dumps(preferences, indent=2)}
        Activity History: {json.dumps(history, indent=2)}
        Available Options: {json.dumps(options, indent=2)}
        
        Format your response as a JSON object with these fields: selected_activity_index (integer), explanation (string).
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are VoyagerVerse, an agentic AI travel assistant that provides personalized recommendations. You always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        # Extract and parse the recommendation
        recommendation_json = response.choices[0].message.content.strip()
        recommendation_data = json.loads(recommendation_json)
        
        # Get the selected activity
        selected_index = recommendation_data.get("selected_activity_index", 0)
        if selected_index >= len(options):
            selected_index = 0
        
        selected_activity = options[selected_index]
        explanation = recommendation_data.get("explanation", FALLBACK_RESPONSES["personalize_recommendation"])
        
        return {"recommendation": selected_activity, "explanation": explanation}
    
    except Exception as e:
        logger.error(f"Error personalizing recommendation: {e}")
        return {"recommendation": options[0] if options else {}, "explanation": FALLBACK_RESPONSES["personalize_recommendation"]}

# Simple test function
def test_ai_model():
    """
    Test the AI model functionality with sample data.
    """
    # Test explanation generation
    decision_data = {
        "type": "itinerary_change",
        "reason": "extreme_heat",
        "original_activity": {"name": "Desert Safari", "location": "Dubai Desert", "is_outdoor": True},
        "new_activity": {"name": "Dubai Museum", "location": "Al Fahidi Fort", "is_indoor": True},
        "weather": {"temperature": 44, "condition": "Sunny"}
    }
    
    explanation = generate_explanation(decision_data)
    print(f"\nGenerated Explanation:\n{explanation}")
    
    # Test alternative generation
    constraints = {
        "weather": {"temperature": 44, "condition": "Sunny"},
        "preferences": ["cultural", "indoor", "budget-friendly"],
        "is_outdoor": False,
        "budget_level": "standard"
    }
    
    alternatives = generate_alternative_activities(constraints)
    print(f"\nGenerated Alternatives:\n{json.dumps(alternatives, indent=2)}")
    
    # Test safety analysis
    activity_data = {
        "name": "Desert Safari",
        "is_outdoor": True,
        "temperature": 44,
        "weather_condition": "Sunny",
        "traveler_health": "good"
    }
    
    safety = analyze_activity_safety(activity_data)
    print(f"\nSafety Analysis:\n{json.dumps(safety, indent=2)}")

if __name__ == "__main__":
    # Only run the test if this file is executed directly
    test_ai_model()
