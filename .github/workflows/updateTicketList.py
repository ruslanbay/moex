import pandas as pd
import requests
import json

df = pd.read_csv('data/issues-by-sector.tsv', sep='\t', skiprows=range(1, 16), header=0)

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
          case _:
            continue

      work_days_range = pd.date_range(periods=7)
      for row in data['boards']['data']:
        if row[1] == 'TQBR':
          listed_till = row[13]
          if pd.to_datetime(listed_till) not in work_days_range:
            companyInfo['listed_till'] = listed_till
          break
      return companyInfo
    except (IndexError, KeyError):
      return None
  else:
    print(f"Error fetching data for {ticker}: {response.status_code}")
    return None

for index, row in df.iterrows():
  ticker = row['labels']
  companyInfo = getCompanyInfo(ticker)
  df.at[index, 'name_rus'] = companyInfo['NAME']
  df.at[index, 'shortname_rus'] = companyInfo['SHORTNAME']
  df.at[index, 'shortname'] = companyInfo['LATNAME']
  df.at[index, 'history_from'] = companyInfo['ISSUEDATE']

df.to_csv('data/updated_issues-by-sector.tsv', sep='\t', index=False)
