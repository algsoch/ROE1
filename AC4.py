import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("DELHI.csv")

# Ensure AC column is treated as a string
df["AC"] = df["AC"].astype(str)

# Extract only the constituency name (remove leading numbers)
df["AC_NAME"] = df["AC"].str.replace(r"^\d+\s*", "", regex=True).str.strip()

# Filter for AC_4 = 'SANGAM VIHAR'
df_sangam = df[df["AC_NAME"] == "SANGAM VIHAR"]

# Function to detect outliers using IQR
def count_outliers(group):
    Q1 = group["VOTES"].quantile(0.25)
    Q3 = group["VOTES"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = group[(group["VOTES"] < lower_bound) | (group["VOTES"] > upper_bound)]
    return len(outliers)

# Apply outlier function per election year
outlier_counts = df_sangam.groupby("YEAR").apply(count_outliers)

# Find the election year with the most outliers
most_outliers_year = outlier_counts.idxmax()
max_outliers = outlier_counts.max()

# Display the result
print("Election year with the most outliers:", most_outliers_year, "with", max_outliers, "outliers")

# Plot a line graph
plt.figure(figsize=(10, 5))
plt.plot(outlier_counts.index, outlier_counts.values, marker='o', linestyle='-', color='b', label='Outliers per Year')
plt.xlabel("Election Year")
plt.ylabel("Number of Outliers")
plt.title("Outliers in Candidate Votes (SANGAM VIHAR)")
plt.xticks(outlier_counts.index)
plt.grid(True)
plt.legend()
plt.show()
