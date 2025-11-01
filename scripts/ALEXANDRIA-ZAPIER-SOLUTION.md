# 🎯 Alexandria via Zapier MCP - The Right Way

## The Problem We Discovered

Bot tokens can't use Slack's `search.messages` API, so automatic monitoring doesn't work.

## The Solution: Zapier MCP (Original Plan!)

Use Zapier to handle the Slack integration - this is what you originally asked for and it's the RIGHT approach!

---

## 🚀 Quick Setup

### Step 1: Go to Zapier

Visit the Zapier MCP config page:
https://mcp.zapier.com/mcp/servers/52cc6e40-ba52-4bc9-8ff8-f3841239dd64/config

### Step 2: Create the Zap

**Trigger**: New Mention in Slack
- App: Slack
- Event: `New Mention`
- Connect your Slack workspace

**Action 1**: Webhooks by Zapier (POST)
- URL: `https://api.x.ai/v1/chat/completions`
- Method: POST
- Headers:
  - `Authorization`: `Bearer YOUR_GROK_API_KEY`
  - `Content-Type`: `application/json`
- Body (JSON):
```json
{
  "model": "grok-2-latest",
  "messages": [
    {
      "role": "system",
      "content": "You are Alexandria, an AI teammate for Alexandria's Design. Revenue goal: $30k/month. Be concise in Slack."
    },
    {
      "role": "user",
      "content": "{{1. Text}}"
    }
  ]
}
```

**Action 2**: Send Channel Message in Slack
- Channel: `{{1. Channel ID}}`
- Message: `{{2. choices__0__message__content}}`
- Thread TS: `{{1. Thread TS}}`

### Step 3: Test & Publish

1. Test each step
2. Publish the Zap
3. Turn it ON

---

## 💰 Cost

**Zapier Free**:
- 100 tasks/month
- 15-minute polling (slow)

**Zapier Starter** ($20/month):
- Instant responses
- 750 tasks/month

---

## 🎯 Meanwhile: Use Our Working Solutions

While you set up Zapier, use these:

### **Chat Mode** (Instant testing):
```bash
python scripts/alexandria_slack_bot_v2.py chat
```

### **Manual Mode** (Post to Slack):
```bash
python scripts/alexandria_slack_bot_v2.py manual
```

---

## Why Zapier is Actually Better

| Feature | Our Bot | Zapier |
|---------|---------|--------|
| Setup | Need to fix permissions | Just connect & go |
| Monitoring | Bot token limitations | Events API works |
| Reliability | Runs on your machine | Cloud-based |
| Maintenance | You manage it | Zapier manages it |

---

**Bottom line**: Zapier MCP is the right solution. I should have built it that way from the start!

Set it up at: https://zapier.com
