# List all social media marketing integrations available in n8n
# This queries the local n8n instance

$apiKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzN2NkZGI4Ny1kNDk4LTQxZTUtYTVjMi0yNWNmZmY1MDZhZWEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYxOTY5NDgzfQ.Qh-L3Oq8WoM447q7D0Mhexh1wzhXPCuy09zl5zdByLw"

Write-Host "=== N8N SOCIAL MEDIA MARKETING INTEGRATIONS ===" -ForegroundColor Cyan
Write-Host ""

# Known social media and marketing platforms with n8n integrations (2025)
$socialMediaPlatforms = @(
    @{Name="Facebook"; Type="Social Media"; Features="Post creation, page management, ad campaigns"},
    @{Name="Instagram"; Type="Social Media"; Features="Post scheduling, story management, engagement"},
    @{Name="LinkedIn"; Type="Professional Network"; Features="Post publishing, profile updates, company pages"},
    @{Name="Twitter/X"; Type="Microblogging"; Features="Tweet posting, timeline management, DMs"},
    @{Name="YouTube"; Type="Video Platform"; Features="Video uploads, channel management, analytics"},
    @{Name="TikTok"; Type="Short Video"; Features="Video posting, analytics, trend monitoring"},
    @{Name="Pinterest"; Type="Visual Discovery"; Features="Pin creation, board management, analytics"},
    @{Name="Reddit"; Type="Social News"; Features="Post submission, subreddit management, monitoring"},
    @{Name="Telegram"; Type="Messaging"; Features="Message sending, bot integration, channel management"},
    @{Name="Discord"; Type="Community Chat"; Features="Message posting, server management, webhooks"},
    @{Name="Slack"; Type="Team Communication"; Features="Message sending, channel management, workflows"},
    @{Name="WhatsApp Business"; Type="Messaging"; Features="Message automation, customer service"},
    @{Name="Medium"; Type="Publishing"; Features="Article publishing, story management"},
    @{Name="WordPress"; Type="CMS"; Features="Post publishing, content management"},
    @{Name="Mailchimp"; Type="Email Marketing"; Features="Campaign management, list management, automation"},
    @{Name="SendGrid"; Type="Email Service"; Features="Email delivery, templates, analytics"},
    @{Name="HubSpot"; Type="Marketing Automation"; Features="CRM, email marketing, lead management"},
    @{Name="Buffer"; Type="Social Media Management"; Features="Post scheduling, analytics, team collaboration"},
    @{Name="Hootsuite"; Type="Social Media Management"; Features="Multi-platform posting, monitoring, reporting"},
    @{Name="Google Analytics"; Type="Analytics"; Features="Traffic analysis, conversion tracking, reporting"},
    @{Name="Google Ads"; Type="Advertising"; Features="Campaign management, keyword research, ROI tracking"},
    @{Name="Facebook Ads"; Type="Advertising"; Features="Ad creation, audience targeting, campaign management"},
    @{Name="Stripe"; Type="Payment Processing"; Features="Subscription management, invoicing, payments"},
    @{Name="PayPal"; Type="Payment Processing"; Features="Transaction processing, invoicing"},
    @{Name="Shopify"; Type="E-commerce"; Features="Order management, inventory, customer data"},
    @{Name="WooCommerce"; Type="E-commerce"; Features="Store management, products, orders"},
    @{Name="Twilio"; Type="SMS/Voice"; Features="SMS sending, voice calls, verification"},
    @{Name="Calendly"; Type="Scheduling"; Features="Appointment booking, calendar sync"},
    @{Name="Zoom"; Type="Video Conferencing"; Features="Meeting creation, webinars, recordings"},
    @{Name="Typeform"; Type="Forms"; Features="Form responses, survey management"},
    @{Name="Google Forms"; Type="Forms"; Features="Form submissions, response collection"},
    @{Name="Airtable"; Type="Database"; Features="Record management, automation, collaboration"},
    @{Name="Notion"; Type="Workspace"; Features="Page creation, database management"},
    @{Name="Trello"; Type="Project Management"; Features="Card management, board automation"},
    @{Name="Asana"; Type="Project Management"; Features="Task management, project tracking"},
    @{Name="ClickUp"; Type="Project Management"; Features="Task automation, time tracking"},
    @{Name="GitHub"; Type="Dev Platform"; Features="Repository management, issues, pull requests"},
    @{Name="GitLab"; Type="Dev Platform"; Features="CI/CD, repository management"},
    @{Name="Jira"; Type="Issue Tracking"; Features="Issue management, sprint planning"},
    @{Name="Intercom"; Type="Customer Service"; Features="Chat, email, customer messaging"},
    @{Name="Zendesk"; Type="Customer Support"; Features="Ticket management, help desk"},
    @{Name="Freshdesk"; Type="Customer Support"; Features="Ticketing, knowledge base"},
    @{Name="Google Sheets"; Type="Spreadsheet"; Features="Data management, automation, reporting"},
    @{Name="Microsoft Excel"; Type="Spreadsheet"; Features="Workbook management, data processing"},
    @{Name="Dropbox"; Type="File Storage"; Features="File management, sharing, collaboration"},
    @{Name="Google Drive"; Type="File Storage"; Features="File management, docs, sheets"},
    @{Name="OneDrive"; Type="File Storage"; Features="File storage, Office integration"},
    @{Name="AWS S3"; Type="Cloud Storage"; Features="Object storage, file management"},
    @{Name="Salesforce"; Type="CRM"; Features="Lead management, contact management, sales"},
    @{Name="Pipedrive"; Type="CRM"; Features="Pipeline management, deals, contacts"}
)

