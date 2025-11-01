# 🚀 Zapier + Grok 4 Slack AI Teammate - Complete Setup Guide

## ✨ What You're Building

A Slack bot that:
- Responds when mentioned (`@Slacking`)
- Uses Grok 4 for intelligent responses
- Has Alexandria's personality (revenue-focused, educational expertise)
- Works instantly (no servers, no ngrok, no localhost)

**Time to setup**: 10 minutes
**Cost**: Free (Zapier free plan: 100 tasks/month)

---

## 📋 Prerequisites

- [x] Slack workspace access
- [x] Grok API key: `xai-K1xq1fOvoO4nOFPEbCK3yNEILrzh1ortXqFK6kw689...`
- [ ] Zapier account (we'll create this)

---

## 🎯 Step-by-Step Setup

### Step 1: Create Zapier Account

1. Go to: https://zapier.com/sign-up
2. Sign up with: `charlesmartinedd@gmail.com`
3. Choose **Free plan** (100 tasks/month)
4. Verify your email

---

### Step 2: Create New Zap

1. Click **"Create Zap"** button (top right)
2. Give it a name: **"Slack AI Teammate - Alexandria"**

---

### Step 3: Set Up Trigger (Slack)

1. **Search for trigger app**: Type `Slack`
2. **Select trigger event**: Choose `New Mention`
3. **Connect Slack account**: Click "Sign in to Slack"
   - Select your workspace
   - Click "Allow"
4. **Configure trigger**:
   - **Channel**: Leave as "Any Channel" (or pick specific channels)
   - **Trigger on**: `@mention only`
5. **Test trigger**:
   - Go to Slack and type: `@Slacking test`
   - Come back to Zapier
   - Click "Test trigger"
   - You should see your test message appear ✅

---

### Step 4: Add Action 1 - Call Grok 4 API

1. **Click "+ Add Step"** → **Action**
2. **Search for app**: Type `Webhooks by Zapier`
3. **Select action**: Choose `POST`
4. **Configure POST request**:

**URL**:
```
https://api.x.ai/v1/chat/completions
```

**Payload Type**: `JSON`

**Data** (click "Switch to Code Mode" for easier pasting):
```json
{
  "model": "grok-2-latest",
  "messages": [
    {
      "role": "system",
      "content": "You are Alexandria, an AI teammate for Alexandria's Design, founded by Charles Martin and Dr. Marie Martin.\n\nBUSINESS CONTEXT:\n- Educational technology consulting for K-12, higher ed, government, military\n- Revenue goal: $30k/month (\"let's get to the bread\")\n- Products: ModelIt!, Alexandria's World, professional development\n\nYOUR CAPABILITIES:\n- Email: Office 365, Gmail\n- Calendar: Google Calendar, Office 365\n- Projects: Monday.com\n- Files: OneDrive, Google Drive\n\nPERSONALITY:\n- Professional yet friendly\n- Revenue-focused and practical\n- Proactive\n- Educational expertise\n\nALWAYS:\n- Think revenue-first\n- Be concise in Slack\n- Ask clarifying questions"
    },
    {
      "role": "user",
      "content": "REPLACE_WITH_SLACK_TEXT"
    }
  ],
  "temperature": 0.7
}
```

**IMPORTANT**: Replace `REPLACE_WITH_SLACK_TEXT` with the dynamic field from Step 1:
- Click on the field
- Select the dropdown
- Choose: **"1. Text"** (from the Slack trigger)

**Headers**:
- Click "Add Header"
- **Key**: `Authorization`
- **Value**: `Bearer YOUR_GROK_API_KEY`

- Click "Add Header" again
- **Key**: `Content-Type`
- **Value**: `application/json`

5. **Test the action**:
   - Click "Test action"
   - You should see a response from Grok! ✅
   - Look for: `choices → 0 → message → content`

---

### Step 5: Add Action 2 - Send Response to Slack

1. **Click "+ Add Step"** → **Action**
2. **Search for app**: Type `Slack`
3. **Select action**: Choose `Send Channel Message`
4. **Use existing Slack connection** (from Step 3)
5. **Configure message**:

**Channel**:
- Click field → Select from dropdown
- Choose: **"1. Channel ID"** (from Slack trigger)

**Message Text**:
- Click field → Select from dropdown
- Choose: **"2. Choices 0 Message Content"** (from Webhooks response)
- This is Grok's AI response!

**Thread TS** (to reply in thread):
- Click field → Select from dropdown
- Choose: **"1. Thread TS"** (from Slack trigger)
- If empty, choose **"1. Timestamp"** instead

**Send as Bot**: Yes

6. **Test the action**:
   - Click "Test action"
   - Check Slack - you should see Alexandria's response! ✅

---

### Step 6: Publish Your Zap

1. **Review the Zap**:
   - Trigger: New Mention in Slack ✅
   - Action 1: Call Grok API ✅
   - Action 2: Send to Slack ✅

2. **Click "Publish"** (top right)
3. **Turn ON the Zap** (toggle switch)

---

## 🧪 Testing

1. Go to your Slack workspace
2. Type: `@Slacking What is our revenue goal?`
3. Wait 2-3 seconds
4. Alexandria responds: "Our revenue goal is $30k/month - let's get to the bread!" ✅

**More test prompts**:
- `@Slacking What can you do?`
- `@Slacking Check my calendar`
- `@Slacking Send an email to...`

---

## 🔍 Troubleshooting

### Bot doesn't respond at all
1. Check Zap is **ON** (green toggle in Zapier dashboard)
2. Go to Zapier → Task History
3. Look for errors in recent tasks
4. Common fixes:
   - Re-authenticate Slack connection
   - Verify Grok API key is correct
   - Check Thread TS field mapping

### Slow responses (15+ minutes delay)
- **Cause**: Zapier free plan checks for new triggers every 15 minutes
- **Solution**: Upgrade to Starter plan ($20/month) for instant triggers

### "Unauthorized" error from Grok
- Check the Authorization header has `Bearer ` prefix
- Verify API key is correct: `xai-K1xq1fOvoO4nOFPEbCK3yNEILrzh1ortXqFK6kw689...`

### Response appears but in wrong channel
- Check Channel ID mapping in Step 5
- Should use `1. Channel ID` from Slack trigger

---

## 💰 Cost Breakdown

**Zapier Free Plan**:
- 100 tasks/month
- 1 mention = 2 tasks (webhook + send message)
- = 50 mentions/month free
- Checks every 15 minutes (not instant)

**Zapier Starter Plan** ($20/month):
- 750 tasks/month
- Instant triggers (< 1 second response)
- = 375 mentions/month

**Grok API**:
- ~$0.02-0.05 per response
- 50 responses = $1-2.50/month

**Total Free Plan**: $1-2.50/month
**Total Starter Plan**: $21-22.50/month

---

## 🎨 Customizing Alexandria

Want to change her personality? Edit the system prompt in Step 4:

**Current personality**:
- Revenue-focused ($30k/month goal)
- Educational technology expert
- Professional yet friendly
- Proactive

**To change**:
1. Open your Zap
2. Go to Action 1 (Webhooks)
3. Edit the `content` field in the system message
4. Save and test

**Example personalities**:
- **Friendly mentor**: "You are a supportive educational mentor..."
- **Sales coach**: "You are a revenue-focused sales coach..."
- **Project manager**: "You are a detail-oriented project manager..."

---

## 📊 Next Steps: Advanced Features

Once basic setup works, you can add:

1. **Tool calling**: Let Alexandria actually send emails, create calendar events
2. **Memory**: Store conversation context across messages
3. **Multiple bots**: Create different bots for different channels
4. **Analytics**: Track how often Alexandria is used

---

## ✅ Success Checklist

- [ ] Zapier account created
- [ ] Zap created with 3 steps (trigger + 2 actions)
- [ ] Slack connected and authenticated
- [ ] Grok API key configured in webhook
- [ ] All 3 steps tested successfully
- [ ] Zap published and turned ON
- [ ] Test mention sent in Slack
- [ ] Alexandria responds! 🎉

---

**Need help?**
- Check Zapier Task History for error details
- Verify all dynamic fields are mapped correctly
- Ensure Thread TS is mapped to reply in threads

**Status**: Ready to deploy
**Time to setup**: 10 minutes
**Difficulty**: Easy (no coding required!)

---

🚀 **Let's get to the bread!**
