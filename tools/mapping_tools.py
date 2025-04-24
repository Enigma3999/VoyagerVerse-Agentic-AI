import requests
import logging
import os
from typing import Dict, List, Any, Optional

from tools.tool_registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mapping_tools")

# API keys would normally be stored in environment variables
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "your_google_maps_api_key")
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY", "your_tomtom_api_key")

def geocode_location(address: str, provider: str = "google") -> Dict[str, Any]:
    """Convert an address to geographic coordinates."""
    if provider.lower() == "google":
        return geocode_google(address)
    elif provider.lower() == "tomtom":
        return geocode_tomtom(address)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def geocode_google(address: str) -> Dict[str, Any]:
    """Geocode an address using Google Maps API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "OK":
            logger.error(f"Google Geocoding API error: {data['status']}")
            return {
                "status": "error",
                "message": f"Geocoding failed: {data['status']}",
                "data": get_simulated_geocode(address)
            }
        
        result = data["results"][0]
        location = result["geometry"]["location"]
        
        geocode_data = {
            "provider": "Google Maps",
            "address": address,
            "formatted_address": result["formatted_address"],
            "latitude": location["lat"],
            "longitude": location["lng"],
            "place_id": result["place_id"]
        }
        
        return {
            "status": "success",
            "data": geocode_data
        }
    
    except Exception as e:
        logger.error(f"Error geocoding with Google Maps: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_geocode(address)
        }

def geocode_tomtom(address: str) -> Dict[str, Any]:
    """Geocode an address using TomTom API."""
    url = "https://api.tomtom.com/search/2/geocode/{}.json".format(address)
    params = {
        "key": TOMTOM_API_KEY,
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results") or len(data["results"]) == 0:
            logger.error("TomTom Geocoding API returned no results")
            return {
                "status": "error",
                "message": "Geocoding failed: No results",
                "data": get_simulated_geocode(address)
            }
        
        result = data["results"][0]
        position = result["position"]
        
        geocode_data = {
            "provider": "TomTom",
            "address": address,
            "formatted_address": result.get("address", {}).get("freeformAddress", address),
            "latitude": position["lat"],
            "longitude": position["lon"],
            "place_id": result.get("id", "")
        }
        
        return {
            "status": "success",
            "data": geocode_data
        }
    
    except Exception as e:
        logger.error(f"Error geocoding with TomTom: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_geocode(address)
        }

def get_distance_matrix(origins: List[str], destinations: List[str], 
                       mode: str = "driving", provider: str = "google") -> Dict[str, Any]:
    """Get distance and duration between multiple origins and destinations."""
    if provider.lower() == "google":
        return get_distance_matrix_google(origins, destinations, mode)
    elif provider.lower() == "tomtom":
        return get_distance_matrix_tomtom(origins, destinations, mode)
    else:
        return {
            "status": "error",
            "message": f"Unknown provider: {provider}"
        }

def get_distance_matrix_google(origins: List[str], destinations: List[str], 
                              mode: str = "driving") -> Dict[str, Any]:
    """Get distance matrix using Google Maps API."""
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(origins),
        "destinations": "|".join(destinations),
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "OK":
            logger.error(f"Google Distance Matrix API error: {data['status']}")
            return {
                "status": "error",
                "message": f"Distance Matrix failed: {data['status']}",
                "data": get_simulated_distance_matrix(origins, destinations)
            }
        
        matrix_data = {
            "provider": "Google Maps",
            "origins": origins,
            "destinations": destinations,
            "mode": mode,
            "results": []
        }
        
        for i, origin_row in enumerate(data["rows"]):
            origin = origins[i]
            origin_results = []
            
            for j, element in enumerate(origin_row["elements"]):
                destination = destinations[j]
                
                if element["status"] == "OK":
                    origin_results.append({
                        "origin": origin,
                        "destination": destination,
                        "distance": {
                            "value": element["distance"]["value"],  # meters
                            "text": element["distance"]["text"]
                        },
                        "duration": {
                            "value": element["duration"]["value"],  # seconds
                            "text": element["duration"]["text"]
                        }
                    })
                else:
                    origin_results.append({
                        "origin": origin,
                        "destination": destination,
                        "status": element["status"]
                    })
            
            matrix_data["results"].extend(origin_results)
        
        return {
            "status": "success",
            "data": matrix_data
        }
    
    except Exception as e:
        logger.error(f"Error getting distance matrix with Google Maps: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_distance_matrix(origins, destinations)
        }

def get_distance_matrix_tomtom(origins: List[str], destinations: List[str], 
                              mode: str = "car") -> Dict[str, Any]:
    """Get distance matrix using TomTom API."""
    # TomTom requires coordinates, so we need to geocode addresses first
    origin_coords = []
    for origin in origins:
        geocode_result = geocode_tomtom(origin)
        if geocode_result["status"] == "success":
            lat = geocode_result["data"]["latitude"]
            lon = geocode_result["data"]["longitude"]
            origin_coords.append(f"{lat},{lon}")
        else:
            # Use simulated coordinates if geocoding fails
            sim_geocode = get_simulated_geocode(origin)
            origin_coords.append(f"{sim_geocode['latitude']},{sim_geocode['longitude']}")
    
    destination_coords = []
    for dest in destinations:
        geocode_result = geocode_tomtom(dest)
        if geocode_result["status"] == "success":
            lat = geocode_result["data"]["latitude"]
            lon = geocode_result["data"]["longitude"]
            destination_coords.append(f"{lat},{lon}")
        else:
            # Use simulated coordinates if geocoding fails
            sim_geocode = get_simulated_geocode(dest)
            destination_coords.append(f"{sim_geocode['latitude']},{sim_geocode['longitude']}")
    
    # Map Google mode to TomTom mode
    mode_map = {
        "driving": "car",
        "walking": "pedestrian",
        "bicycling": "bicycle",
        "transit": "car"  # TomTom doesn't have transit, fallback to car
    }
    tomtom_mode = mode_map.get(mode, "car")
    
    url = "https://api.tomtom.com/routing/1/matrix/sync/json"
    payload = {
        "origins": [{"point": {"latitude": float(coord.split(',')[0]), "longitude": float(coord.split(',')[1])}} for coord in origin_coords],
        "destinations": [{"point": {"latitude": float(coord.split(',')[0]), "longitude": float(coord.split(',')[1])}} for coord in destination_coords],
        "options": {
            "routeType": tomtom_mode
        }
    }
    params = {
        "key": TOMTOM_API_KEY
    }
    
    try:
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        
        matrix_data = {
            "provider": "TomTom",
            "origins": origins,
            "destinations": destinations,
            "mode": mode,
            "results": []
        }
        
        for i, origin_row in enumerate(data.get("data", [])):
            origin = origins[i] if i < len(origins) else f"Origin {i}"
            
            for j, element in enumerate(origin_row):
                destination = destinations[j] if j < len(destinations) else f"Destination {j}"
                
                if element.get("statusCode", 200) == 200:
                    matrix_data["results"].append({
                        "origin": origin,
                        "destination": destination,
                        "distance": {
                            "value": element.get("routeSummary", {}).get("lengthInMeters", 0),
                            "text": f"{element.get('routeSummary', {}).get('lengthInMeters', 0) / 1000:.1f} km"
                        },
                        "duration": {
                            "value": element.get("routeSummary", {}).get("travelTimeInSeconds", 0),
                            "text": f"{element.get('routeSummary', {}).get('travelTimeInSeconds', 0) // 60} mins"
                        }
                    })
                else:
                    matrix_data["results"].append({
                        "origin": origin,
                        "destination": destination,
                        "status": "FAILED"
                    })
        
        return {
            "status": "success",
            "data": matrix_data
        }
    
    except Exception as e:
        logger.error(f"Error getting distance matrix with TomTom: {e}")
        return {
            "status": "error",
            "message": str(e),
            "data": get_simulated_distance_matrix(origins, destinations)
        }

def get_simulated_geocode(address: str) -> Dict[str, Any]:
    """Generate simulated geocode data for testing purposes."""
    # Dubai coordinates as default
    dubai_coords = {"latitude": 25.2048, "longitude": 55.2708}
    
    # Specific locations in Dubai
    dubai_locations = {
        "burj khalifa": {"latitude": 25.197197, "longitude": 55.274376, "formatted": "Burj Khalifa, Downtown Dubai"},
        "dubai mall": {"latitude": 25.198765, "longitude": 55.279503, "formatted": "Dubai Mall, Downtown Dubai"},
        "palm jumeirah": {"latitude": 25.112350, "longitude": 55.138379, "formatted": "Palm Jumeirah, Dubai"},
        "dubai marina": {"latitude": 25.080105, "longitude": 55.133860, "formatted": "Dubai Marina, Dubai"},
        "dubai airport": {"latitude": 25.252777, "longitude": 55.364445, "formatted": "Dubai International Airport (DXB)"},
        "dubai museum": {"latitude": 25.263395, "longitude": 55.297371, "formatted": "Dubai Museum, Al Fahidi Historical District"},
        "al marmoom": {"latitude": 24.826313, "longitude": 55.277814, "formatted": "Al Marmoom Desert Conservation Reserve, Dubai"}
    }
    
    # Check if address contains any known location
    address_lower = address.lower()
    for key, location in dubai_locations.items():
        if key in address_lower:
            return {
                "provider": "Simulated",
                "address": address,
                "formatted_address": location["formatted"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "place_id": f"sim_{key.replace(' ', '_')}"
            }
    
    # Default to Dubai coordinates with slight variation
    import random
    variation = random.uniform(-0.02, 0.02)  # Small coordinate variation
    
    return {
        "provider": "Simulated",
        "address": address,
        "formatted_address": f"{address}, Dubai, UAE",
        "latitude": dubai_coords["latitude"] + variation,
        "longitude": dubai_coords["longitude"] + variation,
        "place_id": "sim_dubai_location"
    }

def get_simulated_distance_matrix(origins: List[str], destinations: List[str]) -> Dict[str, Any]:
    """Generate simulated distance matrix data for testing purposes."""
    import random
    
    matrix_data = {
        "provider": "Simulated",
        "origins": origins,
        "destinations": destinations,
        "mode": "driving",
        "results": []
    }
    
    for origin in origins:
        for destination in destinations:
            # Generate realistic distances within Dubai (5-30 km)
            distance_km = random.uniform(5, 30)
            distance_m = int(distance_km * 1000)
            
            # Generate realistic durations (roughly 2 mins per km plus traffic)
            duration_mins = distance_km * 2 + random.uniform(5, 15)
            duration_secs = int(duration_mins * 60)
            
            matrix_data["results"].append({
                "origin": origin,
                "destination": destination,
                "distance": {
                    "value": distance_m,
                    "text": f"{distance_km:.1f} km"
                },
                "duration": {
                    "value": duration_secs,
                    "text": f"{int(duration_mins)} mins"
                }
            })
    
    return matrix_data

# Register tools with the registry
tool_registry.register_tool(
    tool_name="geocode_location",
    tool_function=geocode_location,
    category="mapping",
    description="Convert an address to geographic coordinates",
    required_params=["address"],
    optional_params=["provider"]
)

tool_registry.register_tool(
    tool_name="get_distance_matrix",
    tool_function=get_distance_matrix,
    category="mapping",
    description="Get distance and duration between multiple origins and destinations",
    required_params=["origins", "destinations"],
    optional_params=["mode", "provider"]
)