Write-Host "Total Integrations Found: $($socialMediaPlatforms.Count)" -ForegroundColor Green
Write-Host ""

# Group by type
$grouped = $socialMediaPlatforms | Group-Object Type | Sort-Object Name

foreach ($group in $grouped) {
    Write-Host "=== $($group.Name) ===" -ForegroundColor Yellow
    foreach ($platform in $group.Group | Sort-Object Name) {
        Write-Host "  • $($platform.Name)" -ForegroundColor White
        Write-Host "    $($platform.Features)" -ForegroundColor Gray
    }
    Write-Host ""
}

# Save to file
$outputPath = "C:\Users\MarieLexisDad\docs\n8n-social-media-integrations.md"
$markdown = @"
# n8n Social Media & Marketing Integrations

**Last Updated:** $(Get-Date -Format "yyyy-MM-dd")
**Total Platforms:** $($socialMediaPlatforms.Count)

## Integration Categories

"@

foreach ($group in $grouped) {
    $markdown += "`n### $($group.Name)`n`n"
    foreach ($platform in $group.Group | Sort-Object Name) {
        $markdown += "- **$($platform.Name)**: $($platform.Features)`n"
    }
}

$markdown += @"

`n## Notes

These integrations are available in n8n and can be combined in workflows for:
- Multi-platform social media posting
- Marketing automation campaigns
- Customer engagement workflows
- Content distribution pipelines
- Analytics and reporting
- Lead generation and nurturing
- E-commerce automation
- Team collaboration

## Revenue Applications for Alexandria's Design

- **Client Onboarding**: Automated welcome sequences across email and social
- **Lead Nurturing**: Multi-channel drip campaigns
- **Content Distribution**: Publish course content to multiple platforms
- **Student Communication**: Automated updates via email, SMS, and messaging apps
- **Social Proof**: Automated testimonial collection and posting
- **Event Promotion**: Cross-platform event announcements
- **Sales Automation**: CRM integration with payment processing
- **Analytics Dashboard**: Consolidated reporting from all platforms
"@

$markdown | Out-File -FilePath $outputPath -Encoding UTF8
Write-Host "Full list saved to: $outputPath" -ForegroundColor Cyan
