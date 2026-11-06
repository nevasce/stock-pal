import json,statistics as st
D=json.load(open("daily.json"))
C={s:[b["c"] for b in v] for s,v in D.items()}
T={s:[b["t"][:10] for b in v] for s,v in D.items()}
def strat3(sym,drop,target,trigger_sym=None,trig_drop=None):
    c=C[sym]; tc=C[trigger_sym] if trigger_sym else c; td=T[sym]
    # align by date if trigger is different
    if trigger_sym:
        idx={d:i for i,d in enumerate(T[trigger_sym])}
    trades=[];i=1
    while i<len(c)-1:
        if trigger_sym:
            j=idx.get(td[i]); 
            if j is None or j==0: i+=1;continue
            day=tc[j]/tc[j-1]-1
        else: day=c[i]/c[i-1]-1
        if day<=-drop:
            e=c[i];worst=0;k=i+1
            while k<len(c) and c[k]<e*(1+target):
                worst=min(worst,c[k]/e-1);k+=1
            if k<len(c): trades.append((td[i],k-i,worst,True)); i=k+1
            else: trades.append((td[i],k-1-i,min(worst,c[-1]/e-1),False)); break
        else: i+=1
    return trades
def show(name,tr,target):
    if not tr: print(name,"no trades");return
    done=[t for t in tr if t[3]];open_=[t for t in tr if not t[3]]
    days=[t[1] for t in done]
    print(f"{name:28s} trades {len(tr):3d} | hit target {len(done):3d} | still stuck {len(open_)} | median hold {st.median(days) if days else 0:4.0f}d | 90% within {sorted(days)[int(.9*len(days))-1] if days else 0:4d}d | longest {max(days) if days else 0:4d}d | worst dip while holding {min(t[2] for t in tr)*100:6.1f}%"+(f" | STUCK since {open_[0][0]} at {open_[0][2]*100:.0f}%" if open_ else ""))
print("STRATEGY 3: buy at close on a down day, sell at first close with profit target, never sell at a loss (2016-2026)\n")
for tgt in (0.02,0.04):
    print(f"--- target +{tgt*100:.0f}% (= ${int(5000*tgt)} on a $5,000 position)")
    show("QQQ, buy after -1% day",strat3("QQQ",0.01,tgt),tgt)
    show("QQQ, buy after -2% day",strat3("QQQ",0.02,tgt),tgt)
    for s in ["NVDA","AMD","META","TSLA","INTC","PYPL","ZM","SNOW","SMCI","ADBE"]:
        show(f"{s}, buy after own -3% day",strat3(s,0.03,tgt),tgt)
    print()
