# Slack AI Agent in n8n - Implementation Plan

**Goal**: Create an AI teammate in Slack using n8n workflows that has access to Claude Code capabilities and your productivity tools.

## Architecture Overview

```
Slack Message → n8n Webhook → Claude API (with tools) → Tool Execution → Response to Slack
                    ↓
            ┌───────┴────────┐
            │  Tool Router   │
            └───────┬────────┘
                    ↓
    ┌───────────────┼───────────────┐
    │               │               │
Office 365    Google Workspace  Monday.com
(Email/Cal)    (Gmail/Drive)    (Projects)
```

## Workflow Components

### 1. Slack Trigger (Webhook or App Mention)
- **Node**: Slack Trigger or Webhook
- **Listens for**: @mentions, DMs, or specific channels
- **Captures**: User message, channel ID, thread timestamp

### 2. Claude API Call with Tools
- **Node**: HTTP Request to Anthropic API
- **Model**: Claude Sonnet 4.5
- **System Prompt**: Alexandria's Design context (from CLAUDE.md)
- **Tools Defined**:
  - `send_email` (Office 365/Gmail)
  - `get_calendar` (Office 365/Google)
  - `create_task` (Monday.com/Planner)
  - `search_documents` (OneDrive/Drive)
  - `get_financial_data` (LunchMoney)

### 3. Tool Router (Switch Node)
- **Node**: Switch/If
- **Routes based on**: Claude's tool_use response
- **Branches**:
  - Email tools → Office 365/Gmail nodes
  - Calendar tools → Calendar API nodes
  - Task tools → Monday.com nodes
  - Document tools → Drive/OneDrive nodes
  - No tool → Direct response

### 4. Tool Execution Nodes
Each tool type gets its own execution branch:

**Email Tools:**
- Office 365 node: `send_email`, `search_email`
- Gmail node: `send_email`, `get_messages`

**Calendar Tools:**
- Google Calendar: `get_events`, `create_event`
- Office 365 Calendar: `list_events`, `create_event`

**Project Management:**
- Monday.com: `create_item`, `update_item`, `get_boards`
- Microsoft Planner: `create_task`, `get_tasks`

**File Storage:**
- Google Drive: `search_files`, `get_file`
- OneDrive: `search_files`, `download_file`

### 5. Response Formatter
- **Node**: Function/Code
- **Formats**: Tool results back to Claude
- **Sends**: Final response to Slack

### 6. Slack Response
- **Node**: Slack Send Message
- **Posts to**: Original channel/thread
- **Formats**: Rich text with markdown

## Setup Steps

### Step 1: Create n8n API Key (One-time)
1. Open http://localhost:5678
2. Go to Settings → API
3. Click "Create API Key"
4. Copy key and add to `.env`:
   ```
   N8N_API_KEY="n8n_api_xxxxx"
   ```

### Step 2: Set Up Slack App (One-time)
1. Go to https://api.slack.com/apps
2. Create new app "Alexandria AI Agent"
3. Enable Socket Mode (optional) or Events API
4. Add Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
   - `im:history`
   - `users:read`
5. Install to workspace
6. Copy tokens to n8n credentials:
   - Bot Token: `xoxb-...`
   - App Token: `xapp-...` (if Socket Mode)

### Step 3: Configure API Credentials in n8n
Add credentials for:
- **Anthropic** (Claude API key)
- **Office 365** (OAuth - already configured)
- **Google Workspace** (OAuth - already configured)
- **Monday.com** (API token from .env)
- **Slack** (Bot token from Step 2)

### Step 4: Build Main Workflow

**Workflow Name**: `slack-ai-agent-main`

**Nodes** (in order):
1. **Slack Trigger** → Listens for @mentions
2. **Extract Message** → Get user input, context
3. **Build System Prompt** → Load Alexandria's Design context
4. **Claude API Call** → POST to Anthropic with tools
5. **Parse Response** → Extract tool calls or text
6. **Tool Router (Switch)** → Route to tool executors
7. **Execute Tools** → Run selected tool(s)
8. **Format Tool Results** → Prepare for Claude
9. **Claude Follow-up** → Send tool results back
10. **Send to Slack** → Post final response

### Step 5: Create System Prompt

Store in n8n as a variable or in a separate workflow:

