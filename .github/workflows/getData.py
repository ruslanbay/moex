from datetime import date, datetime, timedelta
import requests
import sys

def daterange(start, end, stepDays):
  for n in range(0, int((end - start).days), stepDays):
    yield start + timedelta(n)

def getData(myDate):
  with open(f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{myDate}.json', 'w', encoding='utf-8') as f:
    r = requests.get(f'https://iss.moex.com/iss/history/engines/stock/totals/boards/MRKT/securities.json?iss.meta=off&date={myDate}&securities.columns=SECID,CURRENCYID,OPEN,CLOSE,VOLUME,VALUE,NUMTRADES,DAILYCAPITALIZATION')
    if(r.status_code == 200):
      f.write(r.text)
    else:
      echo f'ERROR: Wrong response code: {r.status_code}'
    f.close()

if(len(sys.argv) == 4):
  start = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
  end = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
  step = int(sys.argv[3])
  for myDate in daterange(start, end, step):
    getData(myDate)
else:
  getData(date.today() - timedelta(days=1))
