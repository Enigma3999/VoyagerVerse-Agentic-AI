import json
import logging
import datetime
import random
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("booking_system")

class BookingSystem:
    """Simulated booking system for the VoyagerVerse agentic AI.
    
    This class handles:
    1. Simulating booking operations for activities, restaurants, etc.
    2. Managing cancellations and rebookings
    3. Tracking booking history and status
    """
    
    def __init__(self):
        self.bookings = {}  # Dictionary of active bookings
        self.booking_history = []  # History of all booking operations
        self.providers = {  # Simulated booking providers
            "activities": ["Dubai Tourism", "GetYourGuide", "Viator", "Klook"],
            "dining": ["OpenTable", "Resy", "Direct Booking"],
            "transportation": ["Uber", "Careem", "Dubai Taxi"],
            "accommodations": ["Booking.com", "Hotels.com", "Airbnb", "Direct Booking"]
        }
    
    def book_activity(self, activity: Dict[str, Any], date: str, time_slot: str) -> Dict[str, Any]:
        """Book an activity and return booking details."""
        booking_id = f"ACT-{random.randint(10000, 99999)}"
        provider = random.choice(self.providers["activities"])
        
        booking = {
            "booking_id": booking_id,
            "type": "activity",
            "activity": activity,
            "date": date,
            "time_slot": time_slot,
            "provider": provider,
            "status": "confirmed",
            "booking_time": datetime.datetime.now().isoformat(),
            "confirmation_code": f"{provider[:3].upper()}{random.randint(100000, 999999)}",
            "cancellation_policy": self._generate_cancellation_policy()
        }
        
        # Store the booking
        self.bookings[booking_id] = booking
        
        # Record in history
        self._record_booking_operation("create", booking)
        
        logger.info(f"Booked activity: {activity['name']} on {date} at {time_slot}")
        return booking
    
    def book_dining(self, restaurant: Dict[str, Any], date: str, time: str, party_size: int) -> Dict[str, Any]:
        """Book a restaurant and return booking details."""
        booking_id = f"DIN-{random.randint(10000, 99999)}"
        provider = random.choice(self.providers["dining"])
        
        booking = {
            "booking_id": booking_id,
            "type": "dining",
            "restaurant": restaurant,
            "date": date,
            "time": time,
            "party_size": party_size,
            "provider": provider,
            "status": "confirmed",
            "booking_time": datetime.datetime.now().isoformat(),
            "confirmation_code": f"{provider[:3].upper()}{random.randint(100000, 999999)}",
            "cancellation_policy": "Free cancellation up to 2 hours before reservation"
        }
        
        # Store the booking
        self.bookings[booking_id] = booking
        
        # Record in history
        self._record_booking_operation("create", booking)
        
        logger.info(f"Booked dining at: {restaurant['name']} on {date} at {time}")
        return booking
    
    def book_transportation(self, transport_type: str, pickup_location: str, 
                           dropoff_location: str, date: str, time: str) -> Dict[str, Any]:
        """Book transportation and return booking details."""
        booking_id = f"TRN-{random.randint(10000, 99999)}"
        provider = random.choice(self.providers["transportation"])
        
        booking = {
            "booking_id": booking_id,
            "type": "transportation",
            "transport_type": transport_type,
            "pickup_location": pickup_location,
            "dropoff_location": dropoff_location,
            "date": date,
            "time": time,
            "provider": provider,
            "status": "confirmed",
            "booking_time": datetime.datetime.now().isoformat(),
            "confirmation_code": f"{provider[:3].upper()}{random.randint(100000, 999999)}",
            "cancellation_policy": "Free cancellation up to 1 hour before pickup"
        }
        
        # Store the booking
        self.bookings[booking_id] = booking
        
        # Record in history
        self._record_booking_operation("create", booking)
        
        logger.info(f"Booked {transport_type} from {pickup_location} to {dropoff_location} on {date} at {time}")
        return booking
    
    def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """Cancel an existing booking."""
        if booking_id not in self.bookings:
            logger.error(f"Booking not found: {booking_id}")
            return {"status": "error", "message": "Booking not found"}
        
        booking = self.bookings[booking_id]
        
        # Check if already cancelled
        if booking["status"] == "cancelled":
            return {"status": "error", "message": "Booking already cancelled"}
        
        # Update status
        booking["status"] = "cancelled"
        booking["cancellation_time"] = datetime.datetime.now().isoformat()
        
        # Calculate cancellation fee based on policy
        cancellation_fee = self._calculate_cancellation_fee(booking)
        booking["cancellation_fee"] = cancellation_fee
        
        # Record in history
        self._record_booking_operation("cancel", booking)
        
        logger.info(f"Cancelled booking: {booking_id} with fee: {cancellation_fee}")
        return {"status": "success", "booking": booking}
    
    def modify_booking(self, booking_id: str, modifications: Dict[str, Any]) -> Dict[str, Any]:
        """Modify an existing booking."""
        if booking_id not in self.bookings:
            logger.error(f"Booking not found: {booking_id}")
            return {"status": "error", "message": "Booking not found"}
        
        booking = self.bookings[booking_id]
        
        # Check if already cancelled
        if booking["status"] == "cancelled":
            return {"status": "error", "message": "Cannot modify cancelled booking"}
        
        # Store original for history
        original_booking = booking.copy()
        
        # Apply modifications
        for key, value in modifications.items():
            if key in booking and key not in ["booking_id", "type", "status", "booking_time"]:
                booking[key] = value
        
        # Update modification time
        booking["last_modified"] = datetime.datetime.now().isoformat()
        booking["modification_count"] = booking.get("modification_count", 0) + 1
        
        # Record in history
        self._record_booking_operation("modify", booking, original_booking)
        
        logger.info(f"Modified booking: {booking_id}")
        return {"status": "success", "booking": booking}
    
    def get_booking(self, booking_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a booking by ID."""
        return self.bookings.get(booking_id)
    
    def get_bookings_for_date(self, date: str) -> List[Dict[str, Any]]:
        """Get all bookings for a specific date."""
        return [b for b in self.bookings.values() if b.get("date") == date and b.get("status") == "confirmed"]
    
    def _generate_cancellation_policy(self) -> str:
        """Generate a random cancellation policy."""
        policies = [
            "Free cancellation up to 24 hours before start time",
            "Free cancellation up to 48 hours before start time",
            "50% refund if cancelled 24 hours before start time",
            "Non-refundable"
        ]
        return random.choice(policies)
    
    def _calculate_cancellation_fee(self, booking: Dict[str, Any]) -> float:
        """Calculate cancellation fee based on policy and timing."""
        policy = booking.get("cancellation_policy", "")
        
        # Default price for simulation
        price = booking.get("price", 100.0)
        
        # Parse booking date and time
        booking_date = booking.get("date", "")
        booking_time = booking.get("time", booking.get("time_slot", ""))
        
        if not booking_date or not booking_time:
            return 0.0
        
        # Try to parse the booking datetime
        try:
            # Extract start time if it's a range
            if "-" in booking_time:
                booking_time = booking_time.split("-")[0]
            
            booking_dt_str = f"{booking_date} {booking_time}"
            booking_dt = datetime.datetime.strptime(booking_dt_str, "%Y-%m-%d %H:%M")
            
            # Calculate hours until booking
            now = datetime.datetime.now()
            hours_until_booking = (booking_dt - now).total_seconds() / 3600
            
            # Apply policy
            if "Free cancellation" in policy:
                # Extract hours from policy
                hours_limit = 24  # Default
                if "48 hours" in policy:
                    hours_limit = 48
                elif "24 hours" in policy:
                    hours_limit = 24
                elif "12 hours" in policy:
                    hours_limit = 12
                elif "2 hours" in policy:
                    hours_limit = 2
                
                if hours_until_booking >= hours_limit:
                    return 0.0  # Free cancellation
                else:
                    return price  # Full price as fee
            
            elif "50% refund" in policy:
                hours_limit = 24  # Default
                if "48 hours" in policy:
                    hours_limit = 48
                
                if hours_until_booking >= hours_limit:
                    return price * 0.5  # 50% fee
                else:
                    return price  # Full price as fee
            
            elif "Non-refundable" in policy:
                return price  # Full price as fee
            
        except Exception as e:
            logger.error(f"Error calculating cancellation fee: {e}")
        
        # Default to no fee if we can't calculate
        return 0.0
    
    def _record_booking_operation(self, operation: str, booking: Dict[str, Any], 
                                 original_booking: Dict[str, Any] = None) -> None:
        """Record a booking operation in the history."""
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "operation": operation,
            "booking_id": booking["booking_id"],
            "booking_type": booking["type"],
            "booking": booking
        }
        
        if original_booking:
            record["original_booking"] = original_booking
        
        self.booking_history.append(record)
    
    def check_availability(self, activity_type: str, date: str) -> Dict[str, List[str]]:
        """Check availability for a given activity type and date."""
        # In a real implementation, this would query external APIs
        # For the prototype, we'll simulate availability
        
        available_slots = {}
        
        if activity_type == "desert_safari":
            available_slots = {
                "morning": ["06:00-10:00", "07:00-11:00"],
                "afternoon": ["14:00-18:00", "15:00-19:00"],
                "evening": ["16:00-20:00"]
            }
        elif activity_type == "cultural_tour":
            available_slots = {
                "morning": ["09:00-12:00", "10:00-13:00"],
                "afternoon": ["13:00-16:00", "14:00-17:00"],
                "evening": ["17:00-20:00"]
            }
        elif activity_type == "water_activity":
            available_slots = {
                "morning": ["08:00-10:00", "10:00-12:00"],
                "afternoon": ["13:00-15:00", "15:00-17:00"],
                "evening": ["17:00-19:00"]
            }
        else:
            # Generic availability for other activities
            available_slots = {
                "morning": ["09:00-11:00", "11:00-13:00"],
                "afternoon": ["14:00-16:00", "16:00-18:00"],
                "evening": ["19:00-21:00"]
            }
        
        # Simulate some slots being unavailable
        for time_of_day in available_slots:
            if random.random() < 0.3:  # 30% chance of a time slot being unavailable
                if len(available_slots[time_of_day]) > 1:
                    available_slots[time_of_day].pop(random.randint(0, len(available_slots[time_of_day]) - 1))
        
        return available_slots

# Example usage for Tom & Priya scenario
def create_tom_priya_booking_scenario():
    """Create a sample booking scenario for Tom & Priya's Dubai vacation."""
    booking_system = BookingSystem()
    
    # Book their original desert safari
    desert_safari = {
        "name": "Desert Safari",
        "description": "Experience the thrill of dune bashing followed by a traditional desert camp experience",
        "location": "Al Marmoom Desert",
        "category": "adventure",
        "is_outdoor": True,
        "energy_required": 0.7,
        "price": 150.0
    }
    
    original_booking = booking_system.book_activity(
        activity=desert_safari,
        date="2025-04-25",
        time_slot="14:00-18:00"
    )
    
    # Check availability for alternative morning slots
    morning_availability = booking_system.check_availability("desert_safari", "2025-04-26")
    
    # Book an alternative cultural activity
    museum_tour = {
        "name": "Dubai Museum Cultural Tour",
        "description": "Explore Dubai's rich cultural heritage in the air-conditioned Dubai Museum",
        "location": "Al Fahidi Historical District",
        "category": "culture",
        "is_outdoor": False,
        "energy_required": 0.4,
        "price": 85.0
    }
    
    alternative_booking = booking_system.book_activity(
        activity=museum_tour,
        date="2025-04-25",
        time_slot="14:00-16:00"
    )
    
    # Cancel the original desert safari booking
    cancellation_result = booking_system.cancel_booking(original_booking["booking_id"])
    
    # Book the desert safari for a morning slot on the next day
    if morning_availability["morning"]:
        rescheduled_booking = booking_system.book_activity(
            activity=desert_safari,
            date="2025-04-26",
            time_slot=morning_availability["morning"][0]
        )
    else:
        rescheduled_booking = None
    
    return {
        "original_booking": original_booking,
        "cancellation_result": cancellation_result,
        "alternative_booking": alternative_booking,
        "morning_availability": morning_availability,
        "rescheduled_booking": rescheduled_booking
    }

if __name__ == "__main__":
    # This can be used for testing the module independently
    scenario_result = create_tom_priya_booking_scenario()
    print(json.dumps(scenario_result["cancellation_result"], indent=2))
