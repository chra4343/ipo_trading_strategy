# 🏗️ IPO Scanner Architecture & Deployment Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          NSE IPO BREAKOUT SCANNER                           │
│                              Version 2.0                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                        ┌──────────────────────────┐
                        │   DATA SOURCES (FREE)    │
                        └──────────────────────────┘
                               ↓
                ┌──────────────────────────────────┐
                │  NSE EQUITY_L.csv (Historical)   │
                │  yfinance (Daily + 1H candles)   │
                │  Web Search (News via Anthropic) │
                └──────────────────────────────────┘
                               ↓
                        ╔══════════════╗
                        ║   SCANNER    ║  nse_ipo_breakout_scanner_v2.py
                        ╚══════════════╝
                               ↓
        ┌──────────────────────┼──────────────────────┐
        ↓                      ↓                      ↓
    ┌────────────┐     ┌────────────┐     ┌──────────────────┐
    │  PRICE     │     │  LIQUIDITY │     │  SENTIMENT       │
    │  SIGNALS   │     │  FILTER    │     │  ANALYSIS        │
    │            │     │            │     │                  │
    │ • 1st BO   │     │ • 1h Avg   │     │ • Positive 🟢    │
    │ • Retest   │     │   Volume   │     │ • Negative 🔴    │
    │ • Near BO  │     │ • Min: 100L│     │ • Mixed 🟡       │
    │ • Retrace  │     │   Lakhs    │     │ • Neutral ⚪      │
    └────────────┘     └────────────┘     └──────────────────┘
        ↓                      ↓                      ↓
        └──────────────────────┼──────────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │  SIGNAL COLLECTION   │
                    │  + Formatting        │
                    └──────────────────────┘
                               ↓
                ┌──────────────────────────────────┐
                │  CSV REPORT GENERATION           │
                │  ipo_signals_YYYYMMDD_HHMM.csv   │
                └──────────────────────────────────┘
                               ↓
        ┌──────────────────────┴──────────────────────┐
        ↓                                             ↓
   ┌──────────┐                            ┌──────────────────┐
   │  CONSOLE │                            │   TELEGRAM BOT   │
   │  OUTPUT  │                            │  API (Sending)   │
   │          │                            │                  │
   │ • Tables │                            │ • Summary Msg    │
   │ • Stats  │                            │ • CSV Attached   │
   │ • Links  │                            │ • To: 8328139169 │
   └──────────┘                            └──────────────────┘
        ↓                                             ↓
   ┌──────────┐                            ┌──────────────────┐
   │  LOCAL   │                            │  YOUR TELEGRAM   │
   │  TERMINAL│                            │  PHONE/APP       │
   └──────────┘                            └──────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                    GITHUB DEPLOYMENT PIPELINE

┌─────────────────────────────────────────────────────────────────────────────┐
│                          GITHUB ACTIONS WORKFLOW                            │
│                     (.github/workflows/ipo_scanner.yml)                     │
└─────────────────────────────────────────────────────────────────────────────┘

SCHEDULE: Daily at 9:00 AM IST (3:30 AM UTC)  OR  Manual Trigger
                         ↓

        ┌────────────────────────────────────┐
        │   1. CHECKOUT CODE                 │
        │   (from GitHub repository)         │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   2. SETUP PYTHON 3.10             │
        │   (Ubuntu Linux container)         │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   3. INSTALL DEPENDENCIES          │
        │   • yfinance                       │
        │   • pandas                         │
        │   • requests                       │
        │   • anthropic                      │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   4. LOAD SECRETS                  │
        │   (Encrypted GitHub Secrets)       │
        │   • ANTHROPIC_API_KEY              │
        │   • TELEGRAM_BOT_TOKEN             │
        │   • TELEGRAM_CHAT_ID               │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   5. RUN SCANNER                   │
        │   (Execute Python script)          │
        │   Timeout: 30 minutes max          │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   6. UPLOAD ARTIFACTS              │
        │   • CSV file (30d retention)       │
        │   • Logs (7d retention)            │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   7. SEND TELEGRAM                 │
        │   (Automatic from scanner step)    │
        │   → Your Phone                     │
        └────────────────────────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │   8. WORKFLOW COMPLETE             │
        │   ✅ All steps successful          │
        │   📧 Email notification on failure │
        └────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                    DATA FLOW & SIGNAL DETECTION

