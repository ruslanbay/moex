import argparse
from datetime import datetime
import json
import pandas as pd
import requests

parser = argparse.ArgumentParser(description='')
parser.add_argument('--inputFile', nargs=1, type=str, required=True, help="Input file")
parser.add_argument('--skipRowsRangeStart', nargs=1, type=int, required=True, help="skipRowsRangeStart")
parser.add_argument('--skipRowsRangeEnd', nargs=1, type=int, required=True, help="skipRowsRangeEnd")
parser.add_argument('--outputFile', nargs=1, type=str, required=True, help="Output file")
args=parser.parse_args()
inputFile = args.inputFile[0]
outputFile = args.outputFile[0]
skipRowsRangeStart = int(args.skipRowsRangeStart[0])
skipRowsRangeEnd = int(args.skipRowsRangeEnd[0])

df = pd.read_csv(inputFile, sep='\t', header=0, skiprows=range(skipRowsRangeStart, skipRowsRangeEnd))

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
        'NAME': ticker,
        'SHORTNAME': ticker,
        'LATNAME': ticker,
        'TYPE': 'Others',
        'ISSUEDATE': '',
        'history_till': ''
      }
      history_from = ''
      for item in data['description']['data']:
        value = item[2].replace('"', '').replace(',', '').replace("'", '').replace("/", '').replace("\\", '')
        match item[0]:
          case 'NAME':
            companyInfo['NAME'] = value
          case 'SHORTNAME':
            companyInfo['SHORTNAME'] = value
          case 'LATNAME':
            companyInfo['LATNAME'] = value
          case 'TYPE':
            companyInfo['TYPE'] = value
          case 'ISSUEDATE':
            companyInfo['ISSUEDATE'] = value
            history_from = value
          case 'STARTDATEMOEX':
            companyInfo['ISSUEDATE'] = value
            history_from = value
          case _:
            continue

      current_date = pd.Timestamp.now()
      work_days_range = pd.date_range(start=current_date - pd.Timedelta(days=7), end=current_date)
      for row in data['boards']['data']:
        if row[1] == 'TQBR':
          history_till = row[13]
          if pd.to_datetime(history_till) not in work_days_range:
            companyInfo['history_till'] = history_till
          if datetime.strptime(history_from, "%Y-%m-%d") > datetime.strptime(history_till, "%Y-%m-%d"):
            companyInfo['ISSUEDATE'] = row[12]
          break
      return companyInfo
    except (IndexError, KeyError):
      return None
  else:
    print(f"Error fetching data for {ticker}: {response.status_code}")
    return None

for index, row in df.iterrows():
  ticker = row['labels']
  if ticker in ['labels', 'Moscow Exchange', 'Chemicals and Pertochemicals', 'Conglomerate',
                'Construction (Development)', 'Consumer', 'Electricity, Utilities', 'Energy (Oil, Gas, Coal)',
                'Financials', 'Health Care', 'Industrials', 'Information Technologies',
                'Metals and Mining', 'Telecommunication Services', 'Transportation', 'TQFD. PAI (USD)', 'TQIF. PAI', 'TQPI. Shares PIR', 'TQTF. ETF', 'Others']:
    continue
  companyInfo = getCompanyInfo(ticker)
  df.at[index, 'parents'] = companyInfo['TYPE']
  df.at[index, 'name_rus'] = companyInfo['NAME']
  df.at[index, 'shortname_rus'] = companyInfo['SHORTNAME']
  df.at[index, 'shortname'] = companyInfo['LATNAME']
  df.at[index, 'history_from'] = companyInfo['ISSUEDATE']
  df.at[index, 'history_till'] = companyInfo['history_till']

df.to_csv(outputFile, sep='\t', index=False)