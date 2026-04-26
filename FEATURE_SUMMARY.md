# Telegram Integration - Feature Summary

## ✨ What's New

Your NSE IPO Breakout Scanner now includes **automatic Telegram report delivery**! After each scan completes, the CSV report is automatically sent to your Telegram account.

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Telegram Bot Token
- Open Telegram → Search **@BotFather**
- Type `/newbot` and follow prompts
- Copy the token (format: `123456789:ABCDefgh...`)

### Step 2: Get Your Chat ID
- Open Telegram → Search **@userinfobot**
- It will show your Chat ID immediately

### Step 3: Set Environment Variables
```bash
# macOS/Linux:
export TELEGRAM_BOT_TOKEN=your_token_here
export TELEGRAM_CHAT_ID=your_chat_id_here

# Windows (CMD):
set TELEGRAM_BOT_TOKEN=your_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here

# Or run the setup wizard:
python setup.py
```

## 📊 What You'll Receive

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
- Complete data export
- All signal details
- News sentiment analysis
- Hourly liquidity metrics
- Ready for analysis/trading

## 🔧 Code Changes

### 1. New Configuration Section
```python
# Line ~107-112 in nse_ipo_breakout_scanner_v2.py
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
TELEGRAM_SEND_REPORT = True  # Set False to disable
```

### 2. New Function: `send_to_telegram()`
```python
# Line ~630-698
def send_to_telegram(csv_file: str, signal_summary: dict) -> bool:
    """Send CSV report to Telegram via bot."""
    # Sends both summary message and CSV file
    # Returns True if successful
```

### 3. Call in Main Function
```python
# Line ~856-864 (end of run_scanner)
if signals:
    signal_summary = {...}
    send_to_telegram(csv_file, signal_summary)
```

## 📁 New Files

1. **setup.py** - Interactive setup wizard
   - Checks Python version
   - Installs dependencies
   - Guides through API key configuration
   - Creates `.env` file

2. **TELEGRAM_SETUP.md** - Detailed setup guide
   - Step-by-step instructions
   - Multiple platform support (Windows/Mac/Linux)
   - Troubleshooting tips
   - Security notes

3. **FEATURE_SUMMARY.md** - This file

## 🔒 Security

- Bot token stored as environment variable (not in code)
- Chat ID stored as environment variable (not in code)
- CSV file sent via HTTPS to Telegram API
- No data saved to disk after sending

## 💡 Usage Examples

### Enable/Disable Telegram
```python
# In nse_ipo_breakout_scanner_v2.py, line ~112
TELEGRAM_SEND_REPORT = False  # Disable Telegram
TELEGRAM_SEND_REPORT = True   # Enable Telegram
```

### Send to Multiple Chats
Modify `send_to_telegram()` to loop through multiple `TELEGRAM_CHAT_ID` values

### Send to Group
- Add your bot to a Telegram group
- Get group Chat ID (use @userinfobot, it shows group IDs as negative numbers)
- Set `TELEGRAM_CHAT_ID` to the group ID

## 🧪 Testing

```bash
# Run setup wizard
python setup.py

# Test with environment variables set
python nse_ipo_breakout_scanner_v2.py

# Should see:
# ✅ Report sent to Telegram successfully!
# (or ✅ Scan complete! if no signals found)
```

## 📈 Next Steps

1. **Run setup wizard**: `python setup.py`
2. **Configure Telegram**: Follow on-screen prompts
3. **First run**: `python nse_ipo_breakout_scanner_v2.py`
4. **Check Telegram**: Look for report delivery

## ❓ FAQ

**Q: What if I don't set Telegram credentials?**
A: Scanner works normally, just won't send to Telegram. You'll still get CSV file locally.

**Q: Can I send to multiple users?**
A: Yes, modify `send_to_telegram()` to loop through multiple chat IDs.

**Q: Is my data secure?**
A: Environment variables aren't stored in code. Use Telegram's privacy settings for additional security.

**Q: What if Telegram API fails?**
A: Scanner completes successfully with local CSV. Telegram errors are logged but non-blocking.

**Q: Can I schedule this to run daily?**
A: Yes! Use `cron` (Mac/Linux) or Task Scheduler (Windows) to run the script daily.

---

**Version**: 2.1 (with Telegram integration)  
**Date**: 26 April 2026  
**Your Telegram**: +91 8328139169