PHASE 1: DATA COLLECTION
┌──────────────────────┐
│ Download NSE List    │─────→ Filter: Mainboard only
│ (EQUITY_L.csv)       │       Filter: Last 24 months
└──────────────────────┘

PHASE 2: PRICE ANALYSIS
┌──────────────────────┐
│ Download Daily       │─────→ Identify listing day high
│ Candles (yfinance)   │       Detect: Breakouts
└──────────────────────┘       Detect: Retests
                                Detect: Near-breakouts
                                Detect: Retracements

PHASE 3: LIQUIDITY CHECK
┌──────────────────────┐
│ Download 1-Hour      │─────→ Calculate avg volume × price
│ Candles (yfinance)   │       Filter: Min 100L per hour
└──────────────────────┘       Add liquidity metric to signal

PHASE 4: HAMMER DETECTION
┌──────────────────────┐
│ Retest Candles       │─────→ Measure lower shadow
│ Analysis             │       Measure body
└──────────────────────┘       Measure upper shadow
                                Validate: Hammer pattern?

PHASE 5: SENTIMENT ANALYSIS
┌──────────────────────┐
│ Anthropic API        │─────→ Search web for news
│ + Web Search         │       Classify sentiment
└──────────────────────┘       Extract headline

PHASE 6: CONSOLIDATION
┌──────────────────────┐
│ Combine All Data     │─────→ Format results
│ Create DataFrame     │       Sort by signal type
└──────────────────────┘       Export to CSV
                                Send to Telegram


═══════════════════════════════════════════════════════════════════════════════

                    SIGNAL DETECTION LOGIC

STOCK PROCESSING FLOW:

Entry: Stock Symbol
   ↓
1. Fetch price history from listing date
   ↓
2. Pump-and-dump filter
   If (broke above listing high) AND (later fell below listing low)
   → REJECT
   ↓
3. Did stock ever break above listing high?
   ├─ NO → Check if near breakout
   │       └─→ Send "NEAR BREAKOUT" signal
   │
   └─ YES → Did breakout occur recently (≤15 days)?
            ├─ YES → Send "1ST BREAKOUT" signal
            │
            └─ NO → Did stock retest level?
                   ├─ YES → Is retest candle a hammer?
                   │        ├─ YES → Send "RETEST+HAMMER" signal
                   │        └─ NO  → REJECT
                   │
                   └─ NO → Is stock retracing towards level?
                           ├─ YES → Send "RETRACING" signal
                           └─ NO  → REJECT
   ↓
4. For each signal: Check liquidity
   If (avg 1h volume × price < 100L)
   → REJECT (filter illiquid stocks)
   ↓
5. For each signal: Get sentiment
   Call Anthropic API
   Search web for news
   Return: Positive/Negative/Mixed/Neutral
   ↓
6. Export to CSV & Telegram
   ↓
Exit: Signal recorded or rejected


═══════════════════════════════════════════════════════════════════════════════

                    DEPLOYMENT ARCHITECTURE

LOCAL DEVELOPMENT:
┌─────────────────────┐
│  Your Computer      │
│  ─────────────────  │
│  • Python 3.8+      │
│  • Dependencies     │
│  • API Keys (env)   │
│  • Run manually     │
│  • See output live  │
│  • Download CSV     │
│  • Telegram alerts  │
└─────────────────────┘


GITHUB DEPLOYMENT (RECOMMENDED):
┌─────────────────────────────────────────────┐
│  GitHub Repository                          │
│  • Code version control                     │
│  • Secrets storage (encrypted)              │
│  • GitHub Actions (automation)              │
└─────────────────────────────────────────────┘
           ↓
    ┌────────────────┐
    │  GitHub Actions│
    │  ─────────────│
    │  • Ubuntu VM  │
    │  • Auto-runs  │
    │  • Scheduled  │
    │  • Logs saved │
    │  • Artifacts  │
    └────────────────┘
           ↓
    ┌────────────────┐
    │  1st Run       │
    │  Manual        │
    │  Trigger       │
    └────────────────┘
           ↓
    ┌────────────────┐
    │  Daily Runs    │
    │  At 9:00 AM    │
    │  IST           │
    └────────────────┘
           ↓
    ┌────────────────┐
    │  Results       │
    │  • CSV saved   │
    │  • Telegram    │
    │  • Artifacts   │
    └────────────────┘


