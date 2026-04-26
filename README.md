# NSE Mainboard IPO Breakout Scanner

A sophisticated Python-based scanner that identifies trading opportunities in Indian IPO stocks listed on the NSE Mainboard. The scanner detects multiple breakout patterns and filters signals based on liquidity and sentiment analysis.

## 📋 Features

### Signal Detection Layers

The scanner identifies **6 different signal types** across multiple timeframes:

#### 1️⃣ **First Breakout (1st Breakout)**
- Stock crosses above its listing-day high for the **first time ever**
- Signal must occur within the last `BREAKOUT_WINDOW_DAYS` days
- Ideal entry point for trend-following strategies

#### 2️⃣ **Retest + Hammer**
- Stock already broke out above listing-day high earlier
- Pulls back to retest that level (**first retest**)
- The retest candle forms a **Hammer** pattern (strong reversal signal)
- Long lower wick, small body at top = buyer strength at support
- Excellent risk-reward setup for trend continuation

#### 3️⃣ **Near Breakout**
- Stock has **never** crossed above listing-day high yet
- Current price is within `NEAR_LEVEL_PCT` below the breakout level
- Early warning signal before potential breakout

#### 4️⃣ **Retracing to Level**
- Stock previously broke out above listing-day high
- Now pulling back towards that level for support
- Price is within `NEAR_LEVEL_PCT` above the listing high
- Early warning before potential retest + hammer pattern

#### 5️⃣ **1-Hour Liquidity Filter** ⭐ *NEW*
- **Every signal** must pass minimum hourly liquidity threshold
- Calculates average hourly traded value over `LIQUIDITY_LOOKBACK_DAYS` days
- Formula: `mean(Volume × Close) in ₹ Lakhs`
- Excludes illiquid stocks: minimum `MIN_HOURLY_VALUE_LAKH` (default: 100 L)
- Only bars with actual trades counted (zero-volume pre-market excluded)
- Shown in output as "Avg Hrly Val (L)"

#### 6️⃣ **News Sentiment Analysis** 📰
- Uses **Anthropic Claude API** with web search integration
- Searches for news published in the last `NEWS_LOOKBACK_DAYS` days
- Returns sentiment: `Positive | Negative | Mixed | Neutral`
- Provides one-line news summary

## 🚀 Quick Start

### Prerequisites

```bash
pip install yfinance pandas requests anthropic
```

### Installation

1. **Clone or download the repository:**
   ```bash
   git clone <repository-url>
   cd ipo_trading_strategy
   ```

2. **Set up Anthropic API key** (for news sentiment):
   ```bash
   # macOS / Linux:
   export ANTHROPIC_API_KEY=sk-ant-...
   
   # Windows:
   set ANTHROPIC_API_KEY=sk-ant-...
   ```

   Get your API key from: https://console.anthropic.com/

3. **Run the scanner:**
   ```bash
   python nse_ipo_breakout_scanner_v2.py
   ```

### Example Output

```
═════════════════════════════════════════════════════════════
   NSE MAINBOARD IPO BREAKOUT SCANNER
   Signals in last 15 days  |  26 Apr 2026  03:45 PM
   1H Liquidity filter: avg hourly value ≥ 100.0 L  (lookback 10d)
═════════════════════════════════════════════════════════════

Scanning 145 stocks for price signals (+ 1h liquidity check)...

     [1/145]  TATANX          Tata Nexfab Limited      -
     [2/145]  MAHILOG        Mahindra Logistics Ltd    1st Breakout      26-Apr-2026  Lvl 850.00  Now 875.50  +2.94%  1hVol 245.3L
     [3/145]  INDIAAPT       India Apartments        Retest+Hammer     20-Apr-2026  Lvl 620.00  Now 625.10  +0.82%  1hVol 156.8L
   ...

═════════════════════════════════════════════════════════════
  TOTAL SIGNALS (last 15 days): 3  [1h liq ≥ 100.0 L filtered]
    1st Breakouts   : 1
    Retest + Hammer : 1
    Near Breakout   : 1
    Retracing       : 0
═════════════════════════════════════════════════════════════

─────────────────────────────────────────────────────────────
  NEWS SENTIMENT + LIQUIDITY SUMMARY
─────────────────────────────────────────────────────────────
  🟢  MAHILOG       Positive    1hVol 245.3L  Strong FY26 earnings reported with 15% YoY growth
  🔴  INDIAAPT      Negative    1hVol 156.8L  Regulatory concerns raised by NSE compliance
```

