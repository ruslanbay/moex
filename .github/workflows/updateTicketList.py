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
      companyInfo = dict()
      for item in data['description']['data']:
        match item[0]:
          case 'NAME':
            companyInfo['NAME'] = item[2]
          case 'SHORTNAME':
            companyInfo['SHORTNAME'] = item[2]
          case 'LATNAME':
            companyInfo['LATNAME'] = item[2]
          case 'ISSUEDATE':
            companyInfo['ISSUEDATE'] = item[2]
          case _:
            continue
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
