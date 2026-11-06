# Roadmap

## Done (Nov 6, 2026)
- [x] Data connections: Twelve Data, Finnhub, Alpaca (data + paper trading)
- [x] Market Watch Worker on Cloudflare: 1-minute checks, QQQ/holdings alerts, high-impact news, dip-buy setup alert, Claude explanations, Telegram
- [x] 30-day paper basket experiment: two 7-stock baskets daily (Quick +1.5% vs. Patient +4%), 30-day limit, paper-account safety check
- [x] Permanent history in Cloudflare D1 (baskets, legs, alerts, daily snapshots)
- [x] Backtests of the intraday dip, deep-dip, down-day and basket strategies

## Next
- [ ] Deep-dip scanner: daily list of quality stocks ≥30% off their high while QQQ is ≥10% off, with a news check
- [ ] Trade journal via Telegram (`buy …` / `sell …`), pre-trade GO/NO-GO check, position sizer
- [ ] Loss-limit alarms and 3 PM expiring-options reminders for real trades
- [ ] Weekly scorecard: results vs. QQQ, rules followed vs. broken
- [ ] Market weather (trend, volatility, rates) and concentration guard
- [ ] Earnings lab: implied move vs. usual move from Alpaca options data

## Review dates
- **~Dec 18, 2026**: 30-day paper experiment review: Quick vs. Patient vs. QQQ, win rate, worst drop
- **Nov 17, 2026**: Nvidia earnings
