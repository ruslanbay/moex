import argparse
import requests
import sys

parser = argparse.ArgumentParser(description='Get currency exchange rate')
parser.add_argument('--start', nargs=1, type=str, required=True, help="start date, YYYY-MM-DD")
parser.add_argument('--end', nargs=1, type=str, required=True, help="end date, YYYY-MM-DD")
parser.add_argument('--currency', nargs=1, type=str, required=True, choices=['USDFIXME', 'CNYFIXME', 'EURFIXME', 'BYNFIXME', 'CNYFIX', 'EURUSDFIXME', 'GOLDFIXME', 'HKDFIXME', 'TRYFIXME', 'USDCNYFIXME', 'USDKZTFIXME'])
args=parser.parse_args()
start = args.start[0]
end = args.end[0]
currency = args.currency[0]

if(start > end):
  sys.exit('ERROR: End date has to be greater than start date')

with open(f'history/{currency}.csv', 'a') as f:
  url = f'https://iss.moex.com/iss/history/engines/currency/markets/index/securities/{currency}.json?iss.meta=on&history.columns=TRADEDATE,OPEN,HIGH,LOW,CLOSE&sort_column=TRADEDATE&sort_order=asc&FROM={start}&TILL={end}'
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
  try:
    r = requests.get(url, headers)
    if(r.status_code == 200):
      for row in r.json()['history']['data']:
        f.write('\n' + ','.join(map(str, row)) + '\n')
    else:
      print(f'Unexpected response code: {r.status_code}')
  except Exception as e:
    print("ERROR:", str(e))
