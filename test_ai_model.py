import os
import json
from dotenv import load_dotenv
from ai_model import generate_explanation, generate_alternative_activities, analyze_activity_safety, personalize_recommendation

# Load environment variables
load_dotenv()

def test_ai_model_integration():
    print("\n===== Testing VoyagerVerse AI Model Integration =====\n")
    
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  Warning: OPENAI_API_KEY not set or using default value.")
        print("    Using fallback responses for demonstration.\n")
    else:
        print("✅ OpenAI API key found.\n")
    
    # Test 1: Generate explanation for itinerary change
    print("\n----- Test 1: Generate Explanation -----")
    decision_data = {
        "type": "itinerary_change",
        "reason": "extreme_heat",
        "original_activity": {"name": "Desert Safari", "location": "Dubai Desert", "is_outdoor": True},
        "new_activity": {"name": "Dubai Museum", "location": "Al Fahidi Fort", "is_indoor": True},
        "weather": {"temperature": 44, "condition": "Sunny"}
    }
    
    print("\nInput:")
    print(json.dumps(decision_data, indent=2))
    
    explanation = generate_explanation(decision_data)
    print("\nOutput:")
    print(explanation)
    
    # Test 2: Generate alternative activities
    print("\n\n----- Test 2: Generate Alternative Activities -----")
    constraints = {
        "weather": {"temperature": 44, "condition": "Sunny"},
        "preferences": ["cultural", "indoor", "budget-friendly"],
        "is_outdoor": False,
        "budget_level": "standard"
    }
    
    print("\nInput:")
    print(json.dumps(constraints, indent=2))
    
    alternatives = generate_alternative_activities(constraints)
    print("\nOutput:")
    print(json.dumps(alternatives, indent=2))
    
    # Test 3: Analyze activity safety
    print("\n\n----- Test 3: Analyze Activity Safety -----")
    activity_data = {
        "name": "Desert Safari",
        "is_outdoor": True,
        "temperature": 44,
        "weather_condition": "Sunny",
        "traveler_health": "good"
    }
    
    print("\nInput:")
    print(json.dumps(activity_data, indent=2))
    
    safety = analyze_activity_safety(activity_data)
    print("\nOutput:")
    print(json.dumps(safety, indent=2))
    
    # Test 4: Personalize recommendation
    print("\n\n----- Test 4: Personalize Recommendation -----")
    user_data = {
        "preferences": {
            "activity_preferences": ["cultural", "adventure", "relaxation"],
            "cuisine_preferences": ["Indian", "Mediterranean", "Arabic"],
            "budget_level": "premium"
        },
        "history": [
            {"type": "activity_feedback", "activity": "Museum Visit", "rating": 4.5},
            {"type": "activity_feedback", "activity": "Beach Day", "rating": 3.0}
        ]
    }
    
    options = [
        {"name": "Dubai Museum", "type": "cultural", "price": 35},
        {"name": "Mall of the Emirates", "type": "shopping", "price": 0},
        {"name": "Burj Khalifa Observation Deck", "type": "attraction", "price": 149}
    ]
    
    print("\nInput:")
    print("User Data:")
    print(json.dumps(user_data, indent=2))
    print("\nOptions:")
    print(json.dumps(options, indent=2))
    
    personalized = personalize_recommendation(user_data, options)
    print("\nOutput:")
    print(json.dumps(personalized, indent=2))
    
    print("\n\n===== AI Model Integration Test Complete =====\n")
    print("The VoyagerVerse agentic AI system is now enhanced with AI model capabilities!")
    print("These AI models provide:")
    print("  1. Natural language explanations for agentic decisions")
    print("  2. Dynamic generation of alternative activities")
    print("  3. Intelligent safety analysis for activities")
    print("  4. Personalized recommendations based on user preferences")
    print("\nYou can now update your .env file with a real OpenAI API key to use these capabilities.")

if __name__ == "__main__":
    test_ai_model_integration()
