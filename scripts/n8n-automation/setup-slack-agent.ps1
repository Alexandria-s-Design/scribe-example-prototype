# Slack AI Agent - Automated Setup Script
# This script automates the entire deployment process

param(
    [string]$SlackBotToken = $env:SLACK_BOT_TOKEN,
    [string]$SlackAppToken = $env:SLACK_APP_TOKEN,
    [string]$AnthropicApiKey = $env:ANTHROPIC_API_KEY,
    [string]$N8nApiKey = $env:N8N_API_KEY,
    [switch]$CreateApiKey = $false
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Slack AI Agent - Automated Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check n8n is running
Write-Host "[1/8] Checking n8n status..." -ForegroundColor Yellow
$n8nRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -TimeoutSec 3 -ErrorAction SilentlyContinue
    $n8nRunning = $true
    Write-Host "✓ n8n is running on port 5678" -ForegroundColor Green
} catch {
    Write-Host "✗ n8n is not accessible on port 5678" -ForegroundColor Red
    Write-Host "  Please start n8n with: docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

# Step 2: Get or create n8n API key
Write-Host ""
Write-Host "[2/8] Getting n8n API key..." -ForegroundColor Yellow

if (-not $N8nApiKey -or $CreateApiKey) {
    Write-Host "  Attempting to extract API key from n8n database..." -ForegroundColor Gray

    # Try to get API key from Docker container
    $apiKeyResult = docker exec n8n sh -c "sqlite3 /home/node/.n8n/database.sqlite 'SELECT apiKey FROM api_key LIMIT 1;'" 2>$null

    if ($apiKeyResult -and $apiKeyResult.Trim()) {
        $N8nApiKey = $apiKeyResult.Trim()
        Write-Host "✓ Found existing API key in database" -ForegroundColor Green

        # Update .env file
        $envPath = ".env"
        if (Test-Path $envPath) {
            $envContent = Get-Content $envPath -Raw
            if ($envContent -match "N8N_API_KEY=") {
                $envContent = $envContent -replace "N8N_API_KEY=.*", "N8N_API_KEY=`"$N8nApiKey`""
            } else {
                $envContent += "`nN8N_API_KEY=`"$N8nApiKey`""
            }
            Set-Content -Path $envPath -Value $envContent
            Write-Host "✓ Updated .env file with API key" -ForegroundColor Green
        }
    } else {
        Write-Host "✗ No API key found. Creating one..." -ForegroundColor Yellow

        # Generate a new API key
        $newApiKey = "n8n_api_" + [guid]::NewGuid().ToString("N").Substring(0, 32)

        # Insert into database - escape single quotes for SQL
        $sqlInsert = "INSERT INTO api_key (apiKey, label) VALUES ('$newApiKey', 'Auto-generated for Slack Agent');"
        $insertResult = docker exec n8n sh -c "sqlite3 /home/node/.n8n/database.sqlite `"$sqlInsert`"" 2>$null

        if ($LASTEXITCODE -eq 0) {
            $N8nApiKey = $newApiKey
            Write-Host "✓ Created new API key" -ForegroundColor Green

            # Update .env
            Add-Content -Path ".env" -Value "`nN8N_API_KEY=`"$N8nApiKey`""
            Write-Host "✓ Added to .env file" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to create API key" -ForegroundColor Red
            Write-Host "  Please create manually: http://localhost:5678 → Settings → API" -ForegroundColor Yellow
            exit 1
        }
    }
} else {
    Write-Host "✓ Using API key from environment" -ForegroundColor Green
}

# Step 3: Start ngrok
Write-Host ""
Write-Host "[3/8] Starting ngrok tunnel..." -ForegroundColor Yellow

# Check if ngrok is already running
$ngrokRunning = Get-Process ngrok -ErrorAction SilentlyContinue

if ($ngrokRunning) {
    Write-Host "  ngrok already running, getting URL..." -ForegroundColor Gray
} else {
    Write-Host "  Starting ngrok for port 5678..." -ForegroundColor Gray
    Start-Process -FilePath "ngrok" -ArgumentList "http 5678" -WindowStyle Minimized
    Start-Sleep -Seconds 3
}

# Get ngrok public URL
try {
    $ngrokApi = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction Stop
    $publicUrl = $ngrokApi.tunnels[0].public_url
    Write-Host "✓ ngrok tunnel active: $publicUrl" -ForegroundColor Green

    $webhookUrl = "$publicUrl/webhook/slack-agent"
    Write-Host "  Webhook URL: $webhookUrl" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Failed to get ngrok URL" -ForegroundColor Red
    Write-Host "  Please start ngrok manually: ngrok http 5678" -ForegroundColor Yellow
    $webhookUrl = "http://YOUR_NGROK_URL/webhook/slack-agent"
}

# Step 4: Import workflow
Write-Host ""
Write-Host "[4/8] Importing workflow into n8n..." -ForegroundColor Yellow

$workflowPath = "workflows\slack-ai-agent-basic.json"
if (-not (Test-Path $workflowPath)) {
    Write-Host "✗ Workflow file not found: $workflowPath" -ForegroundColor Red
    exit 1
}

$workflowJson = Get-Content $workflowPath -Raw | ConvertFrom-Json

# Update webhook URL in workflow
foreach ($node in $workflowJson.nodes) {
    if ($node.name -eq "Webhook (Slack)") {
        $node.parameters.path = "slack-agent"
    }
}

$workflowJson.name = "Slack AI Agent - Auto Imported"

# Convert back to JSON
$workflowBody = $workflowJson | ConvertTo-Json -Depth 20

