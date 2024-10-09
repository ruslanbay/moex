import csv
import json
import os
from datetime import datetime, timedelta

# Function to read the first column from the TSV file
def read_issues_by_sector(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        return [row[0] for row in reader]

# Function to get a list of new values from JSON files
def get_new_values(start_date, end_date, existing_values):
    new_values = set()
    current_date = start_date

    while current_date <= end_date:
        file_name = f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{current_date.strftime("%Y-%m-%d")}.json'
        
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                # Extracting values from $.securities.data.*[0]
                for item in data.get('securities', {}).get('data', []):
                    value = item[0]
                    if value not in existing_values:
                        new_values.add(value)
        
        current_date += timedelta(days=1)

    return new_values

# Function to append new values to the TSV file
def append_to_issues_by_sector(file_path, new_values):
    with open(file_path, 'a', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        for value in new_values:
            writer.writerow([value])

# Main logic of the script
def main():
    # Path to the TSV file
    tsv_file_path = 'data/issues-by-sector-test.tsv'
    
    # Read existing values
    existing_values = read_issues_by_sector(tsv_file_path)

    # Define the date range
    start_date = datetime(2011, 12, 19)
    end_date = datetime(2024, 10, 9)

    # Get new values from JSON files
    new_values = get_new_values(start_date, end_date, existing_values)

    # Print new values to the console
    if new_values:
        append_to_issues_by_sector(tsv_file_path, new_values)
        print(f"Added new values: {len(new_values)}")
        print(new_values)
    else:
        print("No new values found.")

if __name__ == "__main__":
    main()