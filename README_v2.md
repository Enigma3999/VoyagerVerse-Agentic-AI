# VoyagerVerse: Agentic AI Travel Assistant

An advanced agentic AI travel concierge system that creates dynamic, adaptive travel experiences in Dubai.

## Project Overview

VoyagerVerse is a true agentic AI system designed to provide personalized, flexible travel experiences in Dubai. Unlike traditional AI agents that simply perform specific tasks, our agentic AI system autonomously makes decisions, adapts to changing conditions, reflects on its own performance, and proactively solves problems before they affect travelers.

### What Makes This Truly Agentic AI (Not Just AI Agents)

1. **Autonomous Decision-Making**: The system makes decisions without constant human intervention, only requesting approval when confidence is below threshold.

2. **Goal-Oriented Behavior**: The system understands and works toward high-level traveler goals rather than just executing commands.

3. **Self-Reflection**: The system evaluates its own performance and adapts its strategies based on past decisions.

4. **Proactive Problem-Solving**: The system anticipates issues (like extreme heat) and resolves them before they affect the traveler.

5. **Preference Evolution**: The system tracks how preferences change throughout the trip, not just static profiles.

## Core Features

- **Real-time Itinerary Adaptation**: Automatically adjusts travel plans based on weather, energy levels, and other contextual factors
- **Personalized Recommendations**: Learns and responds to traveler preferences through minimal input
- **Contextual Awareness**: Monitors weather, time of day, and other environmental factors
- **Seamless Rebooking**: Makes new arrangements with minimal user intervention
- **Push Notifications**: Keeps travelers informed with one-tap approval of changes
- **Transparent Reasoning**: Explains the AI's decision-making process

## System Architecture

The system consists of several key agentic components:

1. **Agentic Core** (`agentic_core.py`)
   - Goal management system
   - Autonomous decision-making engine
   - Self-reflection mechanism
   - Confidence scoring for decisions

2. **Context Engine** (`context_engine.py`)
   - Weather monitoring
   - Location awareness
   - Time-based reasoning
   - Traveler state tracking

3. **Preference System** (`preference_system.py`)
   - Multi-dimensional preference modeling
   - Preference learning from minimal input
   - Preference evolution tracking
   - Exploration vs. exploitation balancing

4. **Booking System** (`booking_system.py`)
   - Simulated booking operations
   - Cancellation management
   - Rebooking logic
   - Availability checking

5. **Main API** (`main_v2.py`)
   - FastAPI endpoints for frontend communication
   - Background tasks for monitoring
   - Notification management
   - Chat interface

## Demo Scenario: Tom & Priya in Dubai

The system includes a demonstration scenario featuring Tom & Priya, a British couple on a luxury vacation in Dubai:

- **Profile**: 36-year-old couple interested in culture, food, and light adventure
- **Challenge**: Frustrated by rigid itineraries that don't respond to heat or personal mood
- **Scenario**: On day 3 of their trip, extreme heat (43°C) makes their planned Desert Safari uncomfortable
- **Agentic Response**: The system autonomously:
  1. Detects the temperature exceeds their comfort threshold (38°C)
  2. Evaluates alternative indoor activities matching their cultural interests
  3. Books a Dubai Museum Cultural Tour for the afternoon
  4. Reschedules the Desert Safari to early morning on another day
  5. Sends a notification with clear explanation and one-tap approval

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- Other dependencies listed in requirements.txt

### Installation

```bash
# Clone the repository
git clone https://github.com/Enigma3999/VoyagerVerse-Agentic-AI.git

# Navigate to the project directory
cd VoyagerVerse-Agentic-AI

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main_v2:app --reload
```

### Running the Demo

1. Start the server: `uvicorn main_v2:app --reload`
2. Open `home_v2.html` in your browser
3. Click "View Today's Plan" to load the Tom & Priya scenario
4. Observe how the system adapts to extreme heat conditions
5. Try different interactions in the chat interface

## Key Differentiators from Traditional Travel Apps

1. **True Autonomy**: The system doesn't just recommend—it acts, with appropriate guardrails
2. **Multi-level Cognition**: Implements a cognitive architecture rather than just a collection of functions
3. **Self-Improvement**: Continuously evaluates and improves its own performance
4. **Minimal User Burden**: Requires only one-tap approval for changes, not complex decision-making
5. **Transparent Reasoning**: Provides natural language explanations for all decisions

## Future Enhancements

- Integration with real booking APIs
- Enhanced natural language processing
- Mobile app with location tracking
- Multi-traveler group preference balancing
- Reinforcement learning from user feedback

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Dubai Tourism for inspiration
- OpenAI for language model capabilities
- The agentic AI research community
