import json,urllib.request,urllib.parse,sys
sym,start,end,out=sys.argv[1:5]
bars=[];tok=None
while True:
    p={"symbols":sym,"timeframe":"5Min","start":start,"end":end,"limit":10000,"adjustment":"split","feed":"sip"}
    if tok:p["page_token"]=tok
    u="https://data.alpaca.markets/v2/stocks/bars?"+urllib.parse.urlencode(p)
    try:
        d=json.load(urllib.request.urlopen(u,timeout=30))
    except urllib.error.HTTPError as e:
        print("ERR",e.code,e.read()[:300]);sys.exit(1)
    bars+=d.get("bars",{}).get(sym,[]);tok=d.get("next_page_token")
    if not tok:break
json.dump(bars,open(out,"w"));print(sym,len(bars),"bars",bars[0]["t"] if bars else None,bars[-1]["t"] if bars else None)
