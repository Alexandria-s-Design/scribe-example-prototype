# 🤖 Alexandria - Complete Setup Guide
## Automatic Slack AI Teammate with Grok 4

---

## 📋 **What You Have Now**

✅ **Working:** Alexandria responds when you tell Claude Code about mentions
- Grok 4 API integration
- Zapier MCP for posting to Slack
- Alexandria's personality (revenue-focused, $30k/month goal)
- Signature: "- Alexandria"

✅ **Current Workflow:**
```
1. Someone mentions @Slacking in #all-alexandrias-design
2. You tell Claude Code: "Respond to: [message]"
3. Alexandria replies via Zapier MCP
4. Response shows as: "Zapier APP" with "- Alexandria" signature
```

---

## 🎯 **Goal: Make It Automatic**

Set up Alexandria to respond automatically without manual intervention.

---

## ⚡ **OPTION 1: Zapier Zap (RECOMMENDED)**

**Best for:** Set it and forget it
**Time:** 10 minutes
**Cost:** FREE (Zapier free tier: 100 tasks/month)
**Maintenance:** None

### **Step 1: Create Zapier Account**

1. Go to: https://zapier.com/sign-up
2. Sign up with: charlesmartinedd@gmail.com
3. Verify your email
4. Choose **FREE** plan

### **Step 2: Create New Zap**

1. Go to: https://zapier.com/app/zaps
2. Click **"Create Zap"** (top right)
3. Give it a name: **"Alexandria - Slack AI Teammate"**

### **Step 3: Configure Trigger (Slack)**

**3.1 - Select Trigger App:**
- Search for: **Slack**
- Click on Slack

**3.2 - Select Trigger Event:**
- Choose: **New Mention**
- Click **Continue**

**3.3 - Connect Slack Account:**
- Click **Sign in to Slack**
- Select: **Alexandria's Design** workspace
- Click **Allow**

**3.4 - Configure Trigger:**
- **Channel:** Leave as "Any Channel" OR select #all-alexandrias-design
- **Bot User:** @Slacking
- Click **Continue**

**3.5 - Test Trigger:**
- Go to Slack
- Type: `@Slacking test zapier setup`
- Come back to Zapier
- Click **Test trigger**
- You should see your test message ✅
- Click **Continue**

### **Step 4: Add Action - Call Grok 4**

**4.1 - Add New Step:**
- Click **"+"** button
- Select **Action**

**4.2 - Select App:**
- Search for: **Webhooks by Zapier**
- Click on it

**4.3 - Select Action Event:**
- Choose: **POST**
- Click **Continue**

**4.4 - Configure POST Request:**

**URL:**
```
https://api.x.ai/v1/chat/completions
```

**Payload Type:**
- Select: **JSON**

**Headers Section:**
- Click **"Show Options"** → **Headers**
- Add first header:
  - **Key:** `Authorization`
  - **Value:** `Bearer YOUR_GROK_API_KEY`

- Add second header:
  - **Key:** `Content-Type`
  - **Value:** `application/json`

**Data Section:**
- Toggle to **"Code Mode"** (easier for JSON)
- Paste this JSON:

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
      "content": "REPLACE_THIS"
    }
  ],
  "temperature": 0.7
}
```

**IMPORTANT:**
- Find `"REPLACE_THIS"` in the JSON
- Click on that field
- A dropdown will appear
- Select: **"1. Text"** (this is the message from Slack)
- The field should now show something like `{{123456789__text}}`

**4.5 - Test Action:**
- Click **Test action**
- You should see a response from Grok with `choices[0].message.content`
- Click **Continue**

### **Step 5: Add Action - Send to Slack**

**5.1 - Add New Step:**
- Click **"+"** button
- Select **Action**

**5.2 - Select App:**
- Search for: **Slack**
- Click on it

**5.3 - Select Action Event:**
- Choose: **Send Channel Message**
- Click **Continue**

**5.4 - Use Existing Connection:**
- Should auto-select your Slack connection
- Click **Continue**

**5.5 - Configure Message:**

**Channel:**
- Click in the field
- Dropdown appears
- Select: **"1. Channel ID"** (from Step 1 - Slack trigger)

**Message Text:**
- Click in the field
- You need to build: `[Grok Response] + "\n\n- Alexandria"`
- First, select from dropdown: **"2. Choices 0 Message Content"** (from Step 2 - Webhooks)
- Then manually type: `\n\n- Alexandria` after it
- Final result should look like: `{{2.choices__0__message__content}}\n\n- Alexandria`

**Thread TS:**
- Click in the field
- Dropdown appears
- Select: **"1. Thread TS"** (from Step 1 - Slack trigger)
- If empty, select **"1. Timestamp"** instead

**Send as:**
- Leave as default (Bot)

**5.6 - Test Action:**
- Click **Test action**
- Check Slack - you should see Alexandria's response! ✅
- Click **Continue**

### **Step 6: Publish Your Zap**

1. Review all 3 steps:
   - ✅ Trigger: New Mention in Slack
   - ✅ Action 1: Call Grok API
   - ✅ Action 2: Send to Slack

2. Click **"Publish"** (top right)

3. **Turn ON the Zap:**
   - Toggle switch to **ON** (blue)

4. **Done!** 🎉

### **Step 7: Test It Live**

1. Go to #all-alexandrias-design in Slack
2. Type: `@Slacking What is our revenue goal?`
3. Wait 2-3 seconds (Zapier free tier has 15-min polling, but new mentions are usually instant on first setup)
4. Alexandria responds automatically! ✅

---

## 🔧 **OPTION 2: Local Webhook Server**

**Best for:** Full control, no external dependencies
**Time:** 20 minutes
**Cost:** FREE
**Maintenance:** Keep server + ngrok running

### **Requirements**

- Python 3.7+ installed
- Administrator access to install packages
- Port 3000 available

### **Step 1: Install Flask**

Open Command Prompt or Terminal:

```bash
pip install flask
```

### **Step 2: Start Alexandria Server**

```bash
python C:\Users\MarieLexisDad\scripts\alexandria_auto.py
```

You should see:
```
============================================================
Alexandria - Automatic Slack Bot
============================================================

