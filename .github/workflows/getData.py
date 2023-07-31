from datetime import date, timedelta
import requests
import sys

def daterange(start, end, stepDays):
    for n in range(0, int((end - start).days), stepDays):
        yield start + timedelta(n)

# start = date(2011, 12, 19) # Monday
start = sys.argv[1]
end = sys.argv[2]
step = int(sys.argv[3])
      
for d in daterange(start, end, step):
  with open(f'securities-{d}.json', 'w', encoding='utf-8') as f:
    r = requests.get(f'https://iss.moex.com/iss/history/engines/stock/totals/boards/MRKT/securities.json?iss.meta=off&date={d}&securities.columns=SECID,CURRENCYID,OPEN,CLOSE,VOLUME,VALUE,NUMTRADES,DAILYCAPITALIZATION')
    f.write(r.text)
    f.close()
