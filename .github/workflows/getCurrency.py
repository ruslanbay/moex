import argparse
import csv
from datetime import datetime
import requests

def get_currency_data(start, end, currency):
  dates = []
  close_prices = []
  url = f'https://www.wsj.com/market-data/quotes/fx/{currency}/historical-prices/download?MOD_VIEW=page&num_rows=all&range_days=10&startDate={start}&endDate={end}'
  headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
  with requests.get(url, headers=headers) as r:
    for row in csv.DictReader(r.text.splitlines()):
      dates.append(row['Date'])
      close_prices.append(row['Close'])
  data = {
    "name": currency,
    "type": "scatter",
    "hoverinfo": "skip",
    "hovertemplate": "",
    "x": dates,
    "y": close_prices
  }
  return data

def main():
  parser = argparse.ArgumentParser(description='Get historical currency data from WSJ.com')
  parser.add_argument('--start', type=str, required=True, help="start date, YYYY-MM-DD")
  parser.add_argument('--end', type=str, required=True, help="end date, YYYY-MM-DD")
  parser.add_argument('--currency', type=str, required=True, help="currency list separated by commas")

  args = parser.parse_args()
  currency_list = args.currency.split(',')
  start = datetime.strptime(args.start, '%Y-%m-%d').strftime('%m/%d/%Y')
  end = datetime.strptime(args.end, '%Y-%m-%d').strftime('%m/%d/%Y')

  chart_data = []
  for currency in currency_list:
    chart_data.append(get_currency_data(start, end, currency))

  with open('data/currency.json', 'w', encoding='utf-8') as f:
    f.write(str(chart_data))

if __name__ == '__main__':
  main()
