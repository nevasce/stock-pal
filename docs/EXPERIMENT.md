# 30-day paper basket experiment

Written **Nov 6, 2026, before any results**, so the questions and pass/fail rules can't be bent to fit the outcome.

## Setup (frozen until review day)

| Setting | Value |
|---|---|
| Account | Alpaca **paper**, $25,000 |
| Entry | Every trading day, last 90 min before the close: two baskets with the same 7 stocks from the 30-stock pool, preferring stocks down on the day and within 0.5% of their day low (fallback: the 7 weakest) |
| Size | $2,500 per basket (about $357 per stock) |
| Basket A "Quick" | sell all together at **+1.5%** |
| Basket B "Patient" | sell all together at **+4%** |
| Limits | never sell on the purchase day; sell anything open **30 trading days**; max 8 open baskets |
| Start | Nov 6, 2026 (first baskets were a manual 10-stock test at 1:59 PM ET; normal daily entries start Nov 9) |
| Review | **~Dec 18, 2026** |

**No settings change during the 30 days.** Ideas for changes go into the journal and are tested in the next round.

## Questions

| # | Question | Data |
|---|---|---|
| Q1 | Quick or Patient: which makes more money per day the money is tied up? | `baskets.pnl`, `days` |
| Q2 | Do baskets bought on QQQ down days beat those bought on up days? | `baskets.qqq_day_chg_at_open` |
| Q3 | Do stocks bought near their day low beat fallback picks? | `basket_legs.near_low` |
| Q4 | Which stocks bounce best, and which drag baskets down? | `basket_legs` cost vs. proceeds |
| Q5 | How far do baskets fall before recovering, and how long is money stuck? | `baskets.worst_ret_pct`, `days` |
| Q6 | Do deep-dip ✅ stocks beat ⚠️ ones over 1, 3 and 6 months? | `deepdip` table (long-term) |
| Q7 | How do I react to drops and alerts, and were my instincts right? | `notes` (Telegram journal) |

## Pass/fail rules (decided now)

The basket strategy is used with real money **only if all of these are true** on review day:

1. At least **20 closed baskets** (fewer → too early, extend the test)
2. **Total profit beats holding QQQ** with the same money over the same period
3. **Average loss ≤ 2× average win**
4. **Worst drop while holding ≤ 15%**

If it fails: change **one** thing (e.g. only buy on QQQ down days) and run another 30 days, or drop the strategy.
If it passes: run another 60 days before real money; start real money small.

## Honest limits

- 30 days ≈ 20–40 baskets: a first look, not proof.
- One market environment (a post-selloff, choppy market in Nov–Dec 2026).
- Paper fills are idealized (no real slippage at the bid/ask).
- The most valuable lesson may be about my own reactions, which is why the daily note matters.

## Daily and weekly routine

| When | What |
|---|---|
| Every morning (Nepal) | Read the daily report + deep-dip scan; send the bot one line: what I noticed, what I'd have done, how I felt |
| Friday after the close | Automatic weekly scorecard + lesson of the week (Telegram, stored in `weekly`) |
| Weekends | Add lessons to `docs/LEARNINGS.md` |
| ~Dec 18 | Apply the pass/fail rules |
