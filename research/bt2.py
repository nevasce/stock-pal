import json,sys
from datetime import datetime,time
from zoneinfo import ZoneInfo
from collections import defaultdict
ET=ZoneInfo("America/New_York")
bars=json.load(open(sys.argv[1]))
days=defaultdict(list)
for b in bars:
    t=datetime.fromisoformat(b["t"].replace("Z","+00:00")).astimezone(ET)
    if time(9,30)<=t.time()<time(16,0): days[t.date()].append((t.time(),b))
days={d:v for d,v in days.items() if len(v)>=70}
def run(th,tp,sl,last_entry=time(12,0)):
    res=[]
    for d,v in sorted(days.items()):
        o=v[0][1]["o"]; low=1e9; armed=False; entry=None
        for i,(t,b) in enumerate(v):
            if entry is None:
                if t>=last_entry: break
                low=min(low,b["l"])
                if low/o-1<=-th: armed=True
                # confirmation: after the dip, a 5-min bar closes above the highs of the previous 2 bars
                if armed and i>=2 and b["c"]>max(v[i-1][1]["h"],v[i-2][1]["h"]) and b["c"]<o:
                    entry=b["c"]; continue
            else:
                if b["l"]<=entry*(1-sl): res.append(-sl);break
                if b["h"]>=entry*(1+tp): res.append(tp);break
                if t>=time(15,45): res.append(b["c"]/entry-1);break
    return res
print("dip  target stop | trades win%  avg/trade  total(1yr)")
for th in (0.005,0.0075,0.01,0.015):
    for tp,sl in ((0.0075,0.0075),(0.01,0.01),(0.01,0.005),(0.015,0.0075)):
        r=run(th,tp,sl)
        if r: print(f"{th*100:4.2f}% +{tp*100:.2f}% -{sl*100:.2f}% | {len(r):4d}  {sum(x>0 for x in r)/len(r)*100:4.0f}%  {sum(r)/len(r)*100:+.3f}%   {sum(r)*100:+.1f}%")
