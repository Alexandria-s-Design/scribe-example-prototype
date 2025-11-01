# 🤖 Alexandria - Slack AI Teammate

## ✅ **WORKING!** Grok 4 Integration Tested

Alexandria successfully responded to: "What is our revenue goal?"
Response: "$30k per month. Let's focus on strategies to get to the bread!"

---

## 🚀 Quick Start

### **Option 1: Monitoring Mode** (Recommended)
```bash
# Double-click or run:
scripts\start_alexandria.bat

# Or command line:
python scripts/alexandria_slack_bot.py monitor
```

**What it does**:
- Checks Slack every 10 seconds for @mentions
- Calls Grok 4 for intelligent responses
- Replies in thread automatically
- Runs continuously

### **Option 2: Test Mode**
```bash
python scripts/alexandria_slack_bot.py test
```

**What it does**:
- Tests Grok 4 connection
- Shows example response
- No Slack interaction

---

## 💬 How to Use in Slack

1. **Start the bot** (run `start_alexandria.bat`)
2. **Go to Slack**
3. **Mention the bot**: `@Slacking What is our revenue goal?`
4. **Wait 10-15 seconds** (bot checks every 10 seconds)
5. **Alexandria responds!**

---

## 🎯 What Alexandria Can Do

**Current capabilities**:
- Answer questions about Alexandria's Design
- Discuss revenue goals ($30k/month)
- Provide information about products (ModelIt!, Alexandria's World)
- Talk about educational technology consulting

**Example prompts**:
- `@Slacking What is our revenue goal?`
- `@Slacking What products do we offer?`
- `@Slacking What tools can you access?`
- `@Slacking Help me with...`

---

## 🔧 Technical Details

**Architecture**:
```
Slack Messages
    ↓
Python Bot (polls every 10s)
    ↓
Grok 4 API
    ↓
Response back to Slack
```

**No external services needed**:
- ✅ No Zapier account required
- ✅ No ngrok tunnels
- ✅ No webhooks to configure
- ✅ Just run the Python script

**APIs used**:
- Slack API (for reading mentions and posting)
- Grok 4 API (for AI responses)

---

## 🛠️ Troubleshooting

### Bot doesn't respond
1. Check script is running (`start_alexandria.bat`)
2. Wait 10-15 seconds (polling interval)
3. Check console for errors

### "Unauthorized" errors
- Verify Slack token in `alexandria_slack_bot.py`
- Verify Grok API key

### Slow responses
- Bot checks every 10 seconds
- To speed up: Change `time.sleep(10)` to `time.sleep(5)` in the script

---

## ⚙️ Configuration

**Edit the bot**: `scripts/alexandria_slack_bot.py`

**Change personality**:
- Line 14: Edit `ALEXANDRIA_PROMPT`

**Change polling interval**:
- Line 181: Change `time.sleep(10)` to desired seconds

**Change Grok model**:
- Line 52: Change `"grok-2-latest"` to other models

---

## 💰 Cost

**This approach**:
- FREE (no Zapier subscription)
- Only Grok API costs (~$0.02-0.05 per response)

**vs Zapier approach**:
- Would cost $20/month for instant responses
- Plus Grok costs

**Savings**: $20/month!

---

## 🚀 Running as Background Service (Optional)

### Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: When computer starts
4. Action: Run `C:\Users\MarieLexisDad\scripts\start_alexandria.bat`
5. Alexandria runs automatically on startup!

### Screen/tmux (if on Linux/WSL):
```bash
screen -S alexandria
python scripts/alexandria_slack_bot.py monitor
# Ctrl+A, D to detach
```

---

## ✅ Status

- [x] Grok 4 integration working
- [x] Alexandria personality configured
- [x] Monitoring mode implemented
- [x] Test mode working
- [ ] Running 24/7 (optional - set up Task Scheduler)
- [ ] Advanced features (calendar, email integration)

---

## 🎉 Success!

**Working now**:
```
You: @Slacking What is our revenue goal?
Alexandria: Our revenue goal is $30k per month. Let's focus on
strategies to get to the bread!
```

**Next steps**:
1. Run `start_alexandria.bat`
2. Test in Slack
3. Leave running for 24/7 operation

---

**Let's get to the bread!** 🚀
