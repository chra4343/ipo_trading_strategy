# 📊 Telegram Integration - Installation & Usage Guide

## 🎯 Overview

Your IPO Trading Scanner now supports **automatic Telegram report delivery**. After each scan completes, the CSV file with all signals is automatically sent to your Telegram account.

---

## 🚀 Quick Start (5 Minutes)

### Option A: Interactive Setup (Recommended)

```bash
# Navigate to project directory
cd ipo_trading_strategy

# Run setup wizard (guides you through everything)
python setup.py

# Follow prompts to:
# 1. Get Telegram Bot Token (@BotFather)
# 2. Get Telegram Chat ID (@userinfobot)
# 3. Install dependencies
# 4. Save configuration

# Then run:
python nse_ipo_breakout_scanner_v2.py
```

### Option B: Manual Setup

**Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
# Or manually:
pip install yfinance pandas requests anthropic
```

**Step 2: Get Telegram Bot Token**
- Open Telegram
- Search for **@BotFather**
- Type `/newbot`
- Follow prompts
- Copy token (format: `123456789:ABCDefgh...`)

**Step 3: Get Telegram Chat ID**
- Open Telegram
- Search for **@userinfobot**
- Chat with it (it replies automatically with your ID)

**Step 4: Set Environment Variables**

**macOS/Linux:**
```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCDefgh..."
export TELEGRAM_CHAT_ID="987654321"

# Make it permanent: Add above lines to ~/.zshrc or ~/.bashrc
# Then: source ~/.zshrc
```

**Windows (Command Prompt):**
```cmd
set TELEGRAM_BOT_TOKEN=123456789:ABCDefgh...
set TELEGRAM_CHAT_ID=987654321
```

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="123456789:ABCDefgh..."
$env:TELEGRAM_CHAT_ID="987654321"
```

**Step 5: Run Scanner**
```bash
python nse_ipo_breakout_scanner_v2.py
```

---

## ✨ What Happens

### Before (Without Telegram)
1. Scanner runs
2. CSV saved locally: `ipo_signals_YYYYMMDD_HHMM.csv`
3. You manually check the file

### After (With Telegram) ⭐ NEW
1. Scanner runs
2. CSV saved locally (same as before)
3. **Automatically sends to Telegram:**
   - Summary message with signal count
   - CSV file as attachment
   - Confirmation: ✅ "Report sent to Telegram successfully!"

---

## 📩 Sample Telegram Messages

### Message 1: Summary
```
🚀 NSE IPO Breakout Signals Report

📅 Generated: 26 Apr 2026 03:45 PM

📊 Signal Summary:
  • Total Signals: 3
  • 1st Breakouts: 1
  • Retest + Hammer: 1
  • Near Breakout: 1
  • Retracing: 0

📎 CSV file attached below.
```

### Message 2: CSV File
```
[Document: ipo_signals_20260426_1545.csv]
📊 IPO Signals Report
26 Apr 2026
```

---

## 📁 File Structure

```
ipo_trading_strategy/
├── README.md                          # Main documentation
├── TELEGRAM_SETUP.md                  # Detailed Telegram guide
├── FEATURE_SUMMARY.md                 # Feature overview
├── INSTALLATION_GUIDE.md              # This file
├── requirements.txt                   # Python dependencies
├── setup.py                           # Setup wizard ⭐ NEW
├── nse_ipo_breakout_scanner_v2.py    # Main scanner (modified)
├── LICENSE                            # License file
│
├── Output Files (created when run):
├── ipo_signals_YYYYMMDD_HHMM.csv     # Signal report
└── .env                               # Environment vars (created by setup.py)
```

---

## 🔧 Configuration

### Enable/Disable Telegram
In `nse_ipo_breakout_scanner_v2.py`, line ~112:
```python
TELEGRAM_SEND_REPORT = True   # Enable (default)
TELEGRAM_SEND_REPORT = False  # Disable to skip Telegram
```

### Adjust Other Parameters
```python
# Same as before - all other configs work as usual
BREAKOUT_WINDOW_DAYS = 15
MIN_HOURLY_VALUE_LAKH = 100.0
# ... etc
```

---

## ✅ Verification

### Check Environment Variables
```bash
# macOS/Linux:
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Windows (CMD):
echo %TELEGRAM_BOT_TOKEN%
echo %TELEGRAM_CHAT_ID%
```

Both should show your actual values (not blank).

