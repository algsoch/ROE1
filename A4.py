import pandas as pd

# Load dataset
df = pd.read_csv("DELHI.csv")

# Ensure "AC" is a string and extract name part
df["AC"] = df["AC"].astype(str)
df["AC_NAME"] = df["AC"].str.extract(r'^\d+\s*(.*)$')[0]

# Filter for AC_4 = 'SANGAM VIHAR'
df_sangam_vihar = df[df["AC_NAME"].str.upper() == "SANGAM VIHAR"]
print(df_sangam_vihar['SEX'])
# Group by year
total_elections = 0
female_won_elections = 0

for year, group in df_sangam_vihar.groupby("YEAR"):
    # Check if there was at least one female candidate
    if (group["SEX"] == "F").any():
        total_elections += 1
        # Check if a female candidate won (highest votes)
        winner = group.loc[group["VOTES"].idxmax()]
        if winner["SEX"] == "F":
            female_won_elections += 1

# Calculate percentage
if total_elections > 0:
    female_win_percentage = round((female_won_elections / total_elections) * 100, 2)
else:
    female_win_percentage = 0.00  # No elections had female candidates

# Print result
print(f"Percentage of elections won by female candidates: {female_win_percentage}%")
