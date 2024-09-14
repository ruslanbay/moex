import pandas as pd
import requests
import json

# Load the TSV file into a DataFrame
df = pd.read_csv('data/issues-by-sector.tsv', sep='\t')

# Function to fetch the history_from date for a given label
def fetch_history_from(label):
    url = f"https://iss.moex.com/iss/securities/{label}.json?iss.meta=off"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        # Save the response as a JSON file
        with open(f"data/iss/securities/{label}.json", 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        # Extract the ISSUEDATE from the description.data
        try:
            issuedate = data['description']['data'][0]['ISSUEDATE']
            return issuedate
        except (IndexError, KeyError):
            return None
    else:
        print(f"Error fetching data for {label}: {response.status_code}")
        return None

# Update the history_from column for each label
for index, row in df.iterrows():
    label = row['labels']
    history_from = fetch_history_from(label)
    df.at[index, 'history_from'] = history_from

# Save the updated DataFrame back to a TSV file
df.to_csv('data/updated_issues-by-sector.tsv', sep='\t', index=False)
