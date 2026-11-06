import json,random,statistics as st
D=json.load(open("daily.json"))
dates=[b["t"][:10] for b in D["QQQ"]]
px={s:{b["t"][:10]:b["c"] for b in v} for s,v in D.items()}
q=[px["QQQ"][d] for d in dates]
POOL=[s for s in D if s not in("QQQ","SPY")]
def run(pick,qdrop,target,size=5000,maxdays=None):
    trades=[];i=1
    while i<len(dates)-1:
        if q[i]/q[i-1]-1<=-qdrop:
            d=dates[i]; basket=pick(i)
            basket=[s for s in basket if d in px[s]]
            if len(basket)<5: i+=1;continue
            ent={s:px[s][d] for s in basket}
            worst=0;k=i+1;closed=False
            while k<len(dates):
                dk=dates[k]
                val=st.mean(px[s][dk]/ent[s] for s in basket if dk in px[s])-1
                worst=min(worst,val)
                if val>=target or (maxdays and k-i>=maxdays): closed=True;break
                k+=1
            if not closed: k=len(dates)-1; val=st.mean(px[s][dates[k]]/ent[s] for s in basket)-1
            trades.append(dict(d=d,days=k-i,ret=val,worst=worst,closed=closed,basket=basket)); i=k+1
        else: i+=1
    return trades
def report(name,tr,size=5000):
    pnl=sum(t["ret"] for t in tr)*size
    days=[t["days"] for t in tr]
    open_=[t for t in tr if not t["closed"]]
    losses=[t for t in tr if t["ret"]<0]
    print(f"{name:52s} trades {len(tr):3d} | wins {sum(t['ret']>0 for t in tr):3d} | losses {len(losses):2d} | median hold {st.median(days):4.0f}d | longest {max(days):4d}d | worst dip {min(t['worst'] for t in tr)*100:6.1f}% | NET ${pnl:+7.0f}"+(f" | open since {open_[0]['d']} at {open_[0]['ret']*100:+.1f}%" if open_ else ""))
MEGA=["NVDA","MSFT","AAPL","AMZN","META","GOOGL","AVGO"]
def biggest_fallers(i,n=7):
    d,p=dates[i],dates[i-1]
    ch=[(px[s][d]/px[s][p]-1,s) for s in POOL if d in px[s] and p in px[s]]
    return [s for _,s in sorted(ch)[:n]]
print("BASKET STRATEGY: when QQQ closes down, buy 7 stocks together ($5,000 total), sell all together when the basket is up X%\n")
for tgt in (0.02,0.04):
    print(f"--- sell when basket is +{tgt*100:.0f}% (= ${int(5000*tgt)})")
    report("7 mega-caps, QQQ -1% day",run(lambda i:MEGA,0.01,tgt),)
    report("7 biggest fallers that day (of 28), QQQ -1% day",run(biggest_fallers,0.01,tgt))
    report("7 biggest fallers, QQQ -1% day, 30-day time limit",run(biggest_fallers,0.01,tgt,maxdays=30))
    # random baskets: distribution
    random.seed(1);nets=[];worsts=[];longest=[]
    for _ in range(200):
        tr=run(lambda i:random.sample(POOL,7),0.01,tgt)
        nets.append(sum(t["ret"] for t in tr)*5000);worsts.append(min(t["worst"] for t in tr));longest.append(max(t["days"] for t in tr))
    print(f"{'200 random 7-stock baskets, QQQ -1% day':52s} NET median ${st.median(nets):+7.0f} | worst basket ${min(nets):+7.0f} | best ${max(nets):+7.0f} | typical worst dip {st.median(worsts)*100:.1f}% | typical longest hold {st.median(longest):.0f}d")
    print()
qtr=sum(1 for _ in [0])
print(f"For comparison: $5,000 simply held in QQQ since 2016 -> +${5000*(q[-1]/q[0]-1):,.0f}")
