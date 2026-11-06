import json,urllib.request,urllib.parse,sys
syms=sys.argv[1].split(",");out={}
tok=None
while True:
    p={"symbols":",".join(syms),"timeframe":"1Day","start":"2016-01-01T00:00:00Z","end":"2026-11-05T00:00:00Z","limit":10000,"adjustment":"all","feed":"sip"}
    if tok:p["page_token"]=tok
    d=json.load(urllib.request.urlopen("https://data.alpaca.markets/v2/stocks/bars?"+urllib.parse.urlencode(p),timeout=60))
    for s,b in d.get("bars",{}).items(): out.setdefault(s,[]).extend(b)
    tok=d.get("next_page_token")
    if not tok:break
json.dump(out,open("daily.json","w"))
for s in syms: print(s,len(out.get(s,[])),out[s][0]["t"][:10] if s in out else "-")
