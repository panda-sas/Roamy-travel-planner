"""
Example script to test Roamy - AI Travel Planner
"""
import os
from dotenv import load_dotenv
from agents.trip_planner import plan_trip

load_dotenv()

if __name__ == "__main__":
    # Example usage
    destination = "Tokyo, Japan"
    dates = "March 15-22, 2024"
    budget = "Mid-range"
    interests = "Technology, food, temples, anime culture"
    
    print("✈️  Roamy - AI Travel Planner - Example")
    print("=" * 50)
    print(f"Destination: {destination}")
    print(f"Dates: {dates}")
    print(f"Budget: {budget}")
    print(f"Interests: {interests}")
    print("\nGenerating travel plan...\n")
    
    try:
        itinerary = plan_trip(destination, dates, budget, interests)
        print("\n" + "=" * 50)
        print("TRAVEL PLAN")
        print("=" * 50)
        print(itinerary)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set OPENAI_API_KEY in your .env file")

