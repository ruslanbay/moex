import argparse
import csv
from datetime import datetime, timedelta
import re
import sys

parser = argparse.ArgumentParser(description='Process locally stored data')
parser.add_argument('--start', nargs=1, type=str, required=True,
           help="start date, YYYY-MM-DD")
parser.add_argument('--end', nargs=1, type=str, required=True,
           help="end date, YYYY-MM-DD")
parser.add_argument('--step', nargs=1, type=int, required=True,
           help="step between data points in days")
parser.add_argument('--mode', nargs=1, type=str, required=True,
                   choices=['total', 'ticket', 'sector'],
                   help='''total - total capitalization,
ticket - capitalization by tickets,
sector - capitalization by setctors''')
parser.add_argument('--filename', nargs=1, type=str, required=True,
           help="Example: total.csv")
args=parser.parse_args()
start = datetime.strptime(args.start[0], '%Y-%m-%d').date()
end = datetime.strptime(args.end[0], '%Y-%m-%d').date()
step = int(args.step[0])
mode = args.mode[0]
filename = args.filename[0]

if(start > end):
  sys.exit('End date has to be greater than start date')
if(step < 1):
  sys.exit('Step has to be greater or equal to 1')

def daterange(start, end, stepDays):
  for n in range(0, int((end - start).days) + 1, stepDays):
    yield start + timedelta(n)

def readLocalData(myDate):
  try:
    f = open(f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{myDate}.json', 'r', encoding='utf-8')
  except FileNotFoundError:
    print(f"securities-{myDate}.jso doesn't exist")
    return ''
  else:
    with f:
      data = json.load(f)
      f.close()
      return data['securities']['data']

traces = dict()
dates = []

for myDate in daterange(start, end, step):
  data = readLocalData(myDate)
  while(len(data) == 0):
    myDate = myDate + timedelta(days=1)
    data = readLocalData(myDate)
  dates.append(myDate)
  for item in data:
    ticket = item[0]
    cap = item[7]
    currency = item[1]
    # skip forein shares
    if(re.search('^[a-zA-Z0-9]+-RM', ticket) != None):
      continue
    # skip bonds
    if(re.search('^RU[0-9]+.*', ticket) != None):
      continue
    # skip bonds
    if(re.search('^XS[0-9]+.*', ticket) != None):
      continue
    # skip ETFs
    if(ticket in ['FXRB', 'FXGD', 'FXAU', 'FXDE', 'FXIT',
                  'FXJP', 'FXUK', 'FXUS', 'FXRU', 'FXCN',
                  'FXMM', 'FXRL', 'FXKZ', 'FXTB', 'FXRB',
                  'FXWO', 'FXTM', 'FXDM', 'FXFA', 'FXTP',
                  'FXIP', 'FXES', 'FXRD', 'FXRE', 'FXEM', 'FXBC']):
      continue
    # use only shares nominated in russian ruble
    if(currency != 'SUR'):
      continue
    
    # If the current ticket didn't appear before,
    # then set capitalization values for previuose dates as 0.00
    if(ticket not in traces.keys()):
      traces[ticket] = {
        'date': dates,
        'market_cap': [0.00] * len(dates),
        'trace_name': ticket * len(dates)
      }
    traces[ticket]['market_cap'][-1] = cap

chartData = []

match mode:
  case 'total':
    total_cap = [0] * len(dates)
    for ticket in traces.keys():
      for i in range(len(dates)):
        total_cap[i] += traces[ticket]["market_cap"][i]
    chartData.append({
      "date": dates,
      "market_cap": total_cap,
      "trace_name": "total"
    })
  case 'ticket':
    for ticket in traces.keys():
      if(set(traces[ticket]["market_cap"]) == {0}): # exclude tickets with capitalization == 0 for each date
        continue
      chartData.append(traces[ticket])
  case 'sector':
    with open('data/issues-by-sector.tsv', 'r', newline='', encoding='utf-8') as f:
      tickets = []
      sectors = []
      sectorCap = dict()
      tsv = csv.DictReader(f, delimiter='\t')
      for row in tsv:
        tickets.append(row['labels'])
        sectors.append(row['parents'])
      for sector in set(sectors):
        sectorCap[sector] = [0] * len(dates)
      for ticket in traces.keys():
        if(set(traces[ticket]['market_cap']) == {0}): # exclude tickets with capitalization == 0 for each date
          continue
        try:
          index = tickets.index(ticket)
          sector = sectors[index]
          sectorCap[sector] = [sum(i) for i in zip(sectorCap[sector], [traces[ticket]['market_cap']])]
        except ValueError:
          sectorCap['Others'] = [sum(i) for i in zip(sectorCap['Others'], [traces[ticket]['market_cap']])]
      for sector in sectorCap:
        if(sector in ['', 'Moscow Exchange']):
          continue
        chartData.append({
          "date": dates,
          "market_cap": sectorCap[sector],
          "trace_name": sector
        })

with open(f'history/{filename}', 'w', newline='') as csvfile:
  fieldnames = ['date', 'market_cap', 'trace_name']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  writer.writeheader()
  for row in chartData:
    writer.writerow(row)