#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        NSE MAINBOARD IPO BREAKOUT SCANNER                    ║
║                                                              ║
║  Data source:                                                ║
║    NSE Archives — EQUITY_L.csv (public, no auth needed)      ║
║                                                              ║
║  THREE LAYERS:                                               ║
║                                                              ║
║  [1] 1ST BREAKOUT                                            ║
║      Stock crossed above its listing-day high for the        ║
║      very first time within the last BREAKOUT_WINDOW_DAYS.   ║
║                                                              ║
║  [2] RETEST  +  HAMMER                                       ║
║      Stock already broke out above listing-day high earlier, ║
║      pulls back to that level for the first time within      ║
║      BREAKOUT_WINDOW_DAYS, AND the retest candle is a        ║
║      Hammer (long lower wick, small body at top).            ║
║                                                              ║
║  [3] NEWS SENTIMENT  (Anthropic API + web search)            ║
║      For every signal stock, searches the web for news in    ║
║      the last NEWS_LOOKBACK_DAYS days and returns:           ║
║        Sentiment : Positive / Negative / Mixed / Neutral     ║
║        Headline  : one-line summary of the key news          ║
║                                                              ║
║  [4] NEAR BREAKOUT                                           ║
║      Stock has NEVER crossed above its listing-day high,     ║
║      but latest close is within NEAR_LEVEL_PCT below it.     ║
║                                                              ║
║  [5] RETRACING TO LEVEL                                      ║
║      Stock already broke out above its listing-day high      ║
║      and is now pulling back towards it — latest close is    ║
║      within NEAR_LEVEL_PCT above the listing-day high        ║
║      (early warning before retest+hammer).                   ║
║                                                              ║
║  [6] 1-HOUR LIQUIDITY FILTER              ★ NEW ★           ║
║      Every signal stock must pass a minimum average          ║
║      hourly traded value (Volume × Close) computed over      ║
║      the last LIQUIDITY_LOOKBACK_DAYS days on the 1h         ║
║      timeframe. Stocks below MIN_HOURLY_VALUE_LAKH are       ║
║      excluded. Avg value is shown in the output table.       ║
╚══════════════════════════════════════════════════════════════╝

Requirements:
    pip install yfinance pandas requests anthropic

Run:
    Set your Anthropic API key:
        Windows : set ANTHROPIC_API_KEY=sk-ant-...
        Mac/Linux: export ANTHROPIC_API_KEY=sk-ant-...

    Then:
        python nse_ipo_breakout_scanner.py