### Test Telegram Connection
```bash
# Before running scanner
python -c "
import requests
import os

token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')

if token and chat_id:
    url = f'https://api.telegram.org/bot{token}/getMe'
    r = requests.get(url)
    if r.status_code == 200:
        print('✅ Telegram bot connection OK')
    else:
        print('❌ Invalid bot token')
else:
    print('❌ Environment variables not set')
"
```

---

## 🐛 Troubleshooting

### "Telegram: BOT_TOKEN or CHAT_ID not set" (Warning)
- **Cause**: Environment variables not set
- **Fix**: Run `python setup.py` or set variables manually
- **Impact**: Scanner runs normally, just won't send to Telegram

### "Telegram message failed: 401"
- **Cause**: Invalid bot token
- **Fix**: Get new token from @BotFather
- **Verify**: Token format is `123456789:ABCDefgh...` with colon

### "Telegram request error: Connection timeout"
- **Cause**: Internet connection issue
- **Fix**: Check internet, try again
- **Note**: Scanner still completes successfully

### "Telegram file upload failed: 413"
- **Cause**: File too large (unlikely)
- **Fix**: Reduce number of stocks scanned or rows

### Still Getting Errors?
1. Check TELEGRAM_SETUP.md for detailed troubleshooting
2. Verify token starts with numbers, contains colon
3. Verify chat ID is numeric
4. Try running from fresh terminal
5. Check Telegram bot exists (search by username)

---

## 🔒 Security & Privacy

✅ **Safe:**
- Bot token stored in environment variables (not in code)
- Chat ID stored in environment variables (not in code)
- CSV sent over HTTPS encrypted connection
- Code is open-source, you can audit it

⚠️ **Important:**
- Don't share your bot token publicly
- Don't commit `.env` file to version control
- Use `.gitignore` to exclude `.env`: add `*.env` to `.gitignore`

---

## 📚 Additional Resources

- **README.md** - Full feature documentation
- **TELEGRAM_SETUP.md** - Complete Telegram setup guide
- **FEATURE_SUMMARY.md** - Feature overview & code changes
- **requirements.txt** - Python package versions
- **setup.py** - Interactive setup wizard

---

## 🎓 Example Workflows

### Workflow 1: Daily Automated Scan

**macOS/Linux (using cron):**
```bash
# Edit cron: crontab -e

# Add this line to run daily at 9:15 AM:
15 9 * * * cd /path/to/ipo_trading_strategy && source .env && python nse_ipo_breakout_scanner_v2.py >> scan.log 2>&1
```

**Windows (using Task Scheduler):**
1. Press `Win + R` → `taskschd.msc`
2. Create Basic Task
3. Set Trigger: Daily at 9:15 AM
4. Set Action: Run program
5. Program: `python` or full path to python.exe
6. Arguments: `nse_ipo_breakout_scanner_v2.py`
7. Start in: Project directory

### Workflow 2: Send to Multiple Groups
Edit `send_to_telegram()` function to support multiple chat IDs:
```python
TELEGRAM_CHAT_IDS = ["ID1", "ID2", "ID3"]  # Multiple chats
for chat_id in TELEGRAM_CHAT_IDS:
    # Send to each
```

### Workflow 3: Advanced Notifications
Extend the summary message with:
- Sentiment breakdown
- Top performing signals
- Risk analysis
- Custom filters

---

## ❓ Common Questions

**Q: Can I send to a group instead of personal chat?**
A: Yes! Add bot to group, get group Chat ID (negative number), use that.

**Q: Will it work if Telegram API is down?**
A: Yes, scanner completes normally. Telegram send is non-blocking (no failure = no error).

**Q: How often can I run this?**
A: As often as you want. Just wait 1+ second between requests to avoid rate limiting.

**Q: Can I customize the message?**
A: Yes, modify `send_to_telegram()` function to customize the summary message.

**Q: What data is sent to Telegram?**
A: Only the CSV file + summary message. No other data is sent.

**Q: Is there a cost?**
A: No! Telegram Bot API is free. You only pay if you create premium features.

---

## 📊 Next Steps

1. ✅ Run setup: `python setup.py`
2. ✅ Configure Telegram following prompts
3. ✅ Run scanner: `python nse_ipo_breakout_scanner_v2.py`
4. ✅ Check Telegram for report
5. ✅ Enjoy automated reports! 🎉

---

**Happy Trading! 📈**

For more help:
- See **TELEGRAM_SETUP.md** for detailed step-by-step instructions
- See **README.md** for feature documentation
- See **setup.py** for interactive configuration
