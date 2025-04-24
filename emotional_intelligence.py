import logging
import json
import random
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("emotional_intelligence")

class EmotionalIntelligence:
    """Emotional intelligence module for VoyagerVerse agentic AI system.
    
    This module processes biometric data, speech patterns, facial expressions,
    and behavioral cues to determine the traveler's emotional and physiological state.
    """
    
    def __init__(self):
        self.current_emotional_state = {}
        self.emotional_history = []
        self.adaptation_threshold = 0.6  # Threshold for triggering adaptations
        
    def process_biometric_data(self, biometric_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process biometric data from wearables or sensors.
        
        Args:
            biometric_data: Dictionary containing biometric readings
            
        Returns:
            Processed biometric assessment
        """
        # In a real implementation, this would process actual biometric data
        # For demo purposes, we'll use the provided data directly
        
        assessment = {
            "fatigue_level": self._calculate_fatigue_level(biometric_data),
            "stress_level": self._calculate_stress_level(biometric_data),
            "comfort_level": self._calculate_comfort_level(biometric_data),
            "timestamp": biometric_data.get("timestamp", "")
        }
        
        logger.info(f"Processed biometric data: {assessment}")
        return assessment
    
    def analyze_speech_patterns(self, speech_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze speech patterns for emotional cues.
        
        Args:
            speech_data: Dictionary containing speech samples or analysis
            
        Returns:
            Speech pattern analysis results
        """
        # In a real implementation, this would use a speech analysis API
        # For demo purposes, we'll simulate the analysis
        
        word_count = speech_data.get("word_count", 0)
        speech_rate = speech_data.get("speech_rate", "normal")
        tone = speech_data.get("tone", "neutral")
        
        analysis = {
            "engagement_level": self._calculate_engagement(word_count, speech_rate),
            "emotional_tone": tone,
            "communication_energy": self._calculate_communication_energy(speech_data),
            "timestamp": speech_data.get("timestamp", "")
        }
        
        logger.info(f"Analyzed speech patterns: {analysis}")
        return analysis
    
    def process_facial_expressions(self, facial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process facial expression data for emotional cues.
        
        Args:
            facial_data: Dictionary containing facial expression analysis
            
        Returns:
            Facial expression analysis results
        """
        # In a real implementation, this would use Affectiva or similar
        # For demo purposes, we'll simulate the analysis
        
        expressions = facial_data.get("expressions", {})
        
        analysis = {
            "dominant_emotion": self._identify_dominant_emotion(expressions),
            "emotional_intensity": self._calculate_emotional_intensity(expressions),
            "attention_level": facial_data.get("attention_level", 0.5),
            "timestamp": facial_data.get("timestamp", "")
        }
        
        logger.info(f"Processed facial expressions: {analysis}")
        return analysis
    
    def analyze_behavioral_patterns(self, behavioral_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns for state assessment.
        
        Args:
            behavioral_data: Dictionary containing behavioral observations
            
        Returns:
            Behavioral pattern analysis
        """
        # In a real implementation, this would process movement patterns, etc.
        # For demo purposes, we'll simulate the analysis
        
        movement_speed = behavioral_data.get("movement_speed", "normal")
        interaction_frequency = behavioral_data.get("interaction_frequency", "normal")
        
        analysis = {
            "energy_level": self._calculate_energy_level(movement_speed),
            "social_engagement": self._calculate_social_engagement(interaction_frequency),
            "activity_interest": behavioral_data.get("activity_interest", 0.5),
            "timestamp": behavioral_data.get("timestamp", "")
        }
        
        logger.info(f"Analyzed behavioral patterns: {analysis}")
        return analysis
    
    def update_emotional_state(self, 
                              biometric_data: Optional[Dict[str, Any]] = None,
                              speech_data: Optional[Dict[str, Any]] = None,
                              facial_data: Optional[Dict[str, Any]] = None,
                              behavioral_data: Optional[Dict[str, Any]] = None,
                              explicit_feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the current emotional state based on all available data.
        
        Args:
            biometric_data: Optional biometric readings
            speech_data: Optional speech analysis data
            facial_data: Optional facial expression data
            behavioral_data: Optional behavioral data
            explicit_feedback: Optional explicit user feedback
            
        Returns:
            Updated emotional state assessment
        """
        # Process each data source if provided
        biometric_assessment = self.process_biometric_data(biometric_data) if biometric_data else {}
        speech_assessment = self.analyze_speech_patterns(speech_data) if speech_data else {}
        facial_assessment = self.process_facial_expressions(facial_data) if facial_data else {}
        behavioral_assessment = self.analyze_behavioral_patterns(behavioral_data) if behavioral_data else {}
        
        # Combine all assessments into a unified emotional state
        new_state = {
            "fatigue_level": biometric_assessment.get("fatigue_level", self.current_emotional_state.get("fatigue_level", 0.5)),
            "stress_level": biometric_assessment.get("stress_level", self.current_emotional_state.get("stress_level", 0.5)),
            "engagement_level": speech_assessment.get("engagement_level", self.current_emotional_state.get("engagement_level", 0.5)),
            "dominant_emotion": facial_assessment.get("dominant_emotion", self.current_emotional_state.get("dominant_emotion", "neutral")),
            "energy_level": behavioral_assessment.get("energy_level", self.current_emotional_state.get("energy_level", 0.5)),
            "comfort_level": biometric_assessment.get("comfort_level", self.current_emotional_state.get("comfort_level", 0.5)),
            "timestamp": biometric_data.get("timestamp", "")
        }
        
        # If explicit feedback is provided, it overrides sensor data
        if explicit_feedback:
            for key, value in explicit_feedback.items():
                if key in new_state:
                    new_state[key] = value
        
        # Save the previous state to history before updating
        if self.current_emotional_state:
            self.emotional_history.append(self.current_emotional_state)
            # Keep history to a reasonable size
            if len(self.emotional_history) > 10:
                self.emotional_history.pop(0)
        
        # Update current state
        self.current_emotional_state = new_state
        
        logger.info(f"Updated emotional state: {new_state}")
        return new_state
    
    def get_current_emotional_state(self) -> Dict[str, Any]:
        """Get the current emotional state assessment.
        
        Returns:
            Current emotional state
        """
        return self.current_emotional_state
    
    def get_adaptation_recommendations(self) -> Dict[str, Any]:
        """Generate adaptation recommendations based on emotional state.
        
        Returns:
            Dictionary of recommendations for adapting services
        """
        state = self.current_emotional_state
        recommendations = {}
        
        # Fatigue adaptations
        if state.get("fatigue_level", 0) > self.adaptation_threshold:
            recommendations["activity_duration"] = "shortened"
            recommendations["activity_intensity"] = "reduced"
            recommendations["rest_breaks"] = "increased"
        
        # Stress adaptations
        if state.get("stress_level", 0) > self.adaptation_threshold:
            recommendations["environment"] = "calming"
            recommendations["pace"] = "relaxed"
            recommendations["sensory_input"] = "reduced"
        
        # Energy adaptations
        if state.get("energy_level", 1) < (1 - self.adaptation_threshold):
            recommendations["physical_exertion"] = "minimized"
            recommendations["transportation"] = "convenient"
            recommendations["scheduling"] = "spacious"
        
        # Comfort adaptations
        if state.get("comfort_level", 1) < (1 - self.adaptation_threshold):
            recommendations["amenities"] = "enhanced"
            recommendations["environment_control"] = "personalized"
            recommendations["seating"] = "prioritized"
        
        logger.info(f"Generated adaptation recommendations: {recommendations}")
        return recommendations
    
    def process_explicit_feedback(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Process explicit feedback from the traveler.
        
        Args:
            feedback: Dictionary containing explicit feedback
            
        Returns:
            Updated state based on feedback
        """
        # Extract relevant feedback
        headache = feedback.get("headache", False)
        fatigue = feedback.get("fatigue", False)
        mood = feedback.get("mood", "")
        
        # Create explicit feedback dictionary
        explicit_state_updates = {}
        
        if headache:
            explicit_state_updates["comfort_level"] = 0.3
            explicit_state_updates["stress_level"] = 0.7
        
        if fatigue:
            explicit_state_updates["fatigue_level"] = 0.8
            explicit_state_updates["energy_level"] = 0.2
        
        if mood:
            explicit_state_updates["dominant_emotion"] = mood
        
        # Update state with explicit feedback
        return self.update_emotional_state(explicit_feedback=explicit_state_updates)
    
    def _calculate_fatigue_level(self, biometric_data: Dict[str, Any]) -> float:
        """Calculate fatigue level from biometric data."""
        # In a real implementation, this would use heart rate, sleep data, etc.
        heart_rate = biometric_data.get("heart_rate", 70)
        sleep_hours = biometric_data.get("sleep_hours", 7)
        steps = biometric_data.get("steps", 5000)
        
        # Simple algorithm for demo purposes
        fatigue_level = 0.5
        
        if sleep_hours < 6:
            fatigue_level += 0.3
        elif sleep_hours > 8:
            fatigue_level -= 0.2
            
        if heart_rate < 60:
            fatigue_level += 0.1
        elif heart_rate > 90:
            fatigue_level += 0.2
            
        if steps < 1000:
            fatigue_level += 0.1
            
        # Ensure value is between 0 and 1
        return max(0, min(1, fatigue_level))
    
    def _calculate_stress_level(self, biometric_data: Dict[str, Any]) -> float:
        """Calculate stress level from biometric data."""
        # In a real implementation, this would use heart rate variability, etc.
        heart_rate = biometric_data.get("heart_rate", 70)
        hrv = biometric_data.get("heart_rate_variability", 50)
        skin_conductance = biometric_data.get("skin_conductance", 0.5)
        
        # Simple algorithm for demo purposes
        stress_level = 0.5
        
        if heart_rate > 80:
            stress_level += 0.2
            
        if hrv < 30:
            stress_level += 0.3
            
        if skin_conductance > 0.7:
            stress_level += 0.2
            
        # Ensure value is between 0 and 1
        return max(0, min(1, stress_level))
    
    def _calculate_comfort_level(self, biometric_data: Dict[str, Any]) -> float:
        """Calculate physical comfort level from biometric data."""
        # In a real implementation, this would use temperature, movement, etc.
        temperature = biometric_data.get("body_temperature", 98.6)
        movement = biometric_data.get("movement_comfort", 0.5)
        pain_indicator = biometric_data.get("pain_indicator", 0)
        
        # Simple algorithm for demo purposes
        comfort_level = 0.8  # Assume relatively comfortable by default
        
        if temperature > 99.5 or temperature < 97.5:
            comfort_level -= 0.3
            
        if movement < 0.3:
            comfort_level -= 0.2
            
        if pain_indicator > 0:
            comfort_level -= pain_indicator * 0.5
            
        # Ensure value is between 0 and 1
        return max(0, min(1, comfort_level))
    
    def _calculate_engagement(self, word_count: int, speech_rate: str) -> float:
        """Calculate engagement level from speech patterns."""
        # Simple algorithm for demo purposes
        engagement = 0.5  # Neutral starting point
        
        if word_count < 10:
            engagement -= 0.3
        elif word_count > 50:
            engagement += 0.2
            
        if speech_rate == "slow":
            engagement -= 0.2
        elif speech_rate == "fast":
            engagement += 0.2
            
        # Ensure value is between 0 and 1
        return max(0, min(1, engagement))
    
    def _calculate_communication_energy(self, speech_data: Dict[str, Any]) -> float:
        """Calculate communication energy from speech data."""
        # Simple algorithm for demo purposes
        volume = speech_data.get("volume", 0.5)
        pitch_variation = speech_data.get("pitch_variation", 0.5)
        word_count = speech_data.get("word_count", 0)
        
        energy = 0.5  # Neutral starting point
        
        energy += (volume - 0.5) * 0.5
        energy += (pitch_variation - 0.5) * 0.5
        
        if word_count < 10:
            energy -= 0.2
        elif word_count > 50:
            energy += 0.2
            
        # Ensure value is between 0 and 1
        return max(0, min(1, energy))
    
    def _identify_dominant_emotion(self, expressions: Dict[str, float]) -> str:
        """Identify the dominant emotion from facial expressions."""
        if not expressions:
            return "neutral"
            
        # Find the emotion with the highest score
        dominant_emotion = max(expressions.items(), key=lambda x: x[1])
        return dominant_emotion[0]
    
    def _calculate_emotional_intensity(self, expressions: Dict[str, float]) -> float:
        """Calculate the intensity of emotional expression."""
        if not expressions:
            return 0.5
            
        # Find the highest intensity value
        max_intensity = max(expressions.values())
        return max_intensity
    
    def _calculate_energy_level(self, movement_speed: str) -> float:
        """Calculate energy level from movement speed."""
        # Simple mapping for demo purposes
        energy_mapping = {
            "very_slow": 0.1,
            "slow": 0.3,
            "normal": 0.5,
            "fast": 0.7,
            "very_fast": 0.9
        }
        
        return energy_mapping.get(movement_speed, 0.5)
    
    def _calculate_social_engagement(self, interaction_frequency: str) -> float:
        """Calculate social engagement from interaction frequency."""
        # Simple mapping for demo purposes
        engagement_mapping = {
            "very_low": 0.1,
            "low": 0.3,
            "normal": 0.5,
            "high": 0.7,
            "very_high": 0.9
        }
        
        return engagement_mapping.get(interaction_frequency, 0.5)

# Initialize the emotional intelligence module
emotional_intelligence = EmotionalIntelligence()

# Example usage
def simulate_arrival_scenario():
    """Simulate the arrival scenario for Tom and Priya."""
    # Biometric data indicating fatigue after long flight
    biometric_data = {
        "heart_rate": 75,
        "sleep_hours": 4,  # Limited sleep on flight
        "steps": 800,      # Limited movement
        "body_temperature": 99.0,  # Slightly elevated
        "heart_rate_variability": 35,  # Lower HRV indicates stress
        "skin_conductance": 0.65,  # Elevated
        "movement_comfort": 0.3,  # Uncomfortable from long flight
        "pain_indicator": 0.2,  # Mild discomfort
        "timestamp": "2025-04-24T07:30:00"
    }
    
    # Speech data indicating low engagement
    speech_data = {
        "word_count": 8,  # Few words spoken
        "speech_rate": "slow",  # Speaking slowly
        "tone": "tired",  # Tired tone
        "volume": 0.4,  # Speaking softly
        "pitch_variation": 0.3,  # Monotone
        "timestamp": "2025-04-24T07:35:00"
    }
    
    # Facial expression data
    facial_data = {
        "expressions": {
            "neutral": 0.6,
            "tired": 0.7,
            "happy": 0.2,
            "stressed": 0.4
        },
        "attention_level": 0.4,  # Lower attention
        "timestamp": "2025-04-24T07:35:00"
    }
    
    # Behavioral data
    behavioral_data = {
        "movement_speed": "slow",  # Moving slowly
        "interaction_frequency": "low",  # Limited interaction
        "activity_interest": 0.3,  # Low interest in activities
        "timestamp": "2025-04-24T07:40:00"
    }
    
    # Update emotional state with all data
    emotional_state = emotional_intelligence.update_emotional_state(
        biometric_data=biometric_data,
        speech_data=speech_data,
        facial_data=facial_data,
        behavioral_data=behavioral_data
    )
    
    # Get adaptation recommendations
    recommendations = emotional_intelligence.get_adaptation_recommendations()
    
    # Process explicit feedback about headache
    explicit_feedback = {
        "headache": True,
        "fatigue": True,
        "mood": "tired"
    }
    
    updated_state = emotional_intelligence.process_explicit_feedback(explicit_feedback)
    updated_recommendations = emotional_intelligence.get_adaptation_recommendations()
    
    return {
        "initial_state": emotional_state,
        "initial_recommendations": recommendations,
        "updated_state": updated_state,
        "updated_recommendations": updated_recommendations
    }

if __name__ == "__main__":
    # Run the simulation
    result = simulate_arrival_scenario()
    print(json.dumps(result, indent=2))
