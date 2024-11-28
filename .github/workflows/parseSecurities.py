import argparse
import csv
from datetime import datetime, timedelta
import json
import os
# import pandas as pd
import requests

parser = argparse.ArgumentParser(description='Parse securities localy')
parser.add_argument('--start', nargs=1, type=str, required=True, help='start date, YYYY-MM-DD')
parser.add_argument('--end', nargs=1, type=str, required=True, help='end date, YYYY-MM-DD')
parser.add_argument('--step', nargs=1, type=int, required=True, help='step between data points in days')
parser.add_argument('--input', nargs=1, type=str, required=True, help='Input TSV file')
parser.add_argument('--output', nargs=1, type=str, required=True, help='Output TSV file')
args=parser.parse_args()
start = datetime.strptime(args.start[0], '%Y-%m-%d')
end = datetime.strptime(args.end[0], '%Y-%m-%d')
step = int(args.step[0])
inputTSVFile = args.input[0]
outputTSVFile = args.output[0]

# Function to read the first column from the TSV file
def read_issues_by_sector(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    return [row[1] for row in reader]

# Function to get a list of new values from JSON files
def get_new_values(start_date, end_date, step, existing_values):
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
    
    current_date += timedelta(days=step)
  
  return new_values

def getCompanyInfo(ticker):
  url = f"https://iss.moex.com/iss/securities/{ticker}.json?iss.meta=off"
  headers = {'User-Agent': 'MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'}
  response = requests.get(url, headers)
  
  if response.status_code == 200:
    data = response.json()
    
    with open(f"data/iss/securities/{ticker}.json", 'w', encoding='utf-8') as json_file:
      json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    try:
      companyInfo = {
        'parents': 'Others',
        'labels': ticker,
        'shortname': ticker,
        'shortname_rus': ticker,
        'name_rus': ticker,
        'history_from': '',
        'history_till': ''
        'trace_color': ''
      }
      history_from = ''
      for item in data['description']['data']:
        value = item[2].replace('"', '').replace(',', '').replace("'", '').replace("/", '').replace("\\", '')
        match item[0]:
          case 'TYPE':
            if value in ['labels', 'Moscow Exchange', 'Chemicals and Pertochemicals', 'Conglomerate',
              'Construction (Development)', 'Consumer', 'Electricity, Utilities', 'Energy (Oil, Gas, Coal)',
              'Financials', 'Health Care', 'Industrials', 'Information Technologies',
              'Metals and Mining', 'Telecommunication Services', 'Transportation',
              'TQFD. PAI (USD)', 'TQIF. PAI', 'TQPI. Shares PIR', 'TQTF. ETF',
              'cb_bond', 'corporate_bond', 'etf_ppif', 'euro_bond', 'exchange_bond', 'exchange_ppif',
              'Foreign Companies', 'ifi_bond', 'interval_ppif', 'municipal_bond', 'ofz_bond',
              'private_ppif', 'public_ppif', 'state_bond', 'stock_mortgage', 'subfederal_bond']:
              companyInfo['parents'] = value
            else:
              companyInfo['parents'] = 'Others'
          case 'LATNAME':
            companyInfo['shortname'] = value
          case 'SHORTNAME':
            companyInfo['shortname_rus'] = value
          case 'NAME':
            companyInfo['name_rus'] = value
          case 'ISSUEDATE':
            companyInfo['history_from'] = value
            history_from = value
          case 'STARTDATEMOEX':
            companyInfo['history_from'] = value
            history_from = value
          case _:
            continue
      
      # current_date = pd.Timestamp.now()
      # work_days_range = pd.date_range(start=current_date - pd.Timedelta(days=7), end=current_date)
      # for row in data['boards']['data']:
      #   if row[1] == 'TQBR':
      #     history_till = row[13]
      #     if pd.to_datetime(history_till) not in work_days_range:
      #       companyInfo['history_till'] = history_till
      #     if datetime.strptime(history_from, "%Y-%m-%d") > datetime.strptime(history_till, "%Y-%m-%d"):
      #       companyInfo['history_from'] = row[12]
      #     break
      return companyInfo
    except (IndexError, KeyError):
      return None
  else:
    print(f"Error fetching data for {ticker}: {response.status_code}")
    return None

# Main logic of the script
def main():
  # Path to the TSV file
  inputTSVFilePath = f'data/{inputTSVFile}.tsv'
  outputTSVFilePath = f'data/{outputTSVFile}.tsv'
  
  # Read existing values
  existing_values = read_issues_by_sector(inputTSVFilePath)
  
  # Get new values from JSON files
  new_values = get_new_values(start, end, step, existing_values)
  
  # Print new values to the console
  if new_values:
    with open(outputTSVFilePath, 'a', encoding='utf-8') as file:
      writer = csv.writer(file)
      for ticker in new_values:
        companyInfo = getCompanyInfo(ticker)
        writer.writerows(list(companyInfo.values())
  else:
    print("No new values found.")

if __name__ == "__main__":
  main()