# Telegram Setup Guide for IPO Scanner

This guide will help you set up Telegram notifications for the NSE IPO Breakout Scanner.

## 📱 Step 1: Get Your Telegram Bot Token

1. **Open Telegram** and search for **@BotFather** (official Telegram bot manager)
2. **Start a conversation** with BotFather by clicking `/start`
3. **Create a new bot** by typing `/newbot`
4. **Follow the prompts:**
   - Enter a name for your bot (e.g., "IPO Scanner Bot")
   - Enter a username (e.g., "my_ipo_scanner_bot")
5. **Copy the API token** that BotFather provides (looks like: `123456789:ABCDefghijklMNOpqrsTUVwxyz`)
6. **Save this token** - you'll need it in Step 3

## 📍 Step 2: Get Your Telegram Chat ID

### Option A: Using @userinfobot (Easiest)
1. Search for **@userinfobot** on Telegram
2. Start a conversation and it will immediately send you your Chat ID
3. Copy your Chat ID (a long number like: `123456789`)

### Option B: Using Your Bot
1. Start a conversation with your newly created bot
2. Send any message to it
3. Visit this URL in your browser (replace TOKEN with your bot token):
   ```
   https://api.telegram.org/botTOKEN/getUpdates
   ```
4. Look for your Chat ID in the JSON response (under `message.chat.id`)

### Option C: If You're Part of a Group
- To send to a group instead of personal chat, add your bot to the group
- The Chat ID for a group is usually negative (e.g., `-1001234567890`)

## 🔧 Step 3: Set Environment Variables

### On macOS / Linux:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

### On Windows (Command Prompt):

```bash
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

### On Windows (PowerShell):

```powershell
$env:TELEGRAM_BOT_TOKEN="your_bot_token_here"
$env:TELEGRAM_CHAT_ID="your_chat_id_here"
```

### Make It Permanent (macOS/Linux):

Add these lines to your `~/.zshrc` or `~/.bashrc`:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

Then reload:
```bash
source ~/.zshrc  # for zsh
# or
source ~/.bashrc  # for bash
```

### Make It Permanent (Windows):

1. Open **Environment Variables**:
   - Press `Win + X` → Select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
2. Click "New" under "User variables"
3. Add:
   - Variable name: `TELEGRAM_BOT_TOKEN`
   - Variable value: `your_bot_token_here`
4. Repeat for `TELEGRAM_CHAT_ID`
5. Restart your terminal/IDE

## ✅ Step 4: Verify Setup

Run this Python command to test:

```bash
python -c "import os; print(f'Token: {os.environ.get(\"TELEGRAM_BOT_TOKEN\", \"NOT SET\")}'); print(f'Chat ID: {os.environ.get(\"TELEGRAM_CHAT_ID\", \"NOT SET\")}')"
```

Both should show values (not "NOT SET").

## 🚀 Step 5: Run the Scanner

```bash
python nse_ipo_breakout_scanner_v2.py
```

When done, if signals are found, the CSV report will be automatically sent to your Telegram account!

## 📊 What You'll Receive

You'll get two messages:

1. **Summary Message** with:
   - Total signals found
   - Breakdown by signal type (1st Breakout, Retest+Hammer, etc.)
   - Generation timestamp

2. **CSV File** with:
   - All signal stocks
   - Prices and breakout levels
   - Sentiment analysis
   - News headlines
   - Liquidity data

## 🔒 Security Notes

- **Never share your bot token** publicly - it allows anyone to control your bot
- **Keep your chat ID private** - it identifies where messages go
- These credentials are read from environment variables only
- They are NOT stored in the code or version control

## 🐛 Troubleshooting

### Not Receiving Messages?

1. **Check if variables are set:**
   ```bash
   echo $TELEGRAM_BOT_TOKEN
   echo $TELEGRAM_CHAT_ID
   ```
   Should show your actual values, not blank.

2. **Verify bot is active:**
   - Open Telegram and search for your bot username
   - Send it any message
   - Check it's not restricted

3. **Check internet connection:**
   - Telegram API requires internet access
   - VPN might block it in some regions

4. **Verify API token format:**
   - Should be: `123456789:ABCDefgh...` (with a colon)
   - Should start with numbers, not text

### Bot Shows "TELEGRAM_BOT_TOKEN not set" Message?

- Environment variables not properly exported
- Terminal session wasn't restarted after setting variables
- Try running from a fresh terminal window

### File Upload Fails?

- CSV file might be too large (though unlikely)
- Telegram API rate limiting (try again in a few minutes)
- Bot might not have file sending permissions

## 📝 Example Run

```bash
$ export TELEGRAM_BOT_TOKEN="123456789:ABCDefghijklMNOpqrsTUVwxyz"
$ export TELEGRAM_CHAT_ID="987654321"
$ python nse_ipo_breakout_scanner_v2.py

═════════════════════════════════════════════════════════════
   NSE MAINBOARD IPO BREAKOUT SCANNER
   Signals in last 15 days  |  26 Apr 2026  03:45 PM
   1H Liquidity filter: avg hourly value ≥ 100.0 L  (lookback 10d)
═════════════════════════════════════════════════════════════

...scanning stocks...

Saved to: ipo_signals_20260426_1545.csv

✅ Report sent to Telegram successfully!
✅ Scan complete!
```

## 🎯 Additional Features

### Disable Telegram Sending (Optional)

If you want to run the scanner without sending to Telegram:

In the code, change:
```python
TELEGRAM_SEND_REPORT = False  # Set False to disable
```

### Send to Group Chat

Instead of a personal chat, you can send to a Telegram group:

1. Create a group in Telegram
2. Add your bot to the group
3. Use the group's Chat ID (usually negative: `-1001234567890`)
4. Set that as `TELEGRAM_CHAT_ID`

### Multiple Recipients

To send to multiple users/groups, modify the `send_to_telegram()` function to loop through multiple chat IDs.

---

**Need help?** Check Telegram's official documentation or the BotFather chat for more info.

Happy trading! 📈
