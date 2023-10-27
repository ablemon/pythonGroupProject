import urllib.parse
import requests

# Constants for the API URL and key to avoid magic numbers or strings in the code.
BASE_API_URL = "https://www.mapquestapi.com/directions/v2/route?"
API_KEY = "BTw9izOjRKvMLuSU4CFHzJvhs34ExhaB"
# All lists created for the ease of usability
end_var = ['q', 'quit', 'stop', 'end']
miles_var = ['m', 'mi', 'miles']
km_var = ['k', 'km', 'kilometers']

# Function to build the URL for the request using the starting and destination locations.
def build_url(start, destination):
    return BASE_API_URL + urllib.parse.urlencode({"key": API_KEY, "from": start, "to": destination})

# Function to fetch route data using the constructed URL.
def get_route_data(url):
    return requests.get(url).json()

# Function to print out the route information in a formatted manner.
# This function now also handles the conversion between miles and kilometers.
def print_route_info(data, orig, dest, unit):
    conversion = 1.61 if unit == 'km' else 1  # Choose conversion factor based on user's choice.
    unit_name = "Kilometers" if unit == 'km' else "Miles"
    
    print("=============================================")
    print(f"Directions from {orig} to {dest}")
    print(f"Trip Duration: {data['route']['formattedTime']}")
    print(f"{unit_name}: {data['route']['distance'] * conversion:.2f}")
    print("=============================================\n")
    
    for idx, step in enumerate(data['route']['legs'][0]['maneuvers'], 1):  # Starting index from 1
        print(f"{idx}. {step['narrative']} ({step['distance'] * conversion:.2f} {unit})\n")
    print("=============================================\n")

# Function to handle different status codes returned by the API.
def handle_response_status(status_code):
    messages = {
        0: "A successful route call.",
        402: "Invalid user inputs for one or both locations.",
        611: "Missing an entry for one or both locations."
    }
    
    if status_code in messages:
        print(f"Status Code: {status_code}; {messages[status_code]}")
    else:
        print(f"For Status Code: {status_code}; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
    print("=============================================\n")

# Main execution flow.
def main():
    while True:
        orig = input("Starting Location: ")
        if orig in end_var:
            print("Ending task...")
            break

        dest = input("Destination: ")
        if dest in end_var:
            print("Ending task...")
            break
        
        # Added prompt for user to choose between kilometers and miles.
        while True:
            unit = input("Choose prefered unit of measurement (Miles or KM): ").strip().lower()
            if unit in miles_var:
                print("You chose miles.\n")
                break  # Exit the unit input loop when a valid choice is provided
            elif unit in km_var:
                print("You chose kilometers.\n")
                break  # Exit the unit input loop when a valid choice is provided
            elif unit in end_var:
                print("Ending task...")
                exit(1)
            else: 
                print("Invalid unit choice, please try again...") # Ask again until a valid input is presented
        
        url = build_url(orig, dest)
        data = get_route_data(url)
        status = data["info"]["statuscode"]
        
        # Using function calls to handle specific tasks.
        if status == 0:
            print_route_info(data, orig, dest, unit)
        else:
            handle_response_status(status)
        
        if not ask_for_another_route():
            print("Thank you, terminating program...")
            break


def ask_for_another_route():
    while True:
        choice = input("Do you want directions to another location? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n'] or end_var:
            return False
        else:
            print("Invalid choice. Please answer with 'yes' or 'no'.")

# Ensuring the script only runs when executed directly.
if __name__ == "__main__":
    main()
