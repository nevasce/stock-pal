# Research findings

Backtests run in November 2026 on Alpaca historical data. Scripts are in `research/`.

**Caveats for all results:** 2016–2026 was an unusually strong decade for tech, and the stock lists are mostly companies that survived and are well known today (survivorship bias). Treat results as encouraging, not guaranteed.

## 1. Intraday QQQ morning dip (5-minute bars, Nov 2025 – Nov 2026, 254 days) — `bt.py`, `bt2.py`

How often QQQ got back to its opening price by the close after a morning drop:

| Drop from open before 11:00 | Days | Back to the open by close |
|---|---|---|
| ≥0.3% | 107 | 39% |
| ≥0.5% | 91 | 33% |
| ≥0.75% | 59 | 27% |
| ≥1.0% | 38 | 21% |

Buy on a reversal signal after the dip, +1.5% target / −0.75% stop:

| Dip size | Trades | Win rate | Total |
|---|---|---|---|
| ≥0.5% | 104 | 42% | −6.8% |
| ≥0.75% | 64 | 48% | −1.5% |
| **≥1.0%** | **41** | **61%** | **+3.6%** |
| ≥1.5% | 13 | 46% | −1.6% |

→ Small dips lose. Only ~1% dips plus waiting for the turn showed an edge, and it's thin.

## 2. Deep-dip quality stocks (daily bars 2016–2026, 28 tech stocks) — `bt1.py`

| Situation | Events | 3 months later | 12 months later | Back to old high within 2 yrs |
|---|---|---|---|---|
| Stock ≥30% off high **while QQQ ≥10% off its high** | 172 | +11% median, 64% up | +42% median, 73% up | 74% |
| Stock ≥30% off high **while QQQ near its high** | 101 | −1% median, 49% up | +25% median, 66% up | 69% |

→ Market-driven falls in quality stocks recovered much faster than stock-specific falls. Worst cases still fell another 46–56%.

## 3. Buy a down day, hold until profit, single stocks — `bt3.py`, `bt3b.py`

~98% of trades hit the target, but one stuck trade could erase years of wins ($5,000 per trade, +2% target):

| Stock | Wins | The stuck trade | Net |
|---|---|---|---|
| QQQ | +$6,400 | −$372 | +$6,028 |
| NVDA | +$9,300 | −$478 | +$8,822 |
| INTC | +$3,400 | −$2,706 (−54%) | +$694 |
| PYPL | +$4,600 | −$3,822 (−85%, since 2021) | +$778 |
| SMCI | +$7,600 | −$3,690 (−84%) | +$3,910 |
| ZM | +$2,800 | −$4,145 (−90%, since 2020) | **−$1,345** |

→ Fine on an index; dangerous on single stocks. Buy-and-hold QQQ over the same period: +$29,197 on $5,000.

## 4. Seven-stock basket on QQQ down days — `bt4.py`

| Version | Profit over 10 yrs ($5,000) | Longest hold | Worst drop while holding |
|---|---|---|---|
| 7 mega-caps, sell at +2% | +$11,757 | 360 d | −44% |
| 7 biggest fallers, sell at +2% | +$13,355 | 556 d | −65% |
| 7 biggest fallers, sell at +4% | +$13,625 | 567 d | −65% |
| **7 biggest fallers + 30-day limit** | **≈+$13,200–13,850** | **30 d** | **−30%** |
| 200 random 7-stock baskets | +$7,661 to +$18,096 (all positive) | ~520 d typical | ~−49% typical |

→ Baskets fix the single-stock blow-up problem. The 30-day limit keeps the profit while halving the worst drop.

## 5. Published research (summary)

- About 4% of US stocks created all net stock-market wealth since 1926 (Bessembinder 2018); most stocks underperformed T-bills.
- Missing the best few days roughly halves long-run returns; best days cluster near the worst days.
- ~85–90% of active US stock funds trail the S&P 500 over 15 years (SPIVA).
- Momentum (3–12 months) and post-earnings drift are among the most durable documented effects.
- Investors trail their own funds by ~1.2%/yr from bad timing (Morningstar "Mind the Gap" 2025); over 80% of day traders lose money after costs (Barber, Lee, Liu, Odean).
- AI trading contests (Alpha Arena 2025): most models, including Claude, lost money trading on their own. AI helps most with research, explanation, rules and record-keeping.
- Price alerts can help investors with accurate beliefs and amplify mistakes for others, so alerts should give context and default to "no action needed".
