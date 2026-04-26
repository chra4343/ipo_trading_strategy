# 🚀 Deploying IPO Scanner to GitHub (FREE)

Complete guide to deploy your NSE IPO Breakout Scanner on GitHub and set it up for free automated runs.

## 📋 Table of Contents
1. [Free Deployment Options](#free-deployment-options)
2. [GitHub Setup](#github-setup)
3. [GitHub Actions (Free CI/CD)](#github-actions-free-cicd)
4. [GitHub Secrets Management](#github-secrets-management)
5. [Scheduling Automated Runs](#scheduling-automated-runs)
6. [Monitoring & Logs](#monitoring--logs)

---

## 🎯 Free Deployment Options

### Option 1: GitHub Actions (RECOMMENDED) ⭐
- **Cost:** FREE (up to 2,000 minutes/month)
- **Setup Time:** 10 minutes
- **Best For:** Scheduled automated runs, daily scans
- **Runs:** Linux Ubuntu containers
- **Output:** CSV → Telegram, Email, or GitHub Actions artifacts

### Option 2: GitHub Pages + Static Site
- **Cost:** FREE
- **Setup Time:** 15 minutes
- **Best For:** Displaying latest signals on a website
- **Limitation:** Can't run Python scripts directly

### Option 3: Cloud Free Tier (Alternative)
- **Replit:** FREE tier with 0.5 CPU (slow)
- **PythonAnywhere:** FREE tier (limited hours)
- **Railway:** $5/month credit (essentially free for 30 days)
- **Heroku:** Discontinued free tier (no longer recommended)

**I recommend Option 1 (GitHub Actions)** ✅

---

## 📱 GitHub Setup

### Step 1: Create a GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `ipo_trading_strategy` (or your choice)
3. **Description:** "NSE IPO Breakout Scanner with automated Telegram alerts"
4. **Visibility:** `Public` (free) or `Private` (free)
5. **Initialize with:** 
   - ✅ Add a README.md
   - ✅ Add .gitignore (Python)
   - ✅ Choose license (MIT or Apache 2.0)
6. **Click:** Create repository

### Step 2: Clone and Push Your Code

```bash
# Navigate to your project directory
cd /Users/chittaprudhviraj/Desktop/python_codes/mini_projects/ipo_trading_strategy

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NSE IPO Breakout Scanner with Telegram integration"

# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Add .gitignore (IMPORTANT!)

Create `.ipo_trading_strategy/.gitignore`:
```
# Environment variables
.env
.env.local
*.env

# API Keys & Secrets
*.key
secrets.json

# Output files
ipo_signals_*.csv
nohup.out

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt

# IDE
.vscode/
.idea/
*.swp
*.swo
*.code-workspace

# OS
.DS_Store
Thumbs.db

# Dependencies
node_modules/
```

```bash
git add .gitignore
git commit -m "Add .gitignore for security and cleanliness"
git push
```

---

## ⚙️ GitHub Actions (Free CI/CD)

### Step 1: Create GitHub Actions Workflow

1. **In your repo**, create: `.github/workflows/ipo_scanner.yml`

```bash
mkdir -p .github/workflows
```

2. **Create the workflow file:**

Create `.github/workflows/ipo_scanner.yml`:

```yaml
name: NSE IPO Breakout Scanner

# Trigger: Every day at 9:00 AM IST (3:30 AM UTC)
on:
  schedule:
    - cron: '30 3 * * *'  # 9:00 AM IST = 3:30 AM UTC
  
  # Allow manual trigger from GitHub UI
  workflow_dispatch:

jobs:
  scan:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install yfinance pandas requests anthropic
      
      - name: Run IPO Scanner
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          python nse_ipo_breakout_scanner_v2.py
      
      - name: Upload CSV to artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: ipo_signals
          path: ipo_signals_*.csv
          retention-days: 30
      
      - name: Upload logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: scan_logs
          path: nohup.out
          retention-days: 7
```

3. **Commit the workflow:**
```bash
git add .github/workflows/ipo_scanner.yml
git commit -m "Add GitHub Actions workflow for daily IPO scans"
git push
```

---

## 🔐 GitHub Secrets Management

Your API keys go HERE, NOT in the code!

### Step 1: Add Secrets to GitHub

1. **Go to your repo:** https://github.com/YOUR_USERNAME/YOUR_REPO
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**

### Step 2: Add Each Secret

**Add Secret #1: ANTHROPIC_API_KEY**
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-...your-key...`
- Click: **Add secret**

**Add Secret #2: TELEGRAM_BOT_TOKEN**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: `123456789:ABCDefgh...`
- Click: **Add secret**

**Add Secret #3: TELEGRAM_CHAT_ID**
- Name: `TELEGRAM_CHAT_ID`
- Value: `8328139169` (your phone number)
- Click: **Add secret**

✅ Now these secrets are:
- NOT visible in logs
- NOT in your code
- Safely injected into GitHub Actions environment

---

## 📅 Scheduling Automated Runs

### Option A: Daily at 9:00 AM IST (Recommended)

Already configured in the workflow above:
```yaml
on:
  schedule:
    - cron: '30 3 * * *'  # 9:00 AM IST
```

### Option B: Run Every 6 Hours

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
```

### Option C: Business Days Only (Mon-Fri) at 9:00 AM IST

```yaml
on:
  schedule:
    - cron: '30 3 * * 1-5'  # Mon-Fri only
```

### Option D: Manual Trigger Only

```yaml
on:
  workflow_dispatch:  # Manually trigger from GitHub UI
```

### Cron Format Reference
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday - Saturday)
│ │ │ │ │
│ │ │ │ │
│ │ │ │ │
* * * * *

Common timezones:
- IST (India):     UTC+5:30, so 9:00 AM = 3:30 AM UTC
- EST (New York):  UTC-5, so 9:00 AM = 2:00 PM UTC  
- CST (Chicago):   UTC-6, so 9:00 AM = 3:00 PM UTC
- UTC:             Keep as-is
```

---

## 📊 Monitoring & Logs

### View Workflow Runs

1. **Go to your repo**
2. **Actions** tab
3. Click on **"NSE IPO Breakout Scanner"**
4. View all runs and logs

### View Detailed Logs

1. Click on a specific run
2. Click on **"scan"** job
3. View full logs in real-time
4. See step-by-step execution

### Get Notifications

1. **Settings** → **Notifications** 
2. Check **"Notify me when workflows fail"**
3. GitHub will email you on failures

### Download CSV Artifacts

1. After a run completes
2. Scroll to **"Artifacts"** section
3. Download `ipo_signals` or `scan_logs`
4. No need to wait for Telegram message!

---

## 🔧 Optional: Notifications Beyond Telegram

### Email Alert on Failure

Add this step to workflow:
```yaml
- name: Notify on failure
  if: failure()
  uses: davismcclain/prow-github-action@v1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    slack-webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

### Discord Webhook Alert

```yaml
- name: Discord notification
  uses: sarisia/actions-status-discord@v1
  if: always()
  with:
    webhook_url: ${{ secrets.DISCORD_WEBHOOK }}
    status: ${{ job.status }}
    description: IPO Scanner completed
```

---

## 📈 Advanced: Store Results in Repository

### Option: Commit CSV Back to Repo

Add this to your workflow:
```yaml
- name: Commit signals to repo
  if: always()
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    mkdir -p signals
    cp ipo_signals_*.csv signals/ 2>/dev/null || true
    git add signals/
    git commit -m "Update IPO signals - $(date)" || echo "No changes"
    git push
```

This keeps a history of all signals in your repo!

---

## 📝 GitHub README Best Practices

Update your `README.md` to include:

```markdown
## 🚀 Automated Deployment

This project runs automatically via **GitHub Actions** every day at 9:00 AM IST.

### View Recent Runs
- Go to: **Actions** tab
- View logs and download CSV results

### Manual Trigger
1. Go to **Actions** → **NSE IPO Breakout Scanner**
2. Click **"Run workflow"**
3. Select **"main"** branch
4. Click **"Run workflow"**

### Environment Setup
Results are sent to Telegram automatically. No local setup needed!

### Secrets Required (Already Configured)
- `ANTHROPIC_API_KEY` - Claude API key
- `TELEGRAM_BOT_TOKEN` - Telegram bot token
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID
```

---

## ✅ Complete Checklist

- [ ] GitHub account created
- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] `.gitignore` added (no secrets in repo)
- [ ] `.github/workflows/ipo_scanner.yml` created
- [ ] `ANTHROPIC_API_KEY` secret added
- [ ] `TELEGRAM_BOT_TOKEN` secret added
- [ ] `TELEGRAM_CHAT_ID` secret added
- [ ] First workflow run manually triggered
- [ ] Telegram message received successfully
- [ ] Schedule cron verified (9:00 AM IST = 3:30 AM UTC)
- [ ] README updated with deployment info

---

## 🎉 What You Now Have (FREE)

✅ **Always-on Python execution** - Runs at scheduled times automatically
✅ **Free storage** - 2,000 minutes/month of computing
✅ **Telegram alerts** - Daily signals delivered to your phone
✅ **CSV storage** - 30 days of historical data in artifacts
✅ **Version control** - Full git history of changes
✅ **Zero cost** - All completely free
✅ **No server to maintain** - GitHub handles everything

---

## 🚨 Troubleshooting

### Workflow Fails?
1. Check the **Actions** tab for error logs
2. Verify all 3 secrets are set correctly
3. Check if API keys are still valid
4. Ensure `nse_ipo_breakout_scanner_v2.py` can run locally first

### No Telegram Message?
1. Verify `TELEGRAM_BOT_TOKEN` is correct
2. Verify `TELEGRAM_CHAT_ID` is correct
3. Check bot is active (@BotFather)
4. See logs in GitHub Actions for error details

### Schedule Not Running?
1. GitHub Actions might be disabled - check **Settings** → **Actions**
2. Account might have disabled scheduled workflows
3. Try manual trigger first: **Actions** → **Run workflow**

### Secrets Not Available in Workflow?
1. Verify secret names match exactly (case-sensitive)
2. Secrets must be added BEFORE workflow runs
3. Re-run workflow after adding new secrets

---

## 📞 Need Help?

### GitHub Actions Docs
- https://docs.github.com/en/actions

### GitHub Secrets
- https://docs.github.com/en/actions/security-guides/encrypted-secrets

### Cron Expression Validator
- https://crontab.guru

### Schedule IST to UTC Converter
- https://www.timeanddate.com/worldclock/converter.html

---

## 💡 Pro Tips

1. **Test locally first:** Run the script on your machine before deploying
2. **Use workflow_dispatch:** Always enable manual trigger for debugging
3. **Keep logs:** 30-day artifact retention helps track performance
4. **Monitor costs:** GitHub Actions shows usage in Settings
5. **Version your API keys:** Rotate keys periodically
6. **Check quota:** You get 2,000 free minutes/month (plenty for daily runs)

---

**Congratulations! Your IPO Scanner is now deployed on GitHub for FREE!** 🎉

Next time you want to run it: Just GitHub does it automatically! ✨