COST ANALYSIS:
┌────────────────────────────────────────────────────────────┐
│  Component              │  Cost      │  Limit             │
├────────────────────────┼────────────┼──────────────────────┤
│  GitHub Repository     │  $0/month  │  Unlimited storage  │
│  GitHub Actions        │  $0/month  │  2,000 min/month    │
│  Anthropic API (News)  │  ~$0.05    │  Per call           │
│  Telegram Bot          │  $0/month  │  Unlimited          │
│  NSE Data (yfinance)   │  $0/month  │  Free tier          │
│  ─────────────────────────────────────────────────────────│
│  TOTAL                 │  ~$0/month │  ESSENTIALLY FREE!  │
└────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                    SECURITY & SECRETS MANAGEMENT

API KEYS FLOW:

┌─────────────────────────┐
│  User's Device          │
│  .env file (LOCAL ONLY) │  ← Secrets stored here
│  NOT committed to Git   │
└─────────────────────────┘
           ↓
      (During local run)
           ↓
┌─────────────────────────┐
│  Environment Variables  │
│  ANTHROPIC_API_KEY      │
│  TELEGRAM_BOT_TOKEN     │
│  TELEGRAM_CHAT_ID       │
└─────────────────────────┘
           ↓
      (Used by Python script)
           ↓
┌─────────────────────────┐
│  API Calls              │
│  • Anthropic            │
│  • Telegram             │
│  • yfinance             │
└─────────────────────────┘


GITHUB DEPLOYMENT:

┌──────────────────────────────┐
│  GitHub Settings → Secrets   │
│  (Encrypted storage)         │
│  ─────────────────────────── │
│  ANTHROPIC_API_KEY = ****    │
│  TELEGRAM_BOT_TOKEN = ****   │
│  TELEGRAM_CHAT_ID = ****     │
└──────────────────────────────┘
           ↓
    (During Actions run)
           ↓
┌──────────────────────────────┐
│  Injected as Environment     │
│  Variables in Secure Context │
│  ────────────────────────────│
│  • NOT in logs              │
│  • NOT in code              │
│  • Only in memory           │
│  • Encrypted in storage     │
└──────────────────────────────┘
           ↓
    (Used by Python script)
           ↓
┌──────────────────────────────┐
│  API Calls to External APIs  │
│  • No secrets stored         │
│  • No secrets logged         │
│  • Fully secure             │
└──────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                    QUICK REFERENCE: SETUP PATHS

PATH 1: LOCAL DEVELOPMENT (Quick Test)
┌─────────────────────────────────────────┐
│ Step 1: pip install -r requirements.txt │
│ Step 2: export ANTHROPIC_API_KEY=...    │
│ Step 3: export TELEGRAM_BOT_TOKEN=...   │
│ Step 4: export TELEGRAM_CHAT_ID=...     │
│ Step 5: python nse_ipo_breakout_scanner │
│ ↓                                        │
│ Result: CSV + Telegram on your phone    │
│ Time: 5 min setup, 10 min run           │
│ Cost: ~$0                                │
│ Maintenance: Manual each time           │
└─────────────────────────────────────────┘


PATH 2: GITHUB AUTOMATION (Recommended)
┌──────────────────────────────────────────────┐
│ Step 1: git init + add + commit              │
│ Step 2: Create GitHub repo                   │
│ Step 3: git push to GitHub                   │
│ Step 4: Add 3 secrets in GitHub Settings     │
│ Step 5: Test manually                        │
│ ↓                                             │
│ Result: Daily 9:00 AM runs, CSV + Telegram   │
│ Time: 5 min setup, then automatic forever    │
│ Cost: ~$0/month (FREE!)                      │
│ Maintenance: <5 min/month                    │
└──────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

                    FILE DEPENDENCIES

RUNTIME DEPENDENCIES:
┌─────────────────────────────────────────┐
│ nse_ipo_breakout_scanner_v2.py          │
│ ├─ pandas         (data processing)     │
│ ├─ yfinance       (stock data)          │
│ ├─ requests       (API calls)           │
│ ├─ anthropic      (sentiment analysis)  │
│ ├─ datetime       (timestamps)          │
│ ├─ json           (parsing)             │
│ └─ os, sys, io    (I/O operations)      │
└─────────────────────────────────────────┘

INPUT FILES:
├─ EQUITY_L.csv (downloaded from NSE)
├─ Environment variables (API keys)
└─ (None required locally)

OUTPUT FILES:
├─ ipo_signals_YYYYMMDD_HHMM.csv
└─ Telegram message (remote)

