# This is the proposed section to add to CLAUDE.md
# Review this before we add it to the main file

---

## 🤖 GROK 4 API (xAI) - REAL-TIME AI ASSISTANCE

**Status**: ✅ Configured (GROK_API_KEY in .env)
**Helper**: `scripts/api-helpers/grok_helper.py`
**Documentation**: `docs/GROK_API_GUIDE.md`
**Model**: Grok 4 (256K context, Nov 2024 knowledge cutoff)

### Why Use Grok 4

**Grok 4's Unique Advantages:**
- **Real-time information access** - Knowledge through November 2024
- **Massive context** - 256K tokens (standard), 2M tokens (fast models)
- **Vision capabilities** - Analyze screenshots, documents, diagrams
- **Native tool use** - Built-in function calling and integration
- **Strong reasoning** - Advanced problem-solving and analysis
- **Code assistance** - Generate, debug, and review code

**Best For:**
- Researching current grant opportunities and deadlines
- Analyzing client screenshots and error messages
- Getting latest education industry trends (through Nov 2024)
- Technical documentation and code review
- Real-time competitive intelligence
- Processing very long documents (256K-2M tokens)

### Available Models

1. **grok-4** - Main Grok 4 model (recommended, 256K context)
2. **grok-vision-beta** - Vision-enabled model (for image analysis)
3. **grok-4-fast-reasoning** - Fast model with reasoning (2M context!)
4. **grok-4-fast-non-reasoning** - Fast model without reasoning (2M context)
5. **grok-4-0709** - Specific Grok 4 version (use grok-4 for latest)

### Claude Code Usage Protocol

**Claude will ask before using Grok API:**

```
User: "What are the latest federal education grants available?"
Claude: "Would you like me to use Grok API for real-time grant information?
         This will use your GROK_API_KEY. (Estimated cost: ~$0.02-0.05)"
User: "Yes"
Claude: [Uses grok_helper.py to get current grant info]
```

**When Claude should offer Grok:**
- User asks about recent/current events or data
- User needs real-time information (grants, trends, news)
- User shares a screenshot that needs analysis
- User requests vision-based tasks (diagram analysis, OCR)
- User needs complex reasoning beyond Claude's knowledge cutoff

### Usage Examples

**1. Real-Time Research (Text):**
```python
from scripts.api_helpers.grok_helper import GrokHelper

helper = GrokHelper()
result = helper.simple_chat(
    "What are the newest Department of Education grants announced in 2025?"
)
print(result)
```

**2. Vision Analysis (Screenshots):**
```python
# Analyze error screenshot
analysis = helper.analyze_image(
    image_url="C:/Users/MarieLexisDad/Pictures/Screenshots/latest.png",
    prompt="What error is shown and how do I fix it?",
    model="grok-vision-beta"
)
```

**3. Complex Reasoning:**
```python
# Database design consultation
response = helper.simple_chat("""
Design a scalable database schema for Alexandria's Design that handles:
- Course catalog and modules
- Student progress tracking
- Client organizations
- Billing and subscriptions
- Content delivery
""")
```

**4. Streaming for Long Responses:**
```python
# Stream responses in real-time
for chunk in helper.chat_stream([
    {"role": "user", "content": "Create a comprehensive lesson plan for AI literacy"}
]):
    print(chunk, end="", flush=True)
```

### Integration with Alexandria's Design Revenue Strategy

**Revenue Applications:**

1. **Grant Research Automation**
   - Weekly Grok queries for new education grants
   - Automated opportunity identification
   - Real-time deadline tracking

2. **Client Technical Support**
   - Analyze client error screenshots instantly
   - Debug technical issues with vision AI
   - Faster resolution = happier clients

3. **Content Currency**
   - Blog posts with latest industry trends
   - Course content using current best practices
   - Professional development with recent research

4. **Competitive Intelligence**
   - Track competitor launches and updates
   - Monitor industry innovations
   - Stay ahead of education technology trends

