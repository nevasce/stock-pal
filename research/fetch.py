import json,time,urllib.request,sys
syms=open("universe.txt").read().split()
def get(u):
    for i in range(3):
        try:
            with urllib.request.urlopen(u,timeout=15) as r: return json.load(r)
        except Exception as e:
            time.sleep(3)
    return {}
out={}
for s in syms:
    m=get(f"https://finnhub.io/api/v1/stock/metric?symbol={s}&metric=all").get("metric",{}) ; time.sleep(1.05)
    q=get(f"https://finnhub.io/api/v1/quote?symbol={s}"); time.sleep(1.05)
    out[s]={"price":q.get("c"),"day":q.get("dp"),"hi52":m.get("52WeekHigh"),"lo52":m.get("52WeekLow"),
            "r52":m.get("52WeekPriceReturnDaily"),"ytd":m.get("yearToDatePriceReturnDaily"),"r13":m.get("13WeekPriceReturnDaily"),
            "mcap":m.get("marketCapitalization")}
    print(s,out[s],flush=True)
json.dump(out,open("metrics.json","w"))
print("DONE")