[INFO] Starting webhook server on port 3000...
```

**Keep this window open!**

### **Step 3: Install & Run ngrok**

**3.1 - Download ngrok:**
1. Go to: https://ngrok.com/download
2. Download Windows 64-bit version
3. Extract `ngrok.exe` to: `C:\Users\MarieLexisDad\tools\ngrok\`

**3.2 - Run ngrok:**

Open a **NEW** Command Prompt window:

```bash
cd C:\Users\MarieLexisDad\tools\ngrok
ngrok http 3000
```

You should see:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:3000
```

**Copy the HTTPS URL** (example: `https://abc123.ngrok.io`)

**Keep this window open too!**

### **Step 4: Configure Slack Events API**

**4.1 - Go to Slack API:**
1. Visit: https://api.slack.com/apps
2. Select your app: **"Slacking"**

**4.2 - Enable Event Subscriptions:**
1. Click **"Event Subscriptions"** in left sidebar
2. Toggle **"Enable Events"** to **ON**

**4.3 - Set Request URL:**
1. In **"Request URL"** field, enter:
   ```
   https://YOUR_NGROK_URL/slack/events
   ```
   (Replace YOUR_NGROK_URL with the ngrok URL you copied)

   Example: `https://abc123.ngrok.io/slack/events`

2. Wait for green **"Verified"** checkmark ✅

**4.4 - Subscribe to Bot Events:**
1. Scroll down to **"Subscribe to bot events"**
2. Click **"Add Bot User Event"**
3. Search for and add: **`app_mention`**
4. Click **"Save Changes"** (bottom right)

**4.5 - Reinstall App (if prompted):**
- If you see "You need to reinstall your app"
- Click **"reinstall your app"** link
- Click **"Allow"**

### **Step 5: Test It**

1. Go to #all-alexandrias-design in Slack
2. Type: `@Slacking What should we focus on today?`
3. Watch your Python terminal - you should see:
   ```
   [MENTION] What should we focus on today?
   [RESPONSE] Sending to Slack...
   [OK] Sent!
   ```
4. Alexandria responds in Slack! ✅

### **Keep It Running**

**Option A: Leave both windows open**
- Terminal 1: Python server
- Terminal 2: ngrok tunnel

**Option B: Windows Task Scheduler** (Advanced)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: When computer starts
4. Action: Run `C:\Users\MarieLexisDad\scripts\start_alexandria_auto.bat`
5. Check "Run whether user is logged on or not"

---

## 📊 **Comparison: Which Option?**

| Feature | Zapier Zap | Local Server |
|---------|-----------|--------------|
| **Setup Time** | 10 min | 20 min |
| **Automatic** | ✅ Yes | ✅ Yes |
| **Always Running** | ✅ Cloud | Requires local server |
| **Free** | 100 tasks/month | ✅ Unlimited |
| **Maintenance** | ✅ None | Keep server + ngrok running |
| **Customizable** | Limited | ✅ Full control |
| **Best For** | Set and forget | Developers/Advanced users |

**Recommendation:** Use **Option 1 (Zapier Zap)** unless you need full control.

---

## 🧪 **Testing Checklist**

Once set up, test these scenarios:

- [ ] Mention @Slacking with a question
- [ ] Alexandria responds within 2-15 seconds
- [ ] Response shows "- Alexandria" signature
- [ ] Thread replies work (mention in a thread)
- [ ] Multiple mentions work
- [ ] Long messages work

---

## 🐛 **Troubleshooting**

### **Zapier: Bot doesn't respond**

**Check:**
1. Is the Zap turned ON? (Toggle should be blue)
2. Go to Zapier → Task History - any errors?
3. Did you map the fields correctly in Step 5?
4. Try turning Zap OFF and back ON

