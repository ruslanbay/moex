from datetime import date, datetime, timedelta
import requests
import sys

def daterange(start, end, stepDays):
    for n in range(0, int((end - start).days), stepDays):
        yield start + timedelta(n)

# start = date(2011, 12, 19) # Monday
start = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
end = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
step = int(sys.argv[3])

for d in daterange(start, end, step):
  with open(f'iss/history/engines/stock/totals/boards/MRKT/securities-{d}.json', 'w', encoding='utf-8') as f:
    r = requests.get(f'https://iss.moex.com/iss/history/engines/stock/totals/boards/MRKT/securities.json?iss.meta=off&date={d}&securities.columns=SECID,CURRENCYID,OPEN,CLOSE,VOLUME,VALUE,NUMTRADES,DAILYCAPITALIZATION')
    f.write(r.text)
    f.close()
