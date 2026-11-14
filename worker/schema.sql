CREATE TABLE IF NOT EXISTS baskets (
  id INTEGER PRIMARY KEY, type TEXT, status TEXT, open_date TEXT, open_ts TEXT, close_date TEXT,
  days INTEGER, symbols TEXT, target REAL, cost REAL, proceeds REAL, pnl REAL, ret_pct REAL,
  reason TEXT, qqq_at_open REAL, qqq_day_chg_at_open REAL, qqq_at_close REAL);
CREATE TABLE IF NOT EXISTS basket_legs (
  basket_id INTEGER, symbol TEXT, day_chg_at_entry REAL, near_low INTEGER, qty REAL, cost REAL, proceeds REAL,
  PRIMARY KEY (basket_id, symbol));
CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, et_date TEXT, lines TEXT, headlines TEXT, ai_text TEXT);
CREATE TABLE IF NOT EXISTS daily (
  date TEXT PRIMARY KEY, qqq REAL, qqq_chg REAL, spy REAL, spy_chg REAL, open_baskets INTEGER,
  open_value_pnl REAL, realized_quick REAL, realized_patient REAL, quotes TEXT);

CREATE TABLE IF NOT EXISTS deepdip (
  date TEXT, symbol TEXT, price REAL, high_52w REAL, dd_pct REAL, qqq_dd_pct REAL, setup_active INTEGER,
  eps_surprise_pct REAL, neg_headlines INTEGER, headlines TEXT, verdict TEXT, PRIMARY KEY (date, symbol));

ALTER TABLE baskets ADD COLUMN worst_ret_pct REAL;
ALTER TABLE baskets ADD COLUMN best_ret_pct REAL;
CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, et_date TEXT, text TEXT);
CREATE TABLE IF NOT EXISTS weekly (week_start TEXT PRIMARY KEY, created_ts TEXT, scorecard TEXT, lesson TEXT);

CREATE TABLE IF NOT EXISTS newsletters (
  id INTEGER PRIMARY KEY AUTOINCREMENT, received_ts TEXT, et_date TEXT, envelope_from TEXT, header_from TEXT,
  subject TEXT, source TEXT, is_newsletter INTEGER, summary TEXT, text_excerpt TEXT);
CREATE TABLE IF NOT EXISTS picks (
  id INTEGER PRIMARY KEY AUTOINCREMENT, newsletter_id INTEGER, et_date TEXT, source TEXT, ticker TEXT,
  action TEXT, detail TEXT, price_at_receipt REAL);

CREATE TABLE IF NOT EXISTS briefs (date TEXT PRIMARY KEY, created_ts TEXT, text TEXT, headline_count INTEGER);

CREATE TABLE IF NOT EXISTS pulses (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, source TEXT, title TEXT, url TEXT, note TEXT);
