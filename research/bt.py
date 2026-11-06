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
print("trading days:",len(days))
def stats(name,rets):
    if not rets: print(f"{name}: no trades");return
    w=sum(r>0 for r in rets)/len(rets)
    print(f"{name}: trades {len(rets):3d} | win {w*100:4.0f}% | avg {sum(rets)/len(rets)*100:+.2f}% | best {max(rets)*100:+.2f}% worst {min(rets)*100:+.2f}% | total {sum(rets)*100:+.1f}%")
# Q1: how often does QQQ fall from the open by 11:00, and what happens after?
for th in (0.003,0.005,0.0075,0.01):
    hold=[];tgt=[];n=0;rebound=0
    for d,v in sorted(days.items()):
        o=v[0][1]["o"]
        m=[b for t,b in v if t<time(11,0)]
        low=min(b["l"] for b in m)
        if low/o-1>-th: continue
        # realistic entry: close of the 10:55 bar (11:00), only if still below open
        entry=m[-1]["c"]
        if entry>=o: continue
        n+=1
        aft=[b for t,b in v if t>=time(11,0)]
        close=aft[-1]["c"]
        hold.append(close/entry-1)
        if max(b["h"] for b in aft)>=o: rebound+=1
        # exit: +1% target, -1% stop, else close
        r=close/entry-1
        for b in aft:
            if b["l"]<=entry*0.99: r=-0.01;break
            if b["h"]>=entry*1.01: r=0.01;break
        tgt.append(r)
    print(f"\n== QQQ down >= {th*100:.2f}% from open before 11:00, still below open at 11:00 ({n} days)")
    print(f"   came back to the open price by close: {rebound}/{n} = {rebound/max(n,1)*100:.0f}%")
    stats("   buy 11:00, sell at close     ",hold)
    stats("   buy 11:00, +1% target/-1% stop",tgt)
# baseline: every day buy 11:00 sell close
base=[]
for d,v in days.items():
    e=[b for t,b in v if t<time(11,0)][-1]["c"]; base.append(v[-1][1]["c"]/e-1)
stats("\n== BASELINE every day buy 11:00 sell close",base)