## ⚙️ Configuration

Edit these parameters in the script to customize the scanner:

### Timing & Windows
```python
MONTHS_BACK          = 24    # Scan IPOs listed in last N months
BREAKOUT_WINDOW_DAYS = 15    # Signal must occur within last N days
NEWS_LOOKBACK_DAYS   = 10    # Search for news in last N days
LIQUIDITY_LOOKBACK_DAYS = 10 # Use last N days for 1h liquidity calc
```

### Breakout Detection
```python
MIN_DAYS_BELOW       = 1     # Stock must dip below listing high ≥ N days
BREAKOUT_BUFFER      = 0.0   # Require N% above listing high to confirm (0 = exact cross)
RETEST_BUFFER        = 0.03  # Retest zone ±N% around listing high
```

### Hammer Pattern Recognition
```python
HAMMER_SHADOW_MULTIPLIER = 2.0  # Lower wick must be ≥ 2× the candle body
HAMMER_MAX_UPPER_RATIO   = 0.5  # Upper wick ≤ 50% of body
HAMMER_MIN_BODY_PCT      = 0.05 # Body ≥ 5% of total candle range
```

### Proximity Signals
```python
NEAR_LEVEL_PCT       = 0.05  # Price within 5% = Near Breakout or Retracing
```

### Liquidity Filter
```python
MIN_HOURLY_VALUE_LAKH  = 100.0  # Minimum ₹ Lakhs per hour (1 L = ₹100,000)
LIQUIDITY_LOOKBACK_DAYS = 10    # Days of 1h data to average over
```

### API & Delays
```python
REQUEST_DELAY        = 1.0   # Pause (sec) between yfinance calls
NEWS_DELAY           = 2.0   # Pause (sec) between Anthropic API calls
ANTHROPIC_MODEL      = "claude-sonnet-4-20250514"  # API model version
PRINT_FAILURES       = False  # Set True to debug why stocks are skipped
```

## 📊 Data Sources

### Equity List
- **Source:** NSE Archives
- **File:** `EQUITY_L.csv` (public, no authentication required)
- **URL:** https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv
- **Update Frequency:** Daily
- **Filters Applied:**
  - Mainboard series: EQ, BE, BL, IL, IQ
  - Listed within last `MONTHS_BACK` months
  - Duplicates removed (prefers EQ series)

### Price History
- **Source:** yfinance (Yahoo Finance / NSE data)
- **Timeframes:** 
  - Daily candles: From listing date to today
  - Hourly candles: Last ~730 days (1h liquidity check)
- **Auto-adjust:** True (splits, dividends adjusted)

### News & Sentiment
- **API:** Anthropic Claude with web search
- **Search Scope:** Last `NEWS_LOOKBACK_DAYS` days
- **Requires:** `ANTHROPIC_API_KEY` environment variable

## 📁 Output

### Console Output
- Real-time scan progress with signal detection
- Organized by signal type (1st Breakout, Retest+Hammer, etc.)
- News sentiment with emoji indicators:
  - 🟢 Positive
  - 🔴 Negative
  - 🟡 Mixed
  - ⚪ Neutral
  - ❓ N/A (API key not set)

### CSV Export
- Filename: `ipo_signals_YYYYMMDD_HHMM.csv`
- Contains: All signal columns + sentiment + news headline
- Location: Current working directory
- Use in spreadsheet apps or further analysis

## 🔧 How It Works