5. **Proposal Enhancement**
   - Research latest requirements for RFPs
   - Current compliance standards
   - Recent successful project examples

### Cost Optimization

**Pricing** (approximate):
- Input: ~$5 per 1M tokens
- Output: ~$15 per 1M tokens
- Typical query: $0.02-0.05

**Smart Usage:**
- Use `grok-4` (standard) for most tasks (256K context)
- Use `grok-4-fast-reasoning` for huge documents (2M context)
- Use `grok-vision-beta` only when analyzing images
- Set `max_tokens` to limit response length and costs
- Leverage Nov 2024 knowledge cutoff for recent info
- Fall back to Claude or OpenRouter free models for older knowledge

### Automation with n8n

**Example Workflow:**
```
Every Monday 9 AM:
  1. Grok API → Search for new education grants
  2. Filter → Relevant to Alexandria's Design services
  3. Gmail → Send Charles digest of opportunities
  4. Monday.com → Create tasks for viable grants
  5. Google Sheets → Log opportunities for tracking
```

### Testing

```bash
# Quick test
python scripts/api-helpers/test_grok.py

# Connection test
python -c "from scripts.api_helpers.grok_helper import GrokHelper; GrokHelper().test_connection()"
```

### When NOT to Use Grok

**Use Claude Code or OpenRouter free models instead when:**
- Task doesn't require real-time information
- General coding or writing tasks
- Knowledge from before 2025 is sufficient
- Cost optimization is priority
- Vision capabilities not needed

### Helper Script Functions

```python
helper = GrokHelper()

# Available methods:
helper.chat(messages, model, temperature, max_tokens)
helper.simple_chat(user_message, model)
helper.analyze_image(image_url, prompt, model)
helper.chat_stream(messages, model, temperature)
helper.list_models()
helper.get_model_info()
helper.test_connection()
```

### Real-World Examples for Alexandria's Design

**Example 1: Grant Opportunity Scout**
```python
# Run this weekly to find opportunities
helper = GrokHelper()
response = helper.simple_chat("""
List federal education grants announced in the past 7 days that are relevant to:
- Professional development for educators
- Educational technology implementation
- AI literacy programs
- K-12 and higher education

Include deadlines and brief descriptions.
""")
```

**Example 2: Client Screenshot Debugging**
```python
# Client sends error screenshot
analysis = helper.analyze_image(
    image_url=client_screenshot_path,
    prompt="""
    1. What error or issue is shown?
    2. What's the likely cause?
    3. What are step-by-step solutions?
    4. Any preventive measures?
    """
)
```

**Example 3: Industry Trend Analysis**
```python
# Monthly competitive intelligence
trends = helper.simple_chat("""
What are the top 5 trends in educational technology and AI for K-12 in 2025?
Focus on:
- Professional development approaches
- AI integration in classrooms
- Teacher training innovations
- Scaling strategies
""")
```

**Example 4: Proposal Research**
```python
# Before writing RFP response
research = helper.simple_chat("""
What are the current priorities and initiatives for the Department of Education
regarding AI literacy and professional development for teachers? Include recent
policy announcements and funding priorities for 2025.
""")
```

### Quick Reference Commands

```bash
# Test connection
python scripts/api-helpers/test_grok.py

# Quick chat from command line
python -c "from scripts.api_helpers.grok_helper import GrokHelper; print(GrokHelper().simple_chat('Your question here'))"

# Check available models
python -c "from scripts.api_helpers.grok_helper import GrokHelper; print(GrokHelper().list_models())"
```

---

**Summary**: Grok 4 gives Alexandria's Design a competitive edge through recent information access (Nov 2024 knowledge), massive context windows (256K-2M tokens), vision capabilities, native tool use, and strong reasoning - perfect for grant research, analyzing long documents, client support, and staying current in fast-moving education technology markets.

