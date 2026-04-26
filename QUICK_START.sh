#!/usr/bin/env bash
# Quick Reference Card - NSE IPO Breakout Scanner with Telegram
# Save this file and source it for quick access to commands

# ╔═══════════════════════════════════════════════════════════════════╗
# ║   NSE IPO BREAKOUT SCANNER - TELEGRAM INTEGRATION - QUICK REF   ║
# ║   Your Telegram: +91 8328139169                                  ║
# ╚═══════════════════════════════════════════════════════════════════╝

echo """
═══════════════════════════════════════════════════════════════════════
   🚀 NSE IPO BREAKOUT SCANNER - QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════

📌 FIRST TIME SETUP (Choose One):

   Option A: Interactive Setup (Recommended)
   ──────────────────────────────────────────
   $ python setup.py
   └─ Guides you through everything!

   Option B: Manual Setup
   ──────────────────────
   1. Get Telegram Bot Token from @BotFather
   2. Get Telegram Chat ID from @userinfobot
   3. Set environment variables:
      
      macOS/Linux:
      export TELEGRAM_BOT_TOKEN=\"your_token\"
      export TELEGRAM_CHAT_ID=\"your_chat_id\"
      
      Windows:
      set TELEGRAM_BOT_TOKEN=your_token
      set TELEGRAM_CHAT_ID=your_chat_id

───────────────────────────────────────────────────────────────────────
📖 DOCUMENTATION:

   README.md               → Full feature documentation
   INSTALLATION_GUIDE.md   → Complete setup & troubleshooting
   TELEGRAM_SETUP.md       → Detailed Telegram guide
   FEATURE_SUMMARY.md      → What's new & code changes
   CHANGES.md              → All modifications made

───────────────────────────────────────────────────────────────────────
▶️  RUNNING THE SCANNER:

   First Time (with setup):
   $ python setup.py
   $ python nse_ipo_breakout_scanner_v2.py

   Regular Usage:
   $ python nse_ipo_breakout_scanner_v2.py

   Expected Output:
   ✅ Report sent to Telegram successfully!
   (or ✅ Scan complete! if no signals found)

───────────────────────────────────────────────────────────────────────
🔧 COMMON COMMANDS:

   Install dependencies:
   $ pip install -r requirements.txt

   Test Telegram connection:
   $ python setup.py

   Check environment variables:
   $ echo \$TELEGRAM_BOT_TOKEN
   $ echo \$TELEGRAM_CHAT_ID

   Run scanner without Telegram (disable):
   → Edit nse_ipo_breakout_scanner_v2.py
   → Change: TELEGRAM_SEND_REPORT = False

───────────────────────────────────────────────────────────────────────
⚡ QUICK TROUBLESHOOTING:

   Telegram not set up?
   → Run: python setup.py

   Getting \"not set\" warnings?
   → Environment variables not saved
   → For macOS/Linux: add to ~/.zshrc then source it
   → For Windows: use Windows Environment Variables (System Properties)

   CSV not saved?
   → Check write permissions in current directory
   → Run from a writable location

   No signals found?
   → Try adjusting thresholds in the config section of the scanner
   → See README.md for parameter explanations

───────────────────────────────────────────────────────────────────────
📊 WHAT YOU'LL GET:

   Message 1: Summary with signal breakdown
   Message 2: CSV file with complete data
   
   Signals include:
   ✓ Stock name & symbol
   ✓ Breakout level & current price
   ✓ News sentiment (Positive/Negative/Mixed/Neutral)
   ✓ Hourly liquidity metrics
   ✓ Signal type & timing

───────────────────────────────────────────────────────────────────────
🎯 NEXT STEPS:

   1. $ python setup.py
      └─ Follow interactive setup

   2. Check Telegram for confirmation
      └─ Bot should send test message

   3. $ python nse_ipo_breakout_scanner_v2.py
      └─ Run first scan

   4. Check Telegram for report
      └─ Should get summary + CSV file

───────────────────────────────────────────────────────────────────────
💡 TIPS:

   • Save environment variables permanently (don't re-enter each time)
   • Can send to personal chat OR group chat
   • Scanner works offline for price analysis (Telegram requires internet)
   • CSV saved locally + sent to Telegram for backup
   • Non-blocking Telegram send (scan completes even if Telegram fails)

───────────────────────────────────────────────────────────────────────
📞 NEED HELP?

   Setup issues?         → See INSTALLATION_GUIDE.md
   Telegram problems?    → See TELEGRAM_SETUP.md
   Feature questions?    → See README.md or FEATURE_SUMMARY.md
   All changes?          → See CHANGES.md

═══════════════════════════════════════════════════════════════════════
Version: 2.1 | Release: 26 April 2026 | Status: ✅ Ready to Use
═══════════════════════════════════════════════════════════════════════
"""
