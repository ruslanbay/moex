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

traces = dict()

if(len(sys.argv) == 4):
  start = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
  end = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
  step = int(sys.argv[3])
  for myDate in daterange(start, end, step):
    data = readLocalData(myDate)['securities']['data']
    while(len(data) == 0):
      myDate = myDate + timedelta(days=step)
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
      if(currency != 'SUR'):
        continue
      
      # If the current ticket didn't appear before,
      # then set capitalization values for previuose dates as 0.00
      if(ticket not in traces.keys()):
        traces[ticket] = {
          'name': ticket,
          'type': 'bar',
          'hoverinfo': 'skip',
          'hovertemplate': '',
          'x': [],
          'y': []
        }
        for d in daterange(start, myDate - timedelta(days=step), step):
          traces[ticket]["x"].append(f'{d}')
          traces[ticket]["y"].append(0.00)
      else: # if(ticket in traces.keys()):
        lastDate = traces[ticket]["x"][-1]
        lastDate = datetime.strptime(lastDate, '%Y-%m-%d').date()
        # if there are skips in dates, then fill capitalization values with 0.00
        if(lastDate < myDate - timedelta(days=step)):
          for d in daterange(lastDate, myDate - timedelta(days=step), step):
            traces[ticket]["x"].append(f'{d}')
            traces[ticket]["y"].append(0.00)
      traces[ticket]["x"].append(f'{myDate}')
      traces[ticket]["y"].append(cap)
  for ticket in traces.keys():
    lastDate = traces[ticket]["x"][-1]
    lastDate = datetime.strptime(lastDate, '%Y-%m-%d').date()
    if(lastDate < end):
      for d in daterange(lastDate + timedelta(days=step), end, step):
        traces[ticket]["x"].append(f'{d}')
        traces[ticket]["y"].append(0.00)
  
  chartData = []
  for ticket in traces.keys():
    chartData.append(traces[ticket])

  with open(f'data/barChartData_{start}_{end}_{step}.json', 'w') as f:
    json.dump(chartData, f)
else:
  # Rewrite this code using exceptions
  print("Missing arguments:\nExample: processLocalData.py 2011-12-19 2011-12-21 1")