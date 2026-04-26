# 📁 Project Structure & Files Overview

## Your IPO Trading Strategy Project

```
ipo_trading_strategy/
├── 📄 nse_ipo_breakout_scanner_v2.py    ← Main scanner script (CORE)
├── 📄 README.md                         ← Full documentation
├── 📄 LICENSE                           ← MIT/Apache license
├── 📄 TELEGRAM_SETUP.md                 ← Telegram setup guide
├── 📄 GITHUB_DEPLOYMENT.md              ← Free GitHub deployment guide
├── 📄 QUICK_GITHUB_DEPLOY.md            ← 5-minute quick start
├── 📄 requirements.txt                  ← Python dependencies
├── 📄 FILE_MANIFEST.txt                 ← This file
├── 📦 .github/
│   └── 📦 workflows/
│       └── 📄 ipo_scanner.yml           ← GitHub Actions workflow (automation)
└── 📄 .gitignore                        ← Git ignore rules (security)
```

---

## 📋 File Descriptions

### 🔧 Core Application

#### **nse_ipo_breakout_scanner_v2.py** (Main Script)
- **Size:** ~870 lines
- **Purpose:** Main IPO breakout scanner
- **Features:**
  - Downloads NSE equity list
  - Detects 6 signal types (1st breakout, retest+hammer, etc.)
  - Filters by 1-hour liquidity
  - Analyzes sentiment via Anthropic API
  - Sends results to Telegram
- **Run:** `python nse_ipo_breakout_scanner_v2.py`
- **Output:** CSV file + Telegram notification

### 📚 Documentation

#### **README.md** (Main Documentation)
- Comprehensive feature overview
- Installation instructions
- Configuration guide
- Example output
- Troubleshooting tips
- Dependencies list
- Use cases & strategies

#### **TELEGRAM_SETUP.md** (Telegram Configuration)
- How to get Telegram bot token (@BotFather)
- How to find your chat ID (@userinfobot)
- Environment variable setup (Mac/Linux/Windows)
- Security best practices
- Troubleshooting common issues

#### **GITHUB_DEPLOYMENT.md** (Complete Deployment Guide)
- 3 free deployment options (GitHub Actions recommended)
- Detailed GitHub setup steps
- GitHub Actions workflow explanation
- Secrets management (API keys)
- Scheduling cron expressions
- Monitoring & logging
- Artifacts storage
- Advanced configurations

#### **QUICK_GITHUB_DEPLOY.md** (Fast 5-Minute Setup)
- Step-by-step quick start
- Commands to copy-paste
- Common mistakes to avoid
- Verification checklist
- Quick troubleshooting

### ⚙️ Configuration Files

#### **requirements.txt** (Python Dependencies)
```
yfinance>=0.2.20
pandas>=1.5.0
requests>=2.28.0
anthropic>=0.7.0
```
- Install all dependencies: `pip install -r requirements.txt`

#### **.github/workflows/ipo_scanner.yml** (GitHub Actions Automation)
- **Trigger:** Daily at 9:00 AM IST (3:30 AM UTC)
- **Also:** Manual trigger via GitHub UI
- **Steps:**
  1. Checkout code
  2. Setup Python 3.10
  3. Install dependencies
  4. Run scanner with API credentials
  5. Upload CSV artifacts (30 days retention)
  6. Upload logs (7 days retention)
- **Timeout:** 30 minutes max

#### **.gitignore** (Security & Cleanliness)
- Excludes API keys (.env files)
- Excludes output CSV files
- Excludes Python cache (__pycache__)
- Excludes IDE files (.vscode, .idea)
- Excludes OS files (.DS_Store, Thumbs.db)
- Excludes virtual environments (venv, .venv)

#### **LICENSE** (MIT or Apache 2.0)
- Open source license
- Allows commercial use
- Requires attribution

---

## 🚀 How to Use Each File

### For Local Development:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export TELEGRAM_BOT_TOKEN="123456:ABC..."
export TELEGRAM_CHAT_ID="8328139169"

# 3. Run the scanner
python nse_ipo_breakout_scanner_v2.py

# 4. Check output
ls -la ipo_signals_*.csv
```

### For GitHub Deployment:
```bash
# 1. Initialize git
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/ipo_trading_strategy.git
git push -u origin main

# 3. Add secrets in GitHub UI
# Settings → Secrets → Add ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# 4. Workflow runs automatically or manually
# Go to Actions → Run workflow
```

---

## 📊 File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| nse_ipo_breakout_scanner_v2.py | 868 | Core application |
| README.md | 339 | Main documentation |
| GITHUB_DEPLOYMENT.md | 400+ | Deployment guide |
| QUICK_GITHUB_DEPLOY.md | 300+ | Quick start |
| TELEGRAM_SETUP.md | 280+ | Telegram setup |
| .github/workflows/ipo_scanner.yml | 45 | GitHub Actions |
| requirements.txt | 4 | Dependencies |
| .gitignore | 35 | Git ignore rules |
| **TOTAL** | **~2,300** | **Complete project** |

---

## 🔑 Key Configurations

### Scanner Parameters (in nse_ipo_breakout_scanner_v2.py)

```python
MONTHS_BACK          = 24      # Scan IPOs from last 24 months
BREAKOUT_WINDOW_DAYS = 15      # Signal must be within 15 days
MIN_HOURLY_VALUE_LAKH = 100.0  # Liquidity filter: ₹100 Lakhs/hour minimum
NEWS_LOOKBACK_DAYS = 10        # Search news from last 10 days
NEAR_LEVEL_PCT = 0.05          # 5% proximity threshold
HAMMER_SHADOW_MULTIPLIER = 2.0 # Hammer pattern validation
REQUEST_DELAY = 1.0            # Pause between API calls (seconds)
```

### Environment Variables (Required)

```bash
ANTHROPIC_API_KEY        # For news sentiment (from Console.anthropic.com)
TELEGRAM_BOT_TOKEN       # Telegram bot token (from @BotFather)
TELEGRAM_CHAT_ID         # Your Telegram chat ID (8328139169)
```

### GitHub Actions Schedule (Cron)

```
30 3 * * *  ← Current: 9:00 AM IST (3:30 AM UTC) daily
```

---

## 🎯 What Each Component Does

### Data Pipeline

```
1. NSE EQUITY LIST (CSV)
   ↓