"""

import io
import os
import sys
import json
import time

import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta

# ──────────────────────────────────────────────────────────────
#  CONFIG  ← tweak these as needed
# ──────────────────────────────────────────────────────────────
MONTHS_BACK          = 24    # scan IPOs listed within this many months
MIN_DAYS_BELOW       = 1     # stock must have dipped below listing-high at least this many days
BREAKOUT_BUFFER      = 0.0   # 0.0 = exact cross; 0.01 = require 1% above to confirm breakout
RETEST_BUFFER        = 0.03  # retest zone: Low must be within this % ABOVE the breakout level
BREAKOUT_WINDOW_DAYS = 15    # signal must occur within this many calendar days
REQUEST_DELAY        = 1.0   # pause between yfinance calls (seconds)
PRINT_FAILURES       = False # True → show why each stock was skipped (for debugging)

# ── Near-level proximity threshold ───────────────────────────
NEAR_LEVEL_PCT       = 0.05  # 5% — raise signal when price is within this % of listing high

# ── Hammer candle parameters ──────────────────────────────────
HAMMER_SHADOW_MULTIPLIER = 2.0   # lower wick at least 2× the body
HAMMER_MAX_UPPER_RATIO   = 0.5   # upper wick at most 50% of body
HAMMER_MIN_BODY_PCT      = 0.05  # body must be at least 5% of total candle range

# ── 1-Hour Liquidity Filter ★ NEW ★ ──────────────────────────
MIN_HOURLY_VALUE_LAKH  = 100.0  # minimum avg hourly traded value in ₹ Lakhs
                                # (10 L = ₹10,00,000 per hour on average)
                                # Lower this if too few signals; raise for higher liquidity
LIQUIDITY_LOOKBACK_DAYS = 10   # number of calendar days of 1h data used to
                                # compute the average hourly traded value

# ── News sentiment (Anthropic API) ───────────────────────────
NEWS_LOOKBACK_DAYS = 10    # how many days back to search for news
NEWS_DELAY         = 2.0   # pause between Anthropic API calls (seconds)
ANTHROPIC_MODEL    = "claude-sonnet-4-20250514"
ANTHROPIC_API_URL  = "https://api.anthropic.com/v1/messages"


# ──────────────────────────────────────────────────────────────
#  STEP 1: DOWNLOAD NSE EQUITY LIST CSV
# ──────────────────────────────────────────────────────────────

EQUITY_CSV_URLS = [
    "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv",
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv",
]

MAINBOARD_SERIES = {"EQ", "BE", "BL", "IL", "IQ"}


def download_equity_csv() -> pd.DataFrame:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept":  "text/html,application/xhtml+xml,*/*",
        "Referer": "https://www.nseindia.com/",
    }
    for url in EQUITY_CSV_URLS:
        try:
            print(f"   Trying: {url} ...", end=" ", flush=True)
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            try:
                df = pd.read_csv(io.StringIO(resp.text))
            except Exception:
                df = pd.read_csv(io.StringIO(resp.content.decode("windows-1252")))
            print(f"OK  ({len(df)} rows)")
            return df
        except Exception as e:
            print(f"FAILED  ({e})")
            continue
    return pd.DataFrame()


def fetch_mainboard_ipos() -> pd.DataFrame:
    print("Fetching NSE equity list (EQUITY_L.csv)...")
    raw = download_equity_csv()
    if raw.empty:
        return pd.DataFrame()

    raw.columns = [c.strip().upper() for c in raw.columns]
    required = {"SYMBOL", "SERIES", "DATE OF LISTING"}
    if not required.issubset(set(raw.columns)):
        print(f"Unexpected CSV columns: {list(raw.columns)}")
        return pd.DataFrame()

    raw["SYMBOL"]          = raw["SYMBOL"].astype(str).str.strip().str.upper()
    raw["SERIES"]          = raw["SERIES"].astype(str).str.strip().str.upper()
    raw["NAME OF COMPANY"] = raw.get("NAME OF COMPANY", pd.Series([""] * len(raw))).astype(str).str.strip()
    raw["LISTING_DT"]      = pd.to_datetime(
        raw["DATE OF LISTING"].astype(str).str.strip(),
        format="%d-%b-%Y", errors="coerce",
    )

    raw = raw[raw["SERIES"].isin(MAINBOARD_SERIES)]
    raw = raw[raw["LISTING_DT"].notna()]

    cutoff = pd.Timestamp.today() - pd.DateOffset(months=MONTHS_BACK)
    raw    = raw[raw["LISTING_DT"] >= cutoff]

    raw["SERIES_RANK"] = raw["SERIES"].map({"EQ": 0}).fillna(1).astype(int)
    raw = (
        raw.sort_values("SERIES_RANK")
           .drop_duplicates(subset="SYMBOL", keep="first")
           .drop(columns="SERIES_RANK")
    )

    result = pd.DataFrame({
        "symbol":      raw["SYMBOL"].values,
        "companyName": raw["NAME OF COMPANY"].values,
        "listingDate": raw["LISTING_DT"].dt.strftime("%Y-%m-%d").values,
    })
    result = result.sort_values("listingDate", ascending=False).reset_index(drop=True)
    print(f"Found {len(result)} mainboard stocks listed in last {MONTHS_BACK} months.\n")
    return result


# ──────────────────────────────────────────────────────────────
#  STEP 2: FETCH PRICE HISTORY VIA yfinance
# ──────────────────────────────────────────────────────────────

def fetch_price_history(symbol: str, listing_date: str) -> pd.DataFrame:
    ticker = f"{symbol}.NS"
    try:
        df = yf.download(
            ticker,
            start=listing_date,
            end=(datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            interval="1d",
            progress=False,
            auto_adjust=True,
        )
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
    except Exception:
        return pd.DataFrame()


# ──────────────────────────────────────────────────────────────
#  STEP 2b: 1-HOUR LIQUIDITY CHECK  ★ NEW ★
#
#  Downloads the last LIQUIDITY_LOOKBACK_DAYS days of 1-hour
#  candles for the symbol and computes the average hourly
#  traded value = mean(Volume × Close) expressed in ₹ Lakhs.
#
#  Returns:
#    (passes: bool, avg_value_lakh: float)
#
#  Notes:
#    • yfinance 1h data is available up to ~730 days back.
#    • Only non-zero volume bars are included in the average
#      (pre-market / zero-trade slots are excluded).
#    • If fewer than 5 valid 1h bars are found the stock is
#      treated as illiquid and fails the filter.
# ──────────────────────────────────────────────────────────────

def check_hourly_liquidity(symbol: str) -> tuple[bool, float]:
    """
    Returns (passes_filter, avg_hourly_value_in_lakhs).
    passes_filter is True when avg >= MIN_HOURLY_VALUE_LAKH.
    """
    ticker = f"{symbol}.NS"
    try:
        end   = datetime.today() + timedelta(days=1)
        start = datetime.today() - timedelta(days=LIQUIDITY_LOOKBACK_DAYS)

        df = yf.download(
            ticker,
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            interval="1h",
            progress=False,
            auto_adjust=True,
        )

        if df.empty:
            if PRINT_FAILURES:
                print(f"  [liq] {symbol}: no 1h data returned")
            return False, 0.0

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Keep only bars with actual trades
        df = df[df["Volume"] > 0].copy()

        if len(df) < 5:
            if PRINT_FAILURES:
                print(f"  [liq] {symbol}: only {len(df)} valid 1h bars — treated as illiquid")
            return False, 0.0

        # Average hourly value traded in ₹ Lakhs (1 Lakh = 100,000)
        avg_value_lakh = float((df["Volume"] * df["Close"]).mean()) / 1e5

        passes = avg_value_lakh >= MIN_HOURLY_VALUE_LAKH
        return passes, round(avg_value_lakh, 2)

    except Exception as e:
        if PRINT_FAILURES:
            print(f"  [liq] {symbol}: exception — {e}")
        return False, 0.0


# ──────────────────────────────────────────────────────────────
#  STEP 3: HAMMER CANDLE DETECTOR
# ──────────────────────────────────────────────────────────────

def is_hammer(o: float, h: float, l: float, c: float) -> bool:
    body        = abs(c - o)
    total_range = h - l
    if total_range < 1e-9:
        return False
    lower_shadow = min(o, c) - l
    upper_shadow = h - max(o, c)
    if body < HAMMER_MIN_BODY_PCT * total_range:
        return False
    if lower_shadow < HAMMER_SHADOW_MULTIPLIER * body:
        return False
    if upper_shadow > HAMMER_MAX_UPPER_RATIO * body:
        return False
    return True


# ──────────────────────────────────────────────────────────────
#  STEP 4: SIGNAL DETECTION (breakout / retest+hammer /
#                            near-breakout / retracing)
#
#  ★ NOW calls check_hourly_liquidity() before returning any
#    signal dict.  Illiquid stocks return None.
# ──────────────────────────────────────────────────────────────

def check_stock(symbol: str, company: str, listing_date: str) -> dict | None:
    df = fetch_price_history(symbol, listing_date)

    if df.empty or len(df) < 2:
        if PRINT_FAILURES:
            print("skipped: not enough price data")
        return None

    day1           = df.iloc[0]
    breakout_level = max(float(day1["High"]), float(day1["Open"]))
    trigger        = breakout_level * (1 + BREAKOUT_BUFFER)

    after      = df.iloc[1:].copy()
    days_below = int((after["Close"] < breakout_level).sum())

    # ── Filter: pump-and-dump ─────────────────────────────────
    listing_day_high = float(day1["High"])
    listing_day_low  = float(day1["Low"])

    above_high_dates = after.index[after["High"] > listing_day_high]
    below_low_dates  = after.index[after["Low"]  < listing_day_low]

    if len(above_high_dates) > 0 and len(below_low_dates) > 0:
        first_above_high = above_high_dates[0]
        first_below_low  = below_low_dates[0]
        if first_below_low > first_above_high:
            if PRINT_FAILURES:
                print(
                    f"skipped: pump-and-dump detected — broke above listing high on "
                    f"{first_above_high.date()} then fell below listing low on "
                    f"{first_below_low.date()}"
                )
            return None

    if days_below < MIN_DAYS_BELOW:
        if PRINT_FAILURES:
            print("skipped: never dipped below listing high")
        return None

    today = pd.Timestamp.today().normalize()

    # ── Find first-ever breakout ──────────────────────────────
    first_co_date  = None
    first_co_close = None
    first_co_high  = None
    below_flag     = False

    for date, row in after.iterrows():
        close = float(row["Close"])
        high  = float(row["High"])
        if close < breakout_level or float(row["Low"]) < breakout_level:
            below_flag = True
        if below_flag and (close > trigger or high > trigger):
            first_co_date  = date
            first_co_close = close
            first_co_high  = high
            break

    # ── Helper: liquidity gate ────────────────────────────────
    def _liquidity_gate() -> tuple[bool, float]:
        """Run 1h liquidity check; print reason on failure."""
        passes, avg_val = check_hourly_liquidity(symbol)
        if not passes and PRINT_FAILURES:
            print(
                f"skipped: 1h avg traded value {avg_val:.1f} L "
                f"< threshold {MIN_HOURLY_VALUE_LAKH} L"
            )
        return passes, avg_val

    # ── SIGNAL: Near Breakout ─────────────────────────────────
    if first_co_date is None:
        latest       = df.iloc[-1]
        latest_close = float(latest["Close"])
        near_floor   = breakout_level * (1 - NEAR_LEVEL_PCT)
        if latest_close >= near_floor:
            passes, avg_val = _liquidity_gate()
            if not passes:
                return None
            pct_away = round((breakout_level - latest_close) / breakout_level * 100, 2)
            return {
                "Signal":             "Near Breakout",
                "Symbol":             symbol,
                "Company":            company[:35],
                "Listed On":          datetime.strptime(listing_date, "%Y-%m-%d").strftime("%d-%b-%Y"),
                "Breakout Level Rs":  round(breakout_level, 2),
                "Signal Date":        today.strftime("%d-%b-%Y"),
                "Days Since Signal":  0,
                "Signal Close Rs":    round(latest_close, 2),
                "Latest Close Rs":    round(latest_close, 2),
                "Latest High Rs":     round(float(latest["High"]), 2),
                "Pct Vs Level":       f"-{pct_away}%",
                "Days Below Lvl":     days_below,
                "Hammer":             "-",
                "Avg Hrly Val (L)":   avg_val,   # ★ NEW
            }
        if PRINT_FAILURES:
            print("skipped: no breakout above listing high ever")
        return None

    co_ts         = pd.Timestamp(first_co_date).normalize()
    days_since_bo = (today - co_ts).days

    # ── SIGNAL 1: first breakout is recent ───────────────────
    if days_since_bo <= BREAKOUT_WINDOW_DAYS:
        passes, avg_val = _liquidity_gate()
        if not passes:
            return None
        latest    = df.iloc[-1]
        pct_above = round(
            (max(first_co_close, first_co_high) - breakout_level) / breakout_level * 100, 2
        )
        return {
            "Signal":             "1st Breakout",
            "Symbol":             symbol,
            "Company":            company[:35],
            "Listed On":          datetime.strptime(listing_date, "%Y-%m-%d").strftime("%d-%b-%Y"),
            "Breakout Level Rs":  round(breakout_level,  2),
            "Signal Date":        co_ts.strftime("%d-%b-%Y"),
            "Days Since Signal":  days_since_bo,
            "Signal Close Rs":    round(first_co_close,  2),
            "Latest Close Rs":    round(float(latest["Close"]), 2),
            "Latest High Rs":     round(float(latest["High"]),  2),
            "Pct Vs Level":       f"+{pct_above}%",
            "Days Below Lvl":     days_below,
            "Hammer":             "-",
            "Avg Hrly Val (L)":   avg_val,   # ★ NEW
        }

    # ── SIGNAL 2: first retest + hammer ──────────────────────
    post_breakout  = after[after.index > first_co_date]
    retest_date    = None
    retest_close   = None
    retest_lower   = breakout_level * 0.999
    retest_ceiling = breakout_level * (1 + RETEST_BUFFER)

    for date, row in post_breakout.iterrows():
        o = float(row["Open"])
        h = float(row["High"])
        l = float(row["Low"])
        c = float(row["Close"])

        if retest_lower <= l <= retest_ceiling:
            if is_hammer(o, h, l, c):
                retest_date  = date
                retest_close = c
                break
            else:
                if PRINT_FAILURES:
                    print(
                        f"skipped: first retest on "
                        f"{pd.Timestamp(date).strftime('%d-%b-%Y')} "
                        f"is NOT a hammer (O={o:.2f} H={h:.2f} L={l:.2f} C={c:.2f})"
                    )
                return None

    if retest_date is None:
        # ── SIGNAL: Retracing to Level ────────────────────────
        latest       = df.iloc[-1]
        latest_close = float(latest["Close"])
        retrace_ceil = breakout_level * (1 + NEAR_LEVEL_PCT)
        if latest_close <= retrace_ceil:
            passes, avg_val = _liquidity_gate()
            if not passes:
                return None
            pct_from = round((latest_close - breakout_level) / breakout_level * 100, 2)
            sign     = "+" if pct_from >= 0 else ""
            return {
                "Signal":             "Retracing",
                "Symbol":             symbol,
                "Company":            company[:35],
                "Listed On":          datetime.strptime(listing_date, "%Y-%m-%d").strftime("%d-%b-%Y"),
                "Breakout Level Rs":  round(breakout_level, 2),
                "Signal Date":        today.strftime("%d-%b-%Y"),
                "Days Since Signal":  0,
                "Signal Close Rs":    round(latest_close, 2),
                "Latest Close Rs":    round(latest_close, 2),
                "Latest High Rs":     round(float(latest["High"]), 2),
                "Pct Vs Level":       f"{sign}{pct_from}%",
                "Days Below Lvl":     days_below,
                "Hammer":             "-",
                "Avg Hrly Val (L)":   avg_val,   # ★ NEW
            }
        if PRINT_FAILURES:
            print(f"skipped: broke out {days_since_bo}d ago but no retest yet")
        return None

    rt_ts      = pd.Timestamp(retest_date).normalize()
    days_since = (today - rt_ts).days

    if days_since > BREAKOUT_WINDOW_DAYS:
        if PRINT_FAILURES:
            print(f"skipped: retest+hammer {days_since}d ago (>{BREAKOUT_WINDOW_DAYS}d window)")
        return None

    passes, avg_val = _liquidity_gate()
    if not passes:
        return None

    latest   = df.iloc[-1]
    pct_from = round((retest_close - breakout_level) / breakout_level * 100, 2)
    sign     = "+" if pct_from >= 0 else ""

    return {
        "Signal":             "Retest+Hammer",
        "Symbol":             symbol,
        "Company":            company[:35],
        "Listed On":          datetime.strptime(listing_date, "%Y-%m-%d").strftime("%d-%b-%Y"),
        "Breakout Level Rs":  round(breakout_level, 2),
        "Signal Date":        rt_ts.strftime("%d-%b-%Y"),
        "Days Since Signal":  days_since,
        "Signal Close Rs":    round(retest_close,   2),
        "Latest Close Rs":    round(float(latest["Close"]), 2),
        "Latest High Rs":     round(float(latest["High"]),  2),
        "Pct Vs Level":       f"{sign}{pct_from}%",
        "Days Below Lvl":     days_below,
        "Hammer":             "YES",
        "Avg Hrly Val (L)":   avg_val,   # ★ NEW
    }


# ──────────────────────────────────────────────────────────────
#  STEP 5: NEWS SENTIMENT via Anthropic API + web search
# ──────────────────────────────────────────────────────────────

def fetch_news_sentiment(company: str, symbol: str) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return {"sentiment": "N/A", "headline": "Set ANTHROPIC_API_KEY env var to enable"}

    since_date = (datetime.today() - timedelta(days=NEWS_LOOKBACK_DAYS)).strftime("%d %b %Y")
    today_str  = datetime.today().strftime("%d %b %Y")

    prompt = f"""Search the web for recent news about the Indian company "{company}" 
