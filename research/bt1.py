import json,statistics as st
D=json.load(open("daily.json"))
C={s:[b["c"] for b in v] for s,v in D.items()};T={s:[b["t"][:10] for b in v] for s,v in D.items()}
qidx={d:i for i,d in enumerate(T["QQQ"])};q=C["QQQ"]
def qdd(d):
    i=qidx[d];hi=max(q[max(0,i-252):i+1]);return q[i]/hi-1
res={"market":[], "own":[]}
for s in C:
    if s in("QQQ","SPY"):continue
    c=C[s];t=T[s];last=-999
    for i in range(252,len(c)):
        hi=max(c[i-252:i+1]); dd=c[i]/hi-1
        if dd<=-0.30 and i-last>60:
            last=i
            kind="market" if qdd(t[i])<=-0.10 else ("own" if qdd(t[i])>-0.05 else None)
            if not kind: continue
            def fwd(n): return c[i+n]/c[i]-1 if i+n<len(c) else None
            rec=None
            for k in range(i,min(len(c),i+504)):
                if c[k]>=hi: rec=k-i;break
            res[kind].append((s,t[i],dd,fwd(63),fwd(126),fwd(252),rec, i+252<len(c)))
for kind,label in (("market","Stock >=30% below high WHILE QQQ >=10% below its high (market-driven fall)"),("own","Stock >=30% below high while QQQ within 5% of its high (stock-specific fall)")):
    r=res[kind];print("\n"+label+f": {len(r)} events")
    for n,ix in (("3 months",3),("6 months",4),("12 months",5)):
        v=[x[ix] for x in r if x[ix] is not None]
        if v: print(f"   {n:9s}: avg {st.mean(v)*100:+6.1f}%  median {st.median(v)*100:+6.1f}%  positive {sum(x>0 for x in v)/len(v)*100:3.0f}%  worst {min(v)*100:+6.1f}%")
    full=[x for x in r if x[7]]
    print(f"   back to the old high within 2 years: {sum(1 for x in full if x[6] is not None)}/{len(full)}")
    if kind=="own":
        print("   examples:",", ".join(f"{x[0]} {x[1][:7]}" for x in r[:12]))
