from datetime import date, datetime, timedelta
import requests
import sys

def daterange(start, end, stepDays):
  for n in range(0, int((end - start).days) + 1, stepDays):
    yield start + timedelta(n)

def getData(myDate):
  with open(f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{myDate}.json', 'w', encoding='utf-8') as f:
    url = f'https://iss.moex.com/iss/history/engines/stock/totals/boards/MRKT/securities.json?iss.meta=off&date={myDate}&securities.columns=SECID,CURRENCYID,OPEN,CLOSE,VOLUME,VALUE,NUMTRADES,DAILYCAPITALIZATION'
    headers = {'User-Agent': 'MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'}
    r = requests.get(url, headers)
    if(r.status_code == 200):
      f.write(r.text)
    else:
      print(f'{myDate} - ERROR: Wrong response code: {r.status_code}')
    f.close()

if(len(sys.argv) == 1):
  getData(date.today() - timedelta(days=1))
else:
  start = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
  end = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
  step = int(sys.argv[3])
  for myDate in daterange(start, end, step):
    getData(myDate)
