import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

# Constituency and file mapping
ac_files = {
    "HOLENARASIPUR": "KARNATAKA.csv",
    "MANDAR": "JHARKHAND.csv",
    "BIKRAM": "BIHAR.csv",
    "SANGAM VIHAR": "DELHI.csv"
}

# Load data for each constituency
dfs = {ac: pd.read_csv(file) for ac, file in ac_files.items()}

# Step 1: Get the geographical coordinates of each constituency
geolocator = Nominatim(user_agent="geo_locator")
locations = {}

for ac in ac_files.keys():
    loc = geolocator.geocode(f"{ac}, India")
    if loc:
        locations[ac] = (loc.latitude, loc.longitude)

# Step 2: Compute pairwise geographical distances
distances = {}
ac_names = list(locations.keys())

for i in range(len(ac_names)):
    for j in range(i + 1, len(ac_names)):
        ac1, ac2 = ac_names[i], ac_names[j]
        dist = geodesic(locations[ac1], locations[ac2]).km
        distances[(ac1, ac2)] = dist

# Step 3: Identify the closest pair of constituencies
closest_pair = min(distances, key=distances.get)
print(f"Closest constituencies: {closest_pair} (Distance: {distances[closest_pair]:.2f} km)")

# Step 4: Extract winners from the earliest elections
def get_winner(df, ac_name):
    min_year = df["YEAR"].min()
    winner_row = df[df["YEAR"] == min_year].nlargest(1, "VOTES")
    return winner_row["CANDIDATE"].values[0] if not winner_row.empty else None

winners = {ac: get_winner(dfs[ac], ac) for ac in closest_pair}
print(f"Winners from earliest elections: {winners}")

# Step 5: Compute cosine similarity between winner names
vectorizer = TfidfVectorizer()
winner_texts = list(winners.values())
vectors = vectorizer.fit_transform(winner_texts).toarray()  # Convert to NumPy array

similarity = 1 - cosine(vectors[0].flatten(), vectors[1].flatten())  # Ensure 1D array
print(f"Cosine similarity between winners' names: {similarity:.4f}")
