import json
exec(open("bt3.py").read().split("print(\"STRATEGY 3")[0])
last={s:C[s][-1] for s in C}
print("Net result, $5,000 per trade, +2% target ($100 wins), stuck trade marked at today's price:")
for s,trig,drop in [("QQQ",None,0.01)]+[(x,None,0.03) for x in ["NVDA","AMD","META","TSLA","INTC","PYPL","ZM","SNOW","SMCI","ADBE"]]:
    tr=strat3(s,drop,0.02)
    wins=sum(1 for t in tr if t[3])*100
    stuck=[t for t in tr if not t[3]]
    # loss on stuck: entry close at date -> today
    loss=0
    for t in stuck:
        i=T[s].index(t[0]); loss+=5000*(C[s][-1]/C[s][i]-1)
    print(f"  {s:5s} wins +${wins:5d}  stuck trade {loss:+8.0f}  NET {wins+loss:+8.0f}")
