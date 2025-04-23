from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for incoming request
class ChatMessage(BaseModel):
    message: str
    language: str = "en-US"

# Simulate AI logic with a generic response
@app.post("/chat")
async def chat(msg: ChatMessage):
    english_reply = "Thank you! We will prepare your personalized travel plan."

    # Translate reply to user-selected language
    target_lang = msg.language.split("-")[0]  # e.g., 'hi' from 'hi-IN'

    try:
        if target_lang != "en":
            translated_reply = GoogleTranslator(source='auto', target=target_lang).translate(english_reply)
        else:
            translated_reply = english_reply
    except Exception as e:
        translated_reply = english_reply + " (Translation failed)"

    return {"reply": translated_reply}

# Sample trip summary endpoint (if needed)
@app.get("/trip-summary")
def get_trip_summary():
    return {
        "itinerary": [
            {"day": "Day 1", "activity": "Arrival & Check-in", "location": "Hotel Downtown"},
            {"day": "Day 2", "activity": "Visit Burj Khalifa", "location": "Downtown"},
            {"day": "Day 3", "activity": "Desert Safari", "location": "Al Marmoom"},
            {"day": "Day 4", "activity": "Cultural Tour", "location": "Old Dubai"},
            {"day": "Day 5", "activity": "Free Time & Departure", "location": "Hotel / Airport"}
        ]
    }