(NSE symbol: {symbol}) published between {since_date} and {today_str}.

Focus on: earnings, orders, results, regulatory actions, management changes, 
legal issues, partnerships, expansion plans, or any market-moving news.

Respond ONLY with a valid JSON object — no markdown, no explanation, nothing else:
{{
  "sentiment": "<Positive|Negative|Mixed|Neutral>",
  "headline": "<one concise sentence summarising the most important news, or 'No significant news found' if nothing relevant>"
}}"""

    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 300,
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": [{"role": "user", "content": prompt}],
    }

    headers = {
        "Content-Type":      "application/json",
        "x-api-key":         api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta":    "web-search-2025-03-05",
    }

    try:
        resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        full_text = " ".join(
            block.get("text", "")
            for block in data.get("content", [])
            if block.get("type") == "text"
        ).strip()

        full_text = full_text.replace("```json", "").replace("```", "").strip()

        start = full_text.find("{")
        end   = full_text.rfind("}") + 1
        if start == -1 or end == 0:
            return {"sentiment": "N/A", "headline": f"Could not parse response: {full_text[:80]}"}

        parsed = json.loads(full_text[start:end])
        sentiment = str(parsed.get("sentiment", "Neutral")).strip()
        headline  = str(parsed.get("headline",  "No summary returned")).strip()

        sentiment_map = {
            "positive": "Positive",
            "negative": "Negative",
            "mixed":    "Mixed",
            "neutral":  "Neutral",
        }
        sentiment = sentiment_map.get(sentiment.lower(), sentiment)

        return {"sentiment": sentiment, "headline": headline}

    except requests.exceptions.HTTPError as e:
        return {"sentiment": "N/A", "headline": f"API HTTP error: {e}"}
    except json.JSONDecodeError as e:
        return {"sentiment": "N/A", "headline": f"JSON parse error: {e}"}
    except Exception as e:
        return {"sentiment": "N/A", "headline": f"Error: {e}"}


# ──────────────────────────────────────────────────────────────
#  STEP 6: MAIN SCANNER
# ──────────────────────────────────────────────────────────────

SENTIMENT_EMOJI = {
    "Positive": "🟢",
    "Negative": "🔴",
    "Mixed":    "🟡",
    "Neutral":  "⚪",
    "N/A":      "❓",
}

def run_scanner():
    print("=" * 65)
    print("   NSE MAINBOARD IPO BREAKOUT SCANNER")
    print(f"   Signals in last {BREAKOUT_WINDOW_DAYS} days  |  "
          f"{datetime.today().strftime('%d %b %Y  %I:%M %p')}")
    print(f"   1H Liquidity filter: avg hourly value ≥ {MIN_HOURLY_VALUE_LAKH} L"
          f"  (lookback {LIQUIDITY_LOOKBACK_DAYS}d)")
    print("=" * 65)

    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        print("\n  ⚠  ANTHROPIC_API_KEY not set — news sentiment will show as N/A.")
        print("     Set it with:  export ANTHROPIC_API_KEY=sk-ant-...\n")

    ipos_df = fetch_mainboard_ipos()
    if ipos_df.empty:
        print("\nERROR: Could not download EQUITY_L.csv from NSE archives.")
        sys.exit(1)

    # ── Phase 1: Price-based signal scan ─────────────────────
    # NOTE: check_stock() now also calls check_hourly_liquidity()
    # internally, so illiquid stocks are already filtered out.
    signals = []
    total   = len(ipos_df)
    print(f"Scanning {total} stocks for price signals (+ 1h liquidity check)...\n")

    for idx, row in enumerate(ipos_df.itertuples(), start=1):
        symbol       = row.symbol
        company      = row.companyName
        listing_date = row.listingDate

        print(f"   [{idx:>3}/{total}]  {symbol:<14}  {company[:28]:<28}", end="  ", flush=True)

        result = check_stock(symbol, company, listing_date)

        if result:
            signals.append(result)
            print(
                f"{result['Signal']:<14}  "
                f"{result['Signal Date']}  "
                f"Lvl {result['Breakout Level Rs']}  "
                f"Now {result['Latest Close Rs']}  "
                f"{result['Pct Vs Level']}  "
                f"1hVol {result['Avg Hrly Val (L)']}L"
            )
        else:
            print("-")

        time.sleep(REQUEST_DELAY)

    # ── Phase 2: News sentiment ───────────────────────────────
    if signals:
        print(f"\n{'─'*65}")
        print(f"  Fetching news sentiment for {len(signals)} signal stock(s)...")
        print(f"{'─'*65}\n")

        for sig in signals:
            company = sig["Company"]
            symbol  = sig["Symbol"]
            print(f"   📰  {symbol:<14}  {company[:35]:<35}", end="  ", flush=True)

            news = fetch_news_sentiment(company, symbol)
            sig["Sentiment"] = news["sentiment"]
            sig["News"]      = news["headline"]

            emoji = SENTIMENT_EMOJI.get(news["sentiment"], "❓")
            print(f"{emoji} {news['sentiment']:<10}  {news['headline'][:60]}")

            time.sleep(NEWS_DELAY)

    # ── Summary ───────────────────────────────────────────────
    first_bo  = [s for s in signals if s["Signal"] == "1st Breakout"]
    retests   = [s for s in signals if s["Signal"] == "Retest+Hammer"]
    near_bo   = [s for s in signals if s["Signal"] == "Near Breakout"]
    retracing = [s for s in signals if s["Signal"] == "Retracing"]

    print("\n" + "=" * 65)
    print(f"  TOTAL SIGNALS (last {BREAKOUT_WINDOW_DAYS} days): {len(signals)}"
          f"  [1h liq ≥ {MIN_HOURLY_VALUE_LAKH} L filtered]")
    print(f"    1st Breakouts   : {len(first_bo)}")
    print(f"    Retest + Hammer : {len(retests)}")
    print(f"    Near Breakout   : {len(near_bo)}")
    print(f"    Retracing       : {len(retracing)}")
    print("=" * 65)

    if not signals:
        print(f"\n  No signals in the last {BREAKOUT_WINDOW_DAYS} days.")
        print("  Tips:")
        print(f"    • Increase BREAKOUT_WINDOW_DAYS (currently {BREAKOUT_WINDOW_DAYS})")
        print(f"    • Increase RETEST_BUFFER (currently {int(RETEST_BUFFER*100)}%)")
        print(f"    • Decrease HAMMER_SHADOW_MULTIPLIER (currently {HAMMER_SHADOW_MULTIPLIER}×)")
        print(f"    • Increase NEAR_LEVEL_PCT (currently {int(NEAR_LEVEL_PCT*100)}%)")
        print(f"    • Decrease MIN_HOURLY_VALUE_LAKH (currently {MIN_HOURLY_VALUE_LAKH} L)")
        return

    result_df = pd.DataFrame(signals)

    if "Sentiment" not in result_df.columns:
        result_df["Sentiment"] = "N/A"
    if "News" not in result_df.columns:
        result_df["News"] = ""

    result_df = result_df.sort_values(
        ["Signal", "Days Since Signal"], ascending=[True, True]
    )
    result_df.index = range(1, len(result_df) + 1)

    pd.set_option("display.max_columns",   25)
    pd.set_option("display.max_rows",     200)
    pd.set_option("display.width",        240)
    pd.set_option("display.max_colwidth",  60)

    if first_bo:
        print(f"\n{'─'*65}")
        print(f"  [1] FIRST-TIME BREAKOUTS  ({len(first_bo)})")
        print(f"{'─'*65}")
        bo_df = result_df[result_df["Signal"] == "1st Breakout"].copy()
        print(f"\n{bo_df.to_string()}\n")

    if retests:
        print(f"\n{'─'*65}")
        print(f"  [2] RETEST + HAMMER  ({len(retests)})")
        print(f"      (first retest of listing high with hammer candle)")
        print(f"{'─'*65}")
        rt_df = result_df[result_df["Signal"] == "Retest+Hammer"].copy()
        print(f"\n{rt_df.to_string()}\n")

    if near_bo:
        print(f"\n{'─'*65}")
        print(f"  [3] NEAR BREAKOUT  ({len(near_bo)})")
        print(f"      (within {int(NEAR_LEVEL_PCT*100)}% below listing high — never broken out yet)")
        print(f"{'─'*65}")
        nb_df = result_df[result_df["Signal"] == "Near Breakout"].copy()
        print(f"\n{nb_df.to_string()}\n")

    if retracing:
        print(f"\n{'─'*65}")
        print(f"  [4] RETRACING TO LEVEL  ({len(retracing)})")
        print(f"      (within {int(NEAR_LEVEL_PCT*100)}% above listing high — pulling back after breakout)")
        print(f"{'─'*65}")
        re_df = result_df[result_df["Signal"] == "Retracing"].copy()
        print(f"\n{re_df.to_string()}\n")

    # ── Sentiment + liquidity quick-view ─────────────────────
    print(f"\n{'─'*65}")
    print("  NEWS SENTIMENT + LIQUIDITY SUMMARY")
    print(f"{'─'*65}")
    for _, row in result_df.iterrows():
        emoji = SENTIMENT_EMOJI.get(row.get("Sentiment", "N/A"), "❓")
        print(
            f"  {emoji}  {row['Symbol']:<12}  "
            f"{row.get('Sentiment','N/A'):<10}  "
            f"1hVol {row.get('Avg Hrly Val (L)', 0):.1f}L  "
            f"{str(row.get('News',''))[:60]}"
        )

    csv_file = f"ipo_signals_{datetime.today().strftime('%Y%m%d_%H%M')}.csv"
    result_df.to_csv(csv_file, index=False)
    print(f"\nSaved to: {csv_file}\n")


if __name__ == "__main__":
    run_scanner()
