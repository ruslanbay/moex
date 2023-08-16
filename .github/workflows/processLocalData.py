import argparse
import csv
from datetime import date, datetime, timedelta
import json
import re

parser = argparse.ArgumentParser(description='Process locally stored data')
parser.add_argument('--start', nargs=1, type=str, required=True,
                   help="start date, YYYY-MM-DD")
parser.add_argument('--end', nargs=1, type=str, required=True,
                   help="end date, YYYY-MM-DD")
parser.add_argument('--step', nargs=1, type=int, required=True,
                   help="step between data points in days")
parser.add_argument('--mode', nargs=1, type=str, required=True,
                   choices=['sum', 'ticket', 'sector', 'combined'],
                   help='''sum - total capitalization,
ticket - capitalization by tickets,
sector - capitalization by setctors,
combined - capitalization by ticket and by sector''')
args=parser.parse_args()
start = datetime.strptime(args.start, '%Y-%m-%d').date()
end = datetime.strptime(args.end, '%Y-%m-%d').date()
step = int(args.step)
mode = args.mode

def daterange(start, end, stepDays):
  for n in range(0, int((end - start).days) + 1, stepDays):
    yield start + timedelta(n)

def readLocalData(myDate):
  with open(f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{myDate}.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()
    return data

traces = dict()
dates = []

for myDate in daterange(start, end, step):
  data = readLocalData(myDate)['securities']['data']
  while(len(data) == 0):
    myDate = myDate + timedelta(days=1)
    data = readLocalData(myDate)['securities']['data']
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
    if(ticket in ['FXRB', 'FXGD', 'FXAU', 'FXDE', 'FXIT', 'FXJP', 'FXUK', 'FXUS', 'FXRU', 'FXCN', 'FXMM', 'FXRL', 'FXKZ', 'FXTB', 'FXRB', 'FXWO', 'FXTM', 'FXDM', 'FXFA', 'FXTP', 'FXIP', 'FXES', 'FXRD', 'FXRE', 'FXEM', 'FXBC']):
      continue
    # use only shares nominated in russian ruble
    if(currency != 'SUR'):
      continue
    
    # If the current ticket didn't appear before,
    # then set capitalization values for previuose dates as 0.00
    if(ticket not in traces.keys()):
      traces[ticket] = {
        'name': ticket,
        'type': 'scatter',
        'mode': 'lines',
        # 'fill': 'toself',
        'stackgroup': 'one',
        'hoverinfo': 'skip',
        'hovertemplate': '',
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
    ySum = traces.[traces.keys()[0]]["y"]
    for ticket in traces.keys():
      for i in range(1, len(ySum)):
        ySum[i] += traces[ticket]["y"][i]
    chartData = [{
      "name": "total",
      "type": "scatter",
      "mode": "lines",
      "stackgroup": "one",
      "hoverinfo": "skip",
      "hovertemplate": "",
      "x": traces.[traces.keys()[0]]["x"],
      "y": ySum
    }]
  case 'ticket':
    for ticket in traces.keys():
      if(set(traces[ticket]["y"]) == {0}): # exclude tickets with capitalization == 0 for each date
        continue
      chartData.append(traces[ticket])
  # case 'sector':
  #   with open('data/issues-by-sector.tsv', 'r', newline='', encoding='utf-8') as f:
  #     sectors = []
  #     tsv = csv.reader(f, delimiter='\t')
  #     for row in tsv:
        
  #     for ticket in traces.keys():
  #       j
  # case 'combined':
  #   sdf

for ticket in traces.keys():
  # exclude tickets with capitalization == 0
  if(set(traces[ticket]["y"]) == {0}):
    continue
  chartData.append(traces[ticket])

with open(f'data/chartData_{start}_{end}_{step}.json', 'w') as f:
  json.dump(chartData, f)