**Common Fixes:**
- Re-test each step in the Zap editor
- Check that Channel ID and Thread TS are mapped from Step 1
- Verify Message Text includes `\n\n- Alexandria`

### **Zapier: Slow responses (15+ minutes)**

**Cause:** Free tier polls every 15 minutes

**Solutions:**
- Upgrade to Starter plan ($20/month) for instant triggers
- OR use Option 2 (local server) for instant responses

### **Local Server: "Verified" checkmark doesn't appear**

**Check:**
1. Is Python server running?
2. Is ngrok running and showing HTTPS URL?
3. Did you copy the HTTPS URL correctly?
4. Is port 3000 available? (try `netstat -ano | findstr :3000`)

**Fix:**
- Restart Python server
- Restart ngrok
- Make sure URL ends with `/slack/events`

### **Local Server: Bot responds but not as "Slacking"**

This is expected! The local server uses the bot token directly, so messages appear from "Slacking APP".

To change: Messages will always show from the bot account (Slacking), not from Zapier.

### **Grok API errors**

**Check:**
1. Is API key correct?
2. Check Grok API status: https://status.x.ai
3. Look at error message in logs

**Common errors:**
- `401 Unauthorized`: API key wrong or expired
- `429 Rate limit`: Too many requests, wait a moment
- `500 Server error`: Grok API issue, try again

---

## 💰 **Cost Breakdown**

### **Option 1: Zapier Zap**

**Free Plan:**
- 100 tasks/month
- 1 mention = 2 tasks (Grok call + Slack post)
- = 50 mentions/month FREE
- Polls every 15 minutes

**Starter Plan ($20/month):**
- 750 tasks/month
- Instant triggers (< 1 second)
- = 375 mentions/month

**Grok API:**
- ~$0.02-0.05 per response
- 50 responses = $1-2.50/month

**Total Free:** $1-2.50/month
**Total Starter:** $21-22.50/month

### **Option 2: Local Server**

**Cost:** FREE (only Grok API usage ~$0.02-0.05 per response)

---

## 📝 **What Happens After Setup**

### **Automatic Workflow:**

```
User mentions @Slacking in Slack
         ↓
(2-15 seconds delay depending on plan)
         ↓
Grok 4 generates Alexandria's response
         ↓
Message posted to Slack:
"[Response]

- Alexandria"
```

### **No manual steps required!**

---

## 🎉 **Success Criteria**

You'll know it's working when:

✅ Someone mentions @Slacking
✅ Alexandria responds automatically within 2-15 seconds
✅ Response is relevant and helpful
✅ Message ends with "- Alexandria"
✅ Works in threads
✅ No manual intervention needed

---

## 📞 **Support**

**If you need help:**
1. Check this guide's Troubleshooting section
2. Review Zapier Task History for errors (Option 1)
3. Check Python terminal logs (Option 2)
4. Ask Claude Code for help!

---

## 🔄 **Updating Alexandria**

### **To Change Personality:**

**Option 1 (Zapier):**
1. Open your Zap
2. Edit Step 2 (Webhooks)
3. Change the "system" message content
4. Save & test

**Option 2 (Local Server):**
1. Edit `C:\Users\MarieLexisDad\scripts\alexandria_auto.py`
2. Find `ALEXANDRIA_PROMPT` variable
3. Change the text
4. Restart server

### **To Change Signature:**

**Option 1 (Zapier):**
1. Open your Zap
2. Edit Step 3 (Send to Slack)
3. Change `\n\n- Alexandria` to whatever you want
4. Save

**Option 2 (Local Server):**
1. Edit `alexandria_auto.py`
2. Find: `text_with_signature = f"{text}\n\n- Alexandria"`
3. Change "- Alexandria" to your preference
4. Restart server

---

## 📚 **Additional Resources**

**Files Created:**
- `scripts/alexandria_auto.py` - Local webhook server
- `scripts/alexandria_respond.py` - Manual response generator
- `scripts/MAKE-IT-AUTOMATIC.md` - Quick reference
- `docs/ALEXANDRIA-COMPLETE-SETUP-GUIDE.md` - This file

**Zapier Help:**
- Zapier Tutorial: https://zapier.com/learn
- Slack Integration: https://zapier.com/apps/slack/integrations

**Grok API:**
- Documentation: https://docs.x.ai
- API Status: https://status.x.ai

---

## ✅ **Quick Start Summary**

**Fastest Path (Option 1):**
1. Sign up for Zapier (2 min)
2. Create 3-step Zap (8 min)
   - Trigger: Slack New Mention
   - Action 1: Webhooks POST to Grok
   - Action 2: Send to Slack
3. Test in Slack (30 sec)
4. Done! ✅

**Total Time:** 10 minutes
**Result:** Automatic Alexandria responding 24/7

---

**Last Updated:** 2025-11-01
**Status:** ✅ Ready to deploy
**Maintainer:** Claude Code with Alexandria's Design team