CONFIGURATION FILES:
├─ .env (local, not in git)
├─ .github/workflows/ipo_scanner.yml (GitHub)
└─ requirements.txt (dependencies)


═══════════════════════════════════════════════════════════════════════════════

                    TROUBLESHOOTING FLOWCHART

Is the scanner working?
│
├─ NO → Check Python installation
│       └─ python --version should show 3.8+
│
├─ Dependencies not found?
│       └─ Run: pip install -r requirements.txt
│
├─ API key errors?
│       ├─ Anthropic → Check API key valid at console.anthropic.com
│       ├─ Telegram → Check token format has ':'
│       └─ Chat ID → Use @userinfobot to verify
│
├─ No signals found?
│       ├─ Increase BREAKOUT_WINDOW_DAYS
│       ├─ Decrease MIN_HOURLY_VALUE_LAKH
│       └─ Adjust NEAR_LEVEL_PCT
│
├─ NSE CSV download fails?
│       └─ NSE servers down or blocked
│           Try later or use alternative data
│
├─ GitHub Actions not running?
│       ├─ Check Settings → Actions → Enable
│       ├─ Verify secrets added correctly
│       └─ Try manual trigger first
│
└─ SUCCESS ✅
    Results in CSV + Telegram!


═══════════════════════════════════════════════════════════════════════════════

                    MONITORING & MAINTENANCE

DAILY:
  □ Check Telegram for signal alerts
  □ Review signal quality (optional)

WEEKLY:
  □ Check GitHub Actions logs (optional)
  □ Verify no errors in logs

MONTHLY:
  □ Review parameter performance
  □ Archive old signals if needed
  □ Check API quotas

QUARTERLY:
  □ Update dependencies
  □ Rotate API keys (security best practice)
  □ Review and adjust parameters

YEARLY:
  □ Major update review
  □ Cost analysis
  □ Strategy refinement


═══════════════════════════════════════════════════════════════════════════════

                    SUCCESS INDICATORS

✅ Everything Working When:

Local Run:
  ✓ Python runs without errors
  ✓ CSV file generated
  ✓ Telegram message received
  ✓ Signals displayed in console

GitHub Actions:
  ✓ Workflow shows "✅ All checks passed"
  ✓ Artifacts available for download
  ✓ Telegram message received daily
  ✓ Logs don't show errors

Trading Results (After 1 Month):
  ✓ Most signals are accurate
  ✓ Positive sentiment signals perform better
  ✓ Liquidity filter prevents bad trades
  ✓ You're tracking win rate


═══════════════════════════════════════════════════════════════════════════════

                    NEXT STEPS

RECOMMENDED SEQUENCE:

Week 1:
  1. Get API keys (30 min)
  2. Run locally (30 min)
  3. Verify output (10 min)

Week 2:
  1. Deploy to GitHub (30 min)
  2. Add secrets (10 min)
  3. Test workflow (30 min)

Week 3-4:
  1. Monitor signals daily
  2. Paper trade (no real money)
  3. Adjust parameters if needed

Month 2+:
  1. Live trade (start small)
  2. Track win/loss rate
  3. Optimize strategy


═══════════════════════════════════════════════════════════════════════════════

                    QUICK COMMAND REFERENCE

Local:
  pip install -r requirements.txt
  export ANTHROPIC_API_KEY=sk-ant-...
  export TELEGRAM_BOT_TOKEN=...
  export TELEGRAM_CHAT_ID=...
  python nse_ipo_breakout_scanner_v2.py

GitHub:
  git init
  git add .
  git commit -m "Initial"
  git remote add origin https://github.com/USER/REPO.git
  git push -u origin main

Check:
  echo $ANTHROPIC_API_KEY
  echo $TELEGRAM_BOT_TOKEN
  echo $TELEGRAM_CHAT_ID
  git status
  git log

═══════════════════════════════════════════════════════════════════════════════

For detailed information, see:
  • README.md - Features & configuration
  • QUICK_GITHUB_DEPLOY.md - 5-minute setup
  • GITHUB_DEPLOYMENT.md - Complete deployment guide
  • TELEGRAM_SETUP.md - Telegram configuration
  • SETUP_SUMMARY.md - Complete overview

═══════════════════════════════════════════════════════════════════════════════

Status: ✅ PRODUCTION READY
Cost: 🆓 COMPLETELY FREE
Support: 📚 Full documentation included

Happy deploying! 🚀

