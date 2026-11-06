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