### Phase 1: Download NSE Data
1. Fetches EQUITY_L.csv from NSE archives
2. Filters mainboard stocks listed in last 24 months
3. Returns symbol, company name, and listing date

### Phase 2: Price Signal Detection
1. Downloads daily price history from listing date to today
2. Identifies listing-day high as the breakout level
3. Detects first crossover with pump-and-dump filter
4. Checks for retest + hammer patterns
5. Flags near-breakout and retracing scenarios

### Phase 3: Liquidity Screening
1. Downloads 1-hour candles (last 10 days by default)
2. Calculates average hourly traded value (Volume × Close)
3. **Rejects** stocks below `MIN_HOURLY_VALUE_LAKH` threshold
4. Adds avg hourly value to signal output

### Phase 4: News Sentiment
1. For each signal stock, queries Anthropic API
2. API searches web for recent news about the company
3. Returns sentiment (Positive/Negative/Mixed/Neutral) + headline
4. Adds to final output table

### Phase 5: Results & Export
1. Displays organized tables by signal type
2. Shows news sentiment summary
3. Exports signals to CSV with timestamp

## 🛡️ Filters & Risk Controls

### Pump-and-Dump Detection
- If stock breaks above listing high, then falls below listing low later → **Rejected**
- Protects against short-lived spikes

### Hammer Validation
- Strict candle pattern rules prevent false signals
- Configurable shadow multiplier and body ratios

### Liquidity Requirements
- Forces signals to have sufficient trading activity
- Prevents illiquid penny stocks
- Minimum 5 valid 1h bars required

### Dip Requirement
- Stock must dip below listing high at least once
- Prevents pump signals that never pull back

## 📈 Use Cases

1. **Swing Trading:** Use 1st Breakout + Retest+Hammer for entry/reentry points
2. **Trend Following:** Monitor Retracing signals for dip-buying opportunities
3. **Anticipation Trading:** Use Near Breakout for early watchlist building
4. **Sentiment Correlation:** Combine news sentiment with technical patterns
5. **Liquidity Screening:** Filter for low-slippage trading

## ⚠️ Troubleshooting

### No Signals Found?
```
Tips:
  • Increase BREAKOUT_WINDOW_DAYS (currently 15)
  • Increase RETEST_BUFFER (currently 3%)
  • Decrease HAMMER_SHADOW_MULTIPLIER (currently 2.0×)
  • Increase NEAR_LEVEL_PCT (currently 5%)
  • Decrease MIN_HOURLY_VALUE_LAKH (currently 100 L)
```

### NSE CSV Download Failed
- Script retries with alternate URL
- Check internet connection
- NSE servers may be temporarily down

### API Key Not Working
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check quota limits at https://console.anthropic.com/
- News sentiment will show as "N/A" if not set

### Very Few Liquidity Passes
- Reduce `MIN_HOURLY_VALUE_LAKH` for less stringent filtering
- Most recent IPOs have lower trading volumes
- Check 1h data availability (may need `LIQUIDITY_LOOKBACK_DAYS ≤ 5`)

## 📚 Dependencies

- **yfinance** - Yahoo Finance data (NSE stocks)
- **pandas** - Data manipulation & analysis
- **requests** - HTTP requests for NSE CSV + API calls
- **anthropic** - Claude API for news sentiment
- **Python 3.8+** - Standard library (datetime, json, io, os, etc.)

## 📝 License

See `LICENSE` file in the repository.

## 🤝 Contributing

For bug reports, feature requests, or improvements:
1. Test your changes thoroughly
2. Document any new parameters or features
3. Update this README accordingly

## 📞 Support

For issues or questions:
- Check `PRINT_FAILURES = True` to debug specific stocks
- Verify all dependencies are installed
- Ensure NSE servers are accessible
- Confirm API keys are properly set

---

**Last Updated:** 26 April 2026

**Version:** 2.0 (with 1-hour liquidity filter & news sentiment)

**Author:** NSE Trading Strategy Team

Happy trading! 📊🚀
