# Slack AI Teammate with Zapier MCP + Grok 4

## Overview
Simple 3-step Zapier automation:
1. **Trigger**: New Slack mention (@Slacking)
2. **Action**: Call Grok 4 API with message
3. **Action**: Send response back to Slack

## Advantages
- ✅ No ngrok needed
- ✅ No localhost issues
- ✅ Zapier handles all webhooks
- ✅ Works immediately
- ✅ No server to maintain

## Step 1: Create Zapier Account (if needed)
1. Go to: https://zapier.com
2. Sign up with charlesmartinedd@gmail.com
3. Free plan allows 100 tasks/month

## Step 2: Set Up Slack Trigger

**Zapier Tool**: `mcp__zapier__slack_find_message` or similar

### Configure in Zapier:
1. **Trigger**: New Mention in Slack
2. **Event**: `app_mention`
3. **Channel**: All channels (or specific ones)
4. **Test**: Send a test mention to verify

## Step 3: Call Grok 4 API

**API Details**:
- **Endpoint**: `https://api.x.ai/v1/chat/completions`
- **Method**: POST
- **Authorization**: `Bearer YOUR_GROK_API_KEY`

**Request Body**:
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
      "content": "{{text_from_slack}}"
    }
  ],
  "temperature": 0.7
}
```

**Response Path**: `choices[0].message.content`

## Step 4: Send Response to Slack

**Zapier Tool**: `mcp__zapier__slack_send_channel_message`

### Configure:
- **Channel**: `{{channel_from_trigger}}`
- **Message**: `{{grok_response}}`
- **Thread TS**: `{{thread_ts_from_trigger}}` (to reply in thread)

## Step 5: Test

1. Go to your Slack workspace
2. Mention the bot: `@Slacking What is the revenue goal?`
3. Wait 2-3 seconds
4. Alexandria responds!

## Troubleshooting

**If bot doesn't respond**:
1. Check Zapier task history for errors
2. Verify Slack connection in Zapier
3. Check Grok API key is valid
4. Ensure bot has permissions (app_mention, chat:write)

**If response is delayed**:
- Zapier free plan processes tasks every 15 minutes
- Upgrade to Starter plan for instant triggers ($20/month)

## Cost Analysis

**Zapier**:
- Free: 100 tasks/month (1 mention = 2 tasks)
- Starter: $20/month for instant triggers + 750 tasks

**Grok API**:
- ~$0.02-0.05 per response
- 100 responses = $2-5/month

**Total**: ~$22-25/month for instant AI teammate

## Alexandria's Full Context

See system prompt above for complete personality and capabilities.

---

**Status**: Ready to implement via Zapier MCP
**Last Updated**: 2025-11-01
