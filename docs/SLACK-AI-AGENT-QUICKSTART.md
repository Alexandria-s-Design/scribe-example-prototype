# Slack AI Agent - Quick Start Guide

**Goal**: Set up an AI teammate in Slack using n8n in under 30 minutes!

## What You'll Get

An AI agent named "Alexandria" in Slack that can:
- Send emails (Office 365 & Gmail)
- Check your calendar (Google & Office 365)
- Create tasks in Monday.com
- Search documents
- Answer questions with business context
- Use tools automatically when needed

---

## Setup Steps

### 1. Create n8n API Key (2 minutes)

n8n is already open at http://localhost:5678

1. Click your profile icon (bottom left)
2. Go to **Settings**
3. Click **API** in the left sidebar
4. Click **Create API Key**
5. Copy the key (looks like `n8n_api_xxxxx`)
6. Add to your `.env` file:
   ```bash
   N8N_API_KEY="n8n_api_xxxxx"
   ```

### 2. Set Up Slack App (10 minutes)

**A. Create the App**
1. Go to https://api.slack.com/apps
2. Click **Create New App**
3. Choose **From scratch**
4. App Name: `Alexandria AI Agent`
5. Pick your workspace
6. Click **Create App**

**B. Enable Event Subscriptions**
1. In the left sidebar, click **Event Subscriptions**
2. Toggle **Enable Events** to ON
3. For Request URL, you'll use: `https://your-ngrok-url/webhook/slack-agent`
   - First, set up ngrok (see step 3 below)
   - Then come back and paste the URL here
4. Under **Subscribe to bot events**, add:
   - `app_mention`
   - `message.im`
5. Click **Save Changes**

**C. Add Bot Scopes**
1. In the left sidebar, click **OAuth & Permissions**
2. Scroll to **Scopes** section
3. Under **Bot Token Scopes**, add:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
   - `channels:read`
   - `im:history`
   - `im:read`
   - `im:write`
   - `users:read`
4. Scroll to top and click **Install to Workspace**
5. Click **Allow**

**D. Copy Tokens**
1. After installation, you'll see **Bot User OAuth Token**
   - Starts with `xoxb-`
   - Copy this token
2. In the left sidebar, click **Basic Information**
3. Scroll to **App-Level Tokens**
4. Click **Generate Token and Scopes**
   - Name: `Socket Token`
   - Add scope: `connections:write`
   - Click **Generate**
   - Copy the token (starts with `xapp-`)

**E. Save Tokens**
Add both tokens to your `.env` file:
```bash
SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
SLACK_APP_TOKEN="xapp-your-app-token-here"
```

### 3. Set Up ngrok (5 minutes)

ngrok creates a public URL for your local n8n webhook.

**A. Install ngrok**
```bash
# Download from https://ngrok.com/download
# Or use winget
winget install ngrok
```

**B. Start ngrok**
```bash
# Forward port 5678 to a public URL
ngrok http 5678
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5678
```

**C. Update Slack Event URL**
1. Copy the `https://abc123.ngrok.io` URL
2. Go back to Slack App settings
3. Go to **Event Subscriptions**
4. Set Request URL to: `https://abc123.ngrok.io/webhook/slack-agent`
5. Wait for the green "Verified" checkmark
6. Click **Save Changes**

### 4. Configure n8n Credentials (5 minutes)

**A. Add Anthropic (Claude) Credentials**
1. In n8n, click **Credentials** in the left sidebar
2. Click **+ Add Credential**
3. Search for "Anthropic"
4. Click **Anthropic Api**
5. Enter your Claude API key from `.env`
6. Click **Save**

**B. Add Slack Credentials**
1. Click **+ Add Credential**
2. Search for "Slack"
3. Click **Slack OAuth2 API**
4. Enter:
   - Access Token: Your `SLACK_BOT_TOKEN` (xoxb-...)
5. Click **Save**

**C. Add Office 365 (Optional)**
1. Click **+ Add Credential**
2. Search for "Microsoft"
3. Click **Microsoft OAuth2 API**
4. Click **Connect my account**
5. Follow OAuth flow
6. Click **Save**

**D. Add Google (Optional)**
1. Click **+ Add Credential**
2. Search for "Google"
3. Click **Google OAuth2 API**
4. Click **Connect my account**
5. Follow OAuth flow
6. Click **Save**

### 5. Import Workflow (2 minutes)

**A. Import the JSON**
1. In n8n, click **Workflows** in the left sidebar
2. Click **+ Add workflow**
3. Click the **⋮** menu (top right)
4. Click **Import from File**
5. Select: `C:\Users\MarieLexisDad\workflows\slack-ai-agent-basic.json`
6. Click **Import**