2. DOWNLOAD & FILTER
   ↓
3. PRICE ANALYSIS (Daily candles)
   ↓
4. SIGNAL DETECTION (6 types)
   ↓
5. LIQUIDITY CHECK (1-hour candles)
   ↓
6. NEWS SENTIMENT (Anthropic API)
   ↓
7. RESULTS FORMATTING
   ↓
8. CSV EXPORT + TELEGRAM SEND
```

### Signal Types Detected

1. **1st Breakout** - First cross above listing high
2. **Retest + Hammer** - Retest with hammer candle pattern
3. **Near Breakout** - Within 5% below listing high
4. **Retracing** - Pulling back after breakout
5. **Liquidity Filter** - Only signals with >100L hourly volume
6. **News Sentiment** - Positive/Negative/Mixed/Neutral

---

## 📱 Output Formats

### Telegram Message
```
🚀 NSE IPO Breakout Signals Report

📅 Generated: 26 Apr 2026 09:00 AM

📊 Signal Summary:
  • Total Signals: 3
  • 1st Breakouts: 1
  • Retest + Hammer: 1
  • Near Breakout: 1
  • Retracing: 0

📎 CSV file attached below.
```

### CSV Columns
- Signal (type)
- Symbol (stock ticker)
- Company (name)
- Listed On (date)
- Breakout Level Rs
- Signal Date
- Days Since Signal
- Signal Close Rs
- Latest Close Rs
- Latest High Rs
- Pct Vs Level
- Days Below Lvl
- Hammer (YES/NO)
- Avg Hrly Val (L)
- Sentiment
- News

### GitHub Artifacts
- `ipo_signals_YYYYMMDD_HHMM.csv` (30-day retention)
- `nohup.out` logs (7-day retention)

---

## 🔒 Security Checklist

- ✅ API keys in environment variables only
- ✅ .gitignore prevents .env file commits
- ✅ GitHub Secrets for encrypted storage
- ✅ No hardcoded credentials in code
- ✅ Telegram bot token protected
- ✅ Chat ID kept private
- ✅ CSV outputs don't contain secrets

---

## 📈 Deployment Options

### Option 1: GitHub Actions (RECOMMENDED - FREE)
- Auto-runs daily
- Free 2,000 min/month
- Notifications via Telegram
- Artifacts storage
- **Status:** ✅ Ready

### Option 2: Local Machine
- Manual execution
- Full control
- No ongoing costs
- **Status:** ✅ Ready

### Option 3: Cron Job (Linux/Mac)
- Schedule via crontab
- Runs on your machine
- Full logs available
- **Status:** ✅ Can be setup

### Option 4: Cloud Providers (Optional)
- Replit, PythonAnywhere, Railway
- $0-5/month alternatives
- **Status:** ✅ Alternative

---

## 🆘 Quick Troubleshooting

### "ModuleNotFoundError: No module named 'yfinance'"
```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Telegram bot not sending"
1. Check token format (should have `:`)
2. Verify chat ID (use @userinfobot)
3. Check bot is active (@BotFather)

### "Workflow not running at scheduled time"
1. GitHub Actions might be disabled
2. Settings → Actions → Enable workflows
3. Adjust cron time for your timezone

### "No signals found"
1. Increase BREAKOUT_WINDOW_DAYS
2. Decrease MIN_HOURLY_VALUE_LAKH
3. Increase NEAR_LEVEL_PCT
4. Adjust other parameters in config

---

## 📞 Support Resources

### Documentation Files
- README.md - Full feature documentation
- TELEGRAM_SETUP.md - Telegram configuration
- GITHUB_DEPLOYMENT.md - Deployment details
- QUICK_GITHUB_DEPLOY.md - Fast setup

### External Resources
- GitHub Actions: https://docs.github.com/actions
- Telegram Bot: https://core.telegram.org/bots
- Cron Expressions: https://crontab.guru
- yfinance: https://github.com/ranaroussi/yfinance

### Your Phone Contact
- Telegram: +91 8328139169 (for receiving signals)

---

## 🎉 Next Steps

1. **Local Testing:**
   - [ ] Install dependencies: `pip install -r requirements.txt`
   - [ ] Set environment variables
   - [ ] Run locally: `python nse_ipo_breakout_scanner_v2.py`
   - [ ] Verify Telegram message received

2. **GitHub Deployment:**
   - [ ] Follow QUICK_GITHUB_DEPLOY.md (5 minutes)
   - [ ] Push code to GitHub
   - [ ] Add 3 secrets
   - [ ] Test workflow manually
   - [ ] Verify scheduled runs

3. **Optimization:**
   - [ ] Tune parameters for your needs
   - [ ] Adjust schedule if needed
   - [ ] Set up additional notifications
   - [ ] Monitor costs (should be $0)

---

**Version:** 2.0 (with Telegram & GitHub Actions)
**Last Updated:** 26 April 2026
**Status:** ✅ Production Ready

