from datetime import date, datetime, timedelta
import json
import re
import sys

def daterange(start, end, stepDays):
  for n in range(0, int((end - start).days) + 1, stepDays):
    yield start + timedelta(n)

def readLocalData(myDate):
  with open(f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{myDate}.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()
    return data

chartData = dict()

if(len(sys.argv) == 4):
  start = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
  end = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
  step = int(sys.argv[3])
  for myDate in daterange(start, end, step):
    data = readLocalData(myDate)['securities']['data']
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
      if(currency != "SUR"):
        continue
      
      # If the current ticket didn't appear before,
      # then set capitalization values for previuose dates as 0.00
      if(ticket not in chartData.keys()):
        chartData[ticket] = {
          'x': [],
          'y': [],
          'type': 'bar',
          'name': ticket,
          'hoverinfo': 'skip',
          'hovertemplate': ''
        }
        for d in daterange(start, myDate - timedelta(days=step), step):
          chartData[ticket]["x"].append(f'{d}')
          chartData[ticket]["y"].append(0.00)
      else: # if(ticket in chartData.keys()):
        lastDate = chartData[ticket]["x"][-1]
        lastDate = datetime.strptime(lastDate, '%Y-%m-%d').date()
        # if there are skips in dates, then fill capitalization values with 0.00
        if(lastDate < myDate - timedelta(days=step)):
          for d in daterange(lastDate, myDate - timedelta(days=step), step):
            chartData[ticket]["x"].append(f'{d}')
            chartData[ticket]["y"].append(0.00)
      chartData[ticket]["x"].append(f'{myDate}')
      chartData[ticket]["y"].append(cap)
  for ticket in chartData.keys():
    lastDate = chartData[ticket]["x"][-1]
    lastDate = datetime.strptime(lastDate, '%Y-%m-%d').date()
    if(lastDate < end):
      for d in daterange(lastDate + timedelta(days=step), end, step):
        chartData[ticket]["x"].append(f'{d}')
        chartData[ticket]["y"].append(0.00)
else:
  # Rewrite this code using exceptions
  print("Missing arguments:\nExample: processLocalData.py 2011-12-19 2011-12-21 1")

def set_default(obj):
  if isinstance(obj, set):
    return list(obj)
  raise TypeError
  
with open('data/barChartData.json', 'w') as f:
  json.dump(chartData, f, default=set_default)
