import json;D=json.load(open("daily.json"))
for s in ["QQQ","NVDA","AMD","META","INTC","PYPL","ZM","SMCI","ADBE"]:
    c=[b["c"] for b in D[s]];d=D[s][0]["t"][:10]
    print(f"{s:5s} buy&hold $5,000 since {d}: ${5000*c[-1]/c[0]:,.0f}")
