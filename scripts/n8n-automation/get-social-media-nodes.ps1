# Script to query n8n for social media marketing integrations
# Uses n8n REST API

$n8nUrl = "http://localhost:5678"
$apiKey = $env:N8N_API_KEY

# Try to get credentials types which includes integration information
try {
    $headers = @{
        "X-N8N-API-KEY" = $apiKey
    }

    Write-Host "Querying n8n server at $n8nUrl..."

    # Try different API endpoints
    $endpoints = @(
        "/api/v1/credentials/schema",
        "/api/v1/credential-types",
        "/rest/credentials/schema",
        "/types/credentials.json"
    )

    foreach ($endpoint in $endpoints) {
        Write-Host "`nTrying endpoint: $endpoint"
        try {
            $response = Invoke-RestMethod -Uri "$n8nUrl$endpoint" -Headers $headers -Method Get -ErrorAction SilentlyContinue
            Write-Host "Success! Got response from $endpoint"
            $response | ConvertTo-Json -Depth 3
            break
        }
        catch {
            Write-Host "Failed: $($_.Exception.Message)"
        }
    }
}
catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# Also try to list available node types via Docker
Write-Host "`n`nTrying Docker approach..."
try {
    $nodeInfo = docker exec n8n n8n list:credentials 2>&1
    Write-Host $nodeInfo
}
catch {
    Write-Host "Docker command failed: $($_.Exception.Message)"
}
