# ⚡ Quick GitHub Deploy Guide (5 Minutes)

Follow these steps to get your IPO Scanner running on GitHub for FREE!

## 🎯 Step 1: Initialize Git (2 minutes)

```bash
cd /Users/chittaprudhviraj/Desktop/python_codes/mini_projects/ipo_trading_strategy

# Initialize git repository
git init

# Configure git (if first time)
git config --global user.email "your_email@example.com"
git config --global user.name "Your Name"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: NSE IPO Breakout Scanner"
```

## 🌐 Step 2: Create Repository on GitHub (2 minutes)

1. Go to: https://github.com/new
2. **Repository name:** `ipo_trading_strategy`
3. **Description:** IPO breakout scanner with Telegram alerts
4. **Public** (FREE) or **Private** (FREE)
5. **Initialize with:** Check README, .gitignore (Python), and License
6. Click **Create repository**

## 📤 Step 3: Push Your Code (1 minute)

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ipo_trading_strategy.git

# Set main branch
git branch -M main

# Push code
git push -u origin main
```

**Done!** Your code is now on GitHub.

---

## 🔐 Step 4: Add Secrets (4 minutes)

These are your API keys - keep them SECRET!

### Go to GitHub Secrets:
1. Open your repo: https://github.com/YOUR_USERNAME/ipo_trading_strategy
2. Click **Settings** (top right)
3. Sidebar → **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Add Secret #1: ANTHROPIC_API_KEY
- **Name:** `ANTHROPIC_API_KEY`
- **Value:** Your Anthropic API key (starts with `sk-ant-`)
- Click **Add secret**

### Add Secret #2: TELEGRAM_BOT_TOKEN
- **Name:** `TELEGRAM_BOT_TOKEN`
- **Value:** Your Telegram bot token (from @BotFather)
- Click **Add secret**

### Add Secret #3: TELEGRAM_CHAT_ID
- **Name:** `TELEGRAM_CHAT_ID`
- **Value:** `8328139169` (your phone number as chat ID)
- Click **Add secret**

✅ **Secrets are now safe and encrypted!**

---

## 🚀 Step 5: Test the Workflow (1 minute)

1. Go to your repo on GitHub
2. Click **Actions** tab
3. See **"NSE IPO Breakout Scanner"** workflow
4. Click it
5. Click **"Run workflow"** (green button)
6. Select **"main"** branch
7. Click **"Run workflow"**

✅ **Workflow starts running!**

### Monitor the Run:
- Watch the job execute in real-time
- See logs for each step
- Check if Telegram message arrives on your phone!

---

## ⏰ Step 6: Set Daily Schedule (Optional, 2 minutes)

The workflow already runs daily at **9:00 AM IST** (3:30 AM UTC).

To change the time, edit `.github/workflows/ipo_scanner.yml`:

### Open file:
1. Go to your repo on GitHub
2. Open `.github/workflows/ipo_scanner.yml`
3. Click ✏️ (edit icon)

### Find this line:
```yaml
- cron: '30 3 * * *'  # 9:00 AM IST = 3:30 AM UTC
```

### Change the time:
```yaml
# Different time examples:
- cron: '0 3 * * *'     # 8:30 AM IST
- cron: '0 5 * * *'     # 10:30 AM IST
- cron: '0 */6 * * *'   # Every 6 hours
- cron: '0 3 * * 1-5'   # 8:30 AM IST, weekdays only
```

### Commit change:
- Scroll down
- Message: "Update schedule"
- Click **Commit changes**

---

## 📊 What Happens Next

### Every Day at 9:00 AM IST:
1. ✅ GitHub automatically runs your scanner
2. ✅ CSV report is generated
3. ✅ Report sent to your Telegram
4. ✅ Results stored in GitHub Artifacts (30 days)
5. ✅ Logs saved for debugging

### You Get:
- 📱 **Telegram message** with summary + CSV file
- 📈 **GitHub Artifacts** - download CSV anytime
- 📝 **Run logs** - see what happened
- 🆓 **FREE** - no costs, no server needed

---

## 🎯 Verify Everything Works

### Check 1: Code on GitHub
```
https://github.com/YOUR_USERNAME/ipo_trading_strategy
```
Should see all your Python files ✅

### Check 2: Workflow File
```
https://github.com/YOUR_USERNAME/ipo_trading_strategy/blob/main/.github/workflows/ipo_scanner.yml
```
Should show the workflow YAML ✅

### Check 3: Secrets Added
```
https://github.com/YOUR_USERNAME/ipo_trading_strategy/settings/secrets/actions
```
Should show 3 secrets (ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) ✅

### Check 4: Manual Run Success
1. Go to Actions tab
2. Should see completed run
3. Check status: ✅ (green checkmark)
4. Telegram message received on phone ✅

---

## 🆘 Quick Troubleshooting

### "Workflow not running at scheduled time?"
- GitHub Actions might not have permissions
- **Settings** → **Actions** → Check "Allow all actions and reusable workflows"
- GitHub runners are in UTC, adjust cron time accordingly

### "No Telegram message received?"
1. Check GitHub Actions logs for errors
2. Verify bot token is correct
3. Verify chat ID is correct (use @userinfobot to confirm)
4. Make sure bot is active in Telegram

### "Code not appearing on GitHub?"
```bash
# Check if push succeeded
git status

# If not pushed, try:
git push -u origin main

# If still failing, check remote:
git remote -v
```

### "Can't find Actions tab?"
- Repository might be private and Actions disabled
- **Settings** → **Actions** → Enable workflows

---

## 📱 Share on GitHub (Optional)

Make your project visible to others:

1. Add **Topics:** Settings → Add topics like:
   - `ipo`
   - `stock-market`
   - `trading-bot`
   - `telegram`
   - `github-actions`

2. Create **GitHub Pages:**
   - Settings → Pages → Deploy from main
   - Shows results on `username.github.io`

3. Add **Shields/Badges** to README:
   ```markdown
   ![Workflow Status](https://github.com/YOUR_USERNAME/ipo_trading_strategy/workflows/NSE%20IPO%20Breakout%20Scanner/badge.svg)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   ```

---

## 🎉 You're Done!

Your IPO Scanner is now:
- ✅ Deployed on GitHub (FREE)
- ✅ Running automatically daily (FREE)
- ✅ Sending results to Telegram (FREE)
- ✅ Storing history (FREE)
- ✅ Zero maintenance needed (FREE)

### Next: Share Your Work
- GitHub link to show others
- Feel free to make it public
- Contribute to open-source community

---

## 📚 Advanced Topics (Optional)

### Want to keep CSV history?
Add to workflow to commit CSVs back to repo:
```yaml
- name: Store results
  run: |
    git config user.email "action@github.com"
    git config user.name "GitHub Action"
    mkdir -p signals
    cp ipo_signals_*.csv signals/
    git add signals/
    git commit -m "Daily signals $(date)" || true
    git push
```

### Want email alerts on failure?
Use GitHub's native notifications or add:
```yaml
- name: Send email on failure
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: ${{ secrets.EMAIL_SERVER }}
    server_port: ${{ secrets.EMAIL_PORT }}
    username: ${{ secrets.EMAIL_USER }}
    password: ${{ secrets.EMAIL_PASS }}
    subject: "IPO Scanner Failed"
    body: "Check: https://github.com/${{ github.repository }}/actions"
    to: your_email@example.com
```

### Want to deploy API?
Use **Vercel, Railway, or Render** to expose results as API (instructions in advanced guide)

---

**Happy deploying!** 🚀

Questions? Check GITHUB_DEPLOYMENT.md for full details.

