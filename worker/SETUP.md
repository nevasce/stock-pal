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

## 9. Deep-dip scanner (automatic)
Runs every weekday after 5:00 PM ET (about 3:45 AM Nepal time) in two steps a couple of minutes apart, and sends one Telegram summary:
- whether QQQ is ≥10% below its 52-week high (setup active or not)
- stocks in the pool ≥30% below their 52-week high, with last EPS surprise, negative headlines in the last 14 days, and a Claude verdict (✅ fits / ⚠️ company-specific / ❌ avoid)

Run it by hand: open `/deepdip?token=YOUR_ADMIN_TOKEN`, wait a minute, open it again.
Optional settings: `DD_STOCK_PCT` (default `30`), `DD_MARKET_PCT` (default `10`), `DEEPDIP_POOL` (defaults to the basket pool).

## 10. Journal and weekly scorecard (automatic)
- **Send the bot any message** → saved as a journal note for today (D1 `notes`), and the bot replies "📝 Saved".
- `/status` → open paper baskets with current, worst and best result. `/help` → commands.
- Only messages from your own chat (`TELEGRAM_CHAT_ID`) are accepted.
- **Every Friday 4:20–5:00 PM ET:** weekly scorecard (Quick vs. Patient, win rate, average win/loss, worst point, QQQ, questions Q2–Q4) plus Claude's lesson of the week. Run by hand: `/weekly?token=YOUR_ADMIN_TOKEN`.
- Note: the Worker now reads the bot's messages every minute, so the `/chatid` link no longer shows your chat ID. Use @userinfobot if you need it again.

## 11. Newsletter inbox (Motley Fool, Zacks, …)
Forwarded newsletters → Claude extracts the stock calls → D1 `newsletters` + `picks` (with the price that day) → Telegram digest flagging overlaps with your holdings, the deep-dip list and open baskets.

**A. Check nevasce.com's existing mail first.** Cloudflare → nevasce.com → **DNS → Records**, filter by **MX**.
- **No MX records** → safe to continue.
- **MX records exist** (Google Workspace, Zoho, etc.) → stop: enabling Email Routing could replace them. Use a subdomain-only setup or another domain.

**B. Turn on Email Routing.** nevasce.com → **Email → Email Routing** → enable (Cloudflare adds the needed DNS records). Under **Settings → Subdomains**, add `in` so mail for `in.nevasce.com` is handled.

**C. Create the address.** **Routing rules → Create address**:
- Custom address: your private inbox address (e.g. `picks-xxxxxxxx@in.nevasce.com`)
- Action: **Send to a Worker** → `market-watch`

**D. Worker settings** (Variables and Secrets, type **Secret**):
- `INBOX_ADDRESS` = the private address from step C
- `ALLOWED_FORWARDERS` = your iCloud address (comma-separate if several)

**E. iCloud rules.** icloud.com → Mail → ⚙️ → **Rules** → Add a rule for each sender:
- If a message **is from** `fool.com` → **Forward to** the private address (keep "also keep in inbox")
- Same for `zacks.com` and any other newsletter

**F. Test.** Forward one newsletter by hand to the private address. You should get a 📬 Telegram digest within a minute. If you get "Rejected an email…", the message shows which sender to add to `ALLOWED_FORWARDERS`.

**Daily limits (Claude cost control):** Motley Fool emails are always analyzed, up to `FOOL_DAILY_CAP` (default `40`) a day. Other senders stop being analyzed after `NEWSLETTER_DAILY_CAP` (default `30`) a day. Emails over the limit are still saved (summary "Not analyzed: daily limit reached"), just not analyzed.

**Current setup:** private inbox `picks-n7makoab@mystockwatching.app` (domain bought Nov 2026, not set to auto-renew). iCloud web rules forward `fool.com`, `zacks.com`, `bloomberg.com`, `stocknews.com`. To move to a new domain later: onboard it in Email Routing, create the address → Send to Worker `market-watch`, update the `INBOX_ADDRESS` secret, update the iCloud rules.

Premium newsletter content is for personal use: it stays in your private database only. No scraping of logged-in subscriber sites (against Motley Fool's terms); enable all email alerts in the Fool account instead.

## 12. Daily news brief (automatic)
Every day at 8:30 PM ET (about 7:15 AM Nepal), one Telegram message: Claude's summary of the last ~24 hours of market news and your stocks' news, grouped as TOP 3 FOR YOUR PORTFOLIO, Macro & Fed, War & geopolitics, Tech & AI, Cyber & outages, Your stocks, Newsletter picks, and a calm "today's stance" line. Stored in D1 `briefs`. Run by hand: `/brief?token=YOUR_ADMIN_TOKEN`.

The instant keyword alerts also cover AI/tech shifts (OpenAI, Anthropic, new AI models, data centers, AI capex, chipmakers, antitrust, IPOs, takeovers), financial shocks (bank failures, bailouts, flash crashes) and disasters (earthquakes, pandemics), in addition to Fed, war, tariffs and cyberattacks.

## 13. Hourly tech pulse (optional, "one tweet an hour")
Set the plain-text variable `TECH_PULSE` = `on`. Every hour at :07 (day and night) the Worker gathers fresh items from Hacker News, arXiv (new AI/ML papers), Hugging Face (trending models), GitHub (fast-rising new AI repos, copycats filtered) and Finnhub tech news, skips anything already sent, and Claude picks the single most useful one: a 2–3 line note with "Why it matters" and a link. Stored in D1 `pulses`.
Cost: one Claude call per hour (~24/day). `PULSE_MODEL` overrides the model just for this (e.g. `claude-haiku-5-5` costs far less than the default `claude-opus-5-5`).

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
