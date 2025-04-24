import requests
import logging
import os
from typing import Dict, List, Any, Optional
import random

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("local_info_tools")

# API keys would normally be stored in environment variables
DUBAI_INFO_API_KEY = os.getenv("DUBAI_INFO_API_KEY", "your_dubai_info_api_key")

def get_cultural_info(topic: str = None) -> Dict[str, Any]:
    """Get cultural information about Dubai."""
    url = "https://api.dubaiinfo.com/cultural"
    
    headers = {
        "Authorization": f"Bearer {DUBAI_INFO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    params = {}
    if topic:
        params["topic"] = topic
    
    try:
        # This would be a real API call in a production environment
        # response = requests.get(url, headers=headers, params=params)
        # response.raise_for_status()
        # data = response.json()
        
        return {
            "status": "success",
            "data": get_simulated_cultural_info(topic)
        }
    
    except Exception as e:
        logger.error(f"Error getting cultural information: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_cultural_info(topic)
        }

def get_practical_info(topic: str = None) -> Dict[str, Any]:
    """Get practical information about Dubai."""
    url = "https://api.dubaiinfo.com/practical"
    
    headers = {
        "Authorization": f"Bearer {DUBAI_INFO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    params = {}
    if topic:
        params["topic"] = topic
    
    try:
        # This would be a real API call in a production environment
        # response = requests.get(url, headers=headers, params=params)
        # response.raise_for_status()
        # data = response.json()
        
        return {
            "status": "success",
            "data": get_simulated_practical_info(topic)
        }
    
    except Exception as e:
        logger.error(f"Error getting practical information: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_practical_info(topic)
        }

def get_emergency_info() -> Dict[str, Any]:
    """Get emergency information for Dubai."""
    url = "https://api.dubaiinfo.com/emergency"
    
    headers = {
        "Authorization": f"Bearer {DUBAI_INFO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # This would be a real API call in a production environment
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()
        # data = response.json()
        
        return {
            "status": "success",
            "data": get_simulated_emergency_info()
        }
    
    except Exception as e:
        logger.error(f"Error getting emergency information: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_emergency_info()
        }

def get_local_customs() -> Dict[str, Any]:
    """Get information about local customs and etiquette in Dubai."""
    url = "https://api.dubaiinfo.com/customs"
    
    headers = {
        "Authorization": f"Bearer {DUBAI_INFO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # This would be a real API call in a production environment
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()
        # data = response.json()
        
        return {
            "status": "success",
            "data": get_simulated_local_customs()
        }
    
    except Exception as e:
        logger.error(f"Error getting local customs information: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_local_customs()
        }

def get_simulated_cultural_info(topic: str = None) -> Dict[str, Any]:
    """Generate simulated cultural information about Dubai for testing purposes."""
    cultural_info = {
        "language": {
            "title": "Language in Dubai",
            "content": "The official language of Dubai is Arabic, but English is widely spoken and understood. Many signs, menus, and official documents are available in both Arabic and English. Other commonly spoken languages include Hindi, Urdu, Filipino, and Persian, reflecting the diverse expatriate population.",
            "key_phrases": [
                {"arabic": "As-salām 'alaykum", "english": "Peace be upon you (Hello)"},
                {"arabic": "Shukran", "english": "Thank you"},
                {"arabic": "Ma'a salama", "english": "Goodbye"},
                {"arabic": "Min fadlak/Min fadlik", "english": "Please (to male/female)"},
                {"arabic": "Kam howa?", "english": "How much is it?"}
            ]
        },
        "religion": {
            "title": "Religion in Dubai",
            "content": "Islam is the official religion of Dubai and the UAE. The city has numerous mosques, with the Jumeirah Mosque being one of the few open to non-Muslims through guided tours. While Islamic traditions influence many aspects of life, Dubai is tolerant of other religions, and non-Muslims are free to practice their faith. During the holy month of Ramadan, non-Muslims are expected to refrain from eating, drinking, and smoking in public during daylight hours.",
            "prayer_times": {
                "note": "Prayer times vary throughout the year based on the sun's position",
                "typical_times": [
                    {"name": "Fajr", "time": "Around dawn"},
                    {"name": "Dhuhr", "time": "Midday"},
                    {"name": "Asr", "time": "Afternoon"},
                    {"name": "Maghrib", "time": "Sunset"},
                    {"name": "Isha", "time": "Night"}
                ]
            }
        },
        "cuisine": {
            "title": "Emirati Cuisine",
            "content": "Traditional Emirati cuisine blends Arabian, Persian, and Indian influences. Staple ingredients include meat (lamb, camel, chicken), fish, rice, dates, and spices like saffron, cardamom, turmeric, and thyme. While international cuisine is widely available in Dubai's restaurants, trying local dishes offers insight into the region's culinary heritage.",
            "traditional_dishes": [
                {"name": "Al Machboos", "description": "Spiced rice dish with meat (usually lamb or chicken)"},
                {"name": "Al Harees", "description": "Wheat and meat slow-cooked into a porridge-like consistency"},
                {"name": "Luqaimat", "description": "Sweet dumplings drizzled with date syrup"},
                {"name": "Shawarma", "description": "Grilled meat wrapped in flatbread with vegetables and sauce"},
                {"name": "Khameer", "description": "Traditional Emirati bread flavored with cardamom and date syrup"}
            ]
        },
        "history": {
            "title": "History of Dubai",
            "content": "Dubai's history dates back to the early 18th century when it was a small fishing village. The Al Maktoum family has ruled Dubai since 1833. The discovery of oil in 1966 transformed Dubai from a port town to a global city. Under Sheikh Rashid bin Saeed Al Maktoum and his son, Sheikh Mohammed bin Rashid Al Maktoum, Dubai diversified its economy beyond oil, focusing on tourism, real estate, and financial services, leading to its rapid development into the cosmopolitan metropolis it is today.",
            "key_dates": [
                {"year": "1833", "event": "The Al Maktoum family establishes rule in Dubai"},
                {"year": "1894", "event": "Dubai becomes a tax-free port, attracting foreign traders"},
                {"year": "1966", "event": "Discovery of oil in Dubai"},
                {"year": "1971", "event": "Formation of the United Arab Emirates"},
                {"year": "1979", "event": "Jebel Ali Port opens, becoming the largest man-made harbor"},
                {"year": "1999", "event": "Burj Al Arab hotel opens"},
                {"year": "2010", "event": "Burj Khalifa, the world's tallest building, opens"}
            ]
        },
        "arts": {
            "title": "Arts and Culture in Dubai",
            "content": "Dubai's cultural scene blends traditional Emirati heritage with contemporary global influences. The city hosts numerous art galleries, museums, and cultural festivals. The Dubai Opera hosts world-class performances, while Alserkal Avenue serves as a creative hub with galleries and studios. Traditional art forms include poetry, dance (like the Ayala and Harbiya), and handicrafts such as weaving, pottery, and metalwork.",
            "cultural_districts": [
                {"name": "Al Fahidi Historical Neighbourhood", "description": "Traditional architecture and the Dubai Museum"},
                {"name": "Alserkal Avenue", "description": "Contemporary art galleries and creative spaces"},
                {"name": "Dubai Design District (d3)", "description": "Hub for design, fashion, and architecture"},
                {"name": "Dubai Opera", "description": "Performing arts center in Downtown Dubai"}
            ]
        }
    }
    
    if topic and topic.lower() in cultural_info:
        return {topic.lower(): cultural_info[topic.lower()]}
    else:
        return cultural_info

def get_simulated_practical_info(topic: str = None) -> Dict[str, Any]:
    """Generate simulated practical information about Dubai for testing purposes."""
    practical_info = {
        "transportation": {
            "title": "Getting Around Dubai",
            "content": "Dubai has an extensive public transportation network, including the Dubai Metro, buses, water taxis (abras), and a monorail on Palm Jumeirah. Taxis are plentiful and can be hailed on the street or booked through apps like Careem or Uber. Renting a car is another option, but be aware of local driving rules and the heavy traffic during peak hours.",
            "options": [
                {
                    "name": "Dubai Metro",
                    "description": "Clean, efficient, and air-conditioned with Red and Green lines covering major areas",
                    "hours": "Saturday to Wednesday: 5am-12am, Thursday: 5am-1am, Friday: 10am-1am",
                    "cost": "Fares from AED 4, based on zones traveled"
                },
                {
                    "name": "Public Buses",
                    "description": "Extensive network covering areas not reached by the metro",
                    "hours": "Varies by route, many operate 24/7",
                    "cost": "Fares from AED 3, based on zones traveled"
                },
                {
                    "name": "Taxis",
                    "description": "Cream-colored cars with red roofs, widely available",
                    "hours": "24/7",
                    "cost": "Starting fare AED 12 (day) or AED 14 (night), plus AED 1.82 per km"
                },
                {
                    "name": "Abras (Water Taxis)",
                    "description": "Traditional wooden boats crossing Dubai Creek",
                    "hours": "24/7",
                    "cost": "AED 1 per trip"
                }
            ]
        },
        "weather": {
            "title": "Dubai Weather",
            "content": "Dubai has a hot desert climate with extremely hot and humid summers (May to September) and mild winters (December to March). Summer temperatures often exceed 40°C (104°F) with high humidity, making outdoor activities challenging. Winter temperatures are pleasant, ranging from 14°C to 25°C (57°F to 77°F), ideal for outdoor exploration. Rainfall is minimal and occurs mainly between December and March.",
            "seasonal_tips": [
                {
                    "season": "Summer (May-September)",
                    "temperature": "35-48°C (95-118°F)",
                    "tips": "Stay hydrated, limit outdoor activities to early morning or evening, use sunscreen, seek air-conditioned venues"
                },
                {
                    "season": "Winter (December-March)",
                    "temperature": "14-25°C (57-77°F)",
                    "tips": "Ideal for outdoor activities, light jacket may be needed in evenings, perfect beach weather"
                },
                {
                    "season": "Transition (April, October-November)",
                    "temperature": "25-35°C (77-95°F)",
                    "tips": "Comfortable for most activities, but sun protection still necessary"
                }
            ]
        },
        "money": {
            "title": "Currency and Payment",
            "content": "The official currency is the United Arab Emirates Dirham (AED or Dhs). Credit cards are widely accepted in hotels, restaurants, and shopping malls. ATMs are readily available throughout the city. Tipping is not mandatory but is becoming more common in service industries. A 5-10% tip is appreciated in restaurants if service charge is not included.",
            "exchange_rate": "1 USD ≈ 3.67 AED (fixed peg)",
            "tipping_guide": [
                {"service": "Restaurants", "tip": "10-15% if service charge not included"},
                {"service": "Taxis", "tip": "Rounding up the fare is sufficient"},
                {"service": "Hotel porters", "tip": "AED 10-20 per bag"},
                {"service": "Tour guides", "tip": "AED 50-100 per day depending on group size"}
            ]
        },
        "visa": {
            "title": "Visa Information",
            "content": "Visa requirements for Dubai vary based on nationality. Citizens of GCC countries do not need a visa. Nationals from many countries, including the US, UK, EU, Australia, and others, can obtain a free visa on arrival valid for 30 or 90 days. Other nationalities need to apply for a visa in advance through a UAE embassy, airline, or sponsor.",
            "visa_on_arrival": [
                "United States", "United Kingdom", "European Union countries", "Australia", 
                "New Zealand", "Japan", "Singapore", "Malaysia", "South Korea", "Brunei", 
                "Hong Kong", "Canada"
            ],
            "visa_types": [
                {"type": "Tourist Visa", "duration": "30 days, extendable", "cost": "Varies by nationality"},
                {"type": "Visit Visa", "duration": "90 days", "cost": "Varies by nationality"},
                {"type": "Transit Visa", "duration": "96 hours", "cost": "Approximately AED 50"}
            ]
        },
        "communication": {
            "title": "Communication Services",
            "content": "Dubai has excellent telecommunications infrastructure with widespread 4G and 5G coverage. The main mobile operators are Etisalat and du, both offering prepaid SIM cards for tourists. Free Wi-Fi is available in many public places, shopping malls, and hotels. International calls can be made using VoIP services, though some may be restricted.",
            "mobile_options": [
                {
                    "provider": "Etisalat",
                    "tourist_sim": "Visitor Line",
                    "cost": "From AED 125 for 7 days with data and call credit",
                    "where_to_buy": "Airport, Etisalat stores, some hotels"
                },
                {
                    "provider": "du",
                    "tourist_sim": "Tourist SIM",
                    "cost": "From AED 110 for 7 days with data and call credit",
                    "where_to_buy": "Airport, du stores, some hotels"
                }
            ],
            "wifi_hotspots": ["Shopping malls", "Metro stations", "Parks", "Beaches", "Government buildings"]
        }
    }
    
    if topic and topic.lower() in practical_info:
        return {topic.lower(): practical_info[topic.lower()]}
    else:
        return practical_info

def get_simulated_emergency_info() -> Dict[str, Any]:
    """Generate simulated emergency information for Dubai."""
    return {
        "emergency_numbers": [
            {"service": "General Emergency", "number": "999"},
            {"service": "Police", "number": "999"},
            {"service": "Ambulance", "number": "998"},
            {"service": "Fire Department", "number": "997"},
            {"service": "Coastguard", "number": "996"},
            {"service": "Dubai Police Tourist Security", "number": "+971 4 608 8888"}
        ],
        "hospitals": [
            {
                "name": "Rashid Hospital",
                "address": "Oud Metha Road, Dubai",
                "phone": "+971 4 219 1000",
                "emergency": "24/7",
                "specialties": ["Trauma Center", "Emergency Medicine"]
            },
            {
                "name": "Dubai Hospital",
                "address": "Al Baraha, Dubai",
                "phone": "+971 4 219 5000",
                "emergency": "24/7",
                "specialties": ["General Medicine", "Surgery"]
            },
            {
                "name": "American Hospital Dubai",
                "address": "Oud Metha, Dubai",
                "phone": "+971 4 377 6000",
                "emergency": "24/7",
                "specialties": ["Multi-specialty", "International patients"]
            },
            {
                "name": "Mediclinic City Hospital",
                "address": "Dubai Healthcare City",
                "phone": "+971 4 435 9999",
                "emergency": "24/7",
                "specialties": ["Multi-specialty", "International standards"]
            }
        ],
        "pharmacies": [
            {"name": "Life Pharmacy", "note": "Chain with many 24-hour locations throughout Dubai"},
            {"name": "Aster Pharmacy", "note": "Widespread chain with extended hours"},
            {"name": "Boots Pharmacy", "note": "International chain with multiple locations"}
        ],
        "embassies": [
            {
                "country": "United States",
                "address": "Corner of Al Seef Rd and 35th St, Umm Hurair 2, Dubai",
                "phone": "+971 4 309 4000"
            },
            {
                "country": "United Kingdom",
                "address": "Al Seef Road, Bur Dubai, Dubai",
                "phone": "+971 4 309 4444"
            },
            {
                "country": "Australia",
                "address": "Level 25, Burjuman Business Tower, Dubai",
                "phone": "+971 4 508 7100"
            },
            {
                "country": "Canada",
                "address": "26th Floor, Jumeirah Emirates Towers, Dubai",
                "phone": "+971 4 404 8444"
            },
            {
                "country": "India",
                "address": "Al Hamriya, Diplomatic Enclave, Dubai",
                "phone": "+971 4 397 1333"
            }
        ],
        "safety_tips": [
            "Dubai is generally very safe, but take normal precautions with valuables",
            "Keep a copy of your passport and visa with you at all times",
            "Respect local laws and customs to avoid legal issues",
            "Stay hydrated, especially during summer months",
            "Use registered taxis or ride-hailing services for transportation",
            "Be cautious when swimming in the sea and follow beach safety flags",
            "In case of emergency, dial 999 for police assistance"
        ]
    }

def get_simulated_local_customs() -> Dict[str, Any]:
    """Generate simulated information about local customs and etiquette in Dubai."""
    return {
        "dress_code": {
            "title": "Dress Code in Dubai",
            "content": "While Dubai is cosmopolitan, it's important to dress modestly, especially in public places. Shoulders and knees should be covered in shopping malls, public buildings, and religious sites. Beachwear is acceptable only at beaches and pool areas. For Emirati cultural sites or mosques, women should cover their hair, shoulders, and wear loose clothing to the ankles.",
            "guidelines": [
                {"location": "Shopping Malls", "recommendation": "Smart casual, shoulders and knees covered"},
                {"location": "Beaches & Pools", "recommendation": "Swimwear acceptable, no topless sunbathing"},
                {"location": "Mosques", "recommendation": "Women: hair, shoulders, arms covered, loose ankle-length clothing; Men: long pants, shoulders covered"},
                {"location": "Restaurants", "recommendation": "Smart casual to formal depending on the venue"},
                {"location": "Business Meetings", "recommendation": "Conservative business attire"}
            ]
        },
        "social_etiquette": {
            "title": "Social Etiquette in Dubai",
            "content": "Emirati culture values hospitality, respect, and modesty. Public displays of affection should be limited to holding hands. Avoid eating, drinking, or smoking in public during Ramadan daylight hours. When greeting Emiratis, wait for them to initiate handshakes, especially with the opposite gender. Using the right hand for eating, accepting items, or handshakes is customary as the left hand is considered unclean.",
            "key_points": [
                "Greet with 'As-salām 'alaykum' (peace be upon you) if you can",
                "Wait for the opposite gender to extend their hand first for a handshake",
                "Remove shoes when entering Emirati homes",
                "Accept offered refreshments as refusing can be considered rude",
                "Avoid showing the soles of your feet to others",
                "Ask permission before photographing locals, especially women",
                "Stand when elderly people or dignitaries enter the room"
            ]
        },
        "religious_customs": {
            "title": "Religious Customs",
            "content": "Islam influences daily life in Dubai. The call to prayer is heard five times daily, and Muslims may pause their activities to pray. During the holy month of Ramadan, Muslims fast from dawn to sunset. Non-Muslims should refrain from eating, drinking, or smoking in public during daylight hours out of respect. Many restaurants offer screened areas for daytime dining during this period.",
            "ramadan_etiquette": [
                "Do not eat, drink, or smoke in public during daylight hours",
                "Dress more conservatively than usual",
                "Be understanding of reduced business hours",
                "Expect restaurants to be busy at sunset for Iftar (breaking fast)",
                "Consider greeting with 'Ramadan Kareem' (Generous Ramadan) or 'Ramadan Mubarak' (Blessed Ramadan)"
            ]
        },
        "business_etiquette": {
            "title": "Business Etiquette",
            "content": "Business in Dubai blends Western practices with Arab traditions. Relationships are valued, so invest time in building rapport before discussing business matters. Punctuality is appreciated, though meetings may not always start on time. Business cards should be presented and received with the right hand. Decision-making may take longer than in Western cultures, requiring patience.",
            "meeting_tips": [
                "Exchange pleasantries and accept refreshments before business discussions",
                "Business cards should be in English and Arabic if possible",
                "Dress conservatively and professionally",
                "Avoid scheduling meetings during prayer times",
                "Be patient with decision-making processes",
                "Friday and Saturday are the weekend in UAE"
            ]
        },
        "photography": {
            "title": "Photography Guidelines",
            "content": "While Dubai is photogenic, there are restrictions on photography. Avoid photographing government buildings, military installations, ports, and airports. Always ask permission before photographing locals, especially women. During religious festivals or in religious areas, be particularly respectful with photography.",
            "restricted_areas": [
                "Government buildings",
                "Military installations",
                "Airport facilities",
                "Port areas",
                "Palaces",
                "Court buildings"
            ]
        },
        "alcohol_consumption": {
            "title": "Alcohol Consumption",
            "content": "Alcohol is available in licensed venues such as hotels, restaurants, and clubs. Non-Muslim residents can obtain a license to purchase alcohol for home consumption. Public intoxication and drinking in public places are illegal and can result in fines or imprisonment. During Ramadan, alcohol service may be restricted to certain hours and venues.",
            "guidelines": [
                "Only consume alcohol in licensed establishments",
                "Never drink and drive - zero tolerance policy",
                "Do not appear intoxicated in public",
                "Alcohol may not be served during certain hours in Ramadan",
                "Legal drinking age is 21"
            ]
        }
    }

# Register tools with the registry
tool_registry.register_tool(
    tool_name="get_cultural_info",
    tool_function=get_cultural_info,
    category="local_info",
    description="Get cultural information about Dubai",
    required_params=[],
    optional_params=["topic"]
)

tool_registry.register_tool(
    tool_name="get_practical_info",
    tool_function=get_practical_info,
    category="local_info",
    description="Get practical information about Dubai",
    required_params=[],
    optional_params=["topic"]
)

tool_registry.register_tool(
    tool_name="get_emergency_info",
    tool_function=get_emergency_info,
    category="local_info",
    description="Get emergency information for Dubai",
    required_params=[],
    optional_params=[]
)

tool_registry.register_tool(
    tool_name="get_local_customs",
    tool_function=get_local_customs,
    category="local_info",
    description="Get information about local customs and etiquette in Dubai",
    required_params=[],
    optional_params=[]
)
