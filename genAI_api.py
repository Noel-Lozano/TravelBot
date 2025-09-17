import os
import google.generativeai as genai

# Configure Gemini API
GEMINI_KEY = os.environ.get("GEMINI_KEY")
if not GEMINI_KEY:
    raise ValueError("GEMINI_KEY environment variable is not set.")

genai.configure(api_key=GEMINI_KEY)

def build_prompt(city, date, budget, weather):
    """Builds a prompt for Gemini based on user input and forecasted weather."""
    return f"""
        You are a smart travel planner. Create a personalized day itinerary for a user visiting {city} on {date}.

        Weather forecast: {weather}.
        Budget: {budget} USD.

        Rules:
        - If the weather is sunny, clear, or warm → prioritize outdoor activities (parks, walking tours, outdoor dining).
        - If the weather is rainy, stormy, or cold → prioritize indoor activities (museums, cafes, shopping, shows).
        - If the weather is moderate or uncertain → balance indoor and outdoor activities.
        - Ensure total activities reasonably fit within the budget.
        - Format response as a clear, hour-by-hour schedule (e.g., "9:00–11:00 AM: Visit ...").

        Return the plan in a clean, readable format without extra commentary.
    """.strip()

def generate_itinerary(city, date, budget, weather):
    """Generates a travel itinerary using the Gemini model."""
    prompt = build_prompt(city, date, budget, weather)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Failed to generate itinerary: {e}")
        return "Sorry, something went wrong while generating your itinerary."