**B. Update Credentials**
The workflow will have red error indicators for credentials.

1. Click the **Claude API Call** node
2. In the right panel, under **Credential to connect with**, select your Anthropic credential
3. Click the **Send to Slack** node
4. Select your Slack credential
5. Click **Save** (top right)

### 6. Activate Workflow (1 minute)

1. Click the toggle switch at the top (should turn blue)
2. You'll see "Active" status
3. The webhook is now listening!

### 7. Test It! (5 minutes)

**A. In Slack**
1. Go to your Slack workspace
2. Search for the app: `@Alexandria AI Agent`
3. Send a message: `Hello!`
4. Wait for response (should take 2-5 seconds)

**B. Test Tool Calling**
Send: `@Alexandria what's on my calendar today?`

The agent should:
1. Recognize this needs the `get_calendar` tool
2. Execute the calendar lookup
3. Return your events

**C. Test Email**
Send: `@Alexandria send a test email to myself`

The agent should ask for details if needed.

---

## Troubleshooting

### "URL verification failed" in Slack
- Make sure ngrok is running
- Make sure n8n workflow is activated
- Check the webhook path is correct: `/webhook/slack-agent`
- Test the webhook URL in a browser - you should get a response

### "No response from agent"
- Check n8n executions (left sidebar → Executions)
- Look for errors in the execution log
- Verify Anthropic credentials are valid
- Check Claude API key has credits

### "Tool execution failed"
- The basic workflow has placeholder tool nodes
- You need to connect actual Office 365/Gmail/Monday nodes
- See the full plan in `docs/workflows/slack-ai-agent-n8n-plan.md`

---

## Next Steps

### Phase 2: Add Real Tool Execution (30 minutes)

Replace the placeholder tool nodes with real integrations:

**Email Tool:**
1. Delete "Execute: Send Email" node
2. Add **Gmail** or **Office 365** node
3. Configure to send email using `{{ $json.tool_input.to }}`, etc.
4. Connect to "Format Tool Response"

**Calendar Tool:**
1. Delete "Execute: Get Calendar" node
2. Add **Google Calendar** or **Office 365 Calendar** node
3. Configure to get events
4. Format results and connect to "Format Tool Response"

**Monday.com Tool:**
1. Delete "Execute: Create Task" node
2. Add **Monday.com** node
3. Configure to create item
4. Connect to "Format Tool Response"

### Phase 3: Add More Tools

Add more tool definitions in the Claude API call:
- `search_documents` → OneDrive/Google Drive search
- `get_financial_data` → LunchMoney API
- `analyze_image` → Vision API
- `create_video` → Video generation workflow

### Phase 4: Add Memory

Add a **Redis** or **Database** node to store:
- Conversation history per user
- User preferences
- Context from previous interactions

---

## Cost Estimate

**Per message:**
- Simple response: ~$0.01 (Claude API)
- With tool calling: ~$0.02-0.05 (Claude API)
- n8n: Free (self-hosted)
- Slack: Free (existing workspace)

**Monthly at 100 messages/day:**
- Total: ~$30-150/month (Claude API only)

---

## Architecture

```
Slack Message → ngrok → n8n Webhook → Claude API → Tool Router
                                           ↓
                                    ┌──────┴──────┐
                                    │   Tools     │
                                    └──────┬──────┘
                                           ↓
                        ┌──────────────────┼──────────────────┐
                        │                  │                  │
                   Office 365         Google Workspace    Monday.com
                   (Email/Cal)        (Gmail/Drive)       (Projects)
                        │                  │                  │
                        └──────────────────┼──────────────────┘
                                           ↓
                                  Format Response → Slack
```

---

## Files Created

- ✅ `workflows/slack-ai-agent-basic.json` - Import this into n8n
- ✅ `docs/workflows/slack-ai-agent-n8n-plan.md` - Full implementation plan
- ✅ `docs/SLACK-AI-AGENT-QUICKSTART.md` - This guide

---

## Support

If you get stuck:
1. Check n8n executions log for errors
2. Review `docs/workflows/slack-ai-agent-n8n-plan.md` for detailed architecture
3. Test individual nodes in n8n
4. Check Slack app event subscriptions are configured
5. Verify ngrok is forwarding to port 5678

---

## What's Next?

Once basic setup works:
1. Add real tool execution nodes
2. Connect Office 365, Google Workspace, Monday.com
3. Add more tools (file search, financials, etc.)
4. Add conversation memory
5. Create specialized workflows for common tasks
6. Share with team!

**You're about to have an AI teammate in Slack!** 🚀
