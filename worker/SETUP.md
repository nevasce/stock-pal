# Market Watch: setup guide (about 20 minutes)

## 1. Create the Telegram bot (2 min)
1. In Telegram, open **@BotFather** and send `/newbot`.
2. Pick a name (e.g. `My Market Watch`) and a username ending in `bot`.
3. BotFather replies with a **token** like `123456:ABC...`. Keep it for step 4.
4. Open your new bot and send it any message (e.g. `hi`). This is needed to find your chat ID.

## 2. Create the Worker (5 min)
1. Go to **dash.cloudflare.com** → sign up or log in (the free plan is fine).
2. **Workers & Pages** → **Create** → **Create Worker** → name it `market-watch` → **Deploy**.
3. Click **Edit code**, delete everything, paste in all of `worker.js`, then click **Deploy**.

## 3. Add storage (KV) (2 min)
1. **Storage & Databases** → **KV** → **Create namespace** → name it `market-watch-state`.
2. Go back to your Worker → **Settings** → **Bindings** → **Add** → **KV namespace**
   - Variable name: `STATE` (exactly that)
   - Namespace: `market-watch-state`

## 4. Add secrets (5 min)
Worker → **Settings** → **Variables and Secrets** → **Add**. Choose type **Secret** for each:

| Name | Value |
|---|---|
| `FINNHUB_KEY` | your Finnhub API key |
| `TELEGRAM_TOKEN` | the BotFather token |
| `TELEGRAM_CHAT_ID` | fill in after step 5 (put `0` for now) |
| `ANTHROPIC_API_KEY` | your Anthropic API key |
| `ADMIN_TOKEN` | any password you make up, e.g. `mw-7Hq2x9` |

Optional plain-text variables:
| Name | Default | Purpose |
|---|---|---|
| `HOLDINGS` | `NVDA,AMD,MU,TSM,AVGO,META,GOOG,ANET,PLTR,CRWD,TSLA,STRL` | stocks to watch (comma-separated) |
| `MAX_AI_CALLS_PER_DAY` | `15` | hard cap on Claude explanations per day |
| `CLAUDE_MODEL` | `claude-opus-5-5` | `claude-haiku-5-5` is about 40× cheaper but less insightful |

## 5. Get your chat ID (1 min)
Open in a browser (use your Worker's URL and your ADMIN_TOKEN):
```
https://market-watch.<your-subdomain>.workers.dev/chatid?token=YOUR_ADMIN_TOKEN
```
Copy the number from `chat_ids` into the `TELEGRAM_CHAT_ID` secret.

## 6. Turn on the 1-minute schedule (1 min)
Worker → **Settings** → **Trigger Events** (or **Triggers**) → **Add Cron Trigger** → enter `* * * * *` → Save.
(The code itself decides what to do: price checks during market hours, news checks every 5 minutes otherwise.)

## 7. Test (1 min)
```
https://market-watch.<your-subdomain>.workers.dev/test?token=YOUR_ADMIN_TOKEN
```
Your phone should get a "✅ Market Watch test alert" with a short Claude explanation.

Other admin links:
- `/status?token=...` shows what it remembers today
- `/run?token=...` runs one check now

## 8. Turn on the 30-day paper basket experiment (2 min)
Add two more **Secrets**, using your **PAPER** account keys (Key ID starts with `PK`):

| Name | Value |
|---|---|
| `ALPACA_KEY_ID` | paper Key ID |
| `ALPACA_SECRET_KEY` | paper Secret Key |

That's all. It starts on the next trading day. Optional plain-text settings:

| Name | Default | Meaning |
|---|---|---|
| `BASKET_USD` | `2500` | dollars per basket (two baskets a day) |
| `BASKET_SIZE` | `7` | stocks per basket |
| `QUICK_TARGET` | `0.015` | Basket A sells at +1.5% |
| `PATIENT_TARGET` | `0.04` | Basket B sells at +4% |
| `MAX_DAYS` | `30` | sell any basket after 30 trading days, win or lose |
| `MAX_OPEN_BASKETS` | `8` | no new baskets while 8 are open ($20k) |
| `BASKET_POOL` | 30 tech/AI leaders | comma-separated list of stocks it may pick from |

⚠️ Never set `FORCE_ENTRY` or `ENTRY_WINDOW_MIN`; those are only for testing.
🛡️ Safety: the Worker checks the account number and **refuses to trade unless it's a paper account** (starts with `PA`).

**How it works each trading day**
1. In the last 90 minutes before the close (about 2:30–3:50 PM ET, or about 1:15–2:35 AM Nepal time), it looks for the 7 stocks in the pool that are **down the most and trading near their low of the day**. If 7 aren't near their lows by 3:45 PM, it takes the 7 biggest fallers.
2. It buys **two baskets with the same 7 stocks**: A "Quick" and B "Patient".
3. From the **next day** on (never the same day), it sells each basket **all together** when it hits its target, or after 30 trading days.
4. Telegram: a message on every buy and sell, plus a **daily report after the close** comparing Quick vs. Patient vs. QQQ.

## What you'll receive
- 🔻/🔺 **QQQ moves ≥0.5% within 10 minutes**
- 📉/📈 **QQQ crosses ±1%, 1.5%, 2%, 2.5%, 3%** on the day (once each)
- 🔻/🔺 **Any holding moves ±4%, 6%, 8%, 10%** (once each)
- ⚡ **Dip-buy setup:** QQQ ≥1% below its open before noon ET and turning up
- 📰 **High-impact headlines:** Fed/rates, war/military, tariffs/sanctions, hacks/outages, and earnings/guidance/downgrades for your stocks
- 🧠 A 3–5 line **"why / scope / what it means for you"** from Claude on each alert (up to 15/day)

## Cost
- Cloudflare, Finnhub, Telegram: **$0**
- Claude (Opus 5.5, low effort): about **$0.01–0.02 per explanation**. With the 15/day cap, the worst case is about $6/month; a typical month is **$1–4**.
