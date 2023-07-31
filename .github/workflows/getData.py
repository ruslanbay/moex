from datetime import date, timedelta
import requests

def daterange(start, end):
    for n in range(int((end - start).days)):
        yield start + timedelta(n) + 7

# start = date(2011, 12, 19) # Monday
start = date(2023, 7, 3)
end = date(2023, 7, 28)
      
for d in daterange(start, end):
  # print(d.strftime("%Y-%m-%d"))
  with open(f'data/iss/history/engines/stock/totals/boards/MRKT/securities-{d}.json', 'w', encoding='utf-8') as f:
    r = requests.get(f'https://iss.moex.com/iss/history/engines/stock/totals/boards/MRKT/securities.json?iss.meta=off&date={d}&securities.columns=SECID,CURRENCYID,OPEN,CLOSE,VOLUME,VALUE,NUMTRADES,DAILYCAPITALIZATION')
    f.write(r.text)
    f.close()
