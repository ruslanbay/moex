from datetime import datetime
import json
import pandas as pd
import requests

df = pd.read_csv('data/issues-by-sector.tsv', sep='\t', header=0)

def getCompanyInfo(ticker):
  url = f"https://iss.moex.com/iss/securities/{ticker}.json?iss.meta=off"
  response = requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    
    with open(f"data/iss/securities/{ticker}.json", 'w', encoding='utf-8') as json_file:
      json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    try:
      companyInfo = {
        'NAME': ticker,
        'SHORTNAME': ticker,
        'LATNAME': ticker,
        'ISSUEDATE': '2014-06-09',
        'listed_till': ''
      }
      listed_from = '2014-06-09'
      for item in data['description']['data']:
        value = item[2].replace('"', '').replace(',', '').replace("'", '')
        match item[0]:
          case 'NAME':
            companyInfo['NAME'] = value
          case 'SHORTNAME':
            companyInfo['SHORTNAME'] = value
          case 'LATNAME':
            companyInfo['LATNAME'] = value
          case 'ISSUEDATE':
            companyInfo['ISSUEDATE'] = value
            listed_from = value
          case _:
            continue

      current_date = pd.Timestamp.now()
      work_days_range = pd.date_range(start=current_date - pd.Timedelta(days=7), end=current_date)
      for row in data['boards']['data']:
        if row[1] == 'TQBR':
          listed_till = row[13]
          if pd.to_datetime(listed_till) not in work_days_range:
            companyInfo['listed_till'] = listed_till
          if datetime.strptime(listed_from, "%Y-%m-%d") > datetime.strptime(listed_till, "%Y-%m-%d"):
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
                'Metals and Mining', 'Telecommunication Services', 'Transportation', 'Others']:
    continue
  companyInfo = getCompanyInfo(ticker)
  df.at[index, 'name_rus'] = companyInfo['NAME']
  df.at[index, 'shortname_rus'] = companyInfo['SHORTNAME']
  df.at[index, 'shortname'] = companyInfo['LATNAME']
  df.at[index, 'history_from'] = companyInfo['ISSUEDATE']

df.to_csv('data/issues-by-sector.tsv', sep='\t', index=False)
