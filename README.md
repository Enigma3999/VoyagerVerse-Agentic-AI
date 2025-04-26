# VoyagerVerse-Agentic-AI

A true agentic AI travel assistant that creates dynamic, adaptive travel experiences in Dubai by autonomously responding to changing conditions and traveler needs.

## Project Overview

VoyagerVerse demonstrates true agentic AI capabilities beyond simple AI agents. The system autonomously monitors environmental conditions and traveler states, making proactive decisions to optimize the travel experience without requiring user intervention.

### Core Features

- **Autonomous Decision-Making**: Makes independent decisions without requiring user input
- **Emotional Intelligence**: Detects and responds to traveler emotional and physical states
- **Contextual Awareness**: Continuously monitors environmental factors like extreme weather
- **Goal-Oriented Planning**: Understands traveler goals and optimizes for overall satisfaction
- **Self-Reflection & Learning**: Analyzes past decisions and improves over time

## System Architecture

The system consists of several key components:

1. **Agentic Core**: The decision-making engine implementing true agentic capabilities
2. **Context Engine**: Monitors real-time conditions affecting travel plans
3. **Preference System**: Learns and adapts to traveler preferences over time
4. **Booking System**: Handles cancellations, rebookings, and schedule modifications
5. **Emotional Intelligence Module**: Detects traveler emotional and physical states
6. **Demo UIs**: Interfaces showcasing the conversational and agent-calling aspects

## Getting Started

### Prerequisites

- Python 3.8 or higher
- FastAPI
- Uvicorn
- OpenAI API key (optional for full AI functionality)

### Installation

```bash
# Clone the repository
git clone https://github.com/Enigma3999/VoyagerVerse-Agentic-AI.git

# Navigate to the project directory
cd VoyagerVerse-Agentic-AI

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your OpenAI API key (optional)
echo OPENAI_API_KEY=your_api_key_here > .env
```

## Running the Demo

```bash
# Start the FastAPI server
python main_v2.py
```

Once the server is running, you can access the following demo interfaces:

1. **Simple Chat Demo**: http://localhost:8000/simple-chat
   - Shows the user-facing conversational experience
   - Demonstrates how the system communicates with travelers

2. **Simple Agent UI**: http://localhost:8000/simple-agent
   - Shows the behind-the-scenes agent calling process
   - Reveals how the system makes autonomous decisions

3. **Conversation Demo**: http://localhost:8000/conversation-demo
   - More detailed conversational interface
   - Includes step-by-step progression

4. **Agent Calling Demo**: http://localhost:8000/agent-calling-demo
   - More detailed agent calling interface
   - Shows the full agent interaction flow

## Demo Scenario

The demo showcases Tom & Priya, a British couple visiting Dubai. The system detects:

1. Extreme heat (45.2°C) in Dubai
2. Priya is experiencing a headache
3. Their desert safari is scheduled for the hottest part of the day

Without any user intervention, the system:

1. Evaluates the safety risks of the desert safari
2. Checks the cancellation policy
3. Identifies indoor alternatives matching their preferences
4. Reschedules the desert safari for a cooler time
5. Books the Dubai Museum as an alternative
6. Notifies the travelers of the changes

This demonstrates true agentic capabilities through autonomous decision-making and proactive problem-solving.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The VoyagerVerse Hackathon Team
- Dubai Tourism Board for destination data
