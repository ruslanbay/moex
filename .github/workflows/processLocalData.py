# {
#   "XYX": {
#     "x": ["2011-12-19", "2011-12-20", "2011-12-21"],
#     "y": [235423.45, 0.00, 564654.87]
#   },
#   "YYY": {
#     "x": ["2011-12-19", "2011-12-20", "2011-12-21"],
#     "y": [6546.45, 6546.00, 98794.46]
#   },
#   "ZZZ": {
#     "x": ["2011-12-19", "2011-12-20", "2011-12-21"],
#     "y": [0.00, 00.00, 46546.45]
#   }
# }

from datetime import date, datetime, timedelta
import json
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
      # use only shares nominated in russian ruble
      if(currency != "SUR"):
        continue
      
      # If the current ticket didn't appear before,
      # then set capitalization values for previuose dates as 0.00
      if(ticket not in chartData.keys()):
        chartData[ticket] = {'x': [], 'y': []}
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
else:
  # Rewrite this code using exceptions
  print("Missing arguments:\nExample: processLocalData.py 2011-12-19 2011-12-21 1")

# with open(f'data/barChartData.json', 'w', encoding='utf-8') as f:
#   f.write(json.dumps(chartData))
#   f.close()

def set_default(obj):
  if isinstance(obj, set):
    return list(obj)
  raise TypeError
  
with open('data/barChartData.json', 'w') as f:
  json.dump(chartData, f, default=set_default)
