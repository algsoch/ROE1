import pandas as pd
import re  # For regex-based text cleaning

# Load dataset
df = pd.read_csv("KARNATAKA.csv")

# Function to extract only the constituency name (remove numbers)
def extract_constituency_name(ac_value):
    words = re.findall(r'[A-Za-z]+', ac_value)  # Keep only letters (remove numbers)
    return ' '.join(words)  # Join words to reconstruct the name

# Apply function to clean the AC column
df["AC_NAME"] = df["AC"].apply(extract_constituency_name)

# Filter for HOLENARASIPUR constituency
df_hn = df[df["AC_NAME"].str.upper() == "HOLENARASIPUR"]

# Dictionary to store margin percentages
margin_percentages = {}

# Process data year-wise
for year, data in df_hn.groupby("YEAR"):
    # Sort candidates by votes in descending order
    sorted_candidates = data.sort_values(by="VOTES", ascending=False)

    # Ensure there are at least 2 candidates
    if len(sorted_candidates) >= 2:
        winner_votes = sorted_candidates.iloc[0]["VOTES"]
        runner_up_votes = sorted_candidates.iloc[1]["VOTES"]

        # Calculate margin percentage
        margin_percentage = ((winner_votes - runner_up_votes) / winner_votes) * 100
        margin_percentages[year] = margin_percentage

# Find the highest margin percentage
if margin_percentages:
    max_year = max(margin_percentages, key=margin_percentages.get)
    highest_margin = margin_percentages[max_year]

    print(f"Highest margin percentage in HOLENARASIPUR: {highest_margin:.2f}% in {max_year}")
else:
    print("No valid data found for HOLENARASIPUR constituency.")
