from datetime import datetime
from weather_api import get_weather
from genAI_api import generate_itinerary
from db_utils import save_search, get_search_history, clear_search_history

def make_itinerary():
    """Collects user input for itinerary generation and displays the result."""
    city = input("Enter the city: ").strip()
    date = input("Enter the date (YYYY-MM-DD) [default: today]: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    budget_input = input("Enter your budget (USD) [default: 100]: ").strip()
    try:
        budget = float(budget_input) if budget_input else 100.0
    except ValueError:
        print("⚠️ Invalid budget. Defaulting to $100.")
        budget = 100.0

    try:
        weather = get_weather(city, date)
    except Exception as e:
        print(f"⚠️ Weather lookup failed: {e}")
        weather = "moderate"

    itinerary = generate_itinerary(city, date, budget, weather)

    print("\nGenerated Itinerary:")
    print(itinerary)
    return city, date, budget, weather, itinerary

def display_search_history():
    """Displays the search history from the database."""
    print("\nSearch History:")
    history = get_search_history()
    if history.empty:
        print("No search history found.")
    else:
        print(history.to_string(index=False))

def clear_history():
    """Clears the search history after user confirmation."""
    confirm = input("\nAre you sure you want to clear the search history? (yes/no): ").strip().lower()
    if confirm == 'yes':
        clear_search_history()
        print("Search history cleared.")
    else:
        print("Search history not cleared.")

def saving_search(city, date, budget, weather, itinerary):
    """Saves the search entry to the database."""
    print("\nSaving your search...")
    entry = {
        "city": city,
        "date": date,
        "budget": budget,
        "weather": str(weather),
        "itinerary": itinerary
    }
    save_search(entry)
    print("Search saved successfully.")

def main():
    exit_program = False
    print("\n🌍 Welcome to TravelBot, the Travel Itinerary Generator! 🌍")
    print("This program helps you plan your trip by generating a personalized itinerary.\n")

    while not exit_program:
        print("\nMenu:")
        print("1. Generate Itinerary")
        print("2. View Search History")
        print("3. Clear Search History")
        print("4. Exit")

        choice = input("\nPlease choose an option (1-4): ").strip()

        if choice == '1':
            city, date, budget, weather, itinerary = make_itinerary()
            save_option = input("Would you like to save this search? (yes/no): ").strip().lower()
            if save_option == 'yes':
                saving_search(city, date, budget, weather, itinerary)
            else:
                print("Search not saved.")
        elif choice == '2':
            display_search_history()
        elif choice == '3':
            clear_history()
        elif choice == '4':
            exit_program = True
            print("Thank you for using TravelBot. Goodbye!")
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
