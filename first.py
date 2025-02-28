import requests
import os
import time
import pandas as pd
from bs4 import BeautifulSoup

# Base URL
BASE_URL = "https://jivraj-18.github.io/tds-jan-2025-mock-roe-1/"

def get_soup(url):
    """ Fetch and parse HTML content from a URL. """
    time.sleep(1)  # Avoid getting blocked
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    return None

def extract_data(state_url):
    """ Extract election data from the state's page. """
    soup = get_soup(state_url)
    if not soup:
        return None

    data = []
    rows = soup.find_all("div", class_="r")  # Finding rows

    for row in rows[1:]:  # Skipping header row
        cols = row.find_all("div", class_="c")
        if len(cols) >= 9:  # Ensuring sufficient columns
            data.append([col.text.strip() for col in cols])

    return data

def scrape_all_states():
    """ Scrape data for all states and save as CSV. """
    next_page = BASE_URL  # Start from main URL

    while next_page:
        soup = get_soup(next_page)
        if not soup:
            break

        # Find all state-year links
        links = soup.find_all("div", class_="c")
        state_data = {}

        for i in range(0, len(links), 2):
            if i+1 >= len(links):
                continue

            year = links[i].text.strip()
            state = links[i+1].text.strip()
            anchor_tag = links[i].find("a")  # Get the <a> tag
            
            if not anchor_tag:  # If no <a> tag found, skip
                print(f"Skipping: {year} - {state} (No Link Found)")
                continue

            state_page = BASE_URL + anchor_tag["href"]

            print(f"Scraping: {state} ({year}) from {state_page}")
            data = extract_data(state_page)

            if data:
                if state not in state_data:
                    state_data[state] = []
                state_data[state].extend(data)

        # Save each state's data into separate CSV files
        for state, data in state_data.items():
            df = pd.DataFrame(data, columns=["Index", "ST_NAME", "YEAR", "AC", "CANDIDATE", "SEX", "AGE", "CATEGORY", "PARTY", "VOTES"])
            filename = f"{state}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Saved: {filename}")

        # Check for next page
        next_link = soup.find("a", string="Next page")
        next_page = BASE_URL + next_link["href"] if next_link else None

if __name__ == "__main__":
    scrape_all_states()
