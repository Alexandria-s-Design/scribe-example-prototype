# Get or Generate n8n API Key
# This script helps you get an API key from n8n without using the GUI

param(
    [string]$n8nUrl = "http://localhost:5678",
    [string]$username = "",
    [string]$password = ""
)

Write-Host "n8n API Key Helper" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# Method 1: Check if running in Docker and query the database directly
Write-Host "METHOD 1: Checking n8n Docker container..." -ForegroundColor Yellow

try {
    $dbCheck = docker exec n8n sh -c "ls /home/node/.n8n/database.sqlite 2>/dev/null"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Found n8n database in Docker container" -ForegroundColor Green
        Write-Host ""
        Write-Host "Querying for existing API keys..." -ForegroundColor Yellow

        # Query the database for API keys
        $apiKeys = docker exec n8n sh -c "sqlite3 /home/node/.n8n/database.sqlite 'SELECT id, label, apiKey FROM api_key;'" 2>$null

        if ($apiKeys) {
            Write-Host "Found existing API keys:" -ForegroundColor Green
            Write-Host $apiKeys
            Write-Host ""
            Write-Host "Copy one of the API keys above and add it to your .env file:" -ForegroundColor Cyan
            Write-Host 'N8N_API_KEY="your-key-here"' -ForegroundColor White
        } else {
            Write-Host "No API keys found in database" -ForegroundColor Yellow
            Write-Host "You need to create one. See Method 2 below." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Could not access n8n Docker container" -ForegroundColor Red
}

Write-Host ""
Write-Host "METHOD 2: Create API key via n8n API..." -ForegroundColor Yellow

if ($username -and $password) {
    Write-Host "Attempting to login and create API key..." -ForegroundColor Yellow

    try {
        # Login to get session cookie
        $loginBody = @{
            email = $username
            password = $password
        } | ConvertTo-Json

        $session = Invoke-WebRequest -Uri "$n8nUrl/rest/login" -Method POST -Body $loginBody -ContentType "application/json" -SessionVariable 'n8nSession'

        if ($session.StatusCode -eq 200) {
            Write-Host "Login successful" -ForegroundColor Green

            # Create API key
            $apiKeyBody = @{
                label = "Claude Code Auto-Generated"
            } | ConvertTo-Json

            $newKey = Invoke-RestMethod -Uri "$n8nUrl/rest/api-keys" -Method POST -Body $apiKeyBody -ContentType "application/json" -WebSession $n8nSession

            if ($newKey.apiKey) {
                Write-Host "API Key Created Successfully!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Your new API key:" -ForegroundColor Cyan
                Write-Host $newKey.apiKey -ForegroundColor White
                Write-Host ""
                Write-Host "Add this to your .env file:" -ForegroundColor Cyan
                Write-Host "N8N_API_KEY=`"$($newKey.apiKey)`"" -ForegroundColor White

                # Update .env file
                $envPath = Join-Path $PSScriptRoot "..\..\."
                $envFile = Join-Path $envPath ".env"

                if (Test-Path $envFile) {
                    Add-Content -Path $envFile -Value "`nN8N_API_KEY=`"$($newKey.apiKey)`""
                    Write-Host ""
                    Write-Host "Added to .env file" -ForegroundColor Green
                } else {
                    Write-Host ""
                    Write-Host ".env file not found. Please create it manually." -ForegroundColor Yellow
                }
            }
        }
    } catch {
        Write-Host "Failed to create API key via API" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Username and password not provided" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To use this method, run:" -ForegroundColor Cyan
    Write-Host ".\get-n8n-api-key.ps1 -username 'your@email.com' -password 'yourpassword'" -ForegroundColor White
}

Write-Host ""
Write-Host "METHOD 3: One-time browser access (last resort)..." -ForegroundColor Yellow
Write-Host "If the above methods do not work:" -ForegroundColor White
Write-Host "1. Open: $n8nUrl" -ForegroundColor White
Write-Host "2. Login if needed" -ForegroundColor White
Write-Host "3. Go to Settings then API" -ForegroundColor White
Write-Host "4. Click Create API Key button" -ForegroundColor White
Write-Host "5. Copy the key and add it to .env file" -ForegroundColor White
Write-Host ""
Write-Host "After this one-time setup, you will never need the GUI again!" -ForegroundColor Green
