import argparse
import csv
from datetime import datetime, timedelta
import json
import re
import sys

parser = argparse.ArgumentParser(description='MarketCap Histogram: Prepare chart data')
parser.add_argument('--start', nargs=1, type=str, required=True, help="start date, YYYY-MM-DD")
parser.add_argument('--end', nargs=1, type=str, required=True, help="end date, YYYY-MM-DD")
parser.add_argument('--step', nargs=1, type=int, required=True, help="step between data points in days")
parser.add_argument('--mode', nargs=1, type=str, required=True, choices=['sum', 'ticket', 'sector'],
help='''sum - sum capitalization,
ticket - capitalization by tickets,
sector - capitalization by setctors''')
parser.add_argument('--filename', nargs=1, type=str, required=True, help="Example: 2015-BACKUP")
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
    # print(f"securities-{myDate}.json doesn't exist")
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
        'name': ticket,
        'x': [],
        'y': []
      }
      if(len(dates) >= 2):
        for d in dates[0:-1]:
          traces[ticket]["x"].append(f'{d}')
          traces[ticket]["y"].append(0.00)
    else: # if(ticket in traces.keys()):
      lastDate = traces[ticket]["x"][-1]
      lastDate = datetime.strptime(lastDate, '%Y-%m-%d').date()
      # if there are skips in dates, then fill capitalization values with 0.00
      if(lastDate < dates[-2]):
        index = dates.index(lastDate) + 1
        for d in dates[index:-1]:
          traces[ticket]["x"].append(f'{d}')
          traces[ticket]["y"].append(0.00)
    traces[ticket]["x"].append(f'{dates[-1]}')
    traces[ticket]["y"].append(cap)
for ticket in traces.keys():
  lastDate = traces[ticket]["x"][-1]
  lastDate = datetime.strptime(lastDate, '%Y-%m-%d').date()
  if(lastDate < dates[-1]):
    index = dates.index(lastDate) + 1
    for d in dates[index:]:
      traces[ticket]["x"].append(f'{d}')
      traces[ticket]["y"].append(0.00)

chartData = []

match mode:
  case 'sum':
    ySum = traces[list(traces.keys())[0]]['y']
    for ticket in traces.keys():
      for i in range(1, len(ySum)):
        ySum[i] += traces[ticket]["y"][i]
    chartData = [{
      "name": ["total"] * len(ySum),
      "x": traces[list(traces.keys())[0]]["x"],
      "y": ySum
    }]
  case 'ticket':
    for ticket in traces.keys():
      if(set(traces[ticket]["y"]) == {0}): # exclude tickets with capitalization == 0 for each date
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
        if(set(traces[ticket]['y']) == {0}): # exclude tickets with capitalization == 0 for each date
          continue
        try:
          index = tickets.index(ticket)
          sector = sectors[index]
          sectorCap[sector] = [sum(i) for i in zip(sectorCap[sector], traces[ticket]['y'])]
        except ValueError:
          sectorCap['Others'] = [sum(i) for i in zip(sectorCap['Others'], traces[ticket]['y'])]
      for sector in sectorCap:
        if(sector in ['', 'Moscow Exchange']):
          continue
        chartData.append({
          "name": [sector] * len(sectorCap[sector]),
          "x": traces[list(traces.keys())[0]]["x"],
          "y": sectorCap[sector]
        })

chartData.sort(key=lambda entry: entry['name'][0])

with open(f'history/{filename}', 'w', newline='') as f:
  fieldnames = ['date', 'marketCap', 'traceName']
  writer = csv.DictWriter(f, fieldnames=fieldnames)

  writer.writeheader()
  
  for entry in chartData:
    for i in range(len(entry['x'])):
      writer.writerow({
        'date': entry['x'][i],
        'marketCap': entry['y'][i],
        'traceName': entry['name'][i]
      })
