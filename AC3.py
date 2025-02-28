import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the dataset
df = pd.read_csv("BIHAR.csv")
# Ensure 'AC' column is treated as string before extraction
df["AC"] = df["AC"].astype(str)

# Extract only the name part (remove leading numbers)
df["AC_NAME"] = df["AC"].str.extract(r'^\d+\s*(.*)$')[0]

# Filter for AC_3 = 'BIKRAM'
df_bikram = df[df["AC_NAME"].str.upper() == "BIKRAM"]

# Group data by YEAR
correlation_results = {}

for year, group in df_bikram.groupby("YEAR"):
    # Get votes for male and female candidates
    female_votes = group[group["SEX"] == "F"]["VOTES"]
    male_votes = group[group["SEX"] == "M"]["VOTES"]

    # Check if at least one female candidate is present
    if len(female_votes) > 0 and len(male_votes) > 0:
        # Compute Pearson correlation
        correlation, _ = pearsonr(female_votes, male_votes)
        correlation_results[year] = round(correlation, 4)
    else:
        correlation_results[year] = None  # Fill NA if no female candidates

# Convert results to DataFrame
correlation_df = pd.DataFrame(list(correlation_results.items()), columns=["YEAR", "Pearson_Coefficient"])

# Print the results
print(correlation_df)

# Plot Line Graph
plt.figure(figsize=(10, 5))
plt.plot(correlation_df["YEAR"], correlation_df["Pearson_Coefficient"], marker="o", linestyle="-", color="b")
plt.xlabel("Election Year")
plt.ylabel("Pearson Correlation Coefficient")
plt.title("Correlation between Male & Female Votes in BIKRAM")
plt.grid(True)
plt.show()
