import argparse
import csv
from datetime import date, datetime, timedelta, timezone
import requests
import sys

parser = argparse.ArgumentParser(description='Get historical currency data from WSJ.com')
parser.add_argument('--start', nargs=1, type=str, required=True,
                   help="start date, YYYY-MM-DD")
parser.add_argument('--end', nargs=1, type=str, required=True,
                   help="end date, YYYY-MM-DD")
parser.add_argument('--currency', nargs=1, type=str, required=True,
                   help="step between data points in days")

args=parser.parse_args()
currencyList = args.currency[0].split(',')
start = datetime.strptime(args.start[0], '%Y-%m-%d').date()
end = datetime.strptime(args.end[0], '%Y-%m-%d').date()
if(start > end):
  sys.exit('End date has to be greater than start date')

start = start.strftime('%m/%d/%Y')
end = end.strftime('%m/%d/%Y')

def getData(start, end, currency):
  dates = []
  closePrice = []
  url = f'https://www.wsj.com/market-data/quotes/fx/{currency}/historical-prices/download?MOD_VIEW=page&num_rows=all&range_days=10&startDate={start}&endDate={end}'
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
  with requests.get(url, headers) as r:
    print(r.text)
    for row in csv.DictReader(r.text, delimiter=', '):
      dates.append(row['Date'])
      closePrice.append(row['Close'])
  data = {
    "name": currency,
    "type": "scatter",
    "hoverinfo": "skip",
    "hovertemplate": "",
    "x": dates,
    "y": closePrice
  }
  return data

chartData = []

with open('data/currency.json', 'w', encoding='utf-8') as f:
  for currency in currencyList:
    chartData.append(getData(start, end, currency))
  f.write(chartData)
  f.close()