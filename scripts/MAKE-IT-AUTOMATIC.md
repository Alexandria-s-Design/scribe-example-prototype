# 🤖 Make Alexandria Automatic - 2 Options

## ⚡ **Option 1: Zapier Zap** (EASIEST - Recommended)

**Time:** 5 minutes
**Cost:** FREE (100 tasks/month)
**Pros:** No server needed, fully automatic, cloud-based

### Setup Steps:

1. **Go to Zapier:**
   https://zapier.com/app/zaps

2. **Create New Zap:**
   - Click "Create Zap"

3. **Step 1 - Trigger (Slack):**
   - App: **Slack**
   - Event: **New Mention**
   - Connect your Alexandria's Design workspace
   - Test it (mention @Slacking to verify)

4. **Step 2 - Call Grok (Webhooks by Zapier):**
   - Action: **Webhooks by Zapier**
   - Action Event: **POST**
   - URL: `https://api.x.ai/v1/chat/completions`

   **Headers:**
   ```
   Authorization: Bearer YOUR_GROK_API_KEY
   Content-Type: application/json
   ```

   **Data (JSON):**
   ```json
   {
     "model": "grok-2-latest",
     "messages": [
       {
         "role": "system",
         "content": "You are Alexandria, an AI teammate for Alexandria's Design. Revenue goal: $30k/month. Be concise in Slack responses."
       },
       {
         "role": "user",
         "content": "{{TEXT_FROM_STEP_1}}"
       }
     ],
     "temperature": 0.7
   }
   ```

   Test this step!

5. **Step 3 - Send to Slack:**
   - Action: **Slack**
   - Action Event: **Send Channel Message**
   - Channel: `{{CHANNEL_FROM_STEP_1}}`
   - Message: `{{RESPONSE_FROM_STEP_2}}\n\n- Alexandria`
   - Thread TS: `{{THREAD_TS_FROM_STEP_1}}`

6. **Publish & Turn On:**
   - Click "Publish"
   - Toggle switch to ON
   - Done!

### Result:
```
User: @Slacking What's the move?
   ↓ (2 seconds)
Alexandria: [intelligent response]

- Alexandria
```

**Completely automatic!** No Claude Code needed.

---

## 🔧 **Option 2: Local Webhook Server** (More Control)

**Time:** 15 minutes
**Cost:** FREE
**Pros:** Full control, can customize behavior
**Cons:** Need to keep server running, need ngrok

### Setup Steps:

1. **Install Flask:**
   ```bash
   pip install flask
   ```

2. **Start the server:**
   ```bash
   python scripts/alexandria_auto.py
   ```
   Server runs on port 3000

3. **Expose with ngrok:**
   ```bash
   ngrok http 3000
   ```
   Copy the https:// URL (e.g., `https://abc123.ngrok.io`)

4. **Configure Slack Events API:**
   - Go to: https://api.slack.com/apps
   - Select your "Slacking" app
   - Click "Event Subscriptions"
   - Enable Events: ON
   - Request URL: `https://YOUR_NGROK_URL/slack/events`
   - Wait for green "Verified" checkmark
   - Subscribe to bot events:
     - `app_mention`
   - Save Changes

5. **Test:**
   ```
   @Slacking Hello!
   ```
   Alexandria responds automatically!

### Keep It Running:

**Option A: Leave terminal open**
```bash
python scripts/alexandria_auto.py
```

**Option B: Background service** (Windows)
- Create Task Scheduler job
- Run on startup

---

## 📊 **Comparison**

| Feature | Zapier Zap | Local Server |
|---------|-----------|--------------|
| Setup Time | 5 min | 15 min |
| Automatic | ✅ Yes | ✅ Yes |
| Always Running | ✅ Yes | Needs ngrok/server |
| Customizable | Limited | ✅ Full control |
| Cost | Free tier | ✅ Free |
| Maintenance | None | Keep server running |

---

## 🎯 **Recommendation**

**Use Option 1 (Zapier Zap)** because:
- ✅ Takes 5 minutes
- ✅ No server management
- ✅ Always running
- ✅ Cloud-based
- ✅ Free tier available

**Use Option 2 (Local Server)** if you want:
- Full control over behavior
- Custom logging
- No external dependencies
- More complex integrations

---

## ✅ **What Happens After Setup**

Once automatic:

```
User mentions @Slacking
         ↓
(2-3 seconds)
         ↓
Alexandria responds with Grok 4
         ↓
Message ends with "- Alexandria"
```

**No manual intervention needed!**

---

**Ready to set up?** I recommend Option 1 (Zapier Zap). Takes 5 minutes and works forever!
