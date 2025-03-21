import requests
import os

directions_api = "https://api.openrouteservice.org/v2/pdirections/driving-car/geojson"
geocode_api = "https://api.openrouteservice.org/pgeocode/search?"
key = os.getenv("API_KEY")


def geocode_address(address):
    url = f"{geocode_api}api_key={key}&text={address}"
    headers = {
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://maps.openrouteservice.org",
        "priority": "u=1, i",
        "referer": "https://maps.openrouteservice.org/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        if json_data["features"]:
            coords = json_data["features"][0]["geometry"]["coordinates"]
            print(f"Geocoded coordinates for '{address}': {coords}")  # Debugging
            if -90 <= coords[1] <= 90 and -180 <= coords[0] <= 180:
                return coords
            else:
                print(f"Error: Invalid coordinates for address '{address}'")
                return None
        else:
            print(f"Error: No results found for address '{address}'")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


while True:
    orig = input("Starting Location: ")
    if (orig == "q") or (orig == "quit"):
        break
    dest = input("Destination: ")
    if (dest == "q") or (dest == "quit"):
        break
    # Geocode the addresses
    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)

    if not orig_coords or not dest_coords:
        print("Unable to geocode one or both addresses. Please try again.\n")
        continue

    # Construct the JSON body for the POST request
    body = {"coordinates": [orig_coords, dest_coords]}

    # Make the POST request
    headers = {
        "authorization": key,
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://maps.openrouteservice.org",
        "priority": "u=1, i",
        "referer": "https://maps.openrouteservice.org/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    }
    response = requests.post(directions_api, headers=headers, json=body)
    json_data = response.json()
    print(json_data)  # Debugging
    if response.status_code == 200:
        if "features" in json_data and json_data["features"]:
            route = json_data["features"][0]["properties"]
            if "segments" in route and route["segments"]:
                segment = route["segments"][0]
                print("\nAPI Status: Successful route call.\n")
                print("=============================================")
                print(f"Directions from {orig} to {dest}")

                # Extract trip duration and distance
                duration = segment.get("duration", "N/A")
                distance = segment.get("distance", "N/A")

                print(f"Trip Duration: {duration} seconds")
                print(f"Distance: {distance} meters")
                print("=============================================")
                # Extract and print step-by-step directions
                if "steps" in segment:
                    for step in segment["steps"]:
                        instruction = step.get("instruction", "N/A")
                        step_distance = step.get("distance", "N/A")
                        print(f"{instruction} ({step_distance} meters)")
                else:
                    print("No step-by-step directions available.")

                print("=============================================\n")
            else:
                print("Error: No segments found in the route.")
        else:
            print("Error: No routes found in the response.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
