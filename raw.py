# This script fetches data from PocketBase and writes it to a CSV file

import requests
import csv

POCKETBASE_API_URL = "https://domain.name/api/collections/" # Specify the PocketBase API URL here
COLLECTION_NAME = "station"  # Specify the collection name here
OUTPUT_CSV_FILE = f"{COLLECTION_NAME}.csv"  # Generate the output file name

# Define function to fetch data from PocketBase using pagination
def fetch_pocketbase_data(api_url):
    page = 1
    per_page = 50
    records = []

    while True:
        params = {
            "page": page,
            "perPage": per_page,
            "sort": "-created"
        }

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            json_response = response.json()
            records += json_response.get("items", [])

            # Check if there are more pages to fetch
            if json_response["page"] == json_response["totalPages"]:
                break

            # Move to the next page
            page += 1
        else:
            print("Request to PocketBase failed with status code:", response.status_code)
            break

    return records

# Construct the PocketBase API URL for the specified collection
pocketbase_api_url = f"{POCKETBASE_API_URL}{COLLECTION_NAME}/records"

# Call the function to fetch data from PocketBase
pocketbase_data = fetch_pocketbase_data(pocketbase_api_url)

# Check if there are results in the PocketBase data
if not pocketbase_data:
    print("No data found in PocketBase")
else:
    print("PocketBase data retrieved successfully!")
    # Extract the keys from the first record to use as CSV headers
    headers = list(pocketbase_data[0].keys())

    # Open the CSV file for writing
    with open(OUTPUT_CSV_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        # Write each record to the CSV file
        for record in pocketbase_data:
            writer.writerow(record)

    print("Data written to CSV file:", OUTPUT_CSV_FILE)