try {
    $headers = @{
        "X-N8N-API-KEY" = $N8nApiKey
        "Content-Type" = "application/json"
    }

    $importResult = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows" `
        -Method Post `
        -Headers $headers `
        -Body $workflowBody `
        -ErrorAction Stop

    $workflowId = $importResult.id
    Write-Host "✓ Workflow imported successfully (ID: $workflowId)" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to import workflow: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 5: Create credentials
Write-Host ""
Write-Host "[5/8] Setting up credentials..." -ForegroundColor Yellow

# Check if Anthropic API key is provided
if (-not $AnthropicApiKey) {
    Write-Host "⚠ ANTHROPIC_API_KEY not found in environment" -ForegroundColor Yellow
    $AnthropicApiKey = Read-Host "Enter your Anthropic API key (or press Enter to skip)"
}

if ($AnthropicApiKey) {
    # Create Anthropic credential
    $anthropicCredential = @{
        name = "Anthropic API (Auto)"
        type = "anthropicApi"
        data = @{
            apiKey = $AnthropicApiKey
        }
    } | ConvertTo-Json

    try {
        $credResult = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/credentials" `
            -Method Post `
            -Headers $headers `
            -Body $anthropicCredential `
            -ErrorAction Stop

        Write-Host "✓ Anthropic credentials created (ID: $($credResult.id))" -ForegroundColor Green
        $anthropicCredId = $credResult.id
    } catch {
        if ($_.Exception.Message -match "already exists") {
            Write-Host "⚠ Anthropic credentials already exist" -ForegroundColor Yellow
        } else {
            Write-Host "✗ Failed to create Anthropic credentials: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Check Slack tokens
if (-not $SlackBotToken) {
    Write-Host "⚠ SLACK_BOT_TOKEN not found" -ForegroundColor Yellow
    Write-Host "  You'll need to configure Slack credentials manually in n8n" -ForegroundColor Yellow
} else {
    # Create Slack credential
    $slackCredential = @{
        name = "Slack Bot (Auto)"
        type = "slackOAuth2Api"
        data = @{
            accessToken = $SlackBotToken
        }
    } | ConvertTo-Json

    try {
        $slackCredResult = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/credentials" `
            -Method Post `
            -Headers $headers `
            -Body $slackCredential `
            -ErrorAction Stop

        Write-Host "✓ Slack credentials created (ID: $($slackCredResult.id))" -ForegroundColor Green
    } catch {
        if ($_.Exception.Message -match "already exists") {
            Write-Host "⚠ Slack credentials already exist" -ForegroundColor Yellow
        } else {
            Write-Host "✗ Failed to create Slack credentials: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Step 6: Activate workflow
Write-Host ""
Write-Host "[6/8] Activating workflow..." -ForegroundColor Yellow

try {
    $activateResult = Invoke-RestMethod -Uri "http://localhost:5678/api/v1/workflows/$workflowId/activate" `
        -Method Post `
        -Headers $headers `
        -ErrorAction Stop

    Write-Host "✓ Workflow activated successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to activate workflow: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 7: Display Slack app setup instructions
Write-Host ""
Write-Host "[7/8] Slack App Setup Required" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To complete setup, configure your Slack app:" -ForegroundColor White
Write-Host ""
Write-Host "1. Go to: https://api.slack.com/apps" -ForegroundColor Gray
Write-Host "2. Create or select your app" -ForegroundColor Gray
Write-Host "3. Go to Event Subscriptions" -ForegroundColor Gray
Write-Host "4. Set Request URL to:" -ForegroundColor Gray
Write-Host "   $webhookUrl" -ForegroundColor Cyan
Write-Host "5. Subscribe to bot events: app_mention, message.im" -ForegroundColor Gray
Write-Host "6. Save and install to workspace" -ForegroundColor Gray
Write-Host ""

if (-not $SlackBotToken) {
    Write-Host "7. Copy your Bot Token (xoxb-...) and add to .env file" -ForegroundColor Gray
    Write-Host ""
}

# Step 8: Test workflow
Write-Host ""
Write-Host "[8/8] Testing workflow..." -ForegroundColor Yellow

$testPayload = @{
    type = "event_callback"
    event = @{
        type = "app_mention"
        text = "<@BOT123> Hello Alexandria!"
        user = "U123456"
        channel = "C123456"
        ts = "1234567890.123456"
    }
} | ConvertTo-Json -Depth 5

if ($webhookUrl -ne "http://YOUR_NGROK_URL/webhook/slack-agent") {
    try {
        $testResult = Invoke-RestMethod -Uri $webhookUrl `
            -Method Post `
            -ContentType "application/json" `
            -Body $testPayload `
            -TimeoutSec 10 `
            -ErrorAction Stop

        Write-Host "✓ Workflow test successful" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Test failed - workflow needs Slack credentials configured" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Skipping test - ngrok URL not available" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Status:" -ForegroundColor White
Write-Host "  ✓ n8n running on http://localhost:5678" -ForegroundColor Green
if ($webhookUrl -ne "http://YOUR_NGROK_URL/webhook/slack-agent") {
    Write-Host "  ✓ ngrok tunnel active: $publicUrl" -ForegroundColor Green
}
Write-Host "  ✓ Workflow imported and activated" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor White
Write-Host "  1. Configure Slack app with webhook URL above" -ForegroundColor Gray
Write-Host "  2. Test in Slack: @YourBot hello" -ForegroundColor Gray
Write-Host "  3. View executions: http://localhost:5678/executions" -ForegroundColor Gray
Write-Host ""
Write-Host "Management Commands:" -ForegroundColor White
Write-Host "  View workflow: http://localhost:5678/workflow/$workflowId" -ForegroundColor Cyan
Write-Host "  Stop ngrok: Stop-Process -Name ngrok" -ForegroundColor Cyan
Write-Host ""
