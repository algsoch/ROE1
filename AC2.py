import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import re

def extract_name(ac):
    """Extracts the name from AC column, removing numbers."""
    return re.sub(r'\d+', '', ac).strip()

def get_coordinates(place, state):
    """Returns latitude and longitude for a given place."""
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(f"{place}, {state}, India")
    return (location.latitude, location.longitude) if location else None

def find_nearby_constituencies(file, target_ac):
    df = pd.read_csv(file)
    df['AC_Name'] = df['AC'].apply(extract_name)  # Extract name only
    
    # Get target constituency details
    target_row = df[df['AC_Name'].str.upper() == target_ac.upper()].iloc[0]
    target_party = target_row['PARTY']
    target_winner = target_row['CANDIDATE']
    target_location = get_coordinates(target_ac, "Jharkhand")
    
    if not target_location:
        print("Could not get coordinates for target constituency.")
        return
    
    # Find nearby constituencies
    nearby = []
    for _, row in df.iterrows():
        cons_name = row['AC_Name']
        cons_location = get_coordinates(cons_name, "Jharkhand")
        
        if cons_location:
            distance = geodesic(target_location, cons_location).km
            if distance < 100:
                nearby.append((cons_name, row['PARTY'], row['CANDIDATE']))
    
    # Count constituencies with the same winning party
    same_party_count = sum(1 for c in nearby if c[1] == target_party)
    
    # Print results
    print(f"Target Constituency: {target_ac} (Winner: {target_winner}, Party: {target_party})")
    print(f"Constituencies within 100 km with the same party: {same_party_count}")
    print("\nNearby Constituencies:")
    for cons in nearby:
        print(f"{cons[0]} - Winner: {cons[2]}, Party: {cons[1]}")

# Example usage
find_nearby_constituencies("JHARKHAND.csv", "GANDEY")
