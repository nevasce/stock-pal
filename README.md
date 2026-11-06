# Stock Pal

A personal stock assistant built for discipline, not speed: calm alerts that explain *why* the market moved, a written rulebook, a paper-trading experiment, and a permanent record of results.

## What's running

| Part | Where | What it does |
|---|---|---|
| **Market Watch Worker** | Cloudflare Worker `market-watch` (runs every minute) | Watches QQQ/SPY and your holdings, scans high-impact news, sends Telegram alerts with a short Claude explanation |
| **Paper basket experiment** | Same Worker → Alpaca **paper** account | Every trading day buys two 7-stock baskets near the day's lows; "Quick" sells at +1.5%, "Patient" at +4%, 30-day limit |
| **History database** | Cloudflare D1 `market-watch-db` | Permanent record of every basket, stock, alert and daily snapshot |
| **Short-term state** | Cloudflare KV `market-watch-state` | Today's alert flags, open baskets |

## Repository layout

```
worker/      Cloudflare Worker code, deploy config, database schema, setup guide
research/    Data-download scripts, backtests, top-100 tech/AI list
docs/        Playbook (rules), research findings, roadmap
```

## Data sources

- **Finnhub**: real-time quotes, news, earnings calendar
- **Alpaca**: live IEX quotes, options prices, historical bars, paper trading
- **Twelve Data**: prices and 52-week ranges
- **Anthropic API**: short "why it moved" explanations (capped at 15 per day)

No API keys are stored in this repository. They live in Cloudflare Secrets.

## Key documents

- [docs/PLAYBOOK.md](docs/PLAYBOOK.md): money split, strategies, risk limits
- [docs/RESEARCH.md](docs/RESEARCH.md): what the backtests and published research showed
- [docs/ROADMAP.md](docs/ROADMAP.md): what's built and what's next
- [worker/SETUP.md](worker/SETUP.md): how to deploy the Worker from scratch