```
You are Alexandria, an AI teammate for Alexandria's Design, founded by Charles Martin and Dr. Marie Martin.

BUSINESS CONTEXT:
- Educational technology consulting
- Focus on K-12, higher ed, government, military
- Revenue goal: $30k/month
- Products: ModelIt!, Alexandria's World, professional development

YOUR CAPABILITIES:
- Email: Office 365 (cmartin@alexandriasdesign.com), Gmail (charlesmartinedd@gmail.com)
- Calendar: Google Calendar, Office 365
- Projects: Monday.com, Microsoft Planner
- Files: OneDrive, SharePoint, Google Drive
- Financials: LunchMoney tracking

TOOLS AVAILABLE:
- send_email(to, subject, body, account)
- get_calendar_events(start_date, end_date, account)
- create_task(title, description, board_id, assignee)
- search_documents(query, location)
- get_financial_summary(date_range)

PERSONALITY:
- Professional yet friendly
- Revenue-focused ("let's get to the bread")
- Proactive with tools
- Educational expertise
- AI/automation expertise

ALWAYS:
- Use tools when they can help
- Ask clarifying questions
- Think revenue-first
- Be concise in Slack
```

### Step 6: Define Tools Schema for Claude

In the Claude API call node, define tools:

```json
{
  "tools": [
    {
      "name": "send_email",
      "description": "Send an email via Office 365 or Gmail",
      "input_schema": {
        "type": "object",
        "properties": {
          "to": {"type": "string", "description": "Recipient email"},
          "subject": {"type": "string"},
          "body": {"type": "string"},
          "account": {"type": "string", "enum": ["office365", "gmail"]}
        },
        "required": ["to", "subject", "body"]
      }
    },
    {
      "name": "get_calendar",
      "description": "Get calendar events",
      "input_schema": {
        "type": "object",
        "properties": {
          "days_ahead": {"type": "integer", "default": 7},
          "account": {"type": "string", "enum": ["google", "office365"]}
        }
      }
    },
    {
      "name": "create_monday_task",
      "description": "Create a task in Monday.com",
      "input_schema": {
        "type": "object",
        "properties": {
          "board_id": {"type": "string"},
          "item_name": {"type": "string"},
          "column_values": {"type": "object"}
        },
        "required": ["board_id", "item_name"]
      }
    }
  ]
}
```

### Step 7: Build Tool Execution Branches

For each tool, create execution logic:

**Example: send_email branch**
```
IF tool_name == "send_email"
  → IF account == "office365"
    → Office 365 Send Email node
  → ELSE IF account == "gmail"
    → Gmail Send Email node
  → Format success response
```

### Step 8: Test Workflow
1. Activate workflow in n8n
2. In Slack, message: `@Alexandria what's on my calendar today?`
3. Verify:
   - Webhook received
   - Claude called with tools
   - Calendar tool executed
   - Response sent to Slack

### Step 9: Add Error Handling
- **Node**: Error Trigger
- **Catches**: Failed API calls, timeout errors
- **Action**: Send friendly error message to Slack
- **Logging**: Store errors for debugging

### Step 10: Add Conversation Memory (Optional)
- **Storage**: Redis or n8n workflow data
- **Stores**: Last 10 messages per user/thread
- **Provides**: Context to Claude for follow-ups

## Advanced Features (Phase 2)

### Multi-Step Workflows
Allow Claude to execute multiple tools in sequence:
1. Search documents → Find relevant file
2. Get file content → Read document
3. Send email → Share with client

### Scheduled Tasks
Create workflows triggered by time:
- Daily revenue summary at 9am
- Weekly project status report
- Monthly financial review

### Integration with Existing Workflows
Connect to your existing n8n workflows:
- Social media posting → Notify in Slack
- Client onboarding → Update via AI agent
- Video generation → Status updates

## Cost Estimate

**Per Message:**
- Claude API: ~$0.01-0.05 (depending on tool calls)
- n8n: Free (self-hosted)
- Slack: Free (existing workspace)

**Monthly at 100 messages/day:**
- Claude: ~$30-150/month
- Total: Same as Claude cost

## Next Steps

1. ✅ n8n running (port 5678)
2. ⏳ Create API key
3. ⏳ Set up Slack app
4. ⏳ Build main workflow
5. ⏳ Configure credentials
6. ⏳ Test and deploy

## Benefits vs Go Slack MCP Client

**n8n Advantages:**
- ✅ Visual editing - no code needed
- ✅ Already running with 50+ integrations
- ✅ Easier to modify and extend
- ✅ Built-in error handling and retries
- ✅ Can integrate with existing workflows
- ✅ Version control via export/import
- ✅ Shareable with team

**When to Use Go Client:**
- Need lower latency
- Want MCP protocol support
- Prefer infrastructure as code
- Need advanced agent mode features

## Files to Create

1. `workflows/slack-ai-agent-main.json` - Main workflow
2. `workflows/slack-ai-agent-tools.json` - Tool execution subworkflow
3. `workflows/slack-ai-agent-test.json` - Testing workflow
4. `scripts/n8n-automation/deploy-slack-agent.ps1` - Deployment script
5. `scripts/n8n-automation/test-slack-agent.ps1` - Testing script